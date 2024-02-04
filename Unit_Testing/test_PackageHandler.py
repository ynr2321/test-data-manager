import os
import sys
import time
# ALTERNATE ADD TO SYS PATH METHOD
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the 'src' directory to the Python path
src_path = os.path.join(current_script_dir, '..', 'src')
sys.path.insert(0, src_path)
# current_path = os.getcwd()
# sys.path.insert(0, current_path + r'\src')
from package_handler import PackageHandler
import unittest
from unittest import mock
from unittest.mock import patch
import xml.etree.ElementTree as ET
import helper

class TestPackageHandler(unittest.TestCase):
    
    def test_unpack_versionExecutesCorrectCommand(self):
        # calling method
        with mock.patch('subprocess.run') as mock_subprocess_run:
            with mock.patch('os.system'):
        
                tst_pkg_hndlr = PackageHandler('fake nuget feed', 'fakeAPIKEY=cjsaf4354iofj343')
                tst_pkg_hndlr.unpack_version('Fake_Patient',r'dir/target','1.0.0')

                # asserts
                mock_subprocess_run.assert_called_once
                self.assertEqual(tst_pkg_hndlr.unpack_command, 
                'nuget install Fake_Patient -Version 1.0.0 -OutputDirectory dir/target')
                
                
                       
    def test_packExecutesCorrectCommandString(self):
        # creating dummies
        dummy_nuspec_path = r'nuget_feed/dummy_nuspec'
        
        # calling pack method
        with mock.patch('subprocess.run') as mock_subprocess_run:
            with mock.patch('os.system'):
                with mock.patch('re.search') as mock_re_search:
                    with mock.patch('helper.get_descript_from_nuspec') as mock_helper_func1:
                        with mock.patch('helper.get_descriptions') as mock_helper_func2:
                        
                            tst_pkg_hndlr = PackageHandler('fake nuget feed', '<fakeASIkey>')
                            # pre-setting package_path attribute since it is determined from terminal output during the method
                            tst_pkg_hndlr.package_path = r'nuget_feed/dummy.pkg'
                            tst_pkg_hndlr.pack(dummy_nuspec_path)

                            # asserts
                            mock_subprocess_run.assert_called_once
                            self.assertEqual(tst_pkg_hndlr.pack_command, 
                            'nuget pack nuget_feed/dummy_nuspec -OutputDirectory fake nuget feed')
                            self.assertEqual(tst_pkg_hndlr.add_command, 
                            'nuget add nuget_feed/dummy.pkg -Source fake nuget feed')
                    


    # COMMENTED OUT FOR NOW WHILE FIXING CANT FIND (DUMMY) FILE ERROR
    def test_add_package_source_AddsCorrectKeyValue(self):
        testing_config_path = './Unit_Testing/fake_nuget_config_for_package_handler_test.Config'
        # patching
        with mock.patch('subprocess.run') as mock_subprocess_run:
            with mock.patch('os.system'):  
                pass
                # When ET.parse() is called, return an ElementTree Object derived from the config file present in the 'Unit_Testing' folder
                # with mock.patch('xml.etree.ElementTree.ElementTree.write') as mock_tree_write:

    def test_add_package_source_AddsCorrectKeyValue(self):
        print('UNIT TEST IN QUESTION DETECTED')
        testing_config_path = './Unit_Testing/fake_nuget_config_for_package_handler_test.Config'
        # patching
        with mock.patch('subprocess.run') as mock_subprocess_run:
            with mock.patch('os.system'):  
                # When ET.parse() is called, return an ElementTree Object derived from the config file present in the 'Unit_Testing' folder
                # with mock.patch('xml.etree.ElementTree.ElementTree.write') as mock_tree_write:
                    
                    # instantiating and adding package source
                    mock_PackageHandler1 = PackageHandler('dummy/path', '<fakeAPIkey>')
                    mock_PackageHandler1.add_package_source(testing_config_path, 'TEST_SOURCE', 'FAKE_SOURCE')
                    
                    # setting expected add element
                    expected_last_add_element = '<add key="TEST_SOURCE" value="FAKE_SOURCE" />'
                    print('expected_last_add_element is : ', expected_last_add_element)
                    
                    # getting the element that was just added
                    tree = ET.parse(testing_config_path)
                    root = tree.getroot()
                    package_sources = root.find('.//packageSources')
                    last_add_element = package_sources.findall('.//add')[-1]
                    source_str = ET.tostring(last_add_element, encoding='unicode', method='xml')
                    print('the added element is: ', source_str)
                    
                    # asserts
                    self.assertEqual(expected_last_add_element.strip(), source_str.strip()) # strip() removes whitespace
                    
                    print('undoing modification')
                    # REMOVE ADDED SOURCE MANUALLY ----------------------------------------------------------------------------------
                    # Load the XML file
                    tree = ET.parse(testing_config_path)
                    root = tree.getroot()
                    # Find the packageSources element
                    package_sources = root.find('.//packageSources')
                    # Get last <add> element from list of all <add> elements
                    last_add_element = package_sources.findall('.//add')[-1]
                    # Remove the last <add> element
                    package_sources.remove(last_add_element)
                    # Save the modified XML back to the file
                    tree.write(testing_config_path)          
                
if __name__ == '__main__':
    unittest.main()