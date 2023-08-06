import time
from pymol import cmd

ofe_color_dict={
    'BadassBlue': [49, 57, 77],
    'Otherblue': [0, 47, 74],
    'SandySergio': [217, 196, 177],
    'Sergioscousin': [237, 227, 218],
    'Feelingspicy': [184, 87, 65],
    'Feelingsick': [0, 147, 132],
    'Beastlygrey': [102, 102, 102]
}
ofe_color_names = list(ofe_color_dict.keys())
def openfe_colors():
    [cmd.set_color(k,v) for k,v in ofe_color_dict.items()]
    print("ADDED OPENFE COLORS: "+", ".join(ofe_color_dict.keys()))

def make_picture(name):
    cmd.ray()
    cmd.save(name+".png")
    time.sleep(5)
