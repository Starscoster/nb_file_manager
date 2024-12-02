"""
This cover all functions that will be used in maya to check topology and files
"""
# Import modules
from maya import cmds
import maya.OpenMaya as om
import os
import maya.standalone

from nb_file_manager import nb_fileManager_lib as fm_lib

# global variables  
IDENTITY = [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]
TRANSFORMATIONS = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0]

def write_output (root, file_name, message) :
    """
    Write a text files as output to format errors and save them
    """
    retake_file = "{}__RETAKES__.txt".format(os.path.join(root, file_name))

    # If file path not exists, creat one new file
    if not os.path.exists(retake_file) :
        with open(retake_file, "a") as file:
            file.write(file_name + " RETAKES: \n")

    with open(retake_file, "a") as file :
        file.write(message)

def verif_scenes(path_):
    """
    Get all maya scenes below path, check if objects naming is "AVALID" or "DEF", and run a checkup in mayapy
    """

    failed_list = []
    text_to_add = ""

    maya.standalone.initialize()
    # Main loop
    for root, dirs, file_name in os.walk(path_, topdown = True):
        if fm_lib.avalid in file_name or fm_lib.complete in file_name :         # Chcking naming
            if file_name.endswith(".ma") or file_name.endswith(".mb"):          # assert file is a maya file
                file_path = os.path.join(root, file_name)
                cmds.file(file_path, open=True, force=True)
                check_result = lunch_fonction(root, file_name)                  # run check function and store resule
                if check_result : 
                    failed_list.append(file_path)

    maya.standalone.uninitialize()
    
    # If errors are founded, add them to output text
    if failed_list :
        text_to_add = "Errors founded :"
        for file_ in failed_list:
            text_to_add += "{}\n".format(file_)
    
    return text_to_add

def lunch_fonction(root, file_name):
    """
    In maya file, get all meshs and with maya MSelectionList function, check each function below
    """
    # Get all meshs
    mesh_list = cmds.ls(type="mesh", objectsOnly=True)
    if not mesh_list :
        return
    nodes = cmds.listRelatives(mesh_list, parent = True)

    # Iterate over nodes
    for node in nodes:

        # Setup MSelectionList
        SLMesh = om.MSelectionList()    
        shapes = cmds.listRelatives(node, shapes=True, typ="mesh")
        if shapes:
            SLMesh.add(node)

        # Run each checking function and store result
        is_duplicate_name = duplicatedNames(node)
        is_namespaces = namespaces(node)
        is_shape_name = shapeNames(node)
        is_triangle = triangles("", SLMesh)
        is_ngone = ngons("", SLMesh)
        is_hard_edge = hardEdges("", SLMesh)
        is_lamina = lamina("", SLMesh)
        is_zero_area_faces = zeroAreaFaces("", SLMesh)
        is_zero_lenght_edges = zeroLengthEdges("", SLMesh)
        is_self_penetrating_uvs = selfPenetratingUVs(node)
        is_none_manifold_edges = noneManifoldEdges("", SLMesh)
        is_poles = poles("", SLMesh)
        is_starlike = starlike("", SLMesh)
        is_missing_uvs = missingUVs("", SLMesh)
        is_uv_range =uvRange("", SLMesh)
        is_on_border = onBorder("", SLMesh)
        is_cross_border = crossBorder("", SLMesh)
        is_unfrozen = unfrozenTransforms(node)
        is_layers = layers(node)
        is_shaders = shaders(node)
        is_history = history(node)
        is_uncentered_pivot = uncenteredPivots(node)
        is_empty_goup = emptyGroups (node)
        is_parent_geometry = parentGeometry(node)

        # If the result isn't good, add corresponding text to output
        if is_duplicate_name or is_namespaces or is_shape_name or is_triangle or is_ngone or is_hard_edge or is_lamina or is_zero_area_faces or is_zero_lenght_edges or is_self_penetrating_uvs or is_none_manifold_edges or is_poles or is_starlike or is_missing_uvs or is_uv_range or is_on_border or is_cross_border or is_unfrozen or is_layers or is_shaders or is_history or is_uncentered_pivot or is_empty_goup or is_parent_geometry :
            write_output (root, file_name, "\n{} :".format(node))

        if is_duplicate_name : 
            write_output (root, file_name, "\t|-> Name is duplicated\n")
        if is_unfrozen :
            write_output (root, file_name, "\t|-> isn't frozen\n")
        if is_history :
            write_output (root, file_name, "\t|-> has history\n")
        if is_uncentered_pivot :
            write_output (root, file_name, "\t|-> pivot not at center\n")
        if is_empty_goup :
            write_output (root, file_name, "\t|-> is an empty group\n")
        if is_parent_geometry :
            write_output (root, file_name, "\t|-> has parent under his shape\n")
        if is_layers :
            write_output (root, file_name, "\t|-> is in layer\n")
        if is_shaders :
            write_output (root, file_name, "\t|-> has no shading group\n")
        if is_namespaces : 
            write_output (root, file_name, "\t|-> Has namespaces\n")
        if is_shape_name :
            write_output (root, file_name, "\t|-> Shape name isn't correct\n")
        if is_self_penetrating_uvs :
            write_output (root, file_name, "\t|-> Uvs are self penetrating\n")
        if is_triangle :
            write_output (root, file_name, "\t|-> {} are triangles\n".format(is_triangle))
        if is_ngone :
            write_output (root, file_name, "\t|-> {} are ngons\n".format(is_ngone))
        if is_hard_edge :
            write_output (root, file_name, "\t|-> {} are hard edges\n".format(is_hard_edge))
        if is_lamina :
            write_output (root, file_name, "\t|-> {} are lamina faces\n".format(is_lamina))
        if is_zero_area_faces :
            write_output (root, file_name, "\t|-> {} are zero area faces\n".format(is_zero_area_faces))
        if is_zero_lenght_edges :
            write_output (root, file_name, "\t|-> {} are zero lenght edges\n".format(is_zero_lenght_edges))
        if is_none_manifold_edges :
            write_output (root, file_name, "\t|-> {} are non manifold edges\n".format(is_none_manifold_edges))
        if is_poles :
            write_output (root, file_name, "\t|-> {} are poles\n".format(is_poles))
        if is_starlike :
            write_output (root, file_name, "\t|-> {} are starlike\n".format(is_starlike))
        if is_missing_uvs :
            write_output (root, file_name, "\t|-> {} has no uvs\n".format(is_missing_uvs))
        if is_uv_range :
            write_output (root, file_name, "\t|-> {} out of uvs range\n".format(is_uv_range))
        if is_on_border :
            write_output (root, file_name, "\t|-> {} has uvs on border\n".format(is_on_border))
        if is_cross_border :
            write_output (root, file_name, "\t|-> {} has uvs cross bordering\n".format(is_on_border))

