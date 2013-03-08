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

from .ac_manager import AC_OPTION
from .xml_manager import XML_OPTION

from . import *
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_root_menu(bpy.types.Menu):
    bl_label = "Flightgear Tools Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.separator()
        layout.operator("view3d.insert_keyframe_rotate",	text='Insert Keyframe Rotate' )
        layout.operator("view3d.insert_keyframe_translate", 	text='Insert Keyframe Translate' )
        layout.separator()
        layout.operator("import.fg2blender",			text='Import (.xml)' )
        layout.separator()
        layout.operator("view3d.create_anim",			text='Creation animations' )
        layout.separator()
        layout.operator("view3d.edge_split",			text='Edge-split' )
        layout.operator("view3d.select_property",		text='Select property' )
        layout.operator("view3d.time_2x",			text='Time x2' )
        layout.operator("view3d.time_0_5x",			text='Time x0.5' )
        layout.operator("view3d.copy_name_bl2ac",		text='Copy blender name to ac name' )
        layout.operator("view3d.copy_ac_file",			text='Copy ac file (active->selects)' )
        layout.separator()
        layout.menu( 'VIEW3D_FG_sub_menu_armature',		text='Armatures' )
        layout.separator()
        layout.menu( 'VIEW3D_FG_sub_menu_unwrap' )
        layout.separator()
        layout.operator("wm.url_open", text='Manual').url="http://wiki.flightgear.org/Fr/fg2blender"
        #layout.operator("view3d.unwrap_4_faces",	text='Unwrap 4 faces' )
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_sub_menu_unwrap(bpy.types.Menu):
    bl_label = "Unwrap 4 faces"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("view3d.unwrap_4_faces",	text='Along X' ).axis = 'X'
        layout.operator("view3d.unwrap_4_faces",	text='Along Y' ).axis = 'Y'
        layout.operator("view3d.unwrap_4_faces",	text='Along Z' ).axis = 'Z'
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_sub_menu_armature(bpy.types.Menu):
    bl_label = "Armatures"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.menu('VIEW3D_FG_sub_menu_create_rotation' )
        layout.menu('VIEW3D_FG_sub_menu_create_translate' )
        layout.operator("view3d.transform_to_rotate",	text='Transform to rotate' )
        layout.operator("view3d.transform_to_translate",	text='Transform to translate' )
        #layout.operator("view3d.create_translate",	text='Create Translation' )
        layout.separator()
        layout.operator("view3d.select_armature_property",		text='Select Property' )
        layout.operator("view3d.copy_xml_file",		text='Copy xml file (active->selects)' )
        layout.operator("view3d.copy_property",		text='Copy property (active->selects)' )
        layout.separator()
        layout.operator("view3d.init_rotation_zero",text='Reset Rotate' )
        layout.operator("view3d.init_rotation",		text='Init Rotate' )
        layout.separator()
        layout.operator("view3d.save_keyframe",		text='Save Keyframe and Reset' )
        layout.operator("view3d.restore_keyframe",	text='Restore Keyframe ' )
        layout.operator("view3d.save_parent",		text='Save Parent and Reset' )
        layout.operator("view3d.restore_parent",	text='Restore Parent ' )
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_sub_menu_create_rotation(bpy.types.Menu):
    bl_label = 'Create Rotation'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("view3d.create_rotate_axis",	text='Create Rotation X').axis = 'X'
        layout.operator("view3d.create_rotate_axis",	text='Create Rotation Y').axis = 'Y'
        layout.operator("view3d.create_rotate_axis",	text='Create Rotation Z').axis = 'Z'
        layout.operator("view3d.create_rotate_axis",	text='Create Rotation -X').axis = 'x'
        layout.operator("view3d.create_rotate_axis",	text='Create Rotation -Y').axis = 'y'
        layout.operator("view3d.create_rotate_axis",	text='Create Rotation -Z').axis = 'z'
        layout.operator("view3d.create_rotate_axis",	text='Create Rotation XY').axis = 'XY'
        layout.operator("view3d.create_rotate_axis",	text='Create Rotation XZ').axis = 'XZ'
        layout.operator("view3d.create_rotate_axis",	text='Create Rotation YZ').axis = 'YZ'
        layout.operator("view3d.create_rotate_axis",	text='Create Rotation XYZ').axis = 'XYZ'
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_sub_menu_create_translate(bpy.types.Menu):
    bl_label = 'Create Translate'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("view3d.create_translate_axis",	text='Create Translation X').axis = 'X'
        layout.operator("view3d.create_translate_axis",	text='Create Translation Y').axis = 'Y'
        layout.operator("view3d.create_translate_axis",	text='Create Translation Z').axis = 'Z'
        layout.operator("view3d.create_translate_axis",	text='Create Translation -X').axis = 'x'
        layout.operator("view3d.create_translate_axis",	text='Create Translation -Y').axis = 'y'
        layout.operator("view3d.create_translate_axis",	text='Create Translation -Z').axis = 'z'
        layout.operator("view3d.create_translate_axis",	text='Create Translation XY').axis = 'XY'
        layout.operator("view3d.create_translate_axis",	text='Create Translation XZ').axis = 'XZ'
        layout.operator("view3d.create_translate_axis",	text='Create Translation YZ').axis = 'YZ'
        layout.operator("view3d.create_translate_axis",	text='Create Translation XYZ').axis = 'XYZ'
