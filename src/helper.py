# A module for hiding all the lengthy logic needed in the main scripts
import os
import shutil
import json
import xml.etree.ElementTree as ET

# func to remove the temporary manifest folders from nuget feed after packing operation
def clean_nuget_feed(nuget_feed, patient_name):
    manifest_folder_path = os.path.join(nuget_feed,patient_name) + '_manifest'
    shutil.rmtree(manifest_folder_path)

def get_dict_from_manifest(manifest_file_path):
    manifest_fd = os.open(manifest_file_path, os.O_RDONLY, 0o777)
    
    file_object = os.fdopen(manifest_fd, 'r')
    data = file_object.read()
    
    dictionary = json.loads(data)
    return dictionary


def get_descript_from_nuspec(nuspec_path):
    # storing nuspec contents as a string (data)
    fd = os.open(nuspec_path, os.O_RDONLY, 0o777)
    file_object = os.fdopen(fd, 'r')
    data = file_object.read()

    root = ET.fromstring(data)
    ns = {'ns': 'http://schemas.microsoft.com/packaging/2010/07/nuspec.xsd'}
    description = root.find('.//ns:description', ns)
    SOP_list = description.text
    return SOP_list


def get_descriptions(nuget_feed, patient_name):
    # ---------- Stores description for each version from nuspec file in dict -----------
    dictionary = {}
    # locating nuspec file for each version
    version_folder_path = os.path.join(nuget_feed, patient_name.lower())
    versions =  os.listdir(version_folder_path)
    
    for folder in versions:
        folder_path = os.path.join(version_folder_path,folder)
        
        for file in os.listdir(folder_path):
            if file.endswith("nuspec"):    
    # storing nuspec contents as a string (data)
                file_path = os.path.join(folder_path,file)
                fd = os.open(file_path, os.O_RDONLY, 0o777)
                file_object = os.fdopen(fd, 'r')
                data = file_object.read()
    # remove first line of xml (BOM)
                lines = data.split('\n')
                lines.pop(0)
                data = '\n'.join(lines)
                root = ET.fromstring(data)
                ns = {'ns': 'http://schemas.microsoft.com/packaging/2010/07/nuspec.xsd'}
                description = root.find('.//ns:description', ns)
                dictionary[folder] = description.text
    return dictionary


def remove_white_space(string):
    char_list = list(string)
    for char in char_list:
        if char == ' ':
            char_list.remove(char)

    processed_string = ''.join(char_list)
    return processed_string  

# ------------------- TEMP -------------------------

    
# ---------------------------------- CHOOSER CLASS -----------------------------------
class chooser:
    def __init__(self):
        self.parent_dir = None
        self.dicom_folder_name = None
        self.new_version_num = None
        self.dicom_folder_path = None
        self.APS_choice = None
        self.nuget_config_file = None
        self.key = None
        self.value = None
        self.package_name = None
        self.unpacking_folder_path = None
        self.unpack_version = None
        
    def choosePatient(self):
        # prompt user to enter parent path and dicom data folder name
        self.parent_dir = input('Enter path of folder containing DICOM data ("without quotes"): ')
        folders = [d for d in os.listdir(self.parent_dir) if os.path.isdir(os.path.join(self.parent_dir, d))]
        folders_with_dicoms_inside = [d for d in folders if any(fname.endswith('.dcm') for fname in os.listdir(os.path.join(self.parent_dir,d)))]
        for index, folder in enumerate(folders_with_dicoms_inside, start=1):
            print(f'{index}. {folder}')
        self.dicom_folder_name = input('ENTER PATIENT/FOLDER NAME: ')
        if self.dicom_folder_name not in folders_with_dicoms_inside:
            entry_valid = False
            while entry_valid == False:
                print('INVALID ENTRY')
                self.dicom_folder_name = input('RE-ENTER PATIENT/FOLDER NAME: ')
                if self.dicom_folder_name in folders_with_dicoms_inside:
                    entry_valid = True          
        self.dicom_folder_path = os.path.join(self.parent_dir,self.dicom_folder_name)
        return os.path.join(self.parent_dir,self.dicom_folder_name)
    # test 
    
    def chooseNewVersionNum(self,nuget_feed):
        # prompt user to select new version number for package being created
        if os.path.exists(nuget_feed):
            print('\n')
            pkg_list = [x.replace('.nupkg', '') for x in os.listdir(nuget_feed) if x.endswith(".nupkg")]
            def version_sort_key(item):
                # split up the string by full stops and take last part (patch num)
                patch_num = int(item.split('.')[-1])
                return patch_num
            sorted_pkg_list = sorted(pkg_list, key=version_sort_key)
            # pretty printing list
            print('CURRENT PACKAGES IN FEED: ')
            if len(sorted_pkg_list) == 0:
                print('NONE')
            for index, folder in enumerate(sorted_pkg_list, start=1):
                print(f'{index}. {folder}')
            print('\n')
            self.new_version_num = str(input('ENTER UPDATED VERSION NUMBER FOR DATA BEING PACKED (major.minor.patch): '))
        else:
            self.new_version_num = '1.0.0'


    def askToAddPackageSource(self):
        self.APS_choice = input('Would you like to add a package source to the nuget config file (this only needs to be done once for each nuget_feed folder generated) - Y/N: ')
        if self.APS_choice == 'Y' or self.APS_choice == 'y': 
            while True: 
                try:
                    self.nuget_config_file = input('Enter path of your nuget config file: ')
                    with open(self.nuget_config_file, 'r') as file:
                        break  # If the file is opened successfully, break the loop
                except FileNotFoundError:
                    print("File not found. Please re-enter the path ")
            self.key = input('Name new package source: ')
            self.value = input('Enter path of the <dicomDataFolder>_NuGet_feed folder created after you entered dicom_data folder path: ')
        else:
            pass
    
    
    def chooseVersionToUnpack(self,nuget_feed):
        # allowing user to input unpack arguments
        pkg_list = [x.replace('.nupkg', '') for x in os.listdir(nuget_feed) if x.endswith(".nupkg")]
        
        # getting list of unique patients
        patient_list = []
        for pkg_name in pkg_list:
            name = pkg_name.split('.')[0]
            if name not in patient_list:
                patient_list.append(name)
        print('DICOM DATA AVAILABLE FOR:')
        for index, name in enumerate(patient_list, start=1):
         print(f'{index}. {name}') 
        print()
        self.package_name = input('ENTER PATIENT NAME FOR DATA BEING UNPACKED: ')  
        
        # getting list of package versions for that patient
        patient_pkg_list = [s for s in pkg_list if s.startswith(str(self.package_name))]
        print('\n','PACKAGES AVAILABLE:')
        for index, package in enumerate(patient_pkg_list, start=1):
            print(f'{index}. {package}') 
        print()
        self.unpack_version = str(input('Enter the version of the package you want to unpack (major.minor.patch): '))
        self.unpacking_folder_path = input('Enter unpacking destination: ')  
        
        
# # testing
# nuget_feed = r"C:\Users\ynooe11004\Documents\test_data_management\TDM_nuget_feed"
# choices = chooser()
# choices.chooseVersionToUnpack(nuget_feed)

