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
#									PROPS_MESHES.PY
#
#----------------------------------------------------------------------------------------------------------------------------------


import bpy
bLock_update = False

#----------------------------------------------------------------------------------------------------------------------------------

class FG_PROP_mesh(bpy.types.PropertyGroup):
	#----------------------------------------------------------------------------------------------------------------------------------

	def update_ac_file( self, context ):
		global bLock_update
		obj = context.active_object
		if obj  == None:
			return None
		if bLock_update == True:
			return None

		print( 'update_ac_file "%s"  %s' % (obj.name, str(bLock_update))  )
			
		bLock_update = True

		active_object = context.active_object
		ac_file = "" + active_object.data.fg.ac_file
		ac_file = bpy.path.relpath( ac_file )
		active_object.data.fg.ac_file = ac_file
		for obj in context.selected_objects:
			if obj.name == active_object.name:
				continue
			if obj.type != 'MESH':
				continue
			print( "\t%s" % obj.name )
			obj.data.fg.ac_file = "" + ac_file
			
		bLock_update = False
		return None	

	ac_file = bpy.props.StringProperty(	attr = 'ac_file', name = 'Filename', update=update_ac_file)
	name_ac = bpy.props.StringProperty(	attr = 'name_ac', name = 'Mesh Name')
#----------------------------------------------------------------------------------------------------------------------------------

def RNA_mesh():
	bpy.types.Mesh.fg = bpy.props.PointerProperty(	attr="ac_file", type=FG_PROP_mesh, name="ac_file", description="File .ac")
	bpy.types.Mesh.fg = bpy.props.PointerProperty(	attr="name_ac", type=FG_PROP_mesh, name="name_ac", description="name in ac file")
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
	bpy.utils.register_class( FG_PROP_mesh )
	RNA_mesh()

def unregister():
	bpy.utils.unregister_class( FG_PROP_mesh )
	#removeProjectRNA()
#----------------------------------------------------------------------------------------------------------------------------------

