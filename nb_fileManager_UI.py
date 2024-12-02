from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance


import maya.OpenMayaUI as omui
import maya.mel as mel
import maya.cmds as cmds
import os
import shutil
import subprocess
import time

from nb_file_manager import nb_fileManager_lib as fm_lib
from nb_file_manager import nb_fileManager_manageFunctions as fm_man


import imp
imp.reload(fm_man)
imp.reload(fm_lib)

json_file = fm_lib.json_file_name.replace ('\\', '/')

def maya_main_windows() :
    '''
    Return maya main window widget as python object
    '''
    maya_main_window = omui.MQtUtil.mainWindow()
    
    #return int value if current python version is 3 or upper, otherwise return long
    if fm_lib.python_version >= 3 :
        return wrapInstance(int(maya_main_window), QtWidgets.QWidget)
    else :
        return wrapInstance(long(maya_main_window), QtWidgets.QWidget)
        
class StandardDialog (QtWidgets.QDialog) :
    '''
    Standard Dialog class used to display QWidget Qmessage defaut warning, error and info box

    __init__(self, maya_main_window)
    warning_dialog (self) : Display a QMessageBox.warning with custom warning message
    '''
    def __init__(self, parent = maya_main_windows()):
        super(StandardDialog, self).__init__(parent)
        
        self.warning_message = 'Warning !'
        self.setWindowFlags(self.windowFlags()^ QtCore.Qt.WindowContextHelpButtonHint)
        
    def warning_dialog(self) :
        
        #Display warning Qwidget Dialog as python object
        QtWidgets.QMessageBox.warning(self, "Warning", self.warning_message)
       
class ConfirmationDialog (QtWidgets.QDialog):
    '''
    A simple Dialog to ask the user bool conformation

    __int__(self, parent, custom_message) 
    create_widget(self, custom_message) : Create widgets for ui
    create_layout(self) : Display widgets in layouts
    create_connections(self) : Connect buttons to functions
    '''
    
    # innit class
    def __init__ (self, parent = maya_main_windows(), custom_message = "Are you sure ?"):
        super (ConfirmationDialog, self).__init__(parent)
        
        # window setup
        self.setWindowTitle("Confirmation")
        self.setWindowFlags(self.windowFlags()^ QtCore.Qt.WindowContextHelpButtonHint)
        
        # window widget, layout and connection functions
        self.create_widget(custom_message)
        self.create_layout()
        self.create_connections()
        
    #create confirmation dialog widget functions
    def create_widget(self, custom_message):
        self.message_text = QtWidgets.QLabel(custom_message)
        self.continue_btn = QtWidgets.QPushButton("Continue")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    # organise wigdets in layout
    def create_layout (self):
        # text layout
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.addStretch()
        text_layout.addWidget(QtWidgets.QLabel("Message :"))
        text_layout.addWidget(self.message_text)
        text_layout.addStretch()
        
        # btn layout
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.continue_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        # main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(text_layout)
        main_layout.addLayout(btn_layout)
        
    # connect widgets
    def create_connections (self) :
        self.continue_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.close)
                      
class TextDialog (QtWidgets.QDialog):
    '''
    A simple Dialog to ask the user string informations
    __init__(self, maya_main_window)
    create_widget(self) : Create widget for ui
    create_layout(self) : Display layout in ui
    create_connections(self) : Connect buttons to functions
    get_text(self) : return current text field text
    '''
    
    # init class
    def __init__ (self, parent = maya_main_windows()):
        super (TextDialog, self).__init__(parent)
        
        # window setup
        self.setWindowTitle("User Entry")
        self.setWindowFlags(self.windowFlags()^ QtCore.Qt.WindowContextHelpButtonHint)
        
        # window widget, layout and connection functions
        self.create_widget()
        self.create_layout()
        self.create_connections()
        
    # create text dialog widget
    def create_widget(self):
        self.text_field = QtWidgets.QLineEdit()
        self.continue_btn = QtWidgets.QPushButton("Continue")

    # organise widgets in layouts
    def create_layout (self):
        # text layout
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.addStretch()
        text_layout.addWidget(QtWidgets.QLabel("Message :"))
        text_layout.addWidget(self.text_field)
        text_layout.addStretch()
        
        # btn layout
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.continue_btn)
        
        # main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(text_layout)
        main_layout.addLayout(btn_layout)
        
    # connect widgets
    def create_connections (self) :
        self.continue_btn.clicked.connect(self.accept)
        
    # return text string
    def get_text(self) :
        return self.text_field.text()

