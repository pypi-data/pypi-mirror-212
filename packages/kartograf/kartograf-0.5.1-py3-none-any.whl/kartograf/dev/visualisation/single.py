import time
import numpy as np

import pymol
from pymol import cmd
pymol.finish_launching()

from pymol_utils import  make_picture, openfe_colors

openfe_colors()


pymol.finish_launching()
time.sleep(1)

cmd.window(action="maximize")
time.sleep(1)

#OFE Style
color_resn1 = "Otherblue"
color_resn2 = "SandySergio"
color_out = "Beastlygrey"
color_map = "Feelingsick"

file_path = "approachPics/lig_CHEMBL34027.sdf"
#"/home/riesbenj/Code/OpenFE/Experiments/setups/mappers/wally/test_visualization_cmet.sdf"
#"/home/riesbenj/Code/OpenFE/Experiments/setups/mappers/wally/test_visualization_cmet.sdf" #"./two_mols.sdf"
cmd.bg_colour("white")
cmd.set("dash_color", 'Feelingspicy')
cmd.load(file_path, "two_mols")
cmd.split_states("two_mols")
cmd.delete("two_mols")
cmd.delete("naphthalene01")
time.sleep(1)


"""
set_view (\
    -0.909637451,   -0.070243672,    0.409417748,\
    -0.126253858,    0.985722840,   -0.111386776,\
    -0.395748824,   -0.153011471,   -0.905522108,\
     0.000000000,    0.000000000,  -29.498178482,\
   -20.368076324,   20.597049713,   97.038482666,\
    13.309098244,   45.687267303,  -20.000000000 )

"""

cmd.set_view(
     [ -0.909637451,   -0.070243672,    0.409417748,
    -0.126253858,    0.985722840,   -0.111386776,
    -0.395748824,   -0.153011471,   -0.905522108,
     0.000000000,    0.000000000,  -29.498178482,
   -20.368076324,   20.597049713,   97.038482666,
    13.309098244,   45.687267303,  -20.000000000 ])

time.sleep(1)

resn1 = "lig_CHEMBL340274" #benzoxazole
resn2 = "lig_CHEMBL340275" #naphthalene

cmd.color(color_map, resn1)
cmd.color(color_map, resn2 )

cmd.color(color_resn1, resn1+" and ID 16+19")
cmd.color(color_resn2, resn2+" and ID 16+23")

cmd.remove(resn1+" and not ID 16+15+19+18")
cmd.create("g2", resn1+" and ID 16+15")
cmd.create("g1", resn1+" and ID 19+18")

