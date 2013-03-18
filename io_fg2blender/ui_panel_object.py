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
# Contributors: Alexis Laillé, Clément de l'Hamaide
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									UI_PANEL_OBJECT.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy
import os

#--------------------------------------------------------------------------------------------------------------------------------

class FG_PT_object_tool(bpy.types.Panel):
	'''Flight Object Panel'''
	bl_label 	= "Flightgear"
	bl_space_type	= "VIEW_3D"
	bl_region_type	= "TOOLS"

	@classmethod
	def poll(self,context):
		obj = context.object

		if obj:      
			if obj.type in ('MESH'):
				return True
		return False

	def draw(self, context):
		obj = context.active_object
		if obj:
			if obj.type in ('MESH'):
				layout_object(self, obj, context);
#--------------------------------------------------------------------------------------------------------------------------------

def layout_object(self, obj, context):
	from . import xml_manager
	
	layout = self.layout
	xml_files = xml_manager.xml_files

	row = layout.row()
	row.label( text='AC3D file' )
	box = layout.box()
	boxTitre = box.column()

	col = box.column()

	if obj.type == 'MESH':
		col.prop( obj.data.fg, "name_ac" )
	row = box.row()

	if obj.type == 'MESH':
		row = box.row(align=True)
		row.prop( obj.data.fg, "ac_file" )
		row.operator( "object.file_select_ac", icon='FILESEL' )
	
	row = box.row()
	row.operator( "view3d.save_ac_file" ).object_name=obj.name

	if obj.parent:
		boxTitre = layout.column()
		boxTitre.label( text='Parent' )
		box = layout.box()
		row = box.row()
		if obj.parent.type == 'MESH':
			row.label( text=obj.parent.name,icon='OBJECT_DATA' )
		elif obj.parent.type == 'ARMATURE':
			row.label( text=obj.parent.name, icon='BONE_DATA' )
		elif obj.parent.type == 'EMPTY':
			row.label( text=obj.parent.name, icon='EMPTY_DATA' )
		else:
			row.label( text=obj.parent.name )
		row.operator("fg.button_select", text="Select").object_name=obj.parent.name
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class(FG_PT_object_tool)
#--------------------------------------------------------------------------------------------------------------------------------

def unregister():
	bpy.utils.unregister_class(FG_PT_object_tool)

