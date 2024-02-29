# PACKAGE HANDLING:
# Before unpacking, package must be added to feed using add command.
# The 'source path' for this operation should be set by pasting its path in the nuget package manager
# (tools - options - nuget package manager - set and untick othe boxes)
# source path must be the same as the directory the package was packed to in order to extract 
# Otherwise 'package not found' error
# Eg my local nuget config path = r"C:\Users\ynooe11004\AppData\Roaming\NuGet\NuGet.Config"
# IMPORTANT FOR UNPACKING: you must provide just the package name NO EXTENSION OR FULL PATH
import os
import subprocess
import xml.etree.ElementTree as ET
import re
import dicom_parser
from dicom_parser import DicomParser
import helper

class PackageHandler():
    def __init__(self, nuget_feed_path, azure_nuget_feed, api_key):
        self.nuspec_path = None
        self.nuget_feed_path = nuget_feed_path
        self.azure_nuget_feed = azure_nuget_feed
        self.nuget = r'nuget'
        self.config_file = None
        self.package_path = None
        self.api_key = api_key
        self.consider_duplicates_exist = True # by default we warn of duplicate data (SOP IDs)
        print()
                
    def pack(self, nuspec_path):
        
        # deriving patient name from nuspec path
        self.nuspec_path = nuspec_path
        nuspec_name = os.path.basename(nuspec_path)
        patient_name = nuspec_name.rsplit('.nuspec',1)[0]
        

        # ---------------------------- Checking for duplicate packages in local feed (not azure feed) ------------------------------- # 

        # # getting SOP list for file about to be packed and existing version
        # SOP_list = helper.get_descript_from_nuspec(nuspec_path)
        # Existing_SOP_lists = helper.get_descriptions(self.nuget_feed_path,patient_name)
        
        # for key in Existing_SOP_lists:
        #     if SOP_list == Existing_SOP_lists[key]:
        #         print(f'version: {key} of this Data contains an identical description to data being packed')
        #         # self.consider_duplicates_exist = True
    
        #     if self.consider_duplicates_exist == True:
        #         print('\nOne or more package containing an identical description to this package exist. \n')
        #         continue_choice = str(input(' Would you like to continue? (y/n)'))
        #         if helper.remove_white_space(continue_choice) == 'y':
        #             self.consider_duplicates_exist = False

                    
        #     if self.consider_duplicates_exist == True:
        #         print('\ncancelling pack command')
        #         return
            
        #     elif self.consider_duplicates_exist == False:
        #         print('\nContinuing')
            
        # ---------------------------- Packing and adding to feed ---------------------------- # 
        # creating command string
        self.pack_command = f'{self.nuget} pack "{self.nuspec_path}" -OutputDirectory "{self.nuget_feed_path}"'
        
        # getting package path
        print('creating package locally using command: ', self.pack_command)
        result = subprocess.run(self.pack_command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        
        # extract and return the name of the created package from the output
        for line in result.stdout.split('\n'): 
            if line.startswith("Successfully created package"):
                self.package_path = line.split("'")[1]
                
        # setting commmands for pushing to remote feed and adding to local feed
        self.push_command = f'{self.nuget} push {self.package_path} -Source {self.azure_nuget_feed} -ApiKey {self.api_key}'
        self.add_command = f'{self.nuget} add {self.package_path} -Source {self.nuget_feed_path}'
        
        # Running nuget commands
        subprocess.run(self.add_command, shell=True, capture_output=True, text=True) 
        
        print('Pushing package')
        subprocess.run(self.push_command)

        
    def unpack_version(self, package_name_without_extension_or_path, output_directory, azure_nuget_feed, version=None):
        # pulls / installs / unpacks latest package version unless version specified
        if version != None:
            self.unpack_command = f'{self.nuget} install {package_name_without_extension_or_path} -Version {version} -OutputDirectory {output_directory} -Source {azure_nuget_feed}'
            print()
            subprocess.run(self.unpack_command, shell=True)
        else: 
            self.unpack_command = f'{self.nuget} install {package_name_without_extension_or_path} -OutputDirectory {output_directory} -Source {azure_nuget_feed}'
            print()
            subprocess.run(self.unpack_command, shell=True)
       # print('THE COMMAND JUST RUN IS: ', self.unpack_command) # REMOVE DEBUG
            


    def add_package_source(self, nuget_config_file=None, key=None, value=None):
        # parse the XML file
        tree = ET.parse(nuget_config_file)
        root = tree.getroot()
        # create a new <add> element
        new_element = ET.Element("add")
        new_element.set("key", key)
        new_element.set("value", value)
        # find the <packageSources> section and append the new element to it
        package_sources = root.find("packageSources")
        if package_sources is not None:
            package_sources.append(new_element)
        # pretty print to console
        ET.indent(root, space="   ")
        xml_str = ET.tostring(root, encoding='utf8').decode('utf8')
        print('PRINTING XML TREE WHICH IS ABOUT TO BE WRITTEN TO FILE: ')
        print(xml_str)
        print(type(xml_str))
        # save the modified XML back to the file
        tree.write(nuget_config_file, encoding="utf-8", xml_declaration=True)

   


# # # Testing unpack -
# testnuget_feed = r"C:\Users\ynooe11004\Documents\TDM_nuget_feed" # change to azure feed once set up
# testazure_nuget_feed = "https://elektasoftwarefactory.pkgs.visualstudio.com/TSM/_packaging/test-data/nuget/v3/index.json"
# testapikey = ''
# dest_path = r"C:\Users\ynooe11004\Documents\TDM_target"


# testhandler = PackageHandler(testnuget_feed, testazure_nuget_feed, testapikey)
# testhandler.pack()
# testhandler.unpack_version('Daniel_Cranium',dest_path, '1.0.3')
  
 
