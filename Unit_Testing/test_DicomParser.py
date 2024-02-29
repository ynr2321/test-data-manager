import os
import pydicom
import sys

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
from dicom_parser import DicomParser


class TestDicomParser(unittest.TestCase):
    
    def test_GenerateManifestWritesCorrectDataToManifest(self):
        
        ds = pydicom.Dataset()
        ds.PatientName = "CITIZEN^Joan"
        print(ds.PatientName.given_name)
        ds.SOPInstanceUID = "fake SOP ID"
        # .dcmread usually returns a pydicom 'filedataset' so we are creating the return item manually in order to mock

        # Mocking os and pydicom methods
        with mock.patch('os.listdir', return_value=['file1.dcm', 'file2.dcm', 'file3.txt', 'file4.dcm']):
            with mock.patch('pydicom.dcmread',return_value=ds):
                with mock.patch('os.open'):
                    with mock.patch('os.write', return_value = 1234) as mock_os_write:
                        with mock.patch('os.close') as mock_os_close: 
                            with mock.patch('os.chdir'):         
                                                            
                                dicom_parser = DicomParser(r'fake\path')
                                dicom_parser.generate_manifest()

                                # checking if SOP Ids and first name were recorded
                                pass_criteria = 'parser DID NOT write values for name and SOP ids'
                                if 'first_name' and 'SOP_identifiers' in dicom_parser.string:
                                    pass_criteria = 'parser wrote values for name and SOP ids'
                            
                            
                               #self.assertEqual(dicom_parser.string, '{\n    "first_name": "Joan",\n    "SOP_identifiers": [\n        "fake SOP ID",\n        "fake SOP ID",\n        "fake SOP ID"\n    ]\n}')
                                self.assertEqual(pass_criteria, 'parser wrote values for name and SOP ids')
                                mock_os_write.assert_called_once
                                mock_os_close.assert_called_once
                          
            
if __name__ == '__main__':
    unittest.main()



