import os
import sys
import json
import subprocess
import time
import re
import argparse
import pydicom
import helper
import numpy as np

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
    
def flatten_string(string):
    formatted_string = json.dumps(string, separators=(",", ":"))
    return formatted_string

def parse_package_list(file_path):
    # Initialize an empty list to store the parsed data
    parsed_data = []
    # Open the file for reading
    with open(file_path, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            # Split each line in the file into elements (delimiter being spaces)
            entries = line.strip().split()
            parsed_data.append(entries)
   
    return parsed_data

result = parse_package_list(r"C:\Users\ynooe11004\Downloads\dummyparsepackageslist.txt")

print("sandbox testing done")