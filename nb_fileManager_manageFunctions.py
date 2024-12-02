import maya.cmds as cmds
import re
import os
import shutil
import subprocess as sp

import json

from nb_file_manager import nb_fileManager_UI as fm_ui
from nb_file_manager import nb_fileManager_lib as fm_lib

from PySide2 import QtWidgets

json_file = fm_lib.json_file_name.replace ('\\', '/')
mayapy_sub_command = "from nb_file_manager import nb_fileManager_mayaPy;{}"

#------------------------------------------------------------------------------------------------------------
#                               Manage Project functions
#------------------------------------------------------------------------------------------------------------

# create project
def create_project (path_) :
    
    # get last folder name
    project_name = re.findall(fm_lib.last_folder_name_key, r'{}'.format(path_.replace('/', '\\')))[0]

    new_project_data = {'project_name' : project_name, 'project_path' : path_, 'CH_asset' : [], 'PR_asset' : [], 'BG_asset' : [], 'FX_asset' : [],
                        'sequences' : [], 'shot' : [], 'materials' : [], 'global_scenes' : [], 'FX_shot' : []}

    save_project_parameters (project_name, new_project_data)
    set_current_project (project_name)

    return path_, project_name

def set_current_project (current_project) :
    
    data = get_projects_datas ()
    data['current_project'] = current_project

    with open(json_file, "w") as f :
        json.dump(data, f, indent=4)

# create project tree in selected path, with current name
def create_project_tree (path_) :

    confirmation = fm_ui.ConfirmationDialog(custom_message = "You're about to create a project folder tree.\nContinue ?")
    result = confirmation.exec_()
    
    if result != QtWidgets.QDialog.Accepted :
        return "Tree creation aborted"
    
    for tree_folder in fm_lib.project_folder_dict.keys() :
        create_folder(r'{}/{}'.format(path_, fm_lib.project_folder_dict[tree_folder]['path']))
        
    return "Folder tree created"

def save_project_parameters (project_name, project_to_save) : 
    
    data = get_projects_datas ()

    if not data :
        data = {}

    data[project_name] = project_to_save

    with open(json_file, "w") as f :
        json.dump(data, f, indent=4)

def get_project_parameters (project) :

    data = get_projects_datas ()
    
    if not project :
        return data
    
    return data[project]

def get_projects_datas () :

    with open (json_file, "r") as f :
        data = json.loads(f.read())

    return data


  
#------------------------------------------------------------------------------------------------------------
#                               Manage folder functions
#------------------------------------------------------------------------------------------------------------

# create a folder if doesn't already exist 
def create_folder (path_) :
        
    if not os.path.isdir(path_):
        os.mkdir(r'{}'.format (path_))
    return path_

# ask the user a name for a new element. return the name if it's valid according to naming key          
def ask_user_for_valid_name (valid_name_key) : 
    
    is_valid = False

    while is_valid == False :

        name_dialog = fm_ui.TextDialog()
        dialog_result = name_dialog.exec_()

        if dialog_result :

            new_elem_name = name_dialog.get_text()
            
            valid_name = re.findall(valid_name_key, r'{0}'.format(new_elem_name))
            
            if valid_name :
                is_valid = True
                return valid_name[0]
            else :
                invalid_name_dialog = fm_ui.StandardDialog()
                invalid_name_dialog.warning_message = 'Invalid Name, must be \n<AssetType>_<Asset> or\n<'
                invalid_name_dialog.warning_dialog()
        
        else :
            return False

