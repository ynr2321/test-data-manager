import os
import sys
import json
import subprocess
import time
import re
import argparse
import pydicom
import helper

def color_invert(rgb):
    new_rgb = list(rgb)
    for i, val in enumerate(rgb):
        new_val = round((1 - (val/255))*255)
        new_rgb[i] = new_val
    new_rgb = tuple(new_rgb)
    
    print('the inverted rgb value is: ', new_rgb)
    return(new_rgb)

def func():
    rgb = color_invert((255,255,0))
    print('random string')
    
def number_length(num):
    # init count
    count = 0
    for char in str(num):
        count = count + 1
        
    return count


def debug_helperGetDict():
    manifest_path = r"C:\Users\ynooe11004\Documents\TDM_patient_data\Jon_Bones_manifest\Jon_Bones_manifest.txt"
    dict1 = helper.get_dict_from_manifest(manifest_path)
    print(dict1)

print('temp and its functions have been imported')
debug_helperGetDict()