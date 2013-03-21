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
import os




bLock_update = False

DEBUG = False

#----------------------------------------------------------------------------------------------------------------------------------

def debug_info( aff):
	global DEBUG
	if DEBUG:
		print( aff )
#----------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------

class FG_PROP_mesh(bpy.types.PropertyGroup):
	#----------------------------------------------------------------------------------------------------------------------------------

	def update_ac_file( self, context ):
		#------------------------------------------------------------------------------------------------------------------------------
		def isGroupExist( groupName ):
			groupName = os.path.basename(groupName)
			print( "Test si le group : %s existe ??" % groupName )
			for group in bpy.data.groups:
				if group.name == groupName:
					print( "Existe")
					return True
			print( "N'Existe pas")
			return False
		#------------------------------------------------------------------------------------------------------------------------------
		def createGroup( groupName ):
			groupName = os.path.basename(groupName)
			bpy.ops.group.create( name = groupName )
			print( "Creation du group : %s" % groupName )
		#------------------------------------------------------------------------------------------------------------------------------
		global bLock_update
		from .. import fg2bl

		if bLock_update == True:
			return None

		active_object = context.active_object
		if active_object  == None:
			return None
		if active_object.type != 'MESH':
			return None

		debug_info( 'update_ac_file "%s"  %s' % (active_object.name, str(bLock_update))  )
			
		bLock_update = True

		ac_file = "" + active_object.data.fg.ac_file
		ac_file = bpy.path.abspath( ac_file )
		ac_file = fg2bl.path.compute_path( ac_file )
		
		if not isGroupExist(ac_file):
			createGroup(ac_file)
		
		active_object.data.fg.ac_file = ac_file
		
		for obj in context.selected_objects:
			if obj.name == active_object.name:
				continue
			if obj.type != 'MESH':
				continue
			debug_info( "\t%s" % obj.name )
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

