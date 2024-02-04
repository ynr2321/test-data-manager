import os
from packaging import version
import dicom_parser
from dicom_parser import DicomParser
import pydicom
import helper

class NuSpecGenerator():
    def __init__(self, dicom_directory_path):
        self.dicom_directory = dicom_directory_path
        self.nuspec_path = None
        
    def generate_nuspec(self, manifest_file_path, nuget_directory, new_version_num):
        dicom_files = [x for x in os.listdir(self.dicom_directory) if x.endswith(".dcm")]
        dicom_folder_name = os.path.basename(self.dicom_directory)
        self.nuspec_path = nuget_directory + r'\{}'.format(dicom_folder_name) + r'.nuspec'
        files_to_package = [manifest_file_path, self.nuspec_path]
        
        # CREATING NUSPEC FILE ------------------------------------------------------------------------
        # specifying files to pack
        for dicom_filename in dicom_files:
            files_to_package.append(self.dicom_directory + '\{}'.format(dicom_filename))  
    
        # getting list of SOP IDs
        manifest_dict = helper.get_dict_from_manifest(manifest_file_path)
        self.sop_instance_uid_list = manifest_dict["SOP_identifiers"]
        
        # specifying metadata for package
        metadata = {
            'id': dicom_folder_name,
            'version': new_version_num,
            'description': self.sop_instance_uid_list,
            'authors': 'IC-package-Handler',
        }
        
        # writing to nuspec file
        nuspec_fd = os.open(self.nuspec_path, os.O_RDWR | os.O_CREAT, 0o777)
        os.write(nuspec_fd,b'<package xmlns="http://schemas.microsoft.com/packaging/2010/07/nuspec.xsd">\n')
        os.write(nuspec_fd,b'  <metadata>\n')
        for key, value in metadata.items():
            os.write(nuspec_fd, f'    <{key}>{value}</{key}>\n'.encode())
        os.write(nuspec_fd, b'  </metadata>\n')
        os.write(nuspec_fd, b'  <files>\n')
        for file in files_to_package:
            os.write(nuspec_fd, f'    <file src="{file}" target="lib" />\n'.encode())
        os.write(nuspec_fd, b'  </files>\n')
        os.write(nuspec_fd, b'</package>\n')
        
        os.close(nuspec_fd)



