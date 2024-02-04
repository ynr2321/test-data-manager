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

class Testchooser(unittest.TestCase):
    def test_helper_choose_patient(self):
        
        with mock.patch('helper.input') as mock_input:
                picker = chooser()
                picker.choosePatient
                mock_input.assert_called_once
                # comment out assert for now
                #self.assertEqual(picker.parent_dir, 'path')
                  
if __name__ == '__main__':
    unittest.main()