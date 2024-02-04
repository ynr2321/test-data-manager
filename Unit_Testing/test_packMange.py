import os
import sys
import subprocess
import time
# ALTERNATE ADD TO SYS PATH METHOD
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the 'src' directory to the Python path
src_path = os.path.join(current_script_dir, '..', 'src')
sys.path.insert(0, src_path)
# current_path = os.getcwd()
# sys.path.insert(0, current_path + r'\src')
import unittest
from unittest import mock
from unittest.mock import patch
from helper import chooser

class TestCLI(unittest.TestCase):
    def test_packMange_pack(self):
        # creating dummies
        dummy_parent = r'drive/fake_patient_data_folder'
        dummy_patient = 'Donovan_Guevara'
        version = '1.0.0'
        
        # Executing
        with mock.patch('packMange.pack') as mock_pack_command:
            command_string = r'python packMange.py pack --PARENT C:\Users\ynooe11004\Documents\TDM_patient_dataFAKE --PATIENT Daniel_Cranium --VERSION 1.0.2'
            os.chdir(r'./'+'src')
            #subprocess.run(command_string, shell=True)

              

if __name__ == '__main__':
    unittest.main()
    
