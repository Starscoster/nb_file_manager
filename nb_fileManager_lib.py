import sys
# get current python version
python_version = sys.version_info.major

# files extension dict
files_extensions_dict = {'All (.)' : '*', 'Maya ASCII (.ma)' : '*.ma', 'Maya Binary (.mb)' : '*.mb', 'FBX (.fbx)' :'*.fbx', 'Object 3D (.obj)' : '*.obj', 'PNG (.png)' : '*.png', 'JPG (.jpeg .jpg)' : '*.jpg|*.jpeg', 'EXR (.exr)' : '*.exr', 'Substance (.spp .sbs .sbar)' : '*.spp|*.sbs|*.sbar',
        'Video (.mp4 .mov .wav .avi .qt)' : '*.mp4|*.mov|*.wav|*.avi|*.qt', 'ext_nuke file (.nk)' : '*.nk', 'houdini (.hipnc .hip .bgeo .bgeo.sc)' : '*.hipnc|*.hip|*.bgeo|*.bgeo.sc'
    
}

# Project naming abreviation
project_naming = 'FW'

story = 'ST'
graphic_styling = 'GS'
proof_of_concept = 'POC'
character = 'CH'
props = 'PR'
background = 'BG'
sequence = r'^SQ\d{3}$'
shot = r'^SH\d{3}$'
effect = 'FX'
image_number = r'^\d{4}$'
work =  r'^\d{3}$'
avalid =  'AVALID'
complete =  'DEF'

modeling =  'MOD'
uv =  'UVS'
texture =  'SHD'
material = 'MAT'
blendshape =  'BS'
lookdev = 'LOOKDEV'
fur = 'FUR'
rigging = 'RIG'
global_scene = 'GLOBAL'
animation = 'ANIM'
set_dress =  'SETDRESS'
layout = 'LAYOUT'
lighting = 'LGT'
rendering = 'RDR'
compositing = 'COMP'
post_production = 'POST'
editing = 'EDIT'
sound_design = 'SOUND'
post_bank = 'BANK'
post_review = 'REV'

substance_painter = 'txtSP'
substance_designer = 'txtSD'

# file extension
ext_mayaAscii =  'ma'
ext_mayaBinari =  'mb'
ext_photoshop = 'psd'
ext_painter =  'spp'
ext_designer = ['sbs', 'sbar']
ext_image = ['png', 'exr', "tx", "tga", "jpg", "jpeg"]
ext_nuke = 'nk'
ext_houdini = ['hipnc', 'hip', 'bgeo']
ext_obj_fbx = ['fbx', 'obj', 'mtl']
ext_zbrush = ['zpr', 'ztl']
ext_houdini_export = ["vdb", "bgeo.sc"]
ext_json = "json"

# Texture maps utilities
txt_color = 'COL'
txt_metal = 'MTL'
txt_bump = 'BMP'
txt_normal = 'NRM'
txt_emissive = 'EMI'
txt_displacement = 'DIS'
txt_coat = 'COAT'
txt_weight = 'WGHT'
txt_transmission = 'TRA'
txt_sub_surface_scattering = 'SSS'
txt_sheen = 'SHE'
txt_roughness = 'RGH'
txt_alpha = 'ALPHA'
txt_opacity = "OPA"
image_type = [txt_color, txt_metal, txt_bump, txt_normal, txt_displacement, txt_coat, txt_weight, txt_transmission,
            txt_sub_surface_scattering, txt_sheen, txt_roughness, txt_alpha, txt_emissive, txt_opacity]

animation_steps = ['POSING','SPLINE']

# folder organization files
preprod_folder = r'/01_PREPROD'
pre_graphic_design_folder = r'/02_GraphicDesign'
pre_tech_doc_folder = r'/03_TechnicalDocuments'
prod_folder = r'/02_PROD'
post_prod_folder = r'/03_POSTPROD'

post_bank_naming = [project_naming, post_production, post_bank, 'name', [work, avalid, complete], 'ext']
CH_asset_prefix = [project_naming, character, 'folderName']
PR_asset_prefix = [project_naming, props, 'folderName']
BG_asset_prefix = [project_naming, background, 'folderName']
FX_asset_prefix = [project_naming, effect, 'folderName']
sequence_shot_naming = ['sequence', 'shot']