# add assets folder if asset doesn't exists and if naming is correct
def add_asset_folder (path_, asset_type) :
    
    if not path_ or not os.path.isdir(path_):
        return False
    
    if asset_type == 'CH' :
        expected_path = fm_lib.project_folder_dict['prod_asset_ch_folder']['path']
        valid_name_key = fm_lib.ch_name_check_key
        asset_folder_dict = fm_lib.ch_folder_path
        asset_data = 'CH_asset'

    elif asset_type == 'PR' :
        expected_path = fm_lib.project_folder_dict['prod_asset_pr_folder']['path']
        valid_name_key = fm_lib.pr_name_check_key
        asset_folder_dict = fm_lib.pr_folder_path
        asset_data = 'PR_asset'

    elif asset_type == 'BG' :
        expected_path = fm_lib.project_folder_dict['prod_asset_bg_folder']['path']
        valid_name_key = fm_lib.bg_name_check_key
        asset_folder_dict = fm_lib.bg_folder_path
        asset_data = 'BG_asset'

    elif asset_type == 'FX asset' :
        expected_path = fm_lib.project_folder_dict['prod_asset_fx_folder']['path']
        valid_name_key = fm_lib.fx_name_check_key
        asset_folder_dict = fm_lib.fx_asset_folder_path
        asset_data = 'FX_asset'

    path_.replace('\\', '/')

    if not path_.endswith(expected_path) :
        return False

    asset_name = ask_user_for_valid_name (valid_name_key)  

    if not asset_name :
        return False

    # set prod and preprod path
    prod_asset_path = r'{}\{}'.format (path_, asset_name) 
    preprod_fx_path = r'{}\{}'.format (path_.replace(fm_lib.project_folder_dict['prod_folder']['path'], fm_lib.project_folder_dict['pre_technical_doc_folder']['path']), asset_name)
        
    # create asset folder
    for folder in asset_folder_dict.keys() :
        create_folder( r'{0}\{1}'.format(prod_asset_path, asset_folder_dict[folder]['path']))
    
    create_folder( r'{0}\{1}'.format(preprod_fx_path, asset_folder_dict['root_folder']['path']))

    current_project = get_project_parameters ('current_project')
    project_datas = get_project_parameters (current_project)

    if not asset_data in project_datas.keys() :
        project_datas[asset_data] = [asset_name]
    else :
        project_datas[asset_data].append(asset_name)

    save_project_parameters (current_project, project_datas)
        
    return prod_asset_path

# add fx to path
def add_fx_folder (path_) :

    # check if directory is valid
    if not path_ or not os.path.isdir(path_):
        return False
    
    if not fm_lib.project_folder_dict['prod_asset_fx_folder']['path'] in path_ or path_.endswith(fm_lib.project_folder_dict['prod_asset_fx_folder']['path']) :
        return
    
    fx_name = ask_user_for_valid_name (fm_lib.fx_name_check_key)
    if not  fx_name:
        return
    
    asset_fx_path = r'{}\{}'.format (path_, fx_name)
    shot_fx_path = r'{}{}\{}'.format (path_.replace(fm_lib.project_folder_dict['prod_asset_fx_folder']['path'], fm_lib.project_folder_dict['prod_sequences_folder']['path']), fm_lib.shot_folder_path["sequence_fx"]['path'], fx_name)
    tested_shot_path = r'{}{}'.format (path_.replace(fm_lib.project_folder_dict['prod_asset_fx_folder']['path'], fm_lib.project_folder_dict['prod_sequences_folder']['path']), fm_lib.shot_folder_path["sequence_fx"]['path'])
    print (tested_shot_path)
    if not os.path.exists(tested_shot_path) :
        cmds.warning ("SHOT path doesn't exist, please create first the shot before create shot's FX")
        return
    
    for folder_path in fm_lib.fx_asset_folder_path.keys() :
        create_folder( r'{}/{}'.format(asset_fx_path, fm_lib.fx_asset_folder_path[folder_path]['path']))

        if folder_path == "root_folder" :
            create_folder( r'{}/{}'.format(shot_fx_path, fm_lib.fx_asset_folder_path[folder_path]['path']))

