# Note: The path of the location you pack .nupkg files to must be added as a source in nuget pacakge manager if you wish to unpack those files
# Use guide: create, add feed, pack, push to feed, unpack
# Create main app object, add inteded packing destination to feed, pack to same folder, push to feed using '.add' unpack to any folder
# Random comment
import sys
import os
import subprocess
import dicom_parser
from dicom_parser import DicomParser
import nuspec_generator
from nuspec_generator import NuSpecGenerator
import package_handler
from package_handler import PackageHandler

class Combiner:
    def __init__(self):
        pass

    def pack(self, nuget_feed, parent_dir, dicom_folder_name, new_version_num, api_key):
        # initializing variables
        self.nuget_feed = nuget_feed
        self.parent_dir = parent_dir
        self.nuget_exe_path = 'nuget'
        self.dicom_folder_name = dicom_folder_name
        self.dicom_directory = os.path.join(self.parent_dir,self.dicom_folder_name)
        self.api_key = api_key
        manifest_directory = os.path.join(self.parent_dir,self.dicom_folder_name + 'manifest')
        
        # instantiating classes, generating nuspec
        dicom_directory_path = os.path.join(parent_dir,dicom_folder_name)
        parser = DicomParser(dicom_directory_path)
        parser.generate_manifest()
        nuspec_gen = NuSpecGenerator(dicom_directory_path)
        nuspec_gen.generate_nuspec(parser.manifest_file_path, self.nuget_feed, new_version_num)
        pkg_handler = PackageHandler(self.nuget_feed, self.api_key)
        pkg_handler.pack(nuspec_gen.nuspec_path)
        
        
    def add_package_source(self, nuget_config_file, key, value, nuget_feed):
        self.package_handler = PackageHandler(nuget_feed)
        self.package_handler.add_package_source(nuget_config_file, key, value)
        
    def unpack_version(self, package_name, output_directory, version, nuget_feed):
        self.package_handler = PackageHandler(nuget_feed)
        self.package_handler.unpack_version(package_name,output_directory, version)
        


        
   

        
        

         
        
        
       
    
        
        
    
