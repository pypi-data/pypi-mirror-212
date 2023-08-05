[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Python wrapper for Molecular Signature Descriptors

Python wrapper to ease the calculation of Signature molecular descriptors.

## Notice

This work relies on Gilleain Torrance's re-write of Jean-Loup Faulon's signature code for molecules (https://github.com/gilleain/signatures/).

The Signature Molecular Descriptor. 2. Enumerating Molecules from Their Extended Valence Sequences
Jean-Loup Faulon, Carla J. Churchwell, and Donald P. Visco
Journal of Chemical Information and Computer Sciences 2003 43 (3), 721-734
DOI: 10.1021/ci020346o

## Installation

From source:

    git clone https://github.com/OlivierBeq/Signature_pywrapper.git
    pip install ./Signature_pywrapper

with pip:

```bash
pip install signature-pywrapper
```

### Get started

```python
from Signature_pywrapper import Signature

smiles_list = [
    # erlotinib
    "n1cnc(c2cc(c(cc12)OCCOC)OCCOC)Nc1cc(ccc1)C#C",
    # midecamycin
    "CCC(=O)O[C@@H]1CC(=O)O[C@@H](C/C=C/C=C/[C@@H]([C@@H](C[C@@H]([C@@H]([C@H]1OC)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)C)O[C@H]3C[C@@]([C@H]([C@@H](O3)C)OC(=O)CC)(C)O)N(C)C)O)CC=O)C)O)C",
    # selenofolate
    "C1=CC(=CC=C1C(=O)NC(CCC(=O)OCC[Se]C#N)C(=O)O)NCC2=CN=C3C(=N2)C(=O)NC(=N3)N",
    # cisplatin
    "N.N.Cl[Pt]Cl"
]
mols = [Chem.MolFromSmiles(smiles) for smiles in smiles_list]

sig = Signature()
print(sig.calculate(mols, depth=1))
```

One can also calculate signatures for multiple depths:
```python
print(sig.calculate(mols, depth=[1, 2, 3]))
```
## Documentation

```python
def calculate(mols, show_banner=True, njobs=1, chunksize=100):
```

Default method to calculate counts of signatures for each vertex of the molecule.

Parameters:

- ***mols  : Iterable[Chem.Mol]***  
  RDKit molecule objects for which to obtain Signature descriptors.
- ***depth  : Union[int, List[int]]***  
  Depth of the signatures of vertices.
- ***show_banner  : bool***  
  Displays default notice about Signature descriptors.
- ***njobs  : int***  
  Maximum number of simultaneous processes.
- ***chunksize  : int***  
  Maximum number of molecules each process is charged of.
- ***return_type  : pd.DataFrame***  
  Pandas DataFrame containing Signature molecular descriptors.
  If executables have not previously been downloaded, attempts to download and install them.