#----------------------------------------------------------------------------------------------------------------------------------
# Pour le raccourci CTRL-F       utilise pour le "debuggage"
# Réouvre le dernier xml     contenu dans '/tmp/script-fg2bl'
# Cela évite la manipulation de la souris
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_exec(bpy.types.Operator):
	bl_idname = "fg.exec"
	bl_label = "fg.exec"

	def execute(self, context ):
		from .ac_manager import AC_OPTION
		from .xml_manager import XML_OPTION
		from .xml_import import import_xml
		
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
		

		if xml_manager.BIDOUILLE:
			f = open('/tmp/script-fg2bl', mode='r')
			filename = f.readline()
			f.close()
		else:
			print( "Bidouille OK" )
			return {'FINISHED'}

		import_xml( filename, ac_option, xml_option )
		
		#from . import xml_jsbsim

		#bpy.ops.object.file_select_jsb()

		#xml_jsbsim.write_jsbsim( context, '' )
		
		bpy.context.scene.layers = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
		#bpy.ops.object.select_all(action='SELECT')
		#bpy.ops.view3d.edge_split()
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
		f.write( "    fg.familly : %s\n" % obj.data.fg.familly )
		f.write( "    fg.familly_value : %s\n" % obj.data.fg.familly_value )
		f.write( "    fg.xml_file : %s\n" % obj.data.fg.xml_file )
		f.write( "    fg.xml_file_no : %s\n" % obj.data.fg.xml_file_no )
		f.write( "    fg.type_anim : %d\n" % obj.data.fg.type_anim )
		
	def execute(self, context ):
		from . import xml_manager

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
		for obj in bpy.data.objects:
			f.write( "object name : %s\n" % obj.name )
			if  obj.type == 'MESH':
				self.print_mesh(obj, f)
			elif  obj.type == 'ARMATURE':
				self.print_armature(obj, f)

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
    bpy.utils.register_class(VIEW3D_FG_sub_menu_create_translate)
def unregister():
    bpy.utils.unregister_class(FG_OT_exec)
    bpy.utils.unregister_class(FG_OT_exec2)
    bpy.utils.unregister_class(VIEW3D_FG_root_menu)
    bpy.utils.unregister_class(VIEW3D_FG_sub_menu_unwrap)
    bpy.utils.unregister_class(VIEW3D_FG_sub_menu_armature)
    bpy.utils.unregister_class(VIEW3D_FG_sub_menu_create_rotation)
    bpy.utils.unregister_class(VIEW3D_FG_sub_menu_create_translate)



