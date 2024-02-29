# TDM - Test Data Manager 
import argparse
import os
import helper
from class_combiner import Combiner 

# Creating local folder for packages if doesn't exist
current_directory = os.path.dirname(os.path.abspath(__file__))
new_local_nuget_feed = os.path.join(current_directory, r'nuget_feed')
if not os.path.exists(new_local_nuget_feed):
    os.mkdir(new_local_nuget_feed)
    print(f"Directory nuget_feed created successfully at: {new_local_nuget_feed}")

nuget_feed = new_local_nuget_feed # hard code eg r"C:\Users\ynooe11004\Documents\TDM_nuget_feed"
azure_nuget_feed = "" # enter azure artifacts / remote nuget feed here
api_key = '' # enter access token here

def pack(parent_dir, dicom_folder_name, new_version_num, description=None):
    manager = Combiner()
    manager.pack(nuget_feed, azure_nuget_feed, parent_dir, dicom_folder_name, new_version_num, api_key, description)

def unpack(package_name, output_directory, version):
    manager = Combiner()
    manager.unpack_version(package_name, output_directory, version, nuget_feed, azure_nuget_feed, api_key)
    
def bulk_pull(list_file_path, output_directory):
    manager = Combiner()
    pkg_list = helper.parse_pkg_list_file(list_file_path)
    # each element should be a list: [<packageName> <versionNum>], if versionNum blank, pull latest
    for sublist in pkg_list:
        
        if len(sublist) != 2:
            version = '' # defaults to latest
            
        elif len(sublist) == 0:
            continue # ignore empty lines 
        
        else:
            version = sublist[1]
        # execute one pull for each line in the file 
        manager.unpack_version(sublist[0], output_directory, version, nuget_feed,azure_nuget_feed, api_key)


def main():
    help_message = '''              \n#################################################### T E S T  D A T A  M A N A G E R ####################################################\n
                    PREREQUESITES:\n 
                        1. Install nuget.exe and add to PATH environment variables\n
                        2. In nuget config file, under 'PackageSources', 
                        add: https://elektasoftwarefactory.pkgs.visualstudio.com/TSM/_packaging/test-data/nuget/v3/index.json
                    
                    USAGE: \n
                        TDM pack --PARENT xxx --PATIENT xxx --VERSION xxx --DESCRIPTION "<package description between quotes>"
                        
                            --PARENT        : Parent directory containing Patient DICOM data folders
                            --PATIENT       : Name of patient/folder containing DICOM files
                            --VERSION       : New version number
                            --DESCRIPTION   : Description that appears in azure artifacts nuget feed when package is selected
                                            (Default: None)

                        TDM unpack --PATIENT xxx --TARGET xxx --VERSION xxx

                            --PATIENT        : Name of patient whose package you want to unpack
                            --TARGET         : Output directory / extraction target
                            --VERSION        : Version to unpack
                            
                        TDM bulk_pull --LIST xxx --TARGET xxx

                            --LIST          : path to txt file where format is: 
                                                <Patient_Name> <Version>
                                                <Patient_Name> <Version>
                                                 .
                                                 .
                                                 .
                            --TARGET        : Output directory / extraction target
                    '''
    print(help_message)
    
    parser = argparse.ArgumentParser(description='Test-data-manager CLI app')
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Subparser for the 'pack' command
    pack_parser = subparsers.add_parser("pack", help="TDM pack --PARENT xxx --PATIENT xxx --VERSION xxx --DESCRIPTION \"<package description between quotes>\"")
    pack_parser.add_argument('--PARENT', dest="parent_dir", help="Parent directory containing Patient DICOM data folders")
    pack_parser.add_argument('--PATIENT', dest="dicom_folder_name", help="Name of patient/folder containing DICOM files")
    pack_parser.add_argument('--VERSION', dest="new_version_num", help="New version number")
    pack_parser.add_argument('--DESCRIPTION', dest="description", help="Description that appears in azure artifacts nuget feed when package is selected", default=None)

    # Subparser for the 'unpack' command
    unpack_parser = subparsers.add_parser("unpack", help="TDM unpack --PATIENT xxx --TARGET xxx --VERSION xxx")
    unpack_parser.add_argument('--PATIENT', dest="package_name", help="Name of patient for whose package you want to unpack")
    unpack_parser.add_argument('--TARGET', dest="output_directory", help="Output directory / extraction target")
    unpack_parser.add_argument('--VERSION', dest="version", help="Version to unpack")
    
    # Subparser for the 'bulk_pull' command
    unpack_parser = subparsers.add_parser("bulk_pull", help="TDM bulk_pull --LIST xxx --TARGET xxx")
    unpack_parser.add_argument('--LIST', dest="list_file_path", help="")
    unpack_parser.add_argument('--TARGET', dest="output_directory", help="Output directory / extraction target")



    # setting up command 
    args = parser.parse_args()
    
    if args.command == "pack":
        parent_dir = args.parent_dir.strip('"')  # Remove leading and trailing quote marks
        dicom_folder_name = args.dicom_folder_name.strip('"')  # Remove leading and trailing quote marks
        pack(parent_dir, dicom_folder_name, args.new_version_num, args.description)
        
    elif args.command == "unpack":
        output_directory = args.output_directory.strip('"')  # Remove leading and trailing quote marks
        package_name = args.package_name.strip('"') 
        unpack(package_name, output_directory, args.version)
        
    elif args.command == "bulk_pull":
        list_file_path = args.list_file_path.strip('"')  # Remove leading and trailing quote marks
        output_directory = args.output_directory.strip('"')  # Remove leading and trailing quote marks
        bulk_pull(list_file_path, output_directory)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