# add shot to sequence 
def add_shot_folder ( path_) :
            
    # check if directory is valid
    if not path_ or not os.path.isdir(path_):
        return False
    
    if not path_.endswith(fm_lib.project_folder_dict['prod_sequences_folder']['path']) :
        return

    shot_name = ask_user_for_valid_name (fm_lib.shot_name_check_key)
    
    if not shot_name :
        return

    # get prod path_split
    shot_path = r'{}\{}'.format (path_, shot_name)
    fx_asset_path = r'{}\{}'.format (path_.replace(fm_lib.project_folder_dict['prod_sequences_folder']['path'], fm_lib.project_folder_dict['prod_asset_fx_folder']['path']), shot_name)
    render_scene_path = r'{}\{}'.format (path_.replace(fm_lib.project_folder_dict['prod_sequences_folder']['path'], fm_lib.project_folder_dict['prod_asset_render_scene_folder']['path']), shot_name)
    render_images_path = r'{}\{}'.format (path_.replace(fm_lib.project_folder_dict['prod_sequences_folder']['path'], fm_lib.project_folder_dict['prod_asset_render_images_folder']['path']), shot_name)
    compo_path =r'{}\{}'.format (path_.replace(fm_lib.project_folder_dict['prod_sequences_folder']['path'], fm_lib.project_folder_dict['prod_asset_compo_folder']['path']), shot_name)
        
    # create shot folders
    for folder_path in fm_lib.shot_folder_path.keys() :
        if 'sequence' in folder_path or 'root' in folder_path :
            create_folder( r'{}/{}'.format(shot_path, fm_lib.shot_folder_path[folder_path]['path']))
            
        if 'render_scene' in folder_path or 'root' in folder_path:
            create_folder( r'{}/{}'.format(render_scene_path, fm_lib.shot_folder_path[folder_path]['path']))

        if 'render_image' in folder_path or 'root' in folder_path:
            create_folder( r'{}/{}'.format(render_images_path, fm_lib.shot_folder_path[folder_path]['path']))
            
        if 'compo' in folder_path or 'root' in folder_path:
            create_folder( r'{}/{}'.format(compo_path, fm_lib.shot_folder_path[folder_path]['path']))

        if 'root' in folder_path :
            create_folder( r'{}/{}'.format(fx_asset_path, fm_lib.shot_folder_path[folder_path]['path']))

            
    return shot_path

def add_prod_folder(path_, asset_type) :

    if not path_ or not os.path.isdir(path_):
        return False

    elif asset_type == 'global scene' :
        valid_name_key = fm_lib.global_scene_name_check_key
        asset_folder_dict = fm_lib.global_scene_path
        asset_data = 'global_scenes'

    elif asset_type == 'material' :
        valid_name_key = fm_lib.material_name_check_key
        asset_folder_dict = fm_lib.material_path
        asset_data = 'materials'

    path_.replace('\\', '/')

    asset_name = ask_user_for_valid_name (valid_name_key)  

    if not asset_name :
        return False

    # set prod and preprod path
    prod_asset_path = r'{}\{}'.format (path_, asset_name) 
    
    # create asset folder
    for folder in asset_folder_dict.keys() :
        create_folder( r'{0}\{1}'.format(prod_asset_path, asset_folder_dict[folder]['path']))

    current_project = get_project_parameters ('current_project')
    project_datas = get_project_parameters (current_project)

    project_datas[asset_data].append(asset_name)

    save_project_parameters (current_project, project_datas)
        
    return prod_asset_path

# delete selected folder  
def delete_folder ( path_):
            
    # if path exists, continue
    if os.path.exists(path_):

        # list sub files and sub directories
        sub_files = os.listdir(path_)
        
        # if sub_files founded, display a warning dialog 
        if sub_files :
            sub_files_confirmation = fm_ui.ConfirmationDialog(custom_message = "Sub folders or files founded. Continue ?")
            result = sub_files_confirmation.exec_()

            # if user cancel the operation, stop function
            if result != QtWidgets.QDialog.Accepted :
                return 'Aborted'
                
            shutil.rmtree(path_)
        
        else :
            os.rmdir(path_)    
    else :
        cmds.warning("Selected path doesn't exist")

# delete selected file    
def delete_file ( path_):
    # if path exists, delete file, else, raise an error
    if os.path.exists(path_):
        os.remove(path_)
    else:
        cmds.warning("Selected path doesn't exist") 

# list all files below selected path. return a list depends on return_filter flag
def get_all_files_below ( path_) :
    
    path_list = []
    for root, dirs, files in os.walk(path_, topdown = True):

        for name in files:
            path_list.append(os.path.join(root, name))
        for name in dirs:
            path_list.append(os.path.join(root, name))
    
    return path_list

def backup_files (file_path, destination_path) :

    if os.path.exists(destination_path) :
                
        from_time = os.path.getmtime(file_path)
        dest_time = os.path.getmtime(destination_path)

        if dest_time >= from_time : 
            return False

        else :
            if os.path.isfile (file_path) == True :
                os.remove(destination_path)
                shutil.copy2(file_path, destination_path)

            elif os.path.isdir (file_path) == True :
                shutil.rmtree(destination_path, ignore_errors=True)
                shutil.copytree(file_path, destination_path)

    else :
        if os.path.isfile (file_path) == True :
            shutil.copy2(file_path, destination_path)

        elif os.path.isdir (file_path) == True :
            shutil.copytree(file_path, destination_path)

    return True


