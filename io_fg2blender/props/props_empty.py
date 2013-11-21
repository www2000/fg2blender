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
# ##### END GPL LICENSE BLOCK #####
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

from ..ui.ui_lang import lang

jsb_items = 	[
		('None',		'None', ''),
		('TAIL_GEAR',		'TAIL_GEAR', ''),
		('RIGHT_GEAR',		'RIGHT_GEAR', ''),
		('LEFT_GEAR',		'LEFT_GEAR', ''),
		('CG',			'CG', ''),
		('AERO_CENTER',		'AERO_CENTER', ''),
		('ENGINE',		'ENGINE', ''),
		('NOSE_CONTACT',	'NOSE_CONTACT', ''),
		('RIGHT_CONTACT',	'RIGHT_CONTACT', ''),
		('LEFT_CONTACT',	'LEFT_CONTACT', ''),
		('TAIL_CONTACT',	'TAIL_CONTACT', ''),
		('GUN0',	'GUN0', ''),
		('GUN1',	'GUN1', ''),
		('GUN2',	'GUN2', ''),
		('GUN3',	'GUN3', ''),
		('GUN4',	'GUN4', ''),
		('GUN5',	'GUN5', ''),
		('GUN6',	'GUN6', ''),
		('GUN7',	'GUN7', ''),
		('GUN8',	'GUN8', ''),
		('GUN9',	'GUN9', '')
		]
			
bLock_update = False
#----------------------------------------------------------------------------------------------------------------------------------

def debug_info( aff ):
	from .. import debug_props_empty
	
	if debug_props_empty:
		print( aff )

#----------------------------------------------------------------------------------------------------------------------------------

class FG_PROP_empty(bpy.types.PropertyGroup):
	#----------------------------------------------------------------------------------------------------------------------------------

	def update_jsb_attr( self, context ):
		obj = context.active_object
		debug_info( 'update_jsb_attr "%s"' % obj.name )
		obj.name = "" + obj.fg.jsb_attr
		obj.show_name = True
		return None	
	#----------------------------------------------------------------------------------------------------------------------------------

	def update_xml_file( self, context ):
		global bLock_update
		from . import props_armature

		if bLock_update == True:
			return None

		obj = context.active_object
		# because when you save the .blend file 
		# path of xml_file can change whithout selection
		if obj == None:
			return None

		debug_info( 'update_xml_file "%s"  %s' % (obj.name, str(bLock_update))  )
			
		bLock_update = True

		active_object = context.active_object
		#print( 'bpy.data.object["%s"].fg.jsb_xml_file = "%s"' %(active_object.name, active_object.fg.jsb_xml_file) )
		xml_file = "" + active_object.fg.jsb_xml_file
		if xml_file != "":
			xml_file = bpy.path.relpath( xml_file )
		active_object.fg.jsb_xml_file = xml_file
		for obj in context.selected_objects:
			if obj.name == active_object.name:
				continue
			if obj.type != 'EMPTY':
				continue
			debug_info( "\t%s" % obj.name )
			obj.fg.jsb_xml_file = "" + xml_file
			
		bLock_update = False
		return None	
	#----------------------------------------------------------------------------------------------------------------------------------


	jsb_xml_file 	= bpy.props.StringProperty(	attr = 'jsb_xml_file', name = lang['UI014'], update = update_xml_file)
	jsb_attr	= bpy.props.EnumProperty(	attr = 'jsb_attr', name = lang['UI016'], items = jsb_items, default = 'None', update = update_jsb_attr )
#----------------------------------------------------------------------------------------------------------------------------------

def RNA_empty():
	bpy.types.Object.fg = bpy.props.PointerProperty(	attr="jsb_xml_file", type=FG_PROP_empty, name="jsb_xml_file", description=lang['DOC038'])
	bpy.types.Object.fg = bpy.props.PointerProperty(	attr="jsb_attr", type=FG_PROP_empty, name="Attribute", description=lang['DOC039'])
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class( FG_PROP_empty )
	RNA_empty()
#----------------------------------------------------------------------------------------------------------------------------------

def unregister():
	bpy.utils.unregister_class( FG_PROP_empty )

