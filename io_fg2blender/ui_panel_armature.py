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
# Contributors: Alexis Laillé
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									UI_PANEL_ARMATURE.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy
from bpy.props import BoolProperty

DEBUG = False

#----------------------------------------------------------------------------------------------------------------------------------

def debug_info( aff):
	global DEBUG
	if DEBUG:
		print( aff )
#--------------------------------------------------------------------------------------------------------------------------------

class FG_PT_armature_tool(bpy.types.Panel):
	'''Flight Object Panel'''
	bl_label	= "Flightgear animation"
	bl_space_type	= 'VIEW_3D'
	bl_region_type	= 'TOOLS'

	@classmethod
	def poll(self,context):
		debug_info( context.mode )
		obj = context.object

		if obj:      
			if obj.type in ('ARMATURE'):
				return True
		return False

	def draw(self, context):
		obj = context.active_object
		if obj:
			if obj.type in ('ARMATURE'):
				layout_armature_tool(self, obj, context);
#--------------------------------------------------------------------------------------------------------------------------------

class FG_PT_armature_properties(bpy.types.Panel):
	'''Flight Object Panel'''
	bl_label	= "Flightgear animation"
	bl_space_type	= 'PROPERTIES'
	bl_region_type	= 'WINDOW'
	bl_context	= 'object'

	@classmethod
	def poll(self,context):
		debug_info( context.mode )
		obj = context.object

		if obj:      
			if obj.type in ('ARMATURE'):
				return True
		return False

	def draw(self, context):
		obj = context.active_object
		if obj:
			if obj.type in ('ARMATURE'):
				layout_armature_properties(self, obj, context);
#--------------------------------------------------------------------------------------------------------------------------------

def layout_armature_properties(self, obj, context):
	from . import xml_manager
	#----------------------------------------------------
	layout = self.layout
	xml_files = xml_manager.xml_files

	col = layout.column()
	col.label( text='Property' )
	box = layout.box()

	row = box.row()
	row.prop( obj.data.fg, "family" )
	#----------------------------------------------------
	if obj.data.fg.family != 'custom':
		row = box.row()
		row.prop(obj.data.fg, "family_value")
		value = obj.data.fg.family_value

	row = box.row()
	row.alignment = 'LEFT'
	if obj.data.fg.family != 'custom':
		row.label( text="Property:" )
		from . import xml_export
		value = xml_export.build_property_name( obj )
		row.label( text=value )
	else:
		row.alignment = 'EXPAND'
		row.prop( obj.data.fg,  "property_value" )

	if obj.data.fg.family_value.find('%d') != -1:
		row = box.row()
		row.prop( obj.data.fg,  "property_idx" )
	#----------------------------------------------------
	boxTitre = layout.column()
	boxTitre.label( text='XML File:' )
	box = layout.box()
	row = box.row()
	row.prop( obj.data.fg, "bIncDiskFile" )
	row.prop( obj.data.fg, "bWriteDisc" )
	row = box.row(align=True)
	row.prop( obj.data.fg, "xml_file" )
	row.operator( "object.file_select_xml", icon='FILESEL' )

	row = box.row()
	row.operator( "view3d.write_xml" ).obj_name = obj.name#.data.fg.xml_file
	
	row = box.row(align=True)
	#----------------------------------------------------
	boxTitre = layout.column()
	boxTitre.label( text='Type' )
	boxType = layout.box()
	colType = boxType.column()	
	if obj.data.fg.type_anim == 1:
		colType.label( text="Rotation" )
	elif obj.data.fg.type_anim == 2:
		colType.label( text="Translation" )
	elif obj.data.fg.type_anim == 7:
		colType.label( text="Spin" )
	#----------------------------------------------------
	row = layout.row()
	row.prop( obj.data.fg, "factor" )
	row.prop( obj.data.fg, "time" )

	row = layout.row()
	row.prop( obj.data.fg, "range_beg" )
	row.prop( obj.data.fg, "range_end" )		
#----------------------------------------------------------------------------------------------------------------------------------

def layout_armature_tool(self, obj, context):
	from . import xml_manager
	#----------------------------------------------------
	layout = self.layout
	xml_files = xml_manager.xml_files

	box = layout.box()
	row = box.row()
	row.operator("view3d.show_animation", text="Show objects related to selected animation")
	row.operator("view3d.show_all", text="Show all objects")

	box_child_object( self, obj, context )
	if obj.parent:
		box_parent( self, obj, context )			
#----------------------------------------------------------------------------------------------------------------------------------

def box_parent( self, obj, context ):
	layout = self.layout

	box = layout.column()
	box.label( text='Parent' )
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

def find_child_object( obj ):
	list_obj = []
	for objet in bpy.data.objects:
		if objet.parent ==  obj:
			list_obj.append( objet )
	return list_obj
#----------------------------------------------------------------------------------------------------------------------------------

def box_child_object( self, obj, context ):
	lst = find_child_object( obj )
	if not lst:
		return
	layout = self.layout
	boxTitre = layout.column()
	boxTitre.label( text='Child(s) object(s):' )
	boxObjects = layout.box()
	for objet in lst:
		if objet.parent ==  obj:
			row = boxObjects.row()
			if objet.type == 'MESH':
				row.label( text=objet.name,icon='OBJECT_DATA' )
			elif objet.type == 'ARMATURE':
				row.label( text=objet.name, icon='BONE_DATA' )
			elif objet.type == 'EMPTY':
				row.label( text=objet.name, icon='EMPTY_DATA' )
			else:
				row.label( text=objet.name )

			row.operator("fg.button_select").object_name=objet.name
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class(FG_PT_armature_tool)
	bpy.utils.register_class(FG_PT_armature_properties)
#--------------------------------------------------------------------------------------------------------------------------------

def unregister():
	bpy.utils.unregister_class(FG_PT_armature_tool)
	bpy.utils.unregister_class(FG_PT_armature_properties)

