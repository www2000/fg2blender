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
#									UI_PANEL_ARMATURE.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy
import os


#--------------------------------------------------------------------------------------------------------------------------------

class FG_PT_object(bpy.types.Panel):
	'''Flight Object Panel'''
	bl_label = "FLightgear"
	#bl_space_type = "PROPERTIES"
	#bl_region_type = "WINDOW"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	#bl_context = "object"

	@classmethod
	def poll(self,context):
		obj = context.object

		if obj:      
			if obj.type in ("MESH"):
				return True
		return False

	def draw(self, context):
		obj = context.active_object
		if obj:
			if obj.type == "MESH":
				layout_object(self, obj, context);
#--------------------------------------------------------------------------------------------------------------------------------

def layout_object(self, obj, context):
	from . import xml_manager
	
	layout = self.layout
	xml_files = xml_manager.xml_files

	boxTitre = layout.column()
	boxTitre.label( text='Ac file' )
	box = layout.box()
	col = box.column()

	for xml_file, no in xml_files:
		for ac_file in xml_file.ac_files:
			for mesh in ac_file.meshs:
				if mesh == obj.name:
					col.label( text=ac_file.name.partition('Aircraft')[2][1:] )
					break;

	if obj.parent:
		boxTitre = layout.column()
		boxTitre.label( text='Parent' )
		box = layout.box()
		row = box.row()
		row.label( text=obj.parent.name, icon='BONE_DATA' )
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
	bpy.utils.register_class(FG_PT_object)
#--------------------------------------------------------------------------------------------------------------------------------

def unregister():
	bpy.utils.unregister_class(FG_PT_object)


