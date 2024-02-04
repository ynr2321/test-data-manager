import argparse
import helper
from class_combiner import Combiner
nuget_feed = r"C:\Users\ynooe11004\Documents\TDM_nuget_feed"
azure_nuget_feed = "https://elektasoftwarefactory.pkgs.visualstudio.com/TSM/_packaging/test-data/nuget/v3/index.json"
api_key = '' # enter access token here

def pack(parent_dir, dicom_folder_name, new_version_num):
    manager = Combiner()
    manager.pack(nuget_feed, parent_dir, dicom_folder_name, new_version_num, azure_nuget_feed, api_key)
    #helper.clean_nuget_feed(nuget_feed,dicom_folder_name)

def unpack(package_name, output_directory, version):
    manager = Combiner()
    manager.unpack_version(package_name, output_directory, version, nuget_feed)

def main():
    parser = argparse.ArgumentParser(description='Test-data-manager CLI app')
    
    subparsers = parser.add_subparsers(dest="command")
    
    # Subparser for the 'pack' command
    pack_parser = subparsers.add_parser("pack", help="python packMange.py pack --PARENT xxx --PATIENT xxx --VERSION xxx")
    pack_parser.add_argument('--PARENT', dest="parent_dir", help="Parent directory containing Patient DICOM data folders")
    pack_parser.add_argument('--PATIENT', dest="dicom_folder_name", help="Name of patient/folder containing DICOM files")
    pack_parser.add_argument('--VERSION', dest="new_version_num", help="New version number")

    # Subparser for the 'unpack' command
    unpack_parser = subparsers.add_parser("unpack", help="python packMange.py unpack --PATIENT xxx --TARGET xxx --VERSION xxx")
    unpack_parser.add_argument('--PATIENT', dest="package_name", help="Name of patient for whose package you want to unpack")
    unpack_parser.add_argument('--TARGET', dest="output_directory", help="Output directory / extraction target")
    unpack_parser.add_argument('--VERSION', dest="version", help="Version to unpack")

    args = parser.parse_args()
    
    if args.command == "pack":
        pack(args.parent_dir, args.dicom_folder_name, args.new_version_num)
    elif args.command == "unpack":
        unpack(args.package_name, args.output_directory, args.version)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

# COMMAND EXAMPLE

# WITH FLAGS
# python auto_runner.py pack --PARENT xxx --PATIENT xxx --VERSION xxx
# python auto_runner.py unpack --PARENT xxx --TARGET xxx --VERSION xxx