project_folder_dict = {
    'preprod_folder' : {'path' : preprod_folder,
                            'naming' : []
                            },
    'prod_folder' : {'path' : prod_folder,
                            'naming' : []
                            },
    'postprod_folder' : {'path' : r'/03_POSTPROD',
                            'naming' : []
                            },
    'review_folder' : {'path' : r'/04_REVIEW',
                            'naming' : []
                            },
    'final_folder' : {'path' : r'/05_FINAL',
                            'naming' : []
                            },
    
    'pre_scenario_folder' : {'path' : r'{}/01_Scenario'.format(preprod_folder),
                            'naming' : [[project_naming, story, 'name', [work, avalid, complete], 'ext']]
                            },
    'pre_graphic_design_folder' : {'path' : r'{}{}'.format(preprod_folder, pre_graphic_design_folder),
                            'naming' : []
                            }, 
    'pre_grades_graphic_style_folder' : {'path' : r'{}{}/01_GraphicStyling'.format(preprod_folder, pre_graphic_design_folder),
                            'naming' : [[project_naming, graphic_styling, 'name', 'name', [work, avalid, complete], 'ext']]
                            }, 
    'pre_grades_character_folder' : {'path' : r'{}{}/02_Characters'.format(preprod_folder, pre_graphic_design_folder),
                            'naming' : [[project_naming, character, 'folderName', 'name', [work, avalid, complete], 'ext']]
                            }, 
    'pre_grades_environnement_folder' : {'path' : r'{}{}/03_Environment'.format(preprod_folder, pre_graphic_design_folder),
                            'naming' : [[project_naming, background, 'folderName', 'name', [work, avalid, complete], 'ext']]
                            }, 
    'pre_grades_asset_folder' : {'path' : r'{}{}/04_Assets'.format(preprod_folder, pre_graphic_design_folder),
                            'naming' : [[project_naming, props, 'folderName', 'name', [work, avalid, complete], 'ext']]
                            }, 
    'pre_grades_fx_folder' :  {'path' : r'{}{}/05_FX'.format(preprod_folder, pre_graphic_design_folder),
                            'naming' : [[project_naming, effect, 'folderName', 'name', [work, avalid, complete], 'ext']]
                            },
    'pre_technical_doc_folder' : {'path' : r'{}/{}'.format(preprod_folder, pre_tech_doc_folder),
                            'naming' : []
                            },
    'pre_tecdoc_ressources_folder' : {'path' : r'{}/{}/00_Materials'.format(preprod_folder, pre_tech_doc_folder),
                            'naming' : [[project_naming, material, 'folderName', 'name', [work, avalid, complete], 'ext']]
                            }, 
    'pre_tecdoc_assets_folder' : {'path' : r'{}/{}/01_Assets'.format(preprod_folder, pre_tech_doc_folder),
                            'naming' : []
                            }, 
    'pre_tecdoc_sequence_folder' : {'path' : r'{}/{}/02_Sequences'.format(preprod_folder, pre_tech_doc_folder),
                            'naming' : [[project_naming, sequence, shot, [animation, set_dress, layout, lighting, rendering, compositing], 'name', [work, avalid, complete], 'ext']]
                            }, 
    'pre_tecdoc_postprod_folder' : {'path' : r'{}/{}/03_PostProduction'.format(preprod_folder, pre_tech_doc_folder),
                            'naming' : []
                            }, 
    'pre_tecdoc_assets_ch_folder' : {'path' : r'{}/{}/01_Assets/01_CH'.format(preprod_folder, pre_tech_doc_folder),
                            'naming' : [[project_naming, character, 'folderName', [modeling, texture, blendshape, lookdev, rigging, animation], 'name', [work, avalid, complete], 'ext']]
                            }, 
    'pre_tecdoc_assets_pr_folder' : {'path' : r'{}/{}/01_Assets/02_PR'.format(preprod_folder, pre_tech_doc_folder),
                            'naming' : [[project_naming, props, 'folderName', [modeling, texture, blendshape, lookdev, rigging, animation], 'name', [work, avalid, complete], 'ext']]
                            }, 
    'pre_tecdoc_assets_bg_folder' : {'path' : r'{}/{}/01_Assets/03_BG'.format(preprod_folder, pre_tech_doc_folder),
                            'naming' : [[project_naming, background, 'folderName', [modeling, texture, blendshape, lookdev, rigging, animation], 'name', [work, avalid, complete], 'ext']]
                            }, 
    'pre_tecdoc_assets_fx_folder' : {'path' : r'{}/{}/01_Assets/04_FX'.format(preprod_folder, pre_tech_doc_folder),
                            'naming' : [[project_naming, effect, 'folderName', 'name', [work, avalid, complete], 'ext']]
                            },
    'pre_tecdoc_postprod_edit_folder' : {'path' : r'{}/{}/03_PostProduction/01_Editing'.format(preprod_folder, pre_tech_doc_folder),
                            'naming' : [[project_naming, post_production, editing, 'name', [work, avalid, complete], 'ext']]
                            }, 
    'pre_tecdoc_postprod_sound_folder' : {'path' : r'{}/{}/03_PostProduction/02_SoundDesign'.format(preprod_folder, pre_tech_doc_folder),
                            'naming' :[ [project_naming, post_production, sound_design, 'name', [work, avalid, complete], 'ext']]
                            },
    'pre_proof_of_concept_folder' : {'path' : r'{}/04_ProofOfConcept'.format(preprod_folder),
                            'naming' : [[project_naming, 'type', 'folderName', [modeling, texture, blendshape, lookdev, rigging, animation, set_dress, layout, lighting, rendering, compositing, post_production, editing, sound_design], 'name', proof_of_concept, [work, avalid, complete], 'ext']]
                            },

    'prod_ressources_folder' : {'path' : r'{}/00_Materials'.format(prod_folder),
                            'naming' : 'materials'
                            }, 
    'prod_asset_folder' : {'path' : r'{}/01_Assets'.format(prod_folder),
                            'naming' : []
                            }, 
    'prod_asset_ch_folder' : {'path' : r'{}/01_Assets/01_CH'.format(prod_folder),
                            'naming' : 'CH'
                            }, 
    'prod_asset_pr_folder' : {'path' : r'{}/01_Assets/02_PR'.format(prod_folder),
                            'naming' : 'PR'
                            }, 
    'prod_asset_bg_folder' : {'path' : r'{}/01_Assets/03_BG'.format(prod_folder),
                            'naming' : 'BG'
                            }, 
    'prod_asset_fx_folder' : {'path' : r'{}/01_Assets/04_FX'.format(prod_folder),
                            'naming' : 'FX_asset'
                            }, 
    'prod_asset_publish_folder' : {'path' : r'{}/01_Assets/05_Publish'.format(prod_folder),
                            'naming' : []
                            }, 
    'prod_asset_publish_asset_folder' : {'path' : r'{}/01_Assets/05_Publish/01_Assets'.format(prod_folder),
                            'naming' : [[project_naming, [character, props, background], 'name', complete, [ext_mayaBinari]]]
                            }, 
    'prod_asset_publish_sourceimage_folder' : {'path' : r'{}/01_Assets/05_Publish/02_SourcesImages'.format(prod_folder),
                            'naming' : [[project_naming, [character, props, background], 'name', 'name', image_type, ext_image]]
                            }, 
    'prod_asset_publish_fx_folder' : {'path' : r'{}/01_Assets/05_Publish/03_FX'.format(prod_folder),
                            'naming' : [[project_naming, effect, 'name', complete, ext_houdini]]
                            }, 
    'prod_sequences_folder' : {'path' : r'{}/03_Sequences'.format(prod_folder),
                            'naming' : 'sequences'
                            }, 
    'prod_sequences_globScene_folder' : {'path' : r'{}/02_GlobalScenes'.format(prod_folder),
                            'naming' : 'global scene'
                            },
    'prod_asset_render_folder' : {'path' : r'{}/04_Render'.format(prod_folder),
                            'naming' : []
                            }, 
    'prod_asset_render_scene_folder' : {'path' : r'{}/04_Render/01_Scenes'.format(prod_folder),
                            'naming' : 'render_scene'
                            }, 
    'prod_asset_render_images_folder' : {'path' : r'{}/04_Render/02_Images'.format(prod_folder),
                            'naming' : 'render_images'
                            }, 
    'prod_asset_compo_folder' : {'path' : r'{}/05_Compo'.format(prod_folder),
                            'naming' : 'compo'
                            },
    
    'post_bank_folder' : {'path' : r'{}/00_Bank'.format(post_prod_folder),
                            'naming' : []
                            }, 
    'post_bank_videos_folder' : {'path' : r'{}/00_Bank/01_Videos'.format(post_prod_folder),
                            'naming' : post_bank_naming
                            }, 
    'post_bank_images_folder' : {'path' : r'{}/00_Bank/02_Images'.format(post_prod_folder),
                            'naming' : post_bank_naming
                            }, 
    'post_bank_sound_folder' : {'path' : r'{}/00_Bank/03_Sounds'.format(post_prod_folder),
                            'naming' : []
                            }, 
    'post_bank_sound_musics_folder' : {'path' : r'{}/00_Bank/03_Sounds/01_Musics'.format(post_prod_folder),
                            'naming' : post_bank_naming
                            }, 
    'post_bank_sound_ambiant_folder' : {'path' : r'{}/00_Bank/03_Sounds/02_Ambiant'.format(post_prod_folder),
                            'naming' : post_bank_naming
                            }, 
    'post_bank_sound_sounds_folder' : {'path' : r'{}/00_Bank/03_Sounds/03_Sounds'.format(post_prod_folder),
                            'naming' : post_bank_naming
                            }, 
    'post_bank_sound_soundsfx_folder' : {'path' : r'{}/00_Bank/03_Sounds/04_SoundsFX'.format(post_prod_folder),
                            'naming' : post_bank_naming
                            }, 
    'post_editing_folder' : {'path' : r'{}/01_Editing'.format(post_prod_folder),
                            'naming' : [[project_naming, post_production, editing, 'name', [work, avalid, complete], 'ext']]
                            }, 
    'post_soundedit_folder' : {'path' : r'{}/02_SoundEdit'.format(post_prod_folder),
                            'naming' : [[project_naming, post_production, sound_design, 'name', [work, avalid, complete], 'ext']]
                            }, 
    'post_review_folder' : {'path' : r'{}/03_Review'.format(post_prod_folder),
                            'naming' : [[project_naming, post_production, post_review, 'name', [work, avalid, complete], 'ext']]
                            }
}