def get_unknown_folders () :
# 'project_name' : project_name, 'project_path' : path_, 'CH_asset' : [], 'PR_asset' : [], 'BG_asset' : [], 'FX_asset' : [],
#                       'sequences' : [], 'shot' : [], 'materials' : [], 'global_scenes' : [], 'FX_shot' : []}

    curr_project = get_project_parameters ('current_project')
    project_datas = get_project_parameters (curr_project)
    root_path = project_datas['project_path']

    unknown_path = []

    for root, dirs, files in os.walk(root_path, topdown = True) :
        for dir_ in dirs :

            abs_dir = os.path.join(root, dir_)

            for path_ in fm_lib.project_folder_dict, fm_lib.pr_folder_path, fm_lib.bg_folder_path, fm_lib.fx_asset_folder_path, fm_lib.shot_folder_path, fm_lib.global_scene_path, fm_lib.material_path:
                if abs_dir.endswith(fm_lib.project_folder_dict[path_]['path']) :
                    unknown_path.append(abs_dir)

    return unknown_path


#-----------------------------------------------------------------------
#                   Verify nomenclature functions
#-----------------------------------------------------------------------

# check windows naming depends on where the user clicked
def check_windows_file_naming (path_, naming_rules_dict):

    unchecked_files = []
    project_folders = fm_lib.project_folder_dict

    # Get curren tproject path, to delete it from root path
    curr_project = get_project_parameters ('current_project')
    project_datas = get_project_parameters (curr_project)
    root_path = project_datas['project_path']

    # For each file, find the naming rule list, based on file root path
    for root, dirs, files in os.walk(path_, topdown = True) :
        
        for file_name in files :

            # pass files
            if file_name == 'Thumbs.db' or root.endswith('.mayaSwatches') or file_name == 'workspace.mel' or "00_Recherches_Perso" in root or "02_GraphicDesign\\06_Anim" in root or "00_Ressources" in root or "_autosave_" in file_name or "painter_lock" in file_name :
                continue

            elif "backup" in root and "04_Houdini" in root :
                continue

            # replace all invalid caracter to get clean path
            absolute_root = root.replace('\\', '/')
            path_location_suffix = ""
            naming_rules = []

            # search in absolute path for file location. When finded, text if "naming" in result, then the file is right placed.
            # get corresponding file naming
            for dict_path in naming_rules_dict :
                if dict_path == "root_folder" :
                    continue

                if absolute_root.endswith(naming_rules_dict[dict_path]["path"]) and naming_rules_dict[dict_path]["naming"]:
                    path_location_suffix = naming_rules_dict[dict_path]["path"]
                    naming_rules = naming_rules_dict[dict_path]["naming"]

                elif absolute_root.endswith(naming_rules_dict[dict_path]["path"]) and not naming_rules_dict[dict_path]["naming"] :
                    unchecked_files.append((root, file_name, 'Invalid File Path', "", ""))

            if not naming_rules or not path_location_suffix :
                unchecked_files.append((root, file_name, "Not founded file path", file_name, naming_rules))
            
            else :
                last_folder = absolute_root[:-len(path_location_suffix)].split("/")[-1]
                file_name_split = get_file_word_list(file_name)
                result = check_naming(file_name_split, naming_rules, last_folder)

                print (file_name, result)

                if not result or isinstance(result, str) :
                    unchecked_files.append((root, file_name, result, file_name_split, naming_rules))
                else :
                    for x in result :
                        if not x :
                            unchecked_files.append((root, file_name, result, file_name_split, naming_rules))
             
    return unchecked_files

def get_asset_folder () :
    pass

def get_file_word_list (file_name) :

    absolute_path_split = re.split(r'(__|[.])', file_name)

    for x in absolute_path_split :
        if x  == "__" or x  == "." :
            absolute_path_split.remove(x)

    return absolute_path_split

