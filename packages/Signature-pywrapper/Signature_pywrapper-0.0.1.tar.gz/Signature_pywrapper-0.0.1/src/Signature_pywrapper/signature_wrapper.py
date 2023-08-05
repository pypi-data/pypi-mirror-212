# -*- coding: utf-8

"""Python wrapper for Signature descriptors"""

from __future__ import annotations

import os
import multiprocessing
import re
import warnings
from collections import Counter
from copy import deepcopy
from subprocess import PIPE, Popen
from typing import Iterable, List, Optional, Union

import more_itertools
import numpy as np
import pandas as pd
from bounded_pool_executor import BoundedProcessPoolExecutor
from rdkit import Chem
from rdkit.rdBase import BlockLogs

from .utils import install_java, mktempfile, needsHs

class Signature:
    """Wrapper to obtain signature molecular descriptors from
    Gilleain Torrance's re-write of Jean-Loup Faulon's signature
    code for molecules (https://github.com/gilleain/signatures/).

    The Signature Molecular Descriptor. 2. Enumerating Molecules from Their Extended Valence Sequences
    Jean-Loup Faulon, Carla J. Churchwell, and Donald P. Visco
    Journal of Chemical Information and Computer Sciences 2003 43 (3), 721-734
    DOI: 10.1021/ci020346o
    """

    lock = multiprocessing.RLock()  # Ensure installation of JRE is thread safe

    def __init__(self):
        """Instantiate a wrapper to calculate signature molecular descriptors."""
        # Path to the JAR file
        self._jarfile = os.path.abspath(os.path.join(__file__, os.pardir, 'eSignature.jar'))
        # Ensure the jar file exists
        if not os.path.isfile(self._jarfile):
            raise IOError('The required JAR file is not present. Reinstall Signature_pywrapper.')

    def calculate(self, mols: Iterable[Chem.Mol], depth: Union[int, List[int]] = 3, show_banner: bool = True, njobs: int = 1,
                  chunksize: Optional[int] = 1000) -> pd.DataFrame:
        """Calclulate signature descriptors.

        :param mols: RDKit molecules for which signature descriptors should be calculated
        :param depth: depth of the signature
        :param show_banner: If True, show notice on signature descriptors usage
        :param njobs: number of concurrent processes
        :param chunksize: number of molecules to be processed by a process; ignored if njobs is 1
        :return: a pandas DataFrame containing all signature descriptor values
        """
        if show_banner:
            self._show_banner()
        if not isinstance(depth, list):
            self.depths = [depth]
        else:
            self.depths = depth
        # Parallelize should need be
        if njobs > 1:
            with BoundedProcessPoolExecutor(max_workers=njobs) as worker:
                futures = [worker.submit(self._calculate, list(chunk))
                           for chunk in more_itertools.batched(mols, chunksize)
                           ]
            return pd.concat([future.result()
                              for future in futures]
                             ).reset_index(drop=True).fillna(0).astype(int)
        # Single process
        return self._calculate(list(mols))

    def _show_banner(self):
        """Print info message for citing."""
        print("""Signatures are ultimately canonical representations of whole molecules or atom valence environments.
For example, the canonical signature for benzene might be as simple as: C(C(C(C1))C(C(C1))) where
brackets denote branching and numbers indicate joining (as with SMILES).
Signatures can be used as descriptors for atom or molecule environments, much like HOSE codes.
They can also be used for structure enumeration.

###################################

Should you publish results based on the signature molecular descriptors, please cite:

The Signature Molecular Descriptor. 1. Using Extended Valence Sequences in QSAR and QSPR Studies
Jean-Loup Faulon, Donald P. Visco, and Ramdas S. Pophale
Journal of Chemical Information and Computer Sciences 2003 43 (3), 707-720
DOI: 10.1021/ci020345w

The Signature Molecular Descriptor. 2. Enumerating Molecules from Their Extended Valence Sequences
Jean-Loup Faulon, Carla J. Churchwell, and Donald P. Visco
Journal of Chemical Information and Computer Sciences 2003 43 (3), 721-734
DOI: 10.1021/ci020346o

The Signature Molecular Descriptor. 4. Canonizing Molecules Using Extended Valence Sequences
Jean-Loup Faulon, Michael J. Collins, and Robert D. Carr
Journal of Chemical Information and Computer Sciences 2004 44 (2), 427-436
DOI: 10.1021/ci0341823

###################################

""")

    def _prepare_command(self, mols: List[Chem.Mol], depth: int) -> str:
        """Create the ePaDEL command to be run to obtain molecular descriptors.

        :param mols: molecules to obtained molecular descriptors of
        :param depth: the depth of signatures to be computed
        :return: The command to run.
        """
        # 1) Ensure JRE is accessible
        with self.lock:
            self._java_path = install_java()
        # 2) Create temp SD v2k file
        self._tmp_sd = mktempfile('molecules_v2k.sd')
        self._skipped = []
        try:
            block = BlockLogs()
            writer = Chem.SDWriter(self._tmp_sd)
            # Ensure V2000 as CDK cannot properly process v3000
            writer.SetForceV3000(False)
            for i, mol in enumerate(mols):
                if mol is not None and isinstance(mol, Chem.Mol):
                    if mol.GetNumAtoms() > 999:
                        raise ValueError('Cannot calculate descriptors for molecules with more than 999 atoms.')
                    # Does molecule lack hydrogen atoms?
                    if needsHs(mol):
                        warnings.warn(
                            'Molecule lacked hydrogen atoms: automatic assignment performed')
                        mol = Chem.AddHs(mol)
                    writer.write(mol)
                else:
                    self._skipped.append(i)
            writer.close()
            del block
        except ValueError as e:
            # Free resources and raise error
            writer.close()
            del block
            os.remove(self._tmp_sd)
            raise e from None
        # 3) Create command
        java_path = install_java()
        command = f"{java_path} -Djava.awt.headless=true -jar {self._jarfile} -i {self._tmp_sd} -d {depth}"
        return command

    def _cleanup(self) -> None:
        """Cleanup resources used for calculation."""
        # Remove temporary file
        os.remove(self._tmp_sd)

    def _run_command(self, command: str) -> pd.DataFrame:
        """Run the eSignature command.

        :param command: The command to be run.
        """
        with Popen(command.split(), stdout=PIPE) as process:
            results = re.split('\r?\n\r?\n', process.stdout.read().decode()) # results per molecule
        # Organize results
        out = []
        for result in results:
            if len(result) > 0:
                out.append(Counter([line.strip().split('\t')[1] for line in result.split('\n')]))
        values = pd.DataFrame(out)
        values.index.name = 'index'
        return values

    def _calculate(self, mols: List[Chem.Mol]) -> pd.DataFrame:
        """Calculate PaDEL descriptors on one process.

        :param mols: RDkit molecules for which PaDEL descriptors should be calculated.
        :param depth: depth of each vertex's signature
        :return: a pandas DataFrame containing signature desciptor values and the path to the temp dir to be removed
        """
        results = []
        # Run command for each depth
        for i, depth in enumerate(self.depths):
            if i == 0: # Avoid overwriting SD file
                # Prepare inputs
                command = self._prepare_command(mols, depth)
            else:
                command = command[: command.rfind(' ') + 1] + f'{depth}'
            # Run command and obtain results
            results.append(self._run_command(command))
        # Combine depths
        if len(results) == 1:
            results = results[0]
        else:
            results = pd.concat(results).groupby(by='index').sum().reset_index(drop=True)
        # Cleanup
        self._cleanup()
        # Insert lines of skipped molecules
        if len(self._skipped):
            results = (pd.DataFrame(np.insert(results.values, self._skipped,
                                              values=[np.NaN] * len(results.columns),
                                              axis=0),
                                    columns=results.columns)
                       .fillna(0)
                       .astype(int))
        return results

    def _multiproc_calculate(self, mols: List[Chem.Mol]) -> pd.DataFrame:
        """Calculate signature descriptors in thread-safe manner.

        :param mols: RDkit molecules for which signature descriptors should be calculated.
        :return: a pandas DataFrame containing signature descriptor values and the path to the temp dir to be removed
        """
        # Copy self instance to make thread safe
        signatures = deepcopy(self)
        # Run copy
        result = signatures.calculate(mols, show_banner=False, njobs=1)
        return result