def duplicatedNames(node):
    
    if '|' in node:
        return False
    return True

def namespaces(node):

    if ':' in node:
        return False
    return True

def shapeNames(node):

    new = node.split('|')
    shape = cmds.listRelatives(node, shapes=True)
    if shape:
        shapename = new[-1] + "Shape"
        if shape[0] != shapename:
            return False
    return True

def triangles(_, SLMesh):
    triangles = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            numOfEdges = faceIt.getEdges()
            if len(numOfEdges) == 3:
                faceIndex = faceIt.index()
                componentName = f"{str(objectName)}.f[{str(faceIndex)}]"
                triangles.append(componentName)
            faceIt.next()
        selIt.next()
    return triangles

def ngons(_, SLMesh):
    ngons = []
    if SLMesh.isEmpty():
        return ngons
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            numOfEdges = faceIt.getEdges()
            if len(numOfEdges) > 4:
                componentName = f"{str(objectName)}.f[{str(faceIt.index())}]"
                ngons.append(componentName)
            faceIt.next()
        selIt.next()
    return ngons

def hardEdges(_, SLMesh):
    hardEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.isSmooth is False and edgeIt.onBoundary() is False:
                componentName = f"{str(objectName)}.e[{str(edgeIt.index())}]"
                hardEdges.append(componentName)
            edgeIt.next()
        selIt.next()
    return hardEdges

def lamina(_, SLMesh):
    selIt = om.MItSelectionList(SLMesh)
    lamina = []
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            laminaFaces = faceIt.isLamina()
            if laminaFaces is True:
                componentName = f"{str(objectName)}.f[{str(faceIt.index())}]"
                lamina.append(componentName)
            faceIt.next()
        selIt.next()
    return lamina

def zeroAreaFaces(_, SLMesh):
    zeroAreaFaces = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            faceArea = faceIt.getArea()
            if faceArea <= 0.00000001:
                componentName = f"{str(objectName)}.f[{str(faceIt.index())}]"
                zeroAreaFaces.append(componentName)
            faceIt.next()
        selIt.next()
    return zeroAreaFaces

def zeroLengthEdges(_, SLMesh):
    zeroLengthEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.length() <= 0.00000001:
                componentName = f"{str(objectName)}.f[{str(edgeIt.index())}]"
                zeroLengthEdges.append(componentName)
            edgeIt.next()
        selIt.next()
    return zeroLengthEdges

def selfPenetratingUVs(node):
    selfPenetratingUVs = []
    
    shape = cmds.listRelatives(node, shapes=True, fullPath=True)
    convertToFaces = cmds.ls(
        cmds.polyListComponentConversion(shape, tf=True), fl=True)
    overlapping = (cmds.polyUVOverlap(convertToFaces, oc=True))
    if overlapping:
        for node in overlapping:
            selfPenetratingUVs.append(node)

    return selfPenetratingUVs

def noneManifoldEdges(_, SLMesh):
    noneManifoldEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.numConnectedFaces() > 2:
                componentName = f"{str(objectName)}.e[{str(edgeIt.index())}]"
                noneManifoldEdges.append(componentName)
            edgeIt.next()
        selIt.next()
    return noneManifoldEdges

