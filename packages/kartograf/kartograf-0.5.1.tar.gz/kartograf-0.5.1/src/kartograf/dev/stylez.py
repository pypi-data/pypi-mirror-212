

import pandas as pd
res_ddG = pd.read_csv(csv_path, sep="\t")



from rdkit import Chem
from openfe import SmallMoleculeComponent

rd_molA = Chem.MolFromSmiles("CCCC")
molA = SmallMoleculeComponent.from_rdkit(rd_molA)



from openfe import SmallMoleculeComponent

sdf_path = "./myPath.sdf"
molA = SmallMoleculeComponent.from_sdf_file(sdf_path)


from openff.toolkit.topology import Molecule
from openfe import SmallMoleculeComponent

Molecule()
sdf_path = "./myPath.sdf"
molA = SmallMoleculeComponent.from_openff(off_mol, name="ps")

from openfe import ProteinComponent

pdb_path = "./my.pdb"
prot = ProteinComponent.from_pdb_file(pdb_path)

from rdkit import Chem
