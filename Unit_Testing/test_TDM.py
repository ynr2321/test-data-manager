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
    def test_TDM_pack(self):
        # creating dummies
        dummy_parent = r'drive/fake_patient_data_folder'
        dummy_patient = 'Donovan_Guevara'
        version = '1.0.0'
        
        # Executing
        with mock.patch('TDM.pack') as mock_pack_command:
            command_string = f'python TDM.py pack --PARENT {dummy_parent} --PATIENT {dummy_patient} --VERSION {version}'
            os.chdir(r'./'+'src')
            subprocess.run(command_string, shell=True)

              

if __name__ == '__main__':
    unittest.main()
    