# bg asset folder path
bg_folder_path = {
    'root_folder' : {'path' : '', 'naming' : []}, 
    'ressources_folder' : {'path' : r'/00_Ressources', 'naming' : []}, 
    'mod_folder' : {'path' : r'/01_Mod', 'naming' : []}, 
    'mod_wrk_folder' : {'path' : r'/01_Mod/01_Work', 'naming' : []}, 
    'mod_wrk_geo_folder' : {'path' : r'/01_Mod/01_Work/01_Geo', 'naming' : []}, 
    'mod_wrk_zbrush_folder' : {'path' : r'/01_Mod/01_Work/02_Zbrush', 'naming' : [BG_asset_prefix + [[modeling, lookdev], [work, avalid], ext_zbrush]]}, 
    'mod_wrk_maya_folder' : {'path' : r'/01_Mod/01_Work/03_Maya', 'naming' : [BG_asset_prefix + [[modeling, lookdev], [work, avalid], ext_mayaAscii]]},
    'mod_wrk_houdini_folder' : {'path' : r'/01_Mod/01_Work/04_Houdini', 'naming' : []}, 
    'mod_wrk_houdini_ressources_folder' : {'path' : r'/01_Mod/01_Work/04_Houdini/00_Ressources', 'naming' : [BG_asset_prefix + [ complete, 'ext']]}, 
    'mod_wrk_houdini_cache_folder' : {'path' : r'/01_Mod/01_Work/04_Houdini/00_Cache', 'naming' : [BG_asset_prefix + [modeling,[work, avalid, complete], ext_houdini]]},
    'mod_wrk_houdini_bank_folder' : {'path' : r'/01_Mod/01_Work/04_Houdini/01_Bank', 'naming' : [BG_asset_prefix + [modeling,[work, avalid, complete], ext_houdini]]}, 
    'mod_wrk_houdini_work_folder' : {'path' : r'/01_Mod/01_Work/04_Houdini/02_Work', 'naming' : [BG_asset_prefix + [modeling,[work, avalid], ext_houdini]]},
    'mod_wrk_geo_zbrush_folder' : {'path' : r'/01_Mod/01_Work/01_Geo/01_fromZbrush', 'naming' : [BG_asset_prefix + [modeling, 'name', [work, avalid], ext_obj_fbx]]}, 
    'mod_wrk_geo_maya_folder' : {'path' : r'/01_Mod/01_Work/01_Geo/02_fromMaya', 'naming' : [BG_asset_prefix + [modeling, 'name', [work, avalid], ext_obj_fbx]]}, 
    'mod_wrk_geo_zbrush_base_obj_folder' : {'path' : r'/01_Mod/01_Work/01_Geo/03_ZbrushBaseOBJ', 'naming' : [BG_asset_prefix + [modeling, 'name', [work, avalid], ext_obj_fbx]]},
    'mod_wrk_geo_houdini_folder' : {'path' : r'/01_Mod/01_Work/01_Geo/04_fromHoudini', 'naming' : [BG_asset_prefix + [modeling, 'name', [work, avalid], ext_obj_fbx]]},    
    'mod_def_folder' : {'path' : r'/01_Mod/02_Def', 'naming' : [BG_asset_prefix + [modeling, complete, ext_mayaAscii]]}, 
    'uvs_folder' : {'path' : r'/02_Uvs', 'naming' : []}, 
    'uvs_wrk_folder' : {'path' : r'/02_Uvs/01_Work', 'naming' : [BG_asset_prefix + [uv, [work, avalid], ext_mayaAscii]]}, 
    'uvs_def_folder' : {'path' : r'/02_Uvs/02_Def', 'naming' : [BG_asset_prefix + [uv, complete, ext_mayaAscii]]}, 
    'uvs_export_folder' : {'path' : r'/02_Uvs/03_Export', 'naming' :[ BG_asset_prefix + [uv, "name", [work, avalid, complete], ext_obj_fbx]]}, 
    'shadding_folder' : {'path' : r'/03_Shading', 'naming' : []}, 
    'shadding_maya_folder' : {'path' : r'/03_Shading/01_Maya', 'naming' : []}, 
    'shadding_maya_wrk_folder' : {'path' : r'/03_Shading/01_Maya/01_Work', 'naming' : [BG_asset_prefix + [[texture, lookdev], [work, avalid], ext_mayaAscii]]},
    'shadding_maya_def_folder' : {'path' : r'/03_Shading/01_Maya/02_Def', 'naming' : [BG_asset_prefix + [[texture, lookdev], complete, ext_mayaAscii]]}, 
    'shadding_substance_folder' : {'path' : r'/03_Shading/02_Substance', 'naming' : [BG_asset_prefix + [substance_painter, [work, avalid, complete], ext_painter]]}, 
    'shadding_export_folder' : {'path' : r'/03_Shading/03_Export', 'naming' : [BG_asset_prefix + ["name", image_type, image_number, ext_image], BG_asset_prefix + ['name', image_type, ext_image]]}, 
    'shadding_lookdev_folder' : {'path' : r'/03_Shading/04_Lookdev', 'naming' : [BG_asset_prefix + [[texture, lookdev], "name", ext_image+["pur"]]]}, 
    'rig_folder' : {'path' : r'/04_Rig', 'naming' : []}, 
    'rig_wrk_folder' : {'path' : r'/04_Rig/01_Work', 'naming' :[ BG_asset_prefix + [rigging, [work, avalid], [ext_mayaAscii, ext_json]]]},
    'rig_def_folder' : {'path' : r'/04_Rig/02_Def', 'naming' : [BG_asset_prefix + [rigging, complete, ext_mayaAscii]]},
    'publish_folder' : {'path' : r'/05_Publish', 'naming' : [BG_asset_prefix + [complete, [ext_mayaAscii]]]}
}

