import sys
import os
import pydicom
import pydicom.data
from pydicom.data import get_testdata_file
import json
import helper

class DicomParser:
    def __init__(self, dicom_directory_path):
        self.dicom_directory_path = dicom_directory_path
        self.dicom_folder_name = os.path.basename(self.dicom_directory_path)
        self.dcm_read_list = []
        self.sop_instance_uid_list = []
        # folder containing manifest will be in parent dir of folder containing dicom data
        self.parent = os.path.dirname(dicom_directory_path)
        self.manifest_folder_path = os.path.join(self.parent,self.dicom_folder_name + '_manifest')
        self.manifest_file_path =  None
        self.manifest_filename = os.path.basename(dicom_directory_path) + '_manifest'
   
    def generate_manifest(self):
        # creating manifest directory if it doesn't exist
        if os.path.isdir(self.manifest_folder_path) == False:
         os.makedirs(self.manifest_folder_path)
        
        # creating manifest file
        manifest_file_path = os.path.join(self.manifest_folder_path,self.manifest_filename) + '.txt'
        self.manifest_file_path = manifest_file_path # storing
        #dicom_files = [x for x in os.listdir(self.dicom_directory_path) if x.endswith(".dcm")]
        dicom_files = [x for x in helper.get_all_files_in_tree(self.dicom_directory_path) if x.endswith(".dcm")]
        print()
        
        manifestation = {'first_name': 'unknown',
                           'SOP_identifiers':'unknown'}
        
        # iteratively parsing dicom files
        print(dicom_files)
        if len(dicom_files) > 0:
            try:
                for dicom_file_path in dicom_files:
                    read_dicom = pydicom.dcmread(dicom_file_path, force = True) # print to see all data
                    self.dcm_read_list.append(read_dicom)
                    self.sop_instance_uid_list.append(read_dicom.SOPInstanceUID)
                    # extracting patient name (should be consistent across all files)
                    if dicom_file_path == dicom_files[0]:
                        first_name = read_dicom.PatientName.given_name
            except:
                first_name = 'Could not parse dicom file / incorrect file type'
                self.sop_instance_uid_list = ['Could not parse dicom file / incorrect file type']
        else:
            first_name = 'Could not parse dicom file / incorrect file type'
            self.sop_instance_uid_list = ['Could not parse dicom file / incorrect file type']
            
            
        # modifying manifest dict
        manifestation['first_name'] = first_name
        manifestation['SOP_identifiers'] = self.sop_instance_uid_list
        
        # doing the writing:
        print('Writing to manifest file')
        fd = os.open(manifest_file_path, os.O_RDWR | os.O_CREAT, 0o777)
        self.string = json.dumps(manifestation,indent=4)
        #print('writing to file: ', self.string) # REMOVE DEBUG
        os.write(fd,self.string.encode())
        os.close(fd) # added to stop 'being used by another process' error when packing   
        
          
