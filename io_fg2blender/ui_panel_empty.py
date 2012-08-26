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
#									UI_PANEL_EMPTY.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy
import os


#--------------------------------------------------------------------------------------------------------------------------------

class FG_PT_empty_properties(bpy.types.Panel):
	'''Flight Object Panel'''
	bl_label = "Flightgear JSBsim"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	#bl_space_type = 'VIEW_3D'
	#bl_region_type = 'TOOLS'
	bl_context = "object"

	@classmethod
	def poll(self,context):
		obj = context.object

		if obj:      
			if obj.type in ('EMPTY'):
				return True
		return False

	def draw(self, context):
		obj = context.active_object
		if obj:
			if obj.type in ('EMPTY'):
				layout_empty(self, obj, context);
#--------------------------------------------------------------------------------------------------------------------------------

def layout_empty(self, obj, context):
	from . import xml_manager
	
	layout = self.layout
	xml_files = xml_manager.xml_files

	row = layout.row()
	row.label( text='JSBSIM  file' )
	box = layout.box()

	row = box.row()
	row.prop( obj.fg, "jsb_attr" )

	row = box.row()
	if obj.type == 'EMPTY':
		row = box.row(align=True)
		row.prop( obj.fg, "jsb_xml_file" )
		row.operator( "object.file_select_jsb", icon='FILESEL' )
	
	row = box.row()
	row.operator( "view3d.write_jsb" ).obj_name=obj.name

#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class(FG_PT_empty_properties)
#--------------------------------------------------------------------------------------------------------------------------------

def unregister():
	bpy.utils.unregister_class(FG_PT_empty_properties)