# pr asset folder path
pr_folder_path = {
    'root_folder' : {'path' : '', 'naming' : []}, 
    'ressources_folder' : {'path' : r'/00_Ressources', 'naming' : []}, 
    'mod_folder' : {'path' : r'/01_Mod', 'naming' : []}, 
    'mod_wrk_folder' : {'path' : r'/01_Mod/01_Work', 'naming' : []}, 
    'mod_wrk_geo_folder' : {'path' : r'/01_Mod/01_Work/01_Geo', 'naming' : []}, 
    'mod_wrk_zbrush_folder' : {'path' : r'/01_Mod/01_Work/02_Zbrush', 'naming' : [PR_asset_prefix + [modeling, [work, avalid], ext_zbrush]]}, 
    'mod_wrk_maya_folder' : {'path' : r'/01_Mod/01_Work/03_Maya', 'naming' : [PR_asset_prefix + [[modeling, lookdev], [work, avalid], ext_mayaAscii]]},
    'mod_wrk_houdini_folder' : {'path' : r'/01_Mod/01_Work/04_Houdini', 'naming' : []}, 
    'mod_wrk_houdini_ressources_folder' : {'path' : r'/01_Mod/01_Work/04_Houdini/00_Ressources', 'naming' :[ PR_asset_prefix + [ complete, 'ext']]}, 
    'mod_wrk_houdini_cache_folder' : {'path' : r'/01_Mod/01_Work/04_Houdini/00_Cache', 'naming' : [PR_asset_prefix + [modeling, [work, avalid, complete], 'ext']]},
    'mod_wrk_houdini_bank_folder' : {'path' : r'/01_Mod/01_Work/04_Houdini/01_Bank', 'naming' : [PR_asset_prefix + [modeling, [work, avalid, complete], 'ext']]}, 
    'mod_wrk_houdini_work_folder' : {'path' : r'/01_Mod/01_Work/04_Houdini/02_Work', 'naming' : [PR_asset_prefix + [modeling, [work, avalid], 'ext']]},
    'mod_wrk_geo_zbrush_folder' : {'path' : r'/01_Mod/01_Work/01_Geo/01_fromZbrush', 'naming' : [PR_asset_prefix + [modeling, 'name', [work, avalid], ext_obj_fbx]]}, 
    'mod_wrk_geo_maya_folder' : {'path' : r'/01_Mod/01_Work/01_Geo/02_fromMaya', 'naming' : [PR_asset_prefix + [modeling, 'name', [work, avalid], ext_obj_fbx]]},
    'mod_wrk_geo_zbrush_base_obj_folder' : {'path' : r'/01_Mod/01_Work/01_Geo/03_ZbrushBaseOBJ', 'naming' : [PR_asset_prefix + [modeling, 'name', [work, avalid], ext_obj_fbx]]},
    'mod_wrk_geo_houdini_folder' : {'path' : r'/01_Mod/01_Work/01_Geo/04_fromHoudini', 'naming' : [PR_asset_prefix + [modeling, 'name', [work, avalid], ext_obj_fbx]]},    
    'mod_def_folder' : {'path' : r'/01_Mod/02_Def', 'naming' : [PR_asset_prefix + [modeling, complete, ext_mayaAscii]]}, 
    'uvs_folder' : {'path' : r'/02_Uvs', 'naming' : []}, 
    'uvs_wrk_folder' : {'path' : r'/02_Uvs/01_Work', 'naming' : [PR_asset_prefix + [uv, [work, avalid], ext_mayaAscii]]},
    'uvs_def_folder' : {'path' : r'/02_Uvs/02_Def', 'naming' : [PR_asset_prefix + [uv, complete, ext_mayaAscii]]}, 
    'uvs_export_folder' : {'path' : r'/02_Uvs/03_Export', 'naming' : [PR_asset_prefix + [uv, 'name', [work, avalid, complete], ext_obj_fbx]]}, 
    'shadding_folder' : {'path' : r'/03_Shading', 'naming' : []}, 
    'shadding_maya_folder' : {'path' : r'/03_Shading/01_Maya', 'naming' : []}, 
    'shadding_maya_wrk_folder' : {'path' : r'/03_Shading/01_Maya/01_Work', 'naming' : [PR_asset_prefix + [[texture, lookdev], [work, avalid], ext_mayaAscii]]},
    'shadding_maya_def_folder' : {'path' : r'/03_Shading/01_Maya/02_Def', 'naming' : [PR_asset_prefix + [texture, complete, ext_mayaAscii]]}, 
    'shadding_substance_folder' : {'path' : r'/03_Shading/02_Substance', 'naming' : [PR_asset_prefix + [substance_painter, [work, avalid, complete], ext_painter]]}, 
    'shadding_export_folder' : {'path' : r'/03_Shading/03_Export', 'naming' : [PR_asset_prefix + ["name", image_type, image_number, ext_image], PR_asset_prefix + ['name', image_type, ext_image]]},
    'shadding_lookdev_folder' : {'path' : r'/03_Shading/04_Lookdev', 'naming' : [PR_asset_prefix + [[texture, lookdev], "name", ext_image+["pur"]]]}, 
    'rig_folder' : {'path' : r'/04_Rig', 'naming' : []}, 
    'rig_wrk_folder' : {'path' : r'/04_Rig/01_Work', 'naming' : [PR_asset_prefix + [rigging, [work, avalid], [ext_mayaAscii, ext_json]]]},
    'rig_def_folder' : {'path' : r'/04_Rig/02_Def', 'naming' : [PR_asset_prefix + [rigging, complete, ext_mayaAscii]]},
    'publish_folder' : {'path' : r'/05_Publish', 'naming' : [PR_asset_prefix + [complete, [ext_mayaAscii]]]}
}

