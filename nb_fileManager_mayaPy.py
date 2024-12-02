import maya.standalone
from maya import cmds



def do_check_naming (file_) :
    print (file_)
    maya.standalone.initialize()

    cmds.file(file_, open=True)

    shadding_engine_list = cmds.objectType(typ = 'shadingEngine')
    aiStandardSurface_list = cmds.objectType(typ = 'aiStandardSurface')
    curve_list = cmds.listRelatives(cmds.objectType(typ = 'nurbsCurve'), p=True)
    cluster_list = cmds.listRelatives(cmds.objectType(typ = 'clusterHandle'), p=True)
    joint_list = cmds.objectType(typ = 'joint')
    locator_list = cmds.listRelatives(cmds.objectType(typ = 'locator'), p=True)
    mesh_list = cmds.listRelatives(cmds.objectType(typ = 'mesh'), p=True)
    transform_list = cmds.listRelatives(cmds.objectType(typ = 'transform'), p=True)

    for transform in transform_list :
        if transform in curve_list or transform in cluster_list or transform in locator_list or transform in mesh_list :
            transform_list.pop(transform_list.index(transform))
    
    for shd_grp in shadding_engine_list :
        check_naming(shd_grp)

    cmds.file(save=True, type = "mayaAscii")

    print ('Done')
    maya.standalone.uninitialize()

def check_naming (name, key) :
    pass
