import time
import pymol
from pymol import cmd

pymol.finish_launching()

import pymol_utils as pu

pu.openfe_colors()

file_path = "/home/riesbenj/Code/OpenFE/kartograf/src/kartograf/dev/visualisation/benenes_RHFE.sdf"

def std_surface():
    cmd.set("transparency_mode", 3)
    cmd.set("surface_quality",5)
    cmd.set("ambient", 0.85)
    cmd.set("direct", 0.25)
    cmd.set("reflect", 0.0)
    cmd.set("backface_cull", 0)
    cmd.set("solvent_radius", 0.3)
    cmd.set("stick_radius", 0.1)



def reinit():
    cmd.reinitialize()
    time.sleep(1)
    pu.openfe_colors()
    time.sleep(1)
    std_surface()
    cmd.bg_colour("white")



pymol.finish_launching()
time.sleep(1)
cmd.window(action="maximize")
time.sleep(1)

cmd.load(file_path, "benz")
cmd.split_states("benz")
cmd.delete("benz")

cmd.bg_colour("white")


# 1. Picture
if(True):
    cmd.set("grid_mode")

    col_names = ["SandySergio", "Otherblue"]
    nColors = len(pu.ofe_color_names)
    for i, obj in enumerate(cmd.get_object_list(),start=1):
        cmd.color(col_names[i%2], obj+" and elem C")
        cmd.alter(obj, "resn=\""+str(obj)+"\"")

    """
    set_view (\
         0.999495685,   -0.010850049,    0.029843107,\
         0.010749210,    0.999936104,    0.003537612,\
        -0.029879577,   -0.003215076,    0.999548554,\
         0.000000000,    0.000000000,  -35.262779236,\
         0.675092220,   -0.212792397,    0.105792284,\
        17.650743484,   52.874805450,  -20.000000000 )
    """
    cmd.set_view([
        0.999495685,   -0.010850049,    0.029843107,
         0.010749210,    0.999936104,    0.003537612,
        -0.029879577,   -0.003215076,    0.999548554,
         0.000000000,    0.000000000,  -35.262779236,
         0.675092220,   -0.212792397,    0.105792284,
        17.650743484,   52.874805450,  -20.000000000
    ])

    pu.make_picture("benzenes_all_mols")
    #cmd.disable()


# 2. Picture Metrics: RMSD Dist
if False:
    reinit()
    file_path = "/home/riesbenj/Code/OpenFE/kartograf/src/kartograf/dev/visualisation/approachPics/lig_CHEMBL34027.sdf"
    cmd.load(file_path, "two_mols")
    cmd.split_states("two_mols")
    resn1 = "lig_CHEMBL340274" #benzoxazole
    resn2 = "lig_CHEMBL340275" #naphthalene

    cmd.set_view(
         [ -0.909637451,   -0.070243672,    0.409417748,
        -0.126253858,    0.985722840,   -0.111386776,
        -0.395748824,   -0.153011471,   -0.905522108,
         0.000000000,    0.000000000,  -29.498178482,
       -20.368076324,   20.597049713,   97.038482666,
        13.309098244,   45.687267303,  -20.000000000 ])

    time.sleep(1)
    mapping = {0: 0, 2: 2, 3: 3, 6: 6, 8: 8, 10: 10, 25: 25, 1: 1, 4: 4, 5: 5, 7: 7, 9: 9, 11: 11, 12: 12, 24: 24}

    cmd.set("stick_radius", 0.1)
    cmd.set("dash_gap", 0.2)
    cmd.set("dash_radius",0.0)
    cmd.set("dash_as_cylinders",0)

    cmd.disable()
    cmd.enable(resn1)
    cmd.enable(resn2)

    cmd.color("Otherblue", resn1)
    cmd.color("SandySergio", resn2)


    cmd.set("grid_mode",0)
    cmd.translate([0.5, 0.5, -0.5], resn2)
    cmd.color("Feelingsick", resn1+" and id "+"+".join(map(lambda x: str(x+1), mapping.values())))
    cmd.color("Feelingsick", resn2+" and id "+"+".join(map(lambda x: str(x+1), mapping.keys())))

    for i, (k,v) in enumerate(mapping.items()):
        cmd.dist("rmsd_"+str(i), selection1=resn1+" and id "+str(v+1), selection2=resn2+" and id "+str(k+1), )

    cmd.hide("labels")
    cmd.color("Feelingspicy", "rmsd_*")

    pu.make_picture("mapping_rmsd_metric")


