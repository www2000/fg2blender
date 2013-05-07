# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#
#
# Script copyright (C) René Nègre
# Contributors: 
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									UI_MENU.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy
import os
import time

from math import radians
from math import degrees

from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import CollectionProperty

from ..meshes.ac3d.ac_manager import AC_OPTION
from ..xml.xml_manager import XML_OPTION

from . import *

#----------------------------------------------------------------------------------------------------------------------------------
#		At loading
#----------------------------------------------------------------------------------------------------------------------------------
def debug_info( aff ):
	from .. import debug_file_debug

	if debug_file_debug:
		print( aff )
#----------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_root_menu(bpy.types.Menu):
	from ..ui.ui_lang import lang
	bl_label = lang['MENTIT'] #"Flightgear Tools Menu"

	def draw(self, context):
		from ..ui.ui_lang import lang

		layout = self.layout
		layout.operator_context = 'INVOKE_REGION_WIN'

		layout.separator()
		layout.operator("view3d.insert_keyframe_rotate",	text=lang['MEN000'] )
		layout.operator("view3d.insert_keyframe_translate",	text=lang['MEN001'] )
		layout.separator()
		layout.operator("import.fg2blender",			text=lang['MEN002'] )
		layout.separator()
		layout.operator("view3d.create_anim",			text=lang['MEN003'] )
		layout.separator()
		layout.operator("view3d.edge_split",			text=lang['MEN004'] )
		#layout.operator("view3d.select_property",		text=lang['MEN005'] )
		layout.operator("view3d.time_2x",			text=lang['MEN006'] ) 		#text='Time x2'
		layout.operator("view3d.time_0_5x",			text=lang['MEN007'] ) 		#text='Time x0.5' )
		layout.operator("view3d.copy_name_bl2ac",		text=lang['MEN008'] ) 		#text='Assign object name' )
		layout.operator("view3d.copy_ac_file",			text=lang['MEN009'] ) 		#text='Assign AC3D filename' )
		layout.separator()
		layout.menu( 'VIEW3D_FG_sub_menu_armature',		text=lang['MEN010'] ) 		#text='Armatures' )
		layout.separator()
		layout.menu( 'VIEW3D_FG_sub_menu_unwrap',		text=lang['MEN011'] ) 		#text='Unwrap' )
		layout.separator()
		layout.operator("wm.url_open", text='Manual').url="http://wiki.flightgear.org/Fr/fg2blender"
		#layout.operator("view3d.unwrap_4_faces",		text='Unwrap 4 faces' )
		#layout.operator("view3d.popup",			text='popup' ).message = "ERR001"
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_sub_menu_unwrap(bpy.types.Menu):
	bl_label = "Unwrap 4 faces"

	def draw(self, context):
		from ..ui.ui_lang import lang

		layout = self.layout
		layout.operator_context = 'INVOKE_REGION_WIN'
		layout.operator("view3d.unwrap_4_faces",	text=lang['MEN020'] ).axis = 'X'	#text='Along X' ).axis = 'X'
		layout.operator("view3d.unwrap_4_faces",	text=lang['MEN021'] ).axis = 'Y'	#text='Along Y' ).axis = 'Y'
		layout.operator("view3d.unwrap_4_faces",	text=lang['MEN022'] ).axis = 'Z'	#text='Along Z' ).axis = 'Z'
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_sub_menu_armature(bpy.types.Menu):
	bl_label = "Armatures"

	def draw(self, context):
		from ..ui.ui_lang import lang

		layout = self.layout
		layout.operator_context = 'INVOKE_REGION_WIN'
		layout.menu('VIEW3D_FG_sub_menu_create_rotation',	text=lang['MEN040']  )
		layout.menu('VIEW3D_FG_sub_menu_create_translate',	text=lang['MEN041']  )
		layout.menu('VIEW3D_FG_sub_menu_create_spin',		text=lang['MEN042']  )
		layout.operator("view3d.transform_to_rotate",		text=lang['MEN043']  )	#'Transform to rotate' )
		layout.operator("view3d.transform_to_translate",	text=lang['MEN044']  )	#'Transform to translate' )
		layout.operator("view3d.transform_to_spin",			text=lang['MEN045']  )	#'Transform to spin' )
		layout.separator()
		#layout.operator("view3d.select_armature_property",	text=lang['MEN046']  )	#'Select related armatures' )
		layout.operator("view3d.select_by_property",		text=lang['MEN047']  )	#'Select by property' )
		layout.operator("view3d.select_object_by_armature",	text=lang['MEN048']  )	#'Select objects by armature' )
		layout.menu('VIEW3D_FG_sub_menu_select_by_file',	text=lang['MEN058']  )	#'Select by file')
		layout.operator("view3d.copy_xml_file",				text=lang['MEN049']  )	#'Copy xml file (active->selects)' )
		layout.operator("view3d.copy_property",				text=lang['MEN050']  )	#'Copy property (active->selects)' )
		layout.separator()
		layout.operator("view3d.init_rotation_zero",		text=lang['MEN051']  )	#'Reset Rotate' )
		layout.operator("view3d.init_rotation",				text=lang['MEN052']  )	#'Init Rotate' )
		layout.separator()
		layout.operator("view3d.freeze_armature",			text=lang['MEN053']  )	#'Freeze selected armatures' )
		layout.operator("view3d.save_keyframe",				text=lang['MEN054']  )	#'Save Keyframe and Reset' )
		layout.menu('VIEW3D_FG_sub_menu_unfreeze_armature',	text=lang['MEN055']  )	#'UNFREEZE')
		#layout.operator("view3d.restore_keyframe",			text='Restore Keyframe ' )
		layout.separator()
		layout.operator("view3d.save_parent",				text=lang['MEN056']  )	#'Save Parent and Reset' )
		layout.operator("view3d.restore_parent",			text=lang['MEN057']  )	#'Restore Parent ' )
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_sub_menu_create_rotation(bpy.types.Menu):
	bl_label = 'Create Rotation'

	def draw(self, context):
		from ..ui.ui_lang import lang

		layout = self.layout
		layout.operator_context = 'INVOKE_REGION_WIN'
		layout.operator("view3d.create_rotate_axis",	text=lang['MEN070']  ).axis = 'X'	#	text='Create Rotation X').axis = 'X'
		layout.operator("view3d.create_rotate_axis",	text=lang['MEN071']  ).axis = 'Y'	#	text='Create Rotation Y').axis = 'Y'
		layout.operator("view3d.create_rotate_axis",	text=lang['MEN072']  ).axis = 'Z'	#	text='Create Rotation Z').axis = 'Z'
		layout.operator("view3d.create_rotate_axis",	text=lang['MEN073']  ).axis = 'x'	#	text='Create Rotation -X').axis = 'x'
		layout.operator("view3d.create_rotate_axis",	text=lang['MEN074']  ).axis = 'y'	#	text='Create Rotation -Y').axis = 'y'
		layout.operator("view3d.create_rotate_axis",	text=lang['MEN075']  ).axis = 'z'	#	text='Create Rotation -Z').axis = 'z'
		layout.operator("view3d.create_rotate_axis",	text=lang['MEN076']  ).axis = 'XY'	#	text='Create Rotation XY').axis = 'XY'
		layout.operator("view3d.create_rotate_axis",	text=lang['MEN077']  ).axis = 'XZ'	#	text='Create Rotation XZ').axis = 'XZ'
		layout.operator("view3d.create_rotate_axis",	text=lang['MEN078']  ).axis = 'YZ'	#	text='Create Rotation YZ').axis = 'YZ'
		layout.operator("view3d.create_rotate_axis",	text=lang['MEN079']  ).axis = 'XYZ'	#	text='Create Rotation XYZ').axis = 'XYZ'
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_sub_menu_create_translate(bpy.types.Menu):
	bl_label = 'Create Translate'

	def draw(self, context):
		from ..ui.ui_lang import lang

		layout = self.layout
		layout.operator_context = 'INVOKE_REGION_WIN'
		layout.operator("view3d.create_translate_axis",	text=lang['MEN070']  ).axis = 'X'	#	text='Create Rotation X').axis = 'X'
		layout.operator("view3d.create_translate_axis",	text=lang['MEN071']  ).axis = 'Y'	#	text='Create Rotation Y').axis = 'Y'
		layout.operator("view3d.create_translate_axis",	text=lang['MEN072']  ).axis = 'Z'	#	text='Create Rotation Z').axis = 'Z'
		layout.operator("view3d.create_translate_axis",	text=lang['MEN073']  ).axis = 'x'	#	text='Create Rotation -X').axis = 'x'
		layout.operator("view3d.create_translate_axis",	text=lang['MEN074']  ).axis = 'y'	#	text='Create Rotation -Y').axis = 'y'
		layout.operator("view3d.create_translate_axis",	text=lang['MEN075']  ).axis = 'z'	#	text='Create Rotation -Z').axis = 'z'
		layout.operator("view3d.create_translate_axis",	text=lang['MEN076']  ).axis = 'XY'	#	text='Create Rotation XY').axis = 'XY'
		layout.operator("view3d.create_translate_axis",	text=lang['MEN077']  ).axis = 'XZ'	#	text='Create Rotation XZ').axis = 'XZ'
		layout.operator("view3d.create_translate_axis",	text=lang['MEN078']  ).axis = 'YZ'	#	text='Create Rotation YZ').axis = 'YZ'
		layout.operator("view3d.create_translate_axis",	text=lang['MEN079']  ).axis = 'XYZ'	#	text='Create Rotation XYZ').axis = 'XYZ'
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_sub_menu_create_spin(bpy.types.Menu):
	bl_label = 'Create Spin'

	def draw(self, context):
		from ..ui.ui_lang import lang

		layout = self.layout
		layout.operator_context = 'INVOKE_REGION_WIN'
		layout.operator("view3d.create_spin",	text=lang['MEN070']  ).axis = 'X'	#	text='Create Rotation X').axis = 'X'
		layout.operator("view3d.create_spin",	text=lang['MEN071']  ).axis = 'Y'	#	text='Create Rotation Y').axis = 'Y'
		layout.operator("view3d.create_spin",	text=lang['MEN072']  ).axis = 'Z'	#	text='Create Rotation Z').axis = 'Z'
		layout.operator("view3d.create_spin",	text=lang['MEN073']  ).axis = 'x'	#	text='Create Rotation -X').axis = 'x'
		layout.operator("view3d.create_spin",	text=lang['MEN074']  ).axis = 'y'	#	text='Create Rotation -Y').axis = 'y'
		layout.operator("view3d.create_spin",	text=lang['MEN075']  ).axis = 'z'	#	text='Create Rotation -Z').axis = 'z'
		layout.operator("view3d.create_spin",	text=lang['MEN076']  ).axis = 'XY'	#	text='Create Rotation XY').axis = 'XY'
		layout.operator("view3d.create_spin",	text=lang['MEN077']  ).axis = 'XZ'	#	text='Create Rotation XZ').axis = 'XZ'
		layout.operator("view3d.create_spin",	text=lang['MEN078']  ).axis = 'YZ'	#	text='Create Rotation YZ').axis = 'YZ'
		layout.operator("view3d.create_spin",	text=lang['MEN079']  ).axis = 'XYZ'	#	text='Create Rotation XYZ').axis = 'XYZ'