class ProjectManagerUI (QtWidgets.QDialog) :
    '''
    Main UI function. It Creates an UI with menu, and a big QTreeView
    __init__ (self, parent=maya_main_windows()) : Init class and parent class. Create and setup window. call sub window creation functions
    create_actions (self) : create actions
    create_widgets (self) : create widgets for ui
    create_layout (self) : display widgets in layout
    ceate_connections (self) : connect actions and widgets to functions
    on_double_clicked (self, index) : trigger when the user double click
    get_current_selected_path (self) : return current selected path as a list or a string
    get_current_selected_index (self) : return current selected item as list
    show_context_menu (self, point) : display on screen context menu with diferents options based on current selected path
    about (self) : display an about window with script indication for user
    set_current_project (self) : change working directory path and python curent working directory
    trigger_create_project_tree (self) : call ProjectTree.create_project_tree()
    trigger_set_project_name (self) : set window title with current folder name
    trigger_add_asset_folder (self) : get path selected and call ProjectTree.add_asset_folder()
    trigger_add_fx_folder (self) : get path selected and call ProjectTree.add_fx_folder()
    trigger_add_shot_folder (self) : get path selected and call ProjectTree.add_shot_folder()
    trigger_add_sequence_folder (self) : get path selected and call ProjectTree.add_sequence_folder()
    trigger_delete_element (self) : get path selected, check if dirs and call ProjectTree.delete_folder() or ProjectTree.delete_file()
    trigger_check_naming (self) : get path and call check_windows_file_naming() if the function return a list, print list index in ui output
    expand_selection(self) : expand selected item
    collapse_selected (self) : collapse selected item
    collapse_all (self) : collapse every items
    expand_all (self) : expand every items
    add_text_to_output (self, text_to_add, bold) : add text to ui output
    clear_text_output (self) : reset ui output 
    set_name_filter (self) : set treeView model name filter depends on combo box text
    '''
    
    def __init__ (self, parent=maya_main_windows()):
        super (ProjectManagerUI, self).__init__(parent)
        
        # message to display in output textfield
        self.output_message = ""
        self.setWindowFlags(self.windowFlags()^QtCore.Qt.WindowContextHelpButtonHint)
        
        # init variables
        data = fm_man.get_projects_datas()
        
        if 'current_project' in data:
            current_project = data['current_project']
            curent_path = True
            if not current_project in data or not os.path.exists(data[current_project]['project_path']):
                curent_path = False
                self.root_path = ''
                self.project_name = "Default Project"

            else :
                self.root_path = data[current_project]['project_path']
                self.project_name = data[current_project]['project_name']

        else :
            curent_path = False
            self.root_path = ''
            self.project_name = "Default Project"

        # set UI name and minimum size
        
        self.setWindowTitle("Project Manager - {0}".format(self.project_name))
        self.setMinimumSize(800,700)
        
        # remonve the ? from dialog window
        self.setWindowFlags(self.windowFlags()^QtCore.Qt.WindowContextHelpButtonHint)
        
        
        # call functions to create ui
        self.create_actions()
        self.create_widgets()
        self.create_layout() 
        self.load_project()
        self.create_connections()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # connect context menu
        self.customContextMenuRequested.connect(self.show_context_menu)

    # create UI actions 
    def create_actions(self) :
        
        # about acion
        self.about_action = QtWidgets.QAction("About", self)
        
        # files action
        

        # project actions
        self.project_tree_action = QtWidgets.QAction("Create Project Tree", self)
        self.load_project_action = QtWidgets.QAction("Load Project", self)
        self.backup_project_action = QtWidgets.QAction("Backup Project", self)
        self.create_project_action = QtWidgets.QAction("Create Project", self)
        self.delete_project_action = QtWidgets.QAction("Delete Project", self)
        
        # edit action
        self.add_ch_action = QtWidgets.QAction("Add Character asset Folder", self)
        self.add_pr_action = QtWidgets.QAction("Add Prop asset folder", self)
        self.add_bg_action = QtWidgets.QAction("Add Background asset folder", self)
        self.add_fx_asset_action = QtWidgets.QAction("Add FX asset folder", self)
        self.add_fx_shot_action = QtWidgets.QAction("Add FX shot folder", self)
        self.add_shot_action = QtWidgets.QAction("Add Shot folder", self)
        self.add_global_scene_action = QtWidgets.QAction("Add Scene folder", self)
        self.add_material_folders_action = QtWidgets.QAction("Add Material folder", self)
        self.remove_element_action = QtWidgets.QAction("Remove", self)
        self.rename_element_action = QtWidgets.QAction("Rename", self)
        self.move_element_action = QtWidgets.QAction("Move Here", self)

        # File action
        self.open_maya_file_action = QtWidgets.QAction("Open File", self)
        self.open_in_explorer_action = QtWidgets.QAction("Open in explorer", self)
        
        # tree actions
        self.expand_selection_action = QtWidgets.QAction("Expand Selection", self)
        self.expand_all_action = QtWidgets.QAction("Expand All", self)
        self.collapse_selection_action = QtWidgets.QAction("Collapse Selection", self)
        self.collapse_all_action = QtWidgets.QAction("Collapse All", self)
        
        # Naming actions
        self.check_update_publish_action = QtWidgets.QAction("Check Update Publish", self)
        self.check_ch_file_naming_action = QtWidgets.QAction("Check CH Naming", self)
        self.check_pr_file_naming_action = QtWidgets.QAction("Check PR Naming", self)
        self.check_bg_file_naming_action = QtWidgets.QAction("Check BG Naming", self)
        self.check_shot_file_naming_action = QtWidgets.QAction("Check SHOT Naming", self)
        self.check_fx_file_naming_action = QtWidgets.QAction("Check FX asset Naming", self)
        self.check_fx_shot_file_naming_action = QtWidgets.QAction("Check FX shot Naming", self)
        self.check_scene_naming_action = QtWidgets.QAction("Check Set Dressing Naming", self)
        self.check_material_naming_action = QtWidgets.QAction("Check Material Naming", self)
        
    # create main UI widgets
    def create_widgets  (self) :
        
        # Create Menu Bar
        self.menu_bar = QtWidgets.QMenuBar()

        # Create file menu and add load_path, project_name and project_tree actions
        file_menu = self.menu_bar.addMenu("File")


        # Create Edit menu and add add_asset, add_fx, add_sequence, add_shot, rename and remove actions
        edit_menu = self.menu_bar.addMenu("Edit")
        edit_menu.addAction(self.remove_element_action)

        # Create Project menu and add project actions
        project_menu = self.menu_bar.addMenu("Project")
        project_menu.addAction(self.backup_project_action)
        project_menu.addSeparator()
        project_menu.addAction(self.project_tree_action)
        project_menu.addSeparator()
        project_menu.addAction(self.create_project_action)
        project_menu.addAction(self.delete_project_action)

        # Create Display Menu, add expand_selection, expand_to_depth, expand_all, collapse_selection, collapse_to_depth, collapse_all actions
        display_menu = self.menu_bar.addMenu("Display")
        display_menu.addAction(self.expand_selection_action)
        display_menu.addAction(self.expand_all_action)
        display_menu.addAction(self.collapse_selection_action)
        display_menu.addAction(self.collapse_all_action)
        
        naming_menu = self.menu_bar.addMenu("Safe Check")

        os_naming_check_menu = QtWidgets.QMenu()
        os_naming_check_menu.setTitle("OS file check")
        os_naming_check_menu.addAction(self.check_ch_file_naming_action)
        os_naming_check_menu.addAction(self.check_pr_file_naming_action)
        os_naming_check_menu.addAction(self.check_bg_file_naming_action)
        os_naming_check_menu.addAction(self.check_fx_file_naming_action)
        os_naming_check_menu.addSeparator()
        os_naming_check_menu.addAction(self.check_material_naming_action)
        os_naming_check_menu.addSeparator()
        os_naming_check_menu.addAction(self.check_scene_naming_action)
        os_naming_check_menu.addAction(self.check_shot_file_naming_action)
        os_naming_check_menu.addAction(self.check_fx_shot_file_naming_action)

        naming_menu.addMenu(os_naming_check_menu)
        naming_menu.addAction(self.check_update_publish_action)
        
        # Create help menu and add about action
        help_menu = self.menu_bar.addMenu("Help")
        help_menu.addAction(self.about_action)
                
        # add QTreeView add setup
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(self.root_path)
        self.model.setNameFilterDisables(False)
        self.tree_view = QtWidgets.QTreeView()
        self.tree_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(self.root_path))
        self.tree_view.hideColumn(1)
        self.tree_view.setColumnWidth(0,250)
        self.tree_view.setExpandsOnDoubleClick(False)
        
        # add text and combo box for extension filter
        self.file_ext_text = QtWidgets.QLabel("Type of File")
        self.file_ext_combobox = QtWidgets.QComboBox()
        self.file_ext_combobox.addItems(fm_lib.files_extensions_dict.keys())
       
        # add text field used as an output terminal for editing
        self.out_text_terminal = QtWidgets.QTextEdit()
        self.out_text_terminal.setText(self.output_message)
        self.out_text_terminal.setLineWrapColumnOrWidth(1)
        self.out_text_terminal.setReadOnly(True)
        
        # add button to clear and hide terminal
        self.termnal_clear_btn = QtWidgets.QPushButton("Clear")
        self.termnal_close_btn = QtWidgets.QPushButton("Close")

        # project comboBox 
        self.project_text = QtWidgets.QLabel("Current Project")
        self.project_comboBox = QtWidgets.QComboBox()

        # progress bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMinimum(0)
        
    # display widgets in layout
    def create_layout (self) :
        
        # file extension filter layout
        file_ext_layout = QtWidgets.QHBoxLayout()
        file_ext_layout.addWidget (self.project_text)
        file_ext_layout.addWidget(self.project_comboBox)
        file_ext_layout.addStretch()
        file_ext_layout.addWidget (self.file_ext_text)
        file_ext_layout.addWidget(self.file_ext_combobox)
        
        # tree viexw layout
        tree_layout = QtWidgets.QVBoxLayout()
        tree_layout.addWidget(self.tree_view)
        tree_layout.addWidget (self.progress_bar)
        tree_layout.addLayout(file_ext_layout)
        
        # output buttons layout
        output_button_layout = QtWidgets.QHBoxLayout()
        output_button_layout.addStretch()
        output_button_layout.addWidget(self.termnal_clear_btn)
        output_button_layout.addWidget(self.termnal_close_btn)
        
        # output layout
        output_layout = QtWidgets.QVBoxLayout()
        output_layout.addWidget(self.out_text_terminal)
        output_layout.addLayout(output_button_layout)
        
        # main layout
        main_layout =  QtWidgets.QHBoxLayout(self)
        main_layout.setMenuBar(self.menu_bar)
        main_layout.addLayout(tree_layout)
        main_layout.addLayout(output_layout)
        main_layout.setContentsMargins(2, 2, 2, 5)
        
    # connect actions to corresponding triggered
    def create_connections (self) :
        
        # about action
        self.about_action.triggered.connect(self.about)
        
        # file actions
        self.open_maya_file_action.triggered.connect(self.open_maya_file)
        self.open_in_explorer_action.triggered.connect(self.open_in_explorer)
        
        # project actions
        self.project_tree_action.triggered.connect(self.trigger_create_project_tree)
        self.backup_project_action.triggered.connect(self.backup_project)
        self.create_project_action.triggered.connect(self.create_project)
        self.delete_project_action.triggered.connect(self.delete_project)
        
        # edit actions
        self.add_ch_action.triggered.connect(lambda _ : self.trigger_add_folder('CH'))
        self.add_pr_action.triggered.connect(lambda _ : self.trigger_add_folder('PR'))
        self.add_bg_action.triggered.connect(lambda _ : self.trigger_add_folder('BG'))
        self.add_shot_action.triggered.connect(lambda _ : self.trigger_add_folder('shot'))
        self.add_fx_asset_action.triggered.connect(lambda _ : self.trigger_add_folder('FX asset'))
        self.add_fx_shot_action.triggered.connect(lambda _ : self.trigger_add_folder('FX shot'))
        self.add_global_scene_action.triggered.connect(lambda _ : self.trigger_add_folder('global scene'))
        self.add_material_folders_action.triggered.connect(lambda _ : self.trigger_add_folder('material'))
        self.remove_element_action.triggered.connect(self.trigger_delete_element)
        
        # Tree actions
        self.expand_selection_action.triggered.connect(self.expand_selection)
        self.expand_all_action.triggered.connect(self.tree_view.expandAll)
        self.collapse_selection_action.triggered.connect(self.collapse_selection)
        self.collapse_all_action.triggered.connect(self.tree_view.collapseAll)
        
        # mouse click action
        self.tree_view.doubleClicked.connect(self.on_double_clicked)
        self.file_ext_combobox.currentIndexChanged.connect(self.set_file_name_filters)
        self.project_comboBox.currentIndexChanged.connect(self.change_project)
        
        #Naming actions
        self.check_ch_file_naming_action.triggered.connect(lambda _ : self.trigger_check_naming(fm_lib.project_folder_dict["prod_asset_ch_folder"]["path"], fm_lib.ch_folder_path))
        self.check_pr_file_naming_action.triggered.connect(lambda _ : self.trigger_check_naming(fm_lib.project_folder_dict["prod_asset_pr_folder"]["path"], fm_lib.pr_folder_path))
        self.check_bg_file_naming_action.triggered.connect(lambda _ : self.trigger_check_naming(fm_lib.project_folder_dict["prod_asset_bg_folder"]["path"], fm_lib.bg_folder_path))
        self.check_shot_file_naming_action.triggered.connect(lambda _ : self.trigger_check_naming(fm_lib.project_folder_dict["prod_sequences_folder"]["path"], fm_lib.shot_folder_path))
        self.check_fx_file_naming_action.triggered.connect(lambda _ : self.trigger_check_naming(fm_lib.project_folder_dict["prod_asset_fx_folder"]["path"], fm_lib.fx_asset_folder_path))
        self.check_scene_naming_action.triggered.connect(lambda _ : self.trigger_check_naming(fm_lib.project_folder_dict["prod_sequences_globScene_folder"]["path"], fm_lib.global_scene_path))
        self.check_material_naming_action.triggered.connect(lambda _ : self.trigger_check_naming(fm_lib.project_folder_dict["prod_ressources_folder"]["path"], fm_lib.material_path))
        self.termnal_clear_btn.clicked.connect(self.clear_text_output)

        self.check_update_publish_action.triggered.connect(self.check_publish_update)
        
    # Print current item selected when double clicked
    def on_double_clicked (self, index) : 
        self.tree_view.edit(index)
        
    # Return current selected item absolute path If one selected, return one single path, otherwise, return a list
    def get_current_selected_path (self):
        
        index_list = self.tree_view.selectedIndexes()
        
        if len(index_list) == 3 :
            index_path = self.model.filePath(index_list[0])
            return index_path

        elif len(index_list) > 3 :
            path_list = []
            
            for index in range (0,len(index_list),3) :
                index_path = self.model.filePath(index_list[index])
                path_list.append(index_path) 
            return path_list
        
        else :
            return
            
    # Return current selected items index as a list
    def get_current_selected_index (self):
        
        index_list = self.tree_view.selectedIndexes()
        
        if len(index_list) == 3 :
            return [index_list[0]]

        elif len(index_list) > 3 :
            path_list = []
            
            for index in range (0,len(index_list),3) :
                path_list.append(index_list[index])
                
            return path_list
    
    # Display context menu at current mous point 
    def show_context_menu (self, point):
        
        # set context menu and get selected path
        context_menu = QtWidgets.QMenu()
        current_selected_path = self.get_current_selected_path()
        
        # check if path exists
        if not current_selected_path :
            return
        # assert path is a list
        if not isinstance(current_selected_path, list):
            current_selected_path = [current_selected_path]
    
        remove_check = True
        
        # Function of where the user clicked, display different actions
        for items in current_selected_path:

            if items == None :
                break
            if items.endswith(fm_lib.project_folder_dict['prod_sequences_folder']['path']):
                context_menu.addAction(self.add_shot_action)
        
            if items.endswith(fm_lib.project_folder_dict['prod_asset_ch_folder']['path']):
                context_menu.addAction(self.add_ch_action)

            elif items.endswith(fm_lib.project_folder_dict['prod_asset_pr_folder']['path']):
                context_menu.addAction(self.add_pr_action)

            elif items.endswith(fm_lib.project_folder_dict['prod_asset_bg_folder']['path']):
                context_menu.addAction(self.add_bg_action)
            
            elif fm_lib.project_folder_dict['prod_asset_fx_folder']['path'] in items and not items.endswith(fm_lib.project_folder_dict['prod_asset_fx_folder']['path']):
                context_menu.addAction(self.add_fx_asset_action)
                
            elif items.endswith(fm_lib.project_folder_dict['prod_sequences_globScene_folder']['path']) :
                context_menu.addAction(self.add_global_scene_action)

            elif items.endswith (fm_lib.project_folder_dict['prod_ressources_folder']['path']) :
                context_menu.addAction(self.add_material_folders_action)

            elif items.endswith (fm_lib.shot_folder_path['sequence_fx']['path']) and  fm_lib.project_folder_dict['prod_sequences_folder']['path'] in items:
                context_menu.addAction(self.add_fx_shot_action)
                
            for defaut_path in fm_lib.project_folder_dict.keys() :
                items.replace ('\\', '/')
                if items.endswith(fm_lib.project_folder_dict[defaut_path]['path']) :
                    remove_check = False
                    break

            if items.endswith(".ma") or items.endswith(".mb") :
                context_menu.addAction(self.open_maya_file_action)
                    
  
        context_menu.addSeparator()
        
        # if selected folder isn't a folder created by script, display the remove action
        if remove_check:
            context_menu.addAction(self.remove_element_action)
        
        # dysplay expand and collapse actions
        context_menu.addSeparator()
        context_menu.addAction(self.open_in_explorer_action)
        context_menu.addAction(self.expand_selection_action)
        context_menu.addAction(self.collapse_selection_action)
        
        context_menu.exec_(self.mapToGlobal(point))
         
    # Display QtWidget base about UI 
    def about (self) :
        QtWidgets.QMessageBox.about(self, "Help", "Add About here")
        
    # Ask the user a path, set the QTreeView root path and ask the user if want's to change os.chdir and maya workspace. If yes, do it. Set the ProjectTree.current_wrkdir variable
    def create_project(self):

        # Ask new path
        path_ = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Path", self.root_path)
        
        if not path_ :
            return
            
        project_path, project_name = fm_man.create_project(path_)

        self.update_tree_view (project_path, project_name)
        self.load_project()
        
    def delete_project(self) :

        print ("TODO : delete_project")

    # load existing project if its exists in computer
    def load_project (self) :

        data = fm_man.get_projects_datas ()

        self.project_comboBox.clear()

        if not data : 
            return

        for values in data.keys() :
            if values == 'current_project':
                continue
            if os.path.exists(data[values]['project_path']) :
                self.project_comboBox.addItem(values)

        for item in range(self.project_comboBox.count()):
            if self.project_comboBox.itemText(item) == data ['current_project'] :
                self.project_comboBox.setCurrentIndex(item)

    def update_tree_view(self, path_, windows_name):

        # Confirm Dialog
        change_project_directory = ConfirmationDialog(custom_message = "Do you want to change current project directory ?")
        result = change_project_directory.exec_()
        
        # if clicked yes, change wrkdir and maya workspace
        if result == QtWidgets.QDialog.Accepted :
            mel.eval(r'setProject "{}";'.format(path_))
            os.chdir (path_)
        
        # update QTreeView 
        self.root_path = path_
        self.project_name = windows_name
        self.tree_view.setRootIndex(self.model.index(self.root_path))
        self.setWindowTitle("Project Manager - {0}".format(self.project_name))

    # change current project working on
    def change_project(self) :

        self.clear_text_output()

        new_project =  self.project_comboBox.currentText()

        datas = fm_man.get_project_parameters(new_project)
        print (datas)

        if os.path.exists(datas['project_path']):
            self.update_tree_view(datas['project_path'], datas['project_name'])
            self.add_text_to_output('\nCurrent working project : {}\n{}'.format(datas['project_name'], datas['project_path']), False)
            fm_man.set_current_project (datas['project_name'])
        else : 
            self.add_text_to_output('\nProject {} not found. ({})'.format(datas['project_name'], datas['project_path']), False)

    # call ProjectTree.create_project_tree()
    def trigger_create_project_tree (self) :

        tree_result = fm_man.create_project_tree(self.root_path)
        self.add_text_to_output('\n' + tree_result, False)
        
    # get current selected path and call corresponding function
    def trigger_add_folder(self, folder_type) :
        
        index_path =  self.get_current_selected_path()

        if folder_type == 'CH' or folder_type == 'PR' or folder_type == 'BG':
            fm_man.add_asset_folder(index_path, folder_type)
        elif folder_type == 'shot' :
            fm_man.add_shot_folder(index_path)
        elif folder_type == 'FX shot' or folder_type == 'global scene' or folder_type == 'material':
            fm_man.add_prod_folder(index_path, folder_type)
        elif folder_type == "FX asset" :
            fm_man.add_fx_folder(index_path)

        
    # get current selected path and call corresponding fm_man function :  delete_folder or delete_file
    def trigger_delete_element (self) :

        list_index_path =  self.get_current_selected_path()

        if not isinstance(list_index_path, list) :
            list_index_path = [list_index_path]

        for index_path in list_index_path :
            if os.path.isdir(index_path):
                fm_man.delete_folder(index_path)
            else :
                fm_man.delete_file(index_path)

    # get current selected path and call check_windows_file_naming()         
    def trigger_check_naming(self, path_, asset_dict) :
               
        text_to_delete = len(path_)
        text_to_add = fm_man.check_windows_file_naming("{}/{}".format(self.root_path, path_), asset_dict)
        

        # if function find unchecked files, print them in output
        if text_to_add :
            self.add_text_to_output('\n========================================\nUNCHECKED FILES FOUNDED IN {}\n========================================'.format(path_), True)
            path_list = []
            printed_file = []

            for root, file_name, result, name_split, naming_rules in text_to_add :
                text_to_print = root[text_to_delete:]

                complete_file_path = os.path.join(root, file_name)
                if complete_file_path in printed_file :
                    continue

                printed_file.append (complete_file_path)

                if not root in path_list :
                    self.add_text_to_output('\n\n' + r'__ {}:'.format(text_to_print) + '\n', False)
                    path_list.append(root)
                else :
                    self.add_text_to_output('\n', False)
                self.add_text_to_output("\n" + r' '*10, False)
                self.add_text_to_output(file_name, False)

                if result == 'Invalid File Path':
                    self.add_text_to_output('   -> invalid path', False)
                    continue

                elif result == "Not founded file path" :
                    self.add_text_to_output('   -> Not founded file path', False)
                    continue

                elif result == "Only one underscore, need two" or result == "Element Missing" or not result:
                    self.add_text_to_output('   -> {}'.format(result), False)
                    self.add_text_to_output('   (expected {})'.format(naming_rules), False)
                    continue
                
                    
                self.add_text_to_output('   -> ', False)
                for naming_elem in range(len(result)) :
                    
                    if result[naming_elem] :
                        self.add_text_to_output(name_split[naming_elem], False)
                    else :
                        self.add_text_to_output(name_split[naming_elem], True)
                    
                    if naming_elem == len(result) -1 :
                        break

                    if naming_elem == len(result) -2 or naming_elem == len(result) -3 :
                        self.add_text_to_output(r'.', False)
                    else :
                        self.add_text_to_output(r'__', False)

                self.add_text_to_output('   -> {}'.format(naming_rules), False)
            
        else :
            self.add_text_to_output('\nFiles check completed succesfuly', False)

    # expand current selected item 
    def expand_selection (self) :
        item_list = self.get_current_selected_index()
        for item in item_list:
            self.tree_view.expand(item)

    # collapse selected item       
    def collapse_selection (self):
        item_list = self.get_current_selected_index()
        for item in item_list:
            self.tree_view.collapse(item)
        
    # add text to output window
    def add_text_to_output(self, text_to_add, italic) :
    
        if italic :
            self.out_text_terminal.setFontItalic(True)
        self.output_message += text_to_add
        self.out_text_terminal.insertPlainText(text_to_add)
        self.out_text_terminal.setFontItalic(False)

    # clear output window
    def clear_text_output (self):
        
        self.output_message = ''
        self.out_text_terminal.clear()

    # set tree view model name filter  
    def set_file_name_filters(self) :
        
        filter_index = self.file_ext_combobox.currentText()
      
        new_filter = fm_lib.files_extensions_dict[filter_index].split('|')
        self.model.setNameFilters(new_filter)

    def backup_project(self) :

        path_ = QtWidgets.QFileDialog.getExistingDirectory(self, "Backup Path", self.root_path)
        start = time.time()

        if not path_ :
            return
            
        project_dict = fm_lib.project_folder_dict
        defaut_path_keys = project_dict.keys()
        
        self.add_text_to_output("Backup...\n", False)
        self.progress_bar.setValue(0)
        time.sleep(1)
        self.add_text_to_output("Getting all files in project...", False)
        
        element_to_copy = []
        time.sleep(.1)
        self.progress_bar.setMaximum(len (defaut_path_keys))
        value = 0
        for folder_path in defaut_path_keys :
            time.sleep(.25)
            element_to_copy += fm_man.get_all_files_below (r'{}{}'.format(self.root_path, project_dict[folder_path]['path']))
            self.progress_bar.setValue(value+1)
            value += 1
        value = 0
        file_number = len(element_to_copy)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(file_number)

        updated_file_count = 0
        delete_file_count = 0
        delete_folder_count = 0

        time.sleep(1)
        
        for file_ in element_to_copy :
            time.sleep(.1)
            self.clear_text_output()
            self.add_text_to_output("Backup...\n", False)
            self.add_text_to_output("Copy file to {} : {}/{}".format(path_, value, file_number), False)
            self.progress_bar.setValue(value)
            value += 1
            time.sleep(.1)
            updated_file = fm_man.backup_files(file_, file_.replace(self.root_path, path_))
            if updated_file :
                updated_file_count += 1

        time.sleep(.25)

        for root, dirs, files in os.walk(path_, topdown = True) :

            for dest_file in files :

                self.clear_text_output()
                self.add_text_to_output("Backup...\n", False)
                self.add_text_to_output("Clean Backup Folder ({})".format(dest_file), False)
                time.sleep(.25)

                file_path = os.path.join(root, dest_file)
                if not file_path in element_to_copy :
                    fm_man.delete_file(file_path)
                    delete_file_count += 1

            for dest_folder in dirs :

                self.clear_text_output()
                self.add_text_to_output("Backup...\n", False)
                self.add_text_to_output("Clean Backup Folder ({})".format(dest_folder), False)
                time.sleep(.25)

                dir_path = os.path.join(root, dest_folder)
                if not dir_path in element_to_copy :
                    if os.path.exists(dir_path):

                        # list sub files and sub directories
                        sub_files = os.listdir(dir_path)
                        
                        # if sub_files founded, display a warning dialog 
                        if sub_files :
                            shutil.rmtree(dir_path)
                        
                        else :
                            os.rmdir(dir_path)
                    delete_folder_count +=1

        time.sleep(.25)
        self.clear_text_output()
        self.add_text_to_output('\nBackup complete sucessfully', False)

        if updated_file_count == 1 :
            self.add_text_to_output('\n     {} file udpated'.format(updated_file_count), False)
        elif updated_file_count > 1 :
            self.add_text_to_output('\n     {} files udpated'.format(updated_file_count), False)

        if delete_file_count == 1 :
            self.add_text_to_output('\n     {} file deleted'.format(delete_file_count), False)
        elif delete_file_count > 1 :
            self.add_text_to_output('\n     {} files deleted'.format(delete_file_count), False)

        if delete_folder_count == 1 :
            self.add_text_to_output('\n     {} file deleted'.format(delete_folder_count), False)
        elif delete_folder_count > 1 :
            self.add_text_to_output('\n     {} files deleted'.format(delete_folder_count), False)

        end = time.time()

        print (time.localtime(end-start))

    def open_maya_file (self) :

        current_selected_path = self.get_current_selected_path()

        if isinstance(current_selected_path, str) :
            cmds.file(current_selected_path, open = True, force = True)

    def open_in_explorer (self) :

        filebrowser_path = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

        current_selected_path = self.get_current_selected_path()
        if not isinstance(current_selected_path, str) :
            return
        
        # explorer would choke on forward slashes
        current_selected_path = os.path.normpath(current_selected_path)

        if os.path.isdir(current_selected_path):
            subprocess.run([filebrowser_path, current_selected_path])
        elif os.path.isfile(current_selected_path):
            subprocess.run([filebrowser_path, '/select,', current_selected_path])

    def check_publish_update(self) :

        result_list = fm_man.check_publish_update(self.root_path)

        text_to_delete = len(self.root_path)

        if result_list :
            self.add_text_to_output('\n========================================\nPublish to update :\n========================================', False)

            for file_path, result in result_list :
                text_to_print = file_path[text_to_delete:]

                self.add_text_to_output('\n{}: {}\n'.format(text_to_print, result), False)

        else :
            self.add_text_to_output('\n========================================\nPublish up to date\n========================================', False)