def check_naming (split_name, key, folder_name) :

    matching_result = []
    
    for matching_key in key :

        matching_elem_list = []
        returned_value = ""
   
        if len(split_name) != len(matching_key) :
            if "_" in split_name[0] :
                returned_value =  "Only one underscore, need two"
            else :
                returned_value =  "Element Missing"
            
            matching_result.append(returned_value)
            continue
        
        for key_item in range(len(matching_key)) :
            
            is_correct_item = True

            if matching_key[key_item] == 'name' :
                is_correct_item = check_matching_key(r'^([a-zA-Z0-9_]+)$', split_name[key_item])

            elif matching_key[key_item] == 'folderName' :
                asset_name = folder_name.split('__')[-1]
                is_correct_item = check_matching_key(r'^({})(.?)+$'.format(asset_name), split_name[key_item])

            elif matching_key[key_item] == 'ext' :
                is_correct_item = check_matching_key(r'^([a-zA-Z0-9_]+)$', split_name[key_item])

            elif matching_key[key_item] == 'type' :
                type_name = folder_name.split('_')[1]
                is_correct_item = check_matching_key(type_name, split_name[key_item])

            elif isinstance(matching_key[key_item], list) :
                in_list = []
                for i in matching_key[key_item] :
                    in_list.append(check_matching_key(i, split_name[key_item]))

                if not True in in_list :
                    is_correct_item = False

            else : 
                is_correct_item = check_matching_key(matching_key[key_item], split_name[key_item])

            matching_elem_list.append(is_correct_item)

        matching_result.append(matching_elem_list)

    post_value = 0
    for result in matching_result :
        if len (matching_result) != 1 :
            print (split_name, matching_result)
        valid_value = 0
        if isinstance(result, str) :
            valid_value = 1
        else : 
            for elem in result :
                if elem :
                    valid_value += 1

        if valid_value > post_value :
            post_value = valid_value
            correct_result = result

    return correct_result

def check_matching_key(key, elem) :

    matching = True

    if '^' in key and '$' in key :
        if not re.findall(key, elem):
            matching = False

    elif not key :
        pass

    elif key != elem :
        matching = False

    return matching