def openEdges(_, SLMesh):
    openEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.numConnectedFaces() < 2:
                componentName = f"{str(objectName)}.e[{str(edgeIt.index())}]"
                openEdges.append(componentName)
            edgeIt.next()
        selIt.next()
    return openEdges

def poles(_, SLMesh):
    poles = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        vertexIt = om.MItMeshVertex(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not vertexIt.isDone():
            if vertexIt.numConnectedEdges() > 5:
                componentName = f"{str(objectName)}.vtx[{str(vertexIt.index())}]"
                poles.append(componentName)
            vertexIt.next()
        selIt.next()
    return poles

def starlike(_, SLMesh):
    starlike = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        polyIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not polyIt.isDone():
            if polyIt.isStarlike() is False:
                componentName = f"{str(objectName)}.f[{str(polyIt.index())}]"
                starlike.append(componentName)
            polyIt.next()
        selIt.next()
    return starlike

def missingUVs(_, SLMesh):
    if SLMesh.isEmpty():
        return []
    missingUVs = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            if faceIt.hasUVs() is False:
                componentName = f"{str(objectName)}.f[{str(faceIt.index())}]"
                missingUVs.append(componentName)
            faceIt.next()
        selIt.next()
    return missingUVs

def uvRange(_, SLMesh):
    if SLMesh.isEmpty():
        return []
    uvRange = []
    selIt = om.MItSelectionList(SLMesh)
    mesh = om.MFnMesh(selIt.getDagPath())
    objectName = selIt.getDagPath().getPath()
    Us, Vs = mesh.getUVs()
    for i in range(len(Us)):
        if Us[i] < 0 or Us[i] > 10 or Vs[i] < 0:
            componentName = f"{str(objectName)}.map[{str(i)}]"
            uvRange.append(componentName)
    return uvRange

def onBorder(_, SLMesh):
    if SLMesh.isEmpty():
        return []
    onBorder = []
    selIt = om.MItSelectionList(SLMesh)
    mesh = om.MFnMesh(selIt.getDagPath())
    objectName = selIt.getDagPath().getPath()
    Us, Vs = mesh.getUVs()
    for i in range(len(Us)):
        if abs(int(Us[i]) - Us[i]) < 0.00001 or abs(int(Vs[i]) - Vs[i]) < 0.00001:
            componentName = f"{str(objectName)}.map[{str(i)}]"
            onBorder.append(componentName)
    return onBorder

def crossBorder(_, SLMesh):
    crossBorder = []
    if SLMesh.isEmpty():
        return crossBorder
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            U, V = set(), set()
            try:
                UVs = faceIt.getUVs()
                Us, Vs, = UVs[0], UVs[1]
                for i in range(len(Us)):
                    uAdd = int(Us[i]) if Us[i] > 0 else int(Us[i]) - 1
                    vAdd = int(Vs[i]) if Vs[i] > 0 else int(Vs[i]) - 1
                    U.add(uAdd)
                    V.add(vAdd)
                if len(U) > 1 or len(V) > 1:
                    componentName = f"{str(objectName)}.f[{str(faceIt.index())}]"
                    crossBorder.append(componentName)
                faceIt.next()
            except:
                cmds.warning("Face " + str(faceIt.index()) + " has no UVs")
                faceIt.next()
        selIt.next()
    return crossBorder

def unfrozenTransforms(node):

    translation = cmds.xform(
        node, q=True, worldSpace=True, translation=True)
    rotation = cmds.xform(node, q=True, worldSpace=True, rotation=True)
    scale = cmds.xform(node, q=True, worldSpace=True, scale=True)
    if translation != [0.0, 0.0, 0.0] or rotation != [0.0, 0.0, 0.0] or scale != [1.0, 1.0, 1.0]:
        return False
    return True

def layers(node):
    
    layer = cmds.listConnections(node, type="displayLayer")
    if layer:
        return False
    return True

def shaders(node):
    
    shape = cmds.listRelatives(node, shapes=True, fullPath=True)
    if cmds.nodeType(shape) == 'mesh' and shape:
        shadingGrps = cmds.listConnections(shape, type='shadingEngine')
        if shadingGrps[0] != 'initialShadingGroup':
            return False
    return True

def history(node):
        
    shape = cmds.listRelatives(node, shapes=True, fullPath=True)
    if shape and cmds.nodeType(shape[0]) == 'mesh':
        historySize = len(cmds.listHistory(shape))
        if historySize > 1:
            return False
    return True

def uncenteredPivots(node):
    
    if cmds.xform(node, q=1, ws=1, rp=1) != [0, 0, 0]:
        return False
    return True

def emptyGroups(node):
    
    children = cmds.listRelatives(node, ad=True)
    if not children:
        return False
    return True

def parentGeometry(node):
    parents = cmds.listRelatives(node, p=True, fullPath=True)
    if parents:
        for parent in parents:
            children = cmds.listRelatives(parent, fullPath=True)
            for child in children:
                if cmds.nodeType(child) == 'mesh':
                    return False
    return True
