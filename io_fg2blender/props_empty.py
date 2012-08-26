# ##### BEGIN GPL LICENSE bLock_update #####
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
# ##### END GPL LICENSE bLock_update #####
#
#
# Script copyright (C) René Nègre
# Contributors: 
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									PROPS_EMPTY.PY
#
#----------------------------------------------------------------------------------------------------------------------------------


import bpy


jsb_items = [	('None',			'None', ''),
				('TAIL_GEAR',		'TAIL_GEAR', ''),
				('RIGHT_GEAR',		'RIGHT_GEAR', ''),
				('LEFT_GEAR',		'LEFT_GEAR', ''),
				('CG',				'CG', ''),
				('AERO_CENTER',		'AERO_CENTER', ''),
				('ENGINE',			'ENGINE', ''),
				('NOSE_CONTACT',	'NOSE_CONTACT', ''),
				('RIGHT_CONTACT',	'RIGHT_CONTACT', ''),
				('LEFT_CONTACT',	'LEFT_CONTACT', ''),
				('TAIL_CONTACT',	'TAIL_CONTACT', '')
			]
			
bLock_update = False
#----------------------------------------------------------------------------------------------------------------------------------

class FG_PROP_empty(bpy.types.PropertyGroup):
	#----------------------------------------------------------------------------------------------------------------------------------

	def update_jsb_attr( self, context ):
		obj = context.active_object
		print( 'update_jsb_attr "%s"' % obj.name )
		obj.name = "" + obj.fg.jsb_attr
		obj.show_name = True
		return None	
	#----------------------------------------------------------------------------------------------------------------------------------

	def update_xml_file( self, context ):
		global bLock_update
		obj = context.active_object
		print( 'update_xml_file "%s"  %s' % (obj.name, str(bLock_update))  )
		if bLock_update == True:
			return None
			
		bLock_update = True

		active_object = context.active_object
		xml_file = "" + active_object.fg.jsb_xml_file
		for obj in context.selected_objects:
			if obj.name == active_object.name:
				continue
			if obj.type != 'EMPTY':
				continue
			print( "\t%s" % obj.name )
			obj.fg.jsb_xml_file = "" + xml_file
			
		bLock_update = False
		return None	
	#----------------------------------------------------------------------------------------------------------------------------------


	jsb_xml_file = bpy.props.StringProperty(	attr = 'jsb_xml_file', name = 'Filename', update = update_xml_file)
	#jsb_xml_file = bpy.props.StringProperty(	attr = 'jsb_xml_file', name = 'Filename' )
	jsb_attr	 = bpy.props.EnumProperty(	attr = 'jsb_attr', name = 'Attribute', items = jsb_items, default = 'None', update = update_jsb_attr )
#----------------------------------------------------------------------------------------------------------------------------------

def RNA_empty():
	bpy.types.Object.fg = bpy.props.PointerProperty(	attr="jsb_xml_file", type=FG_PROP_empty, name="jsb_xml_file", description="File .xml")
	bpy.types.Object.fg = bpy.props.PointerProperty(	attr="jsb_attr", type=FG_PROP_empty, name="Attribute", description="JsbSim attribute")
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

#def removeProjectRNA():
	# complex classes, depending on basic classes
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class( FG_PROP_empty )
	RNA_empty()

def unregister():
	bpy.utils.unregister_class( FG_PROP_empty )
	#removeProjectRNA()
#----------------------------------------------------------------------------------------------------------------------------------