# 2. Picture Metrics: Volume Ratio
if(False):
    reinit()

    file_path = "/home/riesbenj/Code/OpenFE/kartograf/src/kartograf/dev/visualisation/approachPics/lig_CHEMBL34027.sdf"
    cmd.load(file_path, "two_mols")
    cmd.split_states("two_mols")
    resn1 = "lig_CHEMBL340274" #benzoxazole
    resn2 = "lig_CHEMBL340275" #naphthalene

    cmd.set_view(
         [ -0.909637451,   -0.070243672,    0.409417748,
        -0.126253858,    0.985722840,   -0.111386776,
        -0.395748824,   -0.153011471,   -0.905522108,
         0.000000000,    0.000000000,  -29.498178482,
       -20.368076324,   20.597049713,   97.038482666,
        13.309098244,   45.687267303,  -20.000000000 ])

    time.sleep(1)
    mapping = {0: 0, 2: 2, 3: 3, 6: 6, 8: 8, 10: 10, 25: 25, 1: 1, 4: 4, 5: 5, 7: 7, 9: 9, 11: 11, 12: 12, 24: 24}



    cmd.disable()
    cmd.enable(resn1)
    cmd.enable(resn2)

    cmd.color("Otherblue", resn1)
    cmd.color("SandySergio", resn2)

    cmd.set("grid_mode",1)

    cmd.color("Feelingsick", resn1+" and id "+"+".join(map(lambda x: str(x+1), mapping.values())))
    cmd.color("Feelingsick", resn2+" and id "+"+".join(map(lambda x: str(x+1), mapping.keys())))

    cmd.create("mapping" , resn1 +" and id "+"+".join(map(lambda x: str(x+1), mapping.values())))
    cmd.color("Feelingsick", "mapping ")

    cmd.set("transparency", 0.6)

    cmd.alter("all", "vdw=\"1.5\"")
    cmd.alter("mapping", "vdw=\"1.2\"")
    cmd.sort()

    cmd.show("surface")

    cmd.set("surface_color", "Otherblue", resn1)
    cmd.set("surface_color", "SandySergio", resn2)
    cmd.set("grid_slot", "-2", "mapping")
    cmd.zoom()

    pu.make_picture("mapping_vRatio_metric")