# ch asset folder path

ch_folder_path = {
    'root_folder' : {'path' : '', 'naming' : []}, 
    'ressources_folder' : {'path' : r'/00_Ressources', 'naming' : []}, 
    'mod_folder' : {'path' : r'/01_Mod', 'naming' : []}, 
    'mod_wrk_folder' : {'path' : r'/01_Mod/01_Work', 'naming' : []}, 
    'mod_wrk_geo_folder' : {'path' : r'/01_Mod/01_Work/01_Geo', 'naming' : []}, 
    'mod_wrk_zbrush_folder' : {'path' : r'/01_Mod/01_Work/02_Zbrush', 'naming' : [CH_asset_prefix + [modeling, [work, avalid], ext_zbrush]]}, 
    'mod_wrk_maya_folder' : {'path' : r'/01_Mod/01_Work/03_Maya', 'naming' : [CH_asset_prefix + [[modeling, lookdev], [work, avalid], ext_mayaAscii]]}, 
    'mod_wrk_geo_zbrush_folder' : {'path' : r'/01_Mod/01_Work/01_Geo/01_fromZbrush', 'naming' : [CH_asset_prefix + [modeling, 'name', [work, avalid], ext_obj_fbx]]}, 
    'mod_wrk_geo_maya_folder' : {'path' : r'/01_Mod/01_Work/01_Geo/02_fromMaya', 'naming' : [CH_asset_prefix + [modeling, 'name', [work, avalid], ext_obj_fbx]]}, 
    'mod_wrk_geo_zbrush_base_obj_folder' : {'path' : r'/01_Mod/01_Work/01_Geo/03_ZbrushBaseOBJ', 'naming' : [CH_asset_prefix + [modeling, 'name', [work, avalid], ext_obj_fbx]]}, 
    'mod_def_folder' : {'path' : r'/01_Mod/02_Def', 'naming' : [CH_asset_prefix + [modeling, complete, ext_mayaAscii]]}, 
    'uvs_folder' : {'path' : r'/02_Uvs', 'naming' : []}, 
    'uvs_wrk_folder' : {'path' : r'/02_Uvs/01_Work', 'naming' : [CH_asset_prefix + [uv, [work, avalid], ext_mayaAscii]]}, 
    'uvs_def_folder' : {'path' : r'/02_Uvs/02_Def', 'naming' : [CH_asset_prefix + [uv, complete, ext_mayaAscii]]}, 
    'uvs_export_folder' : {'path' : r'/02_Uvs/03_Export', 'naming' : [CH_asset_prefix + [uv, 'name', [work, avalid, complete], ext_obj_fbx]]}, 
    'shadding_folder' : {'path' : r'/03_Shading', 'naming' : []}, 
    'shadding_maya_folder' : {'path' : r'/03_Shading/01_Maya', 'naming' : []}, 
    'shadding_maya_wrk_folder' : {'path' : r'/03_Shading/01_Maya/01_Work', 'naming' : [CH_asset_prefix + [[texture, lookdev], [work, avalid], ext_mayaAscii]]},
    'shadding_maya_def_folder' : {'path' : r'/03_Shading/01_Maya/02_Def', 'naming' : [CH_asset_prefix + [texture, complete, ext_mayaAscii]]}, 
    'shadding_substance_folder' : {'path' : r'/03_Shading/02_Substance', 'naming' : [CH_asset_prefix + [substance_painter, [work, avalid, complete], ext_painter]]}, 
    'shadding_export_folder' : {'path' : r'/03_Shading/03_Export', 'naming' : [CH_asset_prefix + ['name', image_type, image_number, ext_image], CH_asset_prefix + ['name', image_type, ext_image]]}, 
    'shadding_lookdev_folder' : {'path' : r'/03_Shading/04_Lookdev', 'naming' : [CH_asset_prefix + [[texture, lookdev], "name", ext_image+["pur"]]]}, 
    'bs_folder' : {'path' : r'/04_Blendshape', 'naming' : []}, 
    'bs_wrk_folder' : {'path' : r'/04_Blendshape/01_Work', 'naming' : [CH_asset_prefix + [blendshape, [work, avalid], ext_mayaAscii]]},
    'bs_def_folder' : {'path' : r'/04_Blendshape/02_Def', 'naming' : [CH_asset_prefix + [blendshape, complete, ext_mayaAscii]]},
    'rig_folder' : {'path' : r'/05_Rig', 'naming' : []}, 
    'rig_wrk_folder' : {'path' : r'/05_Rig/01_Work', 'naming' : [CH_asset_prefix + [rigging, [work, avalid], [ext_mayaAscii, ext_json]]]},
    'rig_def_folder' : {'path' : r'/05_Rig/02_Def', 'naming' : [CH_asset_prefix + [rigging, complete, ext_mayaAscii]]},
    'publish_folder' : {'path' : r'/06_Publish', 'naming' : [CH_asset_prefix + [complete, [ext_mayaAscii]]]}
}

