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
#									PROPS_CAMERA.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy

from ..ui.ui_lang import lang

camera_items = 	[
		('None',		'None', ''),
		('EXTRA_VIEW',		'EXTRA_VIEW', ''),
		('COCKPIT_VIEW',	'COCKPIT_VIEW', '')
		]	
		
bLock_update = False

#----------------------------------------------------------------------------------------------------------------------------------

def debug_info( aff ):
	from .. import debug_props_camera
	
	if debug_props_camera:
		print( aff )
#----------------------------------------------------------------------------------------------------------------------------------

class FG_PROP_camera(bpy.types.PropertyGroup):
	#----------------------------------------------------------------------------------------------------------------------------------

	def update_type_view( self, context ):
		from . import props_armature

		if props_armature.bLock_update == True:
			return None

		obj = context.active_object
		debug_info( obj.name )
		obj.name = "" + obj.data.fg.type_view
		obj.show_name = True
		return None	
	#----------------------------------------------------------------------------------------------------------------------------------

	def update_xml_file( self, context ):
		from . import props_armature

		if props_armature.bLock_update == True:
			return None

		obj = context.active_object
		# because when you save the .blend file 
		# path of xml_file can change whithout selection
		if obj == None or obj.type != 'CAMERA':
			return None

		debug_info( 'update_xml_file "%s"  %s' % (obj.name, str(props_armature.bLock_update))  )
		if bLock_update == True:
			return None
			
		props_armature.bLock_update = True

		active_object = context.active_object
		xml_file = "" + active_object.data.fg.xml_file
		xml_file = bpy.path.relpath( xml_file )
		active_object.data.fg.xml_file = xml_file
		for obj in context.selected_objects:
			if obj.name == active_object.name:
				continue
			if obj.type != 'CAMERA':
				continue
			debug_info( "\t%s" % obj.name )
			obj.data.fg.xml_file = "" + xml_file
			
		props_armature.bLock_update = False
		return None	
	#----------------------------------------------------------------------------------------------------------------------------------
	xml_file	= bpy.props.StringProperty(	attr = 'xml_file', name = lang['UI014'], update=update_xml_file )
	type_view	= bpy.props.EnumProperty(	attr = 'type_view', name = lang['UI016'], items = camera_items, default = 'None', update = update_type_view )
#----------------------------------------------------------------------------------------------------------------------------------

def RNA_camera():
	bpy.types.Camera.fg = bpy.props.PointerProperty(	attr="xml_file", type=FG_PROP_camera, name="xml_file", description=lang['DOC040'] )
	bpy.types.Camera.fg = bpy.props.PointerProperty(	attr="type_view", type=FG_PROP_camera, name="type_view", description=lang['DOC041'] )
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
	bpy.utils.register_class( FG_PROP_camera )
	RNA_camera()

def unregister():
	bpy.utils.unregister_class( FG_PROP_camera )
	#removeProjectRNA()
#----------------------------------------------------------------------------------------------------------------------------------

