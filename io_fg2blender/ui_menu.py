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
        layout.operator("import.fg2blender",			text='Import (.xml)' )
        layout.separator()
        layout.operator("view3d.create_anim",		text='Creation animations' )
        layout.separator()
        layout.operator("view3d.edge_split",		text='Edge-split' )
        layout.operator("view3d.select_property",	text='Select property' )
        layout.operator("view3d.time_2x",			text='Time x2' )
        layout.operator("view3d.time_0_5x",			text='Time x0.5' )

        layout.separator()
        layout.operator("view3d.create_rotate",		text='Define Rotation' )
        layout.operator("view3d.create_translate",	text='Define Translation' )
        layout.separator()
        layout.menu( 'VIEW3D_FG_sub_menu_unwrap' )
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
# Pour le raccourci CTRL-F       utilise pour le "debuggage"
# Réouvre le dernier xml     contenu dans '/home/rene/tmp/blender/script-fg2bl'
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
		xml_option.include		= False
		xml_option.active_layer	= False
		xml_option.layer_beg	= 1
		xml_option.layer_end	= 10

		if xml_manager.BIDOUILLE:
			f = open('/home/rene/tmp/script-fg2bl', mode='r')
			filename = f.readline()
			f.close()
		else:
			print( "Bidouille OK" )
			return {'FINISHED'}

		import_xml( filename, ac_option, xml_option )
		bpy.context.scene.layers = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
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
    bpy.utils.register_class(VIEW3D_FG_root_menu)
    bpy.utils.register_class(VIEW3D_FG_sub_menu_unwrap)
def unregister():
    bpy.utils.unregister_class(FG_OT_exec)
    bpy.utils.unregister_class(VIEW3D_FG_root_menu)
    bpy.utils.unregister_class(VIEW3D_FG_sub_menu_unwrap)