# folder created when fx is created
fx_asset_folder_path = { 
    'root_folder' : {'path' : '', 'naming' : [[project_naming, FX_asset_prefix]  + ['folderName', 'shotFolderName', 'name', complete, ext_houdini_export]]},
    'ressources_folder' : {'path' : r'/00_Ressources', 'naming' : [[project_naming, FX_asset_prefix] + [ complete, 'ext']]}, 
    'cache_folder' : {'path' : r'/00_Cache', 'naming' : ["pass"]},
    'bank_folder' : {'path' : r'/01_Bank', 'naming' : [[project_naming, FX_asset_prefix]  + ['folderName', 'shotFolderName', [work, avalid, complete], ext_houdini]]}, 
    'work_folder' : {'path' : r'/02_Work', 'naming' : [[project_naming, FX_asset_prefix]  + ['folderName', 'shotFolderName', [work, avalid], ext_houdini]]}, 
    'def_folder' : {'path' : r'/03_Def', 'naming' : [[project_naming, FX_asset_prefix]  + ['folderName', 'shotFolderName', 'name', complete, ext_houdini_export]]}
}

# folder created when shot is created
shot_folder_path = {
    'sequence_root' : {'path' : '', 'naming' : []}, 
    'sequence_ressources_folder' : {'path' : r'/00_Ressources', 'naming' : [[project_naming] + ['folderName'] + [ 'name', complete, 'ext']]}, 
    'sequence_setDress' : {'path' : r'/01_SetDress', 'naming' : []}, 
    'sequence_setDress_work' : {'path' : r'/01_SetDress/01_Work', 'naming' : [[project_naming] + ['folderName'] + [set_dress, [work, avalid], ext_mayaAscii]]}, 
    'sequence_setDress_def' : {'path' : r'/01_SetDress/02_Def', 'naming' : [[project_naming] + ['folderName'] + [set_dress, complete, ext_mayaAscii]]}, 
    'sequence_layout' : {'path' : r'/02_Layout', 'naming' : []}, 
    'sequence_layout_work' : {'path' : r'/02_Layout/01_Work', 'naming' : [[project_naming] + ['folderName'] + [layout, [work, avalid], ext_mayaAscii]]}, 
    'sequence_layout_def' : {'path' : r'/02_Layout/02_Def', 'naming' : [[project_naming] + ['folderName'] + [layout, complete, ext_mayaAscii]]},
    'sequence_anim' : {'path' : r'/03_Animation', 'naming' : []}, 
    'sequence_anim_work' : {'path' : r'/03_Animation/01_Work', 'naming' : [[project_naming] + ['folderName'] + [animation, animation_steps, [work, avalid], ext_mayaAscii]]}, 
    'sequence_anim_def' : {'path' : r'/03_Animation/02_Def', 'naming' : [[project_naming] + ['folderName'] + [animation, animation_steps, complete, ext_mayaAscii]]},
    'sequence_lighting' : {'path' : r'/04_Lighting', 'naming' : []}, 
    'sequence_lighting_work' : {'path' : r'04_Lighting/01_Work', 'naming' : [[project_naming] + ['folderName'] + [lighting, [work, avalid], ext_mayaAscii]]}, 
    'sequence_lighting_def' : {'path' : r'04_Lighting/02_Def', 'naming' : [[project_naming] + ['folderName'] + [lighting, complete, ext_mayaAscii]]}, 
    'sequence_fx' : {'path' : r'/05_FX', 'naming' : 'FX_shot'}, 
    'render_scene_root' :  {'path' : '', 'naming' : [[project_naming] + ['folderName'] + [rendering, 'subscene', [work, avalid, complete], ext_mayaAscii]]},
    'render_image_root' :  {'path' : '', 'naming' : [[project_naming] + ['folderName'] + [rendering, 'subscene', 'image', ext_image]]},
    'compo_work' : {'path' : r'/01_Work', 'naming' : [[project_naming] + ['folderName'] + [compositing, [work, avalid, complete], ext_nuke]]}, 
    'compo_images' : {'path' : r'/02_Render', 'naming' : [[project_naming] + ['folderName'] + [compositing, 'image', ext_image]]}
}
# global scene folders
global_scene_path = {
    'root_folder': {'path' : '', 'naming' : []}, 
    'setDress' : {'path' : r'/01_SetDress', 'naming' :[]},
    'setDress_work' : {'path' : r'/01_SetDress/01_Work', 'naming' : [[project_naming, 'scene', global_scene, set_dress, [work, avalid], ext_mayaAscii]]}, 
    'setDress_def': {'path' : r'/01_SetDress/02_Def', 'naming' : [[project_naming, 'scene', global_scene, set_dress, complete, ext_mayaAscii]]},
    'lighting' : {'path' : r'/02_Lighting', 'naming' : []},
    'lighting_work' : {'path' : r'/02_Lighting/01_Work', 'naming' : [[project_naming, 'scene', global_scene, lighting, [work, avalid], ext_mayaAscii]]}, 
    'lighting_def': {'path' : r'/02_Lighting/02_Def', 'naming' : [[project_naming, 'scene', global_scene, lighting, complete, ext_mayaAscii]]}
}