# 3. Picture Metrics: Tanimoto Ratio
if(False):
    reinit()

    file_path = "/home/riesbenj/Code/OpenFE/kartograf/src/kartograf/dev/visualisation/approachPics/lig_CHEMBL34027.sdf"
    cmd.load(file_path, "two_mols")
    cmd.split_states("two_mols")
    resn1 = "lig_CHEMBL340274" #benzoxazole
    resn2 = "lig_CHEMBL340275" #naphthalene

    cmd.set_view(
         [ -0.909637451,   -0.070243672,    0.409417748,
        -0.126253858,    0.985722840,   -0.111386776,
        -0.395748824,   -0.153011471,   -0.905522108,
         0.000000000,    0.000000000,  -29.498178482,
       -20.368076324,   20.597049713,   97.038482666,
        13.309098244,   45.687267303,  -20.000000000 ])

    time.sleep(1)
    mapping = {0: 0, 2: 2, 3: 3, 6: 6, 8: 8, 10: 10, 25: 25, 1: 1, 4: 4, 5: 5, 7: 7, 9: 9, 11: 11, 12: 12, 24: 24}


    cmd.color("Otherblue", resn1)
    cmd.color("SandySergio", resn2)
    cmd.color("Feelingsick", resn1+" and id "+"+".join(map(lambda x: str(x+1), mapping.values())))
    cmd.color("Feelingsick", resn2+" and id "+"+".join(map(lambda x: str(x+1), mapping.keys())))

    cmd.create("overlay", resn1+" or "+resn2)
    cmd.disable()
    cmd.enable("overlay")

    cmd.create("mapping" , resn1 +" and id "+"+".join(map(lambda x: str(x+1), mapping.values())))
    cmd.color("Feelingsick", "mapping ")

    cmd.set("transparency", 0.6)

    cmd.alter("all", "vdw=\"1.5\"")
    cmd.alter("mapping", "vdw=\"1.2\"")
    cmd.sort()

    cmd.show("surface")

    cmd.set("surface_color", "SandySergio", "overlay")
    cmd.set("surface_color", "Feelingspicy", "mapping")

    cmd.set("grid_slot", "-2", "mapping")
    cmd.zoom()

    pu.make_picture("mapping_shapeTanimoto_metric")


# 4. Picture Metrics: Protrude Ratio
if(False):
    reinit()

    file_path = "/home/riesbenj/Code/OpenFE/kartograf/src/kartograf/dev/visualisation/approachPics/lig_CHEMBL34027.sdf"
    cmd.load(file_path, "two_mols")
    cmd.split_states("two_mols")
    resn1 = "lig_CHEMBL340274" #benzoxazole
    resn2 = "lig_CHEMBL340275" #naphthalene

    cmd.set_view(
         [ -0.909637451,   -0.070243672,    0.409417748,
        -0.126253858,    0.985722840,   -0.111386776,
        -0.395748824,   -0.153011471,   -0.905522108,
         0.000000000,    0.000000000,  -29.498178482,
       -20.368076324,   20.597049713,   97.038482666,
        13.309098244,   45.687267303,  -20.000000000 ])

    time.sleep(1)
    mapping = {0: 0, 2: 2, 3: 3, 6: 6, 8: 8, 10: 10, 25: 25, 1: 1, 4: 4, 5: 5, 7: 7, 9: 9, 11: 11, 12: 12, 24: 24}


    cmd.color("Otherblue", resn1)
    cmd.color("SandySergio", resn2)
    cmd.color("Feelingsick", resn1+" and id "+"+".join(map(lambda x: str(x+1), mapping.values())))
    cmd.color("Feelingsick", resn2+" and id "+"+".join(map(lambda x: str(x+1), mapping.keys())))

    cmd.create("overlay", resn1+" or "+resn2)

    cmd.create("mapping" , resn1 +" and id "+"+".join(map(lambda x: str(x+1), mapping.values())))
    cmd.create("nmapping" , "( "+resn1 +" and not id "+"+".join(map(lambda x: str(x+1), mapping.values())) +" ) or ( "+resn2 +" and not id "+"+".join(map(lambda
                                                                                                                                                              x:                                                                                                                              str(
                                                                                                                                                              x+1), mapping.keys())) +" )")
    cmd.disable()
    cmd.enable("mapping")
    cmd.enable("nmapping")
    cmd.enable("overlay")
    cmd.set("transparency", 0.6)

    cmd.color("Feelingsick", "mapping ")

    cmd.alter("all", "vdw=\"1.5\"")
    cmd.alter("nmapping", "vdw=\"1.2\"")
    cmd.sort()

    cmd.hide("everything", "nmapping")
    cmd.show("surface", "overlay or nmapping")
    cmd.show("sticks")

    cmd.set("surface_color", "SandySergio", "overlay")
    cmd.set("surface_color", "Feelingspicy", "nmapping")

    cmd.zoom()

    pu.make_picture("mapping_shapeProtrude_metric")