#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_sub_menu_unfreeze_armature(bpy.types.Menu):
	bl_label = "Unfreeze"

	#-----------------------------------------------------------------------------------------------------------------------------
	def draw(self, context):

		layout = self.layout
		layout.operator("view3d.unfreeze_armature",
		                    text="All armatures",
		                    icon='MATERIAL_DATA').object_name = "All"
		                    
		for armature in bpy.data.objects:
			if armature.type != 'ARMATURE':
				continue
			if len(armature.data.fg.keyframes) != 0:
				layout.operator("view3d.unfreeze_armature",
					                text=armature.name,
					                icon='ARMATURE_DATA').object_name = armature.name
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_sub_menu_select_by_file(bpy.types.Menu):
	bl_label = "Select by File"

	#-----------------------------------------------------------------------------------------------------------------------------
	def draw(self, context):
		layout = self.layout
		xml_files = []
		ac_files = []

		for obj in bpy.data.objects:
			if obj.type == 'ARMATURE':
				xml_file = obj.data.fg.xml_file
				if xml_file != "" and not xml_file in xml_files:
					xml_files.append( xml_file )
			elif obj.type == 'MESH':
				ac_file = obj.data.fg.ac_file
				if ac_file != "" and not ac_file in ac_files:
					ac_files.append( ac_file )
					
		for f in xml_files:
			layout.operator(	"view3d.select_by_file",
								text=f,
								icon='ARMATURE_DATA').filename = f
		for f in ac_files:
			layout.operator(	"view3d.select_by_file",
								text=f,
								icon='MESH_CUBE').filename = f
