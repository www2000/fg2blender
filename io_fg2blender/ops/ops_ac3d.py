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
# Contributors: Alexis Laillé, Clément de l'Hamaide
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									OPS_AC3D.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy
import os

from . import *
from bpy.props import StringProperty

#--------------------------------------------------------------------------------------------------------------------------------
def debug_info(aff):
	from .. import debug_ops_ac3d

	if debug_ops_ac3d:
		print(aff)
#--------------------------------------------------------------------------------------------------------------------------------

class FG_OT_copy_ac_file(bpy.types.Operator):
	'''Assign AC3D filename from active object to selected objects'''
	bl_idname = "view3d.copy_ac_file"
	bl_label = "Copy AC3D filename"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		#if context.active_object == None:
		if context.scene.objects.active.type == 'MESH':
			if context.scene.objects.active.data.fg.ac_file != '':
				if len(context.selected_objects) > 1:
					return True
				else:
					return False
			else:
				return False
		else:
			return False
		#return context.scene.objects.active.type == 'MESH'
		#return True

	def execute(self, context):
		from ..xml import xml_manager

		debug_info( 'bpy.ops.view3d.copy_ac_file()' )
		active_obj = context.scene.objects.active
		ac_file = active_obj.data.fg.ac_file
		for obj in context.selected_objects:
			if obj == active_obj:
				continue
			if obj.type != 'MESH':
				continue
			obj.data.fg.ac_file = ac_file
			debug_info( '\tObject "%s"' % obj.name )
			
				#obj.delta_rotation_euler = obj.delta_rotation_euler + active_obj.delta_rotation_euler
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_select_file_ac(bpy.types.Operator):
	bl_idname = "object.file_select_ac"
	bl_label = ""

	#filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	filepath = bpy.props.StringProperty()
	filter_glob = StringProperty(default="*.ac", options={'HIDDEN'})
	

	def execute(self, context):
		obj = context.active_object

		if obj.type == 'MESH':
			obj.data.fg.ac_file = self.filepath
		
		#context.window_manager.fileselect_add(self)
		return {'FINISHED'}

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		debug_info( self.filepath )
		#return {'FINISHED'}
		return {'RUNNING_MODAL'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_copy_name_bl2ac(bpy.types.Operator):
	'''Copy object name to Mesh Name for selected objects'''
	bl_idname = "view3d.copy_name_bl2ac"					# sera appelé par bpy.ops.view3d.exemple()
	bl_label = "Copy object name in Mesh Name"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		for obj in context.selected_objects:
			if obj.type == 'MESH':
				return True

	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		current_obj = context.scene.objects.active

		for obj in context.selected_objects:
			if obj.type != 'MESH':
				continue
			bpy.context.scene.objects.active = obj
			obj.data.fg.name_ac = "" + obj.name

		context.scene.objects.active = current_obj
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_save_ac_file(bpy.types.Operator):
	'''Save AC3D file (create it automatically if not exit)'''
	bl_idname = "view3d.save_ac_file"					# sera appelé par bpy.ops.view3d.exemple()
	bl_label = "Save ac file "
	bl_options = {'REGISTER', 'UNDO'}

	object_name = bpy.props.StringProperty()

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		from ..meshes.ac3d import ac_export
		#-----------------------------------------------------------------------------------------------------

		def set_ac_file( ac_filename ):
			filename = os.path.basename(ac_filename)
			for obj in bpy.data.objects:
				if obj.type != 'MESH':
					continue
				for group in obj.users_group:
					if group.name == filename:
						if obj.data.fg.ac_file == '':
							obj.data.fg.ac_file = "" + group.name
		#-----------------------------------------------------------------------------------------------------

		def clear_parent( list_objects ):
			for obj in bpy.data.objects:
				obj.select = False
			for obj in list_objects:
				obj.select = True
			bpy.ops.view3d.save_parent()
		#-----------------------------------------------------------------------------------------------------

		def restore_parent( list_objects ):
			for obj in bpy.data.objects:
				obj.select = False
			for obj in list_objects:
				obj.select = True
			bpy.ops.view3d.restore_parent()
		#-----------------------------------------------------------------------------------------------------

		active_object = bpy.data.objects[self.object_name]
		
		group_name = ''		
		for group in bpy.data.objects[self.object_name].users_group:
			debug_info( str(group) )
			if group.name.find('.ac') != -1:
				group_name = group.name
			else:
				print( "Can't export to AC3D : object %s is not in a group" %bpy.data.objects[self.object_name].name )
			debug_info( group_name )
			set_ac_file( group_name )
		
		#if active_object.data.fg.ac_file == "":
		if group_name == "":
			return {'FINISHED'}
		else:
			if group_name == active_object.data.fg.ac_file:
				filename = bpy.path.abspath('//') + group_name
			else:
				filename = active_object.data.fg.ac_file
				filename = bpy.path.abspath(filename)
				
			
			
			
		debug_info( bpy.data.objects[self.object_name].data.fg.ac_file )
		debug_info( bpy.path.abspath('//') )
		debug_info( 'Group name "%s"' % group_name )
		debug_info( 'Filename "%s"' % filename )
		
		list_objects = []
		for obj in bpy.data.objects:
			for group in obj.users_group:
				if group.name == group_name:
					list_objects.append(obj)

		for obj in list_objects:
			debug_info( obj.name )
			print( obj.name )
			
		#clear_parent( list_objects )
		from ..xml import xml_import
		ac_export.write_ac_file( context, xml_import.conversion(filename), list_objects, True, False, True )
		#restore_parent( list_objects )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------
#
#				REGISTER
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class( FG_OT_copy_ac_file)
	bpy.utils.register_class( FG_OT_select_file_ac )
	bpy.utils.register_class( FG_OT_copy_name_bl2ac )
	bpy.utils.register_class( FG_OT_save_ac_file )
	
def unregister():
	bpy.utils.unregister_class( FG_OT_copy_ac_file)
	bpy.utils.unregister_class( FG_OT_select_file_ac )
	bpy.utils.unregister_class( FG_OT_copy_name_bl2ac )
	bpy.utils.unregister_class( FG_OT_save_ac_file )
	
