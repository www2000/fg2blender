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


camera_items = [	('None',			'None', ''),
					('COCKPIT_VIEW',	'COCKPIT_VIEW', '')
			]
#----------------------------------------------------------------------------------------------------------------------------------

class FG_PROP_camera(bpy.types.PropertyGroup):
	#----------------------------------------------------------------------------------------------------------------------------------

	def update_type_view( self, context ):
		obj = context.active_object
		print( obj.name )
		obj.name = "" + obj.data.fg.type_view
		obj.show_name = True
		return None	
	#----------------------------------------------------------------------------------------------------------------------------------
	xml_file	= bpy.props.StringProperty(	attr = 'xml_file', name = 'Filename' )
	type_view	= bpy.props.EnumProperty(	attr = 'type_view', name = 'Attribute', items = camera_items, default = 'None', update = update_type_view )
#----------------------------------------------------------------------------------------------------------------------------------

def RNA_camera():
	bpy.types.Camera.fg = bpy.props.PointerProperty(	attr="xml_file", type=FG_PROP_camera, name="xml_file", description="File .xml")
	bpy.types.Camera.fg = bpy.props.PointerProperty(	attr="type_view", type=FG_PROP_camera, name="type_view", description="Name of view")
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

