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

class ANIM_PT_armature(bpy.types.Panel):
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

def layout_armature(self, obj, context):
	from . import xml_manager
	
	layout = self.layout
	xml_files = xml_manager.xml_files

	boxTitre = layout.column()
	boxTitre.label( text='Type' )
	boxType = layout.box()
	colType = boxType.column()
	for xml_file, no in xml_files:
		for anim in xml_file.anims:
			if anim.name == obj.name:
				if anim.type == 1:
					colType.label( text="Rotation" )
					break;
				elif anim.type == 2:
					colType.label( text="Translation" )
					break;
			
	boxTitre = layout.column()
	boxTitre.label( text='Property' )
	boxAnimProperty = layout.box()

	rowProperty = boxAnimProperty.row()
	rowProperty.label( text='Familly :' )
	rowProperty.prop(obj.property, "familly", text="")

	if obj.property.familly == 'controls':
		rowProperty = boxAnimProperty.row()
		rowProperty.label( text='PROPERTY :' )
		rowProperty.prop(obj.controls, "controls", text="")

	elif obj.property.familly == 'instrumentation':
		rowProperty = boxAnimProperty.row()
		rowProperty.label( text='PROPERTY :' )
		rowProperty.prop(obj.instrumentation, "instrumentation", text="")

	colProperty = boxAnimProperty.column()
	for xml_file, no in xml_files:
		for anim in xml_file.anims:
			if anim.name == obj.name:
				colProperty.label( text="Value :" )
				colProperty.label( text=anim.property )
				break;

	boxTitre = layout.column()
	boxTitre.label( text='Valeurs' )
	boxValeurs = layout.box()
	rowValeurs = boxValeurs.row()
	for xml_file, no in xml_files:
		for anim in xml_file.anims:
			if anim.name == obj.name:
				rowValeurs.label( text="Factor :" )
				rowValeurs.label( text=str(anim.factor) )
				break;
			
	boxTitre = layout.column()
	boxTitre.label( text='Objets liés' )
	boxObjects = layout.box()
	row = boxObjects.row()
	for objet in bpy.data.objects:
		if objet.parent ==  obj:
			if objet.type == 'MESH':
				row.label( text=objet.name,icon='OBJECT_DATA' )
			elif objet.type == 'ARMATURE':
				colObjects.label( text=objet.name, icon='BONE_DATA' )
			else:
				colObjects.label( text=objet.name )

			row.operator("fg.button_select", text="Select").object_name=objet.name
			
	boxTitre = layout.column()
	boxTitre.label( text='Défini' )
	boxDef = layout.box()
	colDef = boxDef.column()
	for xml_file, no in xml_files:
		for anim in xml_file.anims:
			if anim.name == obj.name:
				colDef.label( text=xml_file.name.partition('Aircraft')[2][1:] )
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
	bpy.utils.register_class(ANIM_PT_armature)
#--------------------------------------------------------------------------------------------------------------------------------

def unregister():
	bpy.utils.unregister_class(ANIM_PT_armature)