# material folders
material_path = {
    'root_folder': {'path' : '', 'naming' : []},
    'bank_folder' : {'path' : r'/00_Bank', 'naming' : [[project_naming, material, 'folderName', substance_designer, 'name', 'ext']]},
    'substance_folder' : {'path' : r'/01_Substance', 'naming' : [[project_naming, material, 'folderName', substance_designer,[work, avalid], ext_designer]]},
    'material_folder' : {'path' : r'/02_Material', 'naming' : [[project_naming, material, 'folderName', complete, ext_designer]]},
    }


# regex keys
context_menu_shot_path_key = r'^.+(SQ\d{3})$'
last_folder_name_key = r'^.+\\([a-zA-Z0-9_-]+)\\?$'
last_folder_name_key_else = r'^.+/([a-zA-Z0-9_-]+)/?$'

ch_name_check_key = r'^FW__CH__\w+$'
pr_name_check_key = r'^FW__PR__\w+$'
bg_name_check_key = r'^FW__BG__\w+$'
fx_name_check_key = r'^FW__FX__\w+$'
sequence_name_check_key = r'^SQ\d{3}$'
shot_name_check_key = r'^SH\d{3}$'
global_scene_name_check_key = r'^GLOBAL__\w+$'
material_name_check_key = r'^MAT__\w+$'

# json file name
json_file_name = __file__.replace ('_lib.py','_project.json')

