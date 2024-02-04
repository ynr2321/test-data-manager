import os
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
from nuspec_generator import NuSpecGenerator

class TestNuspecGenerator(unittest.TestCase): 
    
    def test_IfAnyNuspecGenerated(self):
        mock_dicom_path = r'user/documents/DICOM_directory'
        with mock.patch('os.listdir', return_value=['file1.dcm', 'file2.dcm', 'file3.txt', 'file4.dcm']):
            with mock.patch('os.path.basename',return_value = r'DICOM_directory'):
                with mock.patch('os.open', return_value = 1234):
                    with mock.patch('os.close') as mock_os_close:
                        with mock.patch('os.write') as mock_os_write:
                            with mock.patch('os.fdopen') as mock_fdopen:
                                mock_file_object = mock_fdopen.return_value
                                mock_file_object.read.return_value = "Mock manfiest file contents"
                                with mock.patch('json.loads', return_value={'first_name': 'DANIEL', 'SOP_identifiers': ['2.16.840.1.114337.1.1.1488285161.15', '2.16.840.1.114337.1.1.1488285161.15', '2.16.840.1.114337.1.1.1488285161.15']}):
                                    generator = NuSpecGenerator(mock_dicom_path)
                                    MockManifestFilepath = 'fake path'
                                    MockNugetDirectory = 'another fake path'
                                    generator.generate_nuspec(MockManifestFilepath, MockNugetDirectory, '1.0.0')
                                    
                                    # asserts
                                    mock_os_write.assert_called_once
                                    mock_os_close.assert_called_once
                
    def test_IfCorrectNumberOfWritesUsedInNuspecGeneration(self):
        mock_dicom_path = r'user/documents/DICOM_directory'
        with mock.patch('os.listdir', return_value=['file1.dcm', 'file2.dcm', 'file3.txt', 'file4.dcm']):
            with mock.patch('os.path.basename',return_value = r'DICOM_directory'):
                with mock.patch('os.open', return_value = 1234):
                    with mock.patch('os.close') as mock_os_close:
                        with mock.patch('os.write') as mock_os_write:
                            with mock.patch('os.fdopen') as mock_fdopen:
                                mock_file_object = mock_fdopen.return_value
                                mock_file_object.read.return_value = "Mock manfiest file contents"
                                with mock.patch('json.loads', return_value={'first_name': 'DANIEL', 'SOP_identifiers': ['2.16.840.1.114337.1.1.1488285161.15', '2.16.840.1.114337.1.1.1488285161.15', '2.16.840.1.114337.1.1.1488285161.15']}):
                                    generator = NuSpecGenerator(mock_dicom_path)
                                    MockManifestFilepath = 'fake path'
                                    MockNugetDirectory = 'another fake path'
                                    generator.generate_nuspec(MockManifestFilepath, MockNugetDirectory, '1.0.0')
                                    # ASSERTS
                                    # .call_count is an attribute of every object of the 'mock' class.
                                    # It gets updated every time the mock object is called
                                    print('os.write was called ', mock_os_write.call_count, 'times.')
                                    self.assertEqual(mock_os_write.call_count, 15)
                                    mock_os_close.assert_called_once
                
                

                        
if __name__ == '__main__':
    unittest.main()