#----------------------------------------------------------------------------------------------------------------------------------
# Pour le raccourci CTRL-F       utilise pour le "debuggage"
# Réouvre le dernier xml     contenu dans '/tmp/script-fg2bl'
# Cela évite la manipulation de la souris
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_exec(bpy.types.Operator):
	bl_idname = "fg.exec"
	bl_label = "fg.exec"

	def execute(self, context ):
		from ..meshes.ac3d.ac_manager import AC_OPTION
		from ..xml.xml_manager import XML_OPTION
		from ..xml.xml_import import import_xml
		
		ac_option = AC_OPTION()
		ac_option.smooth_all	= True
		ac_option.edge_split	= True
		ac_option.split_angle	= 60.0

		xml_option = XML_OPTION()
		xml_option.include		= True

		xml_option.mesh_active_layer	= False
		xml_option.mesh_layer_beg		= 1
		xml_option.mesh_layer_end		= 10
		xml_option.arma_active_layer	= False
		xml_option.arma_layer_beg		= 11
		xml_option.arma_layer_end		= 20
		
		from .. import debug_file_debug
		if debug_file_debug:
			debug_info( "Raccourci Ctrl+F" )
			f = open('/tmp/script-fg2bl', mode='r')
			filename = f.readline()
			f.close()
		else:
			return {'FINISHED'}

		import_xml( filename, ac_option, xml_option )
		bpy.context.scene.layers = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------
