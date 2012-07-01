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


#--------------------------------------------------------------------------------------------------------------------------------

class FG_PT_armature(bpy.types.Panel):
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
			if obj.type in ("ARMATURE"):
				return True
		return False

	def draw(self, context):
		obj = context.active_object
		if obj:
			if obj.type == "ARMATURE":
				layout_armature(self, obj, context);
#--------------------------------------------------------------------------------------------------------------------------------

def layout_property(self, obj, context):
	from . import xml_manager

	layout = self.layout
	xml_files = xml_manager.xml_files

	col = layout.column()
	col.label( text='Property' )
	box = layout.box()

	row = box.row()
	row.prop( obj.data.fg, "familly" )

	anim = None
	for xml_file, no in xml_files:
		for anim in xml_file.anims:
			if anim.name == obj.name:
				break;


	if obj.data.fg.familly != 'custom':
		row = box.row()
		row.prop(obj.data.fg, "familly_value")
		value = obj.data.fg.familly_value

		#print( context.mode )
		#obj.data.fg.property_value = value

	row = box.row()
	row.alignment = 'LEFT'
	if obj.data.fg.familly != 'custom':
		row.label( text="Property:" )
		#if anim :
		row.label( text=obj.data.fg.familly_value )
	else:
		row.alignment = 'EXPAND'
		row.prop( obj.data.fg,  "property_value" )

#--------------------------------------------------------------------------------------------------------------------------------

def layout_armature(self, obj, context):
	from . import xml_manager
	
	layout = self.layout
	xml_files = xml_manager.xml_files

	boxTitre = layout.column()
	boxTitre.label( text='Type' )
	boxType = layout.box()
	colType = boxType.column()

	if obj.data.fg.type_anim == 1:
		colType.label( text="Rotation" )
	elif obj.data.fg.type_anim == 2:
		colType.label( text="Translation" )

	layout_property( self, obj, context )
			
	col = layout.column()
	for xml_file, no in xml_files:
		for anim in xml_file.anims:
			if anim.name == obj.name:
				col.prop( obj.data.fg, "factor" )
				break;
			
	boxTitre = layout.column()
	boxTitre.label( text='Objets liés:' )
	boxObjects = layout.box()
	for objet in bpy.data.objects:
		if objet.parent ==  obj:
			row = boxObjects.row()
			if objet.type == 'MESH':
				row.label( text=objet.name,icon='OBJECT_DATA' )
			elif objet.type == 'ARMATURE':
				row.label( text=objet.name, icon='BONE_DATA' )
			else:
				row.label( text=objet.name )

			row.operator("fg.button_select").object_name=objet.name
			
	boxTitre = layout.column()
	boxTitre.label( text='xml file:' )
	box = layout.box()
	row = box.row(align=True)
	row.prop( obj.data.fg, "xml_file" )
	ret = row.operator( "object.file_select", icon='FILESEL' ).filepath
	
	#print( ret )

	row = box.row(align=True)
	for xml_file, no in xml_files:
		for anim in xml_file.anims:
			if anim.name == obj.name:
				row.prop( obj.data.fg, "xml_present" )
				break;

#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class(FG_PT_armature)
#--------------------------------------------------------------------------------------------------------------------------------

def unregister():
	bpy.utils.unregister_class(FG_PT_armature)


