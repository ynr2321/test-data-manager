
import os
from class_combiner import Combiner
from helper import chooser

nuget_exe_path = r'nuget' # nuget must be added to PATH environment variables for this scrip to work
#nuget_feed = r"C:\Users\ynooe11004\Documents\TDM_nuget_feed" #  change to azure feed once set up
nuget_feed = "https://elektasoftwarefactory.visualstudio.com/TSM/_artifacts/feed/TestData@Local"

# Select mode of use
print()
use_mode = input('Select use-mode (PACK OR UNPACK): ')
print()

if use_mode == 'pack' or use_mode == 'PACK' or use_mode == 'Pack':
    # prompt user to input parent directory, patient and new package version number
    choices = chooser()
    choices.choosePatient()
    choices.chooseNewVersionNum(nuget_feed)
    choices.askToAddPackageSource()
    
    # executing packing
    object = Combiner()
    if choices.APS_choice == 'Y' or choices.APS_choice == 'y':
        object.add_package_source(choices.nuget_config_file, choices.key, choices.value, nuget_feed)
    else:
        pass
    object.pack(nuget_feed, choices.parent_dir, choices.dicom_folder_name, choices.new_version_num)


elif use_mode == 'unpack' or use_mode == 'UNPACK' or use_mode == 'Unpack':
    # allows user to input args for unpacking command
    choices = chooser()
    choices.chooseVersionToUnpack(nuget_feed)

    object = Combiner()
    object.unpack_version(choices.package_name, choices.unpacking_folder_path,
                          choices.unpack_version, nuget_feed)