def check_publish_update(path_) :

    publish_path = os.path.join (path_, fm_lib.project_folder_dict["prod_asset_publish_asset_folder"]["path"][1:])

    ch_path = os.path.join (path_, fm_lib.project_folder_dict["prod_asset_ch_folder"]["path"][1:])
    pr_path = os.path.join (path_, fm_lib.project_folder_dict["prod_asset_pr_folder"]["path"][1:])
    bg_path = os.path.join (path_, fm_lib.project_folder_dict["prod_asset_bg_folder"]["path"][1:])

    ch_test_key = ["mod_def_folder",
                     "uvs_def_folder",
                     "shadding_maya_def_folder",
                     "bs_def_folder",
                     "rig_def_folder",
                     "publish_folder"
                     ]
    
    pr_bg_path_check = ["mod_def_folder","uvs_def_folder","shadding_maya_def_folder","rig_def_folder", "publish_folder"]

    result_list = []

    for asset_path in [ch_path, pr_path, bg_path] :
        asset_list = []
    
        for root, dirs, files in os.walk(asset_path, topdown = True) :

            for file_ in files :
                result = False
                abs_root = root.replace("\\","/")

                if ".mayaSwatches" in root :
                    continue
                

                if "/01_CH/" in abs_root or "/02_PR/" in abs_root or "/03_BG/" in abs_root :
                    if "_Def" in abs_root :

                        if "/03_Shading/" in abs_root :
                            is_done_asset = abs_root.split ("/")[-4]
                        else :
                            is_done_asset = abs_root.split ("/")[-3]

                        if is_done_asset in asset_list :
                            continue
                        else :
                            asset_list.append(is_done_asset)

                        if "/01_CH/" in abs_root :
                            for test_key in ch_test_key:
                                if fm_lib.ch_folder_path[test_key]["path"] in abs_root :

                                    target_replace_path = fm_lib.ch_folder_path[test_key]["path"]
                                    target_replace_file = fm_lib.ch_folder_path[test_key]["naming"][0][-3]

                                    mod_def_path = abs_root.replace(target_replace_path, fm_lib.ch_folder_path["mod_def_folder"]["path"])
                                    uvs_def_path = abs_root.replace(target_replace_path, fm_lib.ch_folder_path["uvs_def_folder"]["path"])
                                    shd_def_path = abs_root.replace(target_replace_path, fm_lib.ch_folder_path["shadding_maya_def_folder"]["path"])
                                    bs_def_path = abs_root.replace(target_replace_path, fm_lib.ch_folder_path["bs_def_folder"]["path"])
                                    rig_def_path = abs_root.replace(target_replace_path, fm_lib.ch_folder_path["rig_def_folder"]["path"])
                                    publish_asset_path = abs_root.replace(target_replace_path, fm_lib.ch_folder_path["publish_folder"]["path"])

                                    mod_def_file = file_.replace(target_replace_file, fm_lib.modeling)
                                    uvs_def_file = file_.replace(target_replace_file, fm_lib.uv)
                                    shd_def_file = file_.replace(target_replace_file, fm_lib.texture)
                                    bs_def_file = file_.replace(target_replace_file, fm_lib.blendshape)
                                    rig_def_file = file_.replace(target_replace_file, fm_lib.rigging)
                                    publish_file = file_.replace("__{}.DEF.ma".format(target_replace_file), ".DEF.ma")

                                    file_path_list = [(mod_def_path, mod_def_file), 
                                                      (uvs_def_path, uvs_def_file), 
                                                      (bs_def_path, bs_def_file),
                                                      (shd_def_path, shd_def_file), 
                                                      (rig_def_path, rig_def_file), 
                                                      (publish_asset_path, publish_file)]

                        else :
                            for test_key in pr_bg_path_check:
                                if fm_lib.pr_folder_path[test_key]["path"] in abs_root :

                                    target_replace_path = fm_lib.pr_folder_path[test_key]["path"]
                                    target_replace_file = fm_lib.pr_folder_path[test_key]["naming"][0][-3]

                                    mod_def_path = abs_root.replace(target_replace_path, fm_lib.pr_folder_path["mod_def_folder"]["path"])
                                    uvs_def_path = abs_root.replace(target_replace_path, fm_lib.pr_folder_path["uvs_def_folder"]["path"])
                                    shd_def_path = abs_root.replace(target_replace_path, fm_lib.pr_folder_path["shadding_maya_def_folder"]["path"])
                                    rig_def_path = abs_root.replace(target_replace_path, fm_lib.pr_folder_path["rig_def_folder"]["path"])
                                    publish_asset_path = abs_root.replace(target_replace_path, fm_lib.pr_folder_path["publish_folder"]["path"])

                                    mod_def_file = file_.replace(target_replace_file, fm_lib.modeling)
                                    uvs_def_file = file_.replace(target_replace_file, fm_lib.uv)
                                    shd_def_file = file_.replace(target_replace_file, fm_lib.texture)
                                    rig_def_file = file_.replace(target_replace_file, fm_lib.rigging)
                                    publish_file = file_.replace("__{}.DEF.ma".format(target_replace_file), ".DEF.ma")

                                    file_path_list = [(mod_def_path, mod_def_file), 
                                                      (uvs_def_path, uvs_def_file), 
                                                      (shd_def_path, shd_def_file), 
                                                      (rig_def_path, rig_def_file), 
                                                      (publish_asset_path, publish_file)]

                        newer_local_file = ""
                        for x in  range(len(file_path_list)):
                            
                            test_path, test_name = file_path_list[x]

                            if not newer_local_file :
                                test_path_plus1 , test_name_plus1 = file_path_list[x+1]
                                local_result = test_file_date(os.path.join(test_path, test_name), os.path.join(test_path_plus1, test_name_plus1))
                                newer_local_file = os.path.join(test_path, test_name)
                            else :
                                local_result = test_file_date(newer_local_file, os.path.join(test_path, test_name))
                            if local_result == "newer" :
                                newer_local_file = os.path.join(test_path, test_name)
                            elif local_result :
                                print ("result undifine")

                        def_mb_file_name = publish_file.replace(".ma", ".mb")
                        print (newer_local_file)
                        test_result = test_file_date(newer_local_file, os.path.join(publish_path, def_mb_file_name))
                    
                        if test_result == "newer" :
                            result = "Is newer"
                        elif test_result == "not exist" :
                            result = "Publish file doesn't exists"

                if result :
                    result_list.append ([newer_local_file, result])

    return result_list

def test_file_date (test_file, compare_file) :
    if not os.path.exists(test_file) :
        return ("test not exist")
    
    if os.path.exists (compare_file) :
        file_time = os.path.getmtime (test_file)
        publish_file_time = os.path.getmtime (compare_file)

        # print (test_file)
        # print ((compare_file))
        # print ("{} -- {}".format(file_time, publish_file_time))

        if file_time > publish_file_time :
            return "newer"

    else :
        return "not exist"
    
    return False  