# Pour le raccourci CTRL-X       utilise pour le "debuggage"
# AFFICHAGE d'information sur la liste xml_manager.xml_files
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_exec2(bpy.types.Operator):
	bl_idname = "fg.exec2"
	bl_label = "fg.exec2"

	def print_ac_file( self, ac_file, f ):
		f.write( "     ac_file.name  = %s\n" % ac_file.name )
		f.write( "     ac_file.meshs = List de mesh\n" )
		for mesh in ac_file.meshs:
			f.write( "        mesh = %s\n" % mesh )
		f.write( "     ac_file.dic_name_meshs = Dictionnary\n" )
		for key in ac_file.dic_name_meshs.keys():
			f.write( "        dic = %s <-> %s\n" % (key,ac_file.dic_name_meshs[key]) )
		
	def print_mesh( self, obj, f ):
		f.write( "    fg.name_ac : %s\n" % obj.data.fg.name_ac )
		f.write( "    fg.ac_file : %s\n" % obj.data.fg.ac_file )
		
	def print_armature( self, obj, f ):
		f.write( "    fg.xml_file : %s\n" % obj.data.fg.xml_file )
		f.write( "    fg.xml_file_no : %s\n" % obj.data.fg.xml_file_no )
		f.write( "    fg.xml_present : %s\n" % obj.data.fg.xml_present )
		f.write( "    fg.family : %s\n" % obj.data.fg.family )
		f.write( "    fg.family_value : %s\n" % obj.data.fg.family_value )
		f.write( "    fg.propety_value : %s\n" % obj.data.fg.property_value )
		f.write( "    fg.propety_idx : %d\n" % obj.data.fg.property_idx )
		f.write( "    fg.type_anim : %s\n" % obj.data.fg.type_anim )
		f.write( "    fg.factor : %f\n" % obj.data.fg.factor )
		f.write( "    fg.factor : %.2f\n" % obj.data.fg.factor )
		f.write( "    fg.factor_ini : %.2f\n" % obj.data.fg.factor_ini )
		f.write( "    fg.range_beg : %.2f\n" % obj.data.fg.range_beg )
		f.write( "    fg.range_end : %.2f\n" % obj.data.fg.range_end )
		f.write( "    fg.range_beg_ini : %.2f\n" % obj.data.fg.range_beg_ini )
		f.write( "    fg.range_end_ini : %.2f\n" % obj.data.fg.range_end_ini )
		f.write( "    fg.time : %.2f\n" % obj.data.fg.time )
		f.write( "    fg.time_ini : %.2f\n" % obj.data.fg.time_ini )
		f.write( "    fg.offset_deg : %.2f\n" % obj.data.fg.offset_deg )
		f.write( "    fg.bIncDickFile : %s\n" % obj.data.fg.bIncDiskFile )
		f.write( "    fg.bWriteDisc : %s\n" % obj.data.fg.bWriteDisc )

	def print_camera( self, obj, f ):
		f.write( "    fg.xml_file : %s\n" % obj.data.fg.xml_file )
		f.write( "    fg.type_view : %s\n" % obj.data.fg.type_view )
		
	def print_empty( self, obj, f ):
		f.write( "    fg.jsb_xml_file : %s\n" % obj.fg.jsb_xml_file )
		f.write( "    fg.jsb_attr : %s\n" % obj.fg.jsb_attr )
		
	def execute(self, context ):
		from ..xml import xml_manager
		from .. import fg2bl

		f = open("/tmp/debug_script.txt", "w")

		f.write ( "---------------------------------\n")		
		f.write ( "\n")		
		f.write ( "    Donnees interne du script    \n")		
		f.write ( "\n")		
		f.write ( "---------------------------------\n")		

		for xml_file, no in xml_manager.xml_files:
			f.write ( "xml_file.name    = %s\n" % xml_file.name )		
			f.write ( "xml_file.no      = %d\n" % xml_file.no )		
			for ac_file in xml_file.ac_files:
				self.print_ac_file( ac_file, f )
				
		f.write ( "---------------------------------\n")		
		f.write ( "\n")		
		f.write ( "    Donnees Blender    \n")		
		f.write ( "\n")		
		f.write ( "---------------------------------\n")
		f.write ( "Blender filename : %s\n" % fg2bl.path.get_blender_filename() )
		f.write ( "---------------------------------\n")		
		for obj in bpy.data.objects:
			f.write( "object name : %s\n" % obj.name )
			if  obj.type == 'MESH':
				self.print_mesh(obj, f)
			elif  obj.type == 'ARMATURE':
				print( "Name " + obj.name )
				self.print_armature(obj, f)
			elif  obj.type == 'CAMERA':
				self.print_camera(obj, f)
			elif  obj.type == 'EMPTY':
				self.print_empty(obj, f)

		f.close()
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
    bpy.utils.register_class(FG_OT_exec)
    bpy.utils.register_class(FG_OT_exec2)
    bpy.utils.register_class(VIEW3D_FG_root_menu)
    bpy.utils.register_class(VIEW3D_FG_sub_menu_unwrap)
    bpy.utils.register_class(VIEW3D_FG_sub_menu_armature)
    bpy.utils.register_class(VIEW3D_FG_sub_menu_create_rotation)
    bpy.utils.register_class(VIEW3D_FG_sub_menu_create_spin)
    bpy.utils.register_class(VIEW3D_FG_sub_menu_create_translate)
    bpy.utils.register_class(VIEW3D_FG_sub_menu_unfreeze_armature)
    bpy.utils.register_class(VIEW3D_FG_sub_menu_select_by_file)
def unregister():
    bpy.utils.unregister_class(FG_OT_exec)
    bpy.utils.unregister_class(FG_OT_exec2)
    bpy.utils.unregister_class(VIEW3D_FG_root_menu)
    bpy.utils.unregister_class(VIEW3D_FG_sub_menu_unwrap)
    bpy.utils.unregister_class(VIEW3D_FG_sub_menu_armature)
    bpy.utils.unregister_class(VIEW3D_FG_sub_menu_create_rotation)
    bpy.utils.unregister_class(VIEW3D_FG_sub_menu_create_spin)
    bpy.utils.unregister_class(VIEW3D_FG_sub_menu_create_translate)
    bpy.utils.unregister_class(VIEW3D_FG_sub_menu_unfreeze_armature)
    bpy.utils.unregister_class(VIEW3D_FG_sub_menu_select_by_file)


