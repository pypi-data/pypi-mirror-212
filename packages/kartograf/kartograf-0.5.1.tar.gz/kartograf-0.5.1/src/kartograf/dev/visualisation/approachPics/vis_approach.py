import time
import numpy as np

import pymol
from pymol import cmd
pymol.finish_launching()

from dev.visualisation.pymol_utils import  make_picture, openfe_colors

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

file_path = "/dev/visualisation/approachPics/lig_CHEMBL34027.sdf"
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

cmd.color(color_resn1, resn1+" and elem C")
cmd.color(color_resn2, resn2+" and elem C")

make_picture("a_start")
cmd.set("grid_mode")
make_picture("a_start_grid")
cmd.set("grid_mode", 0)

cmd.set("sphere_scale", 0.15)
cmd.set("stick_radius", 0.075)
cmd.set("dash_gap", 0)
cmd.set("dash_radius",0.2)

cmd.color(color_resn1, resn1)
#cmd.set_colour("")
cmd.color(color_resn2, resn2)

import sys
sys.path.append("/src")

cmd.show("spheres")


resn1_atoms = []
cmd.iterate_state(-1, selection=resn1,
                  expression="resn1_atoms.append({\"elem\":elem,\"id\":ID, \"name\":name, \"x\":x, \"y\":y, \"z\":z, \"model\": model, \"chain\":chain, \"resn\":resn, \"resi\":resi, \"alt\":alt,  \"label\":label, \"b\":b})",
                  space=locals())

resn2_atoms= []
cmd.iterate_state(-1, selection=resn2,
                  expression="resn2_atoms.append({\"elem\":elem,\"id\":ID, \"name\":name, \"x\":x, \"y\":y, \"z\":z, \"model\": model, \"chain\":chain, "
                             "\"resn\":resn, \"resi\":resi, \"alt\":alt,  \"label\":label, \"b\":b})",
                  space=locals())




dist = []
eucl = lambda a1, a2: np.sqrt(np.sum(np.square([a2['x']-a1['x'], a2['y']-a1['y'], a2['z']-a1['z']])))
for n_atom in sorted(resn1_atoms, key=lambda x: x['id']):
    dist_i = []
    for b_atom in sorted(resn2_atoms, key=lambda x: x['id']):
        dist_i.append(eucl(n_atom, b_atom))
    dist.append(dist_i)
dist = np.array(dist)

masked_dmatrix = np.array(
    np.ma.where(dist < 0.95, dist, 10 ** 6)
)

# All dists
cmd.set("dash_radius", 0.01)
for i, drow in enumerate(dist, start=1):
    for j, d in enumerate(drow, start=1):
        cmd.dist("d"+str(i)+str(j), resn1+" and id "+str(i), resn2+" and id "+str(j))

cmd.hide("sticks")
cmd.hide("labels")
make_picture("b_all_atoms_distances")
cmd.delete("d*")
cmd.set("dash_radius", 0.045)

# filtered Dists
for i, drow in enumerate(dist, start=1):
    for j, d in enumerate(drow, start=1):
        if(d < 0.95):
            cmd.dist("d"+str(i)+str(j), resn1+" and id "+str(i), resn2+" and id "+str(j))

cmd.hide("sticks")
cmd.hide("labels")
make_picture("c_FILTERED_atoms_distances")

from scipy.optimize import linear_sum_assignment
def _map(distance_matrix):
    row_ind, col_ind = linear_sum_assignment(distance_matrix    )
    raw_mapping = list(zip(map(int, row_ind), map(int, col_ind)))
    # filter for mask value
    mapping = dict(filter(lambda x: distance_matrix[x] < 0.95, raw_mapping))
    return mapping

raw_mapping = _map(dist)

cmd.hide("")
cmd.show("sticks")
cmd.delete("d*")
cmd.color(color_out)
#cmd.color(color_resn1, resn1)
#cmd.color(color_resn2, resn2)

#cmd.show("sticks")
cmd.show("spheres")
print(raw_mapping)
for k,v in raw_mapping.items():
    #cmd.set("sphere_color",color_resn2, "naphthalene and id "+str(k+1))
    #cmd.set("sphere_color", color_resn1, "benzoxazole and id "+str(v+1))
    #time.sleep(1)

    cmd.color(color_map, resn2+" and id "+str(v+1))
    cmd.color(color_map, resn1+" and id "+str(k+1))

    cmd.set("stick_color", color_resn2, resn2+" and id "+str(v+1))

    cmd.show("spheres", resn2+" and id "+str(v+1))
    cmd.show("spheres", resn1+" and id "+str(k+1))
    cmd.dist("m" + str(k) + str(v), resn1+" and id " + str(k+1), resn2+" and id " + str(v+1))
cmd.hide("labels")

make_picture("d_Optimize_pair_Selection")

cmd.hide("")
cmd.show("sticks")
cmd.delete("d*")
cmd.color(color_out)
#cmd.color(color_resn1, resn1)
#cmd.color(color_resn2, resn2)
cmd.show("spheres")
final_map = {0: 1, 1: 0, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4, 8: 3, 9: 2, 14: 12, 15: 11, 16: 10, 17: 9}
final_map = {0: 0, 3: 3, 7: 7, 11: 11, 15: 15, 19: 19, 20: 20, 23: 23, 25: 25, 27: 27, 42: 42, 1: 1, 2: 2, 4: 4, 5: 5, 6: 6, 8: 8, 9: 9, 10: 10, 12: 12, 13: 13, 14: 14, 16: 16, 17: 17, 18: 18, 21: 21, 22: 22, 24: 24, 26: 26, 28: 28, 29: 29, 41: 41, 43: 43, 44: 44}
final_map = {0: 0,
 2: 2,
 3: 3,
 6: 6,
 8: 8,
 10: 10,
 25: 25,
 1: 1,
 4: 4,
 5: 5,
 7: 7,
 9: 9,
 11: 11,
 12: 12,
 24: 24}

for k,v in final_map.items():
    #cmd.set("sphere_color",color_resn2, "naphthalene and id "+str(k+1))
    #cmd.set("sphere_color", color_resn1, "benzoxazole and id "+str(v+1))
    #time.sleep(1)
    if(k==14):
        continue
    cmd.color(color_map, resn2+" and id "+str(k+1))
    cmd.color(color_map, resn1+" and id "+str(v+1))

    cmd.set("stick_color", color_resn2, resn2+" and id "+str(k+1))

    cmd.show("spheres", resn1+" and id "+str(k+1))
    cmd.show("spheres", resn2+" and id "+str(v+1))
    cmd.dist("m" + str(k) + str(v), resn1+" and id " + str(k+1), resn2+" and id " + str(v+1))
cmd.hide("labels")

make_picture("e_Optimize_pair_Selection_largestSet")

cmd.hide("")
cmd.align(resn1, resn2)
cmd.set("stick_radius", 0.2)
cmd.show("sticks")
make_picture("f_mapping")
