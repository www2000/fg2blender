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
#									OPS_XML.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy
import xml.dom.minidom
import os

from . import *

from mathutils import Euler
from bpy.props import StringProperty
#--------------------------------------------------------------------------------------------------------------------------------

def debug_info(aff):
	from .. import debug_ops_xml

	if debug_ops_xml:
		print(aff)
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_copy_xml_file(bpy.types.Operator):
	'''Assign XML filename from active object to selected objects'''
	bl_idname = "view3d.copy_xml_file"
	bl_label = "Copy XML filename"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object == None:
			return False
		return context.scene.objects.active.type == 'ARMATURE'
		#return True

	def execute(self, context):
		from ..xml import xml_manager

		debug_info( 'bpy.ops.view3d.copy_xml_file()' )
		active_obj = context.scene.objects.active
		xml_file = active_obj.data.fg.xml_file
		xml_file_no = active_obj.data.fg.xml_file_no
		for obj in context.selected_objects:
			if obj == active_obj:
				continue
			if obj.type != 'ARMATURE':
				continue
			obj.data.fg.xml_file = xml_file
			obj.data.fg.xml_file_no = xml_file_no
			debug_info( '\tObject "%s"' % obj.name )
			
			if active_obj.delta_location != obj.delta_location:
				debug_info( "\t\tChange delta_location" )
				obj.location = obj.location - active_obj.delta_location
				obj.delta_location = obj.delta_location + active_obj.delta_location
			if active_obj.delta_rotation_euler != obj.delta_rotation_euler:
				debug_info( "\t\tChange delta_rotation_euler" )
				eul_0 = obj.rotation_euler
				eul_1 = active_obj.delta_rotation_euler
				obj.rotation_euler = Euler( (eul_0.x-eul_1.x, eul_0.y-eul_1.y, eul_0.z-eul_1.z) )

				eul_0 = obj.delta_rotation_euler
				obj.delta_rotation_euler = Euler( (eul_0.x+eul_1.x, eul_0.y+eul_1.y, eul_0.z+eul_1.z) )
				#obj.delta_rotation_euler = obj.delta_rotation_euler + active_obj.delta_rotation_euler
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_select_file_xml(bpy.types.Operator):
	bl_idname = "object.file_select_xml"
	bl_label = ""

	#filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	filepath = bpy.props.StringProperty()
	filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})
	

	def execute(self, context):
		obj = context.active_object

		if obj.type == 'ARMATURE':
			obj.data.fg.xml_file = self.filepath
		if obj.type == 'CAMERA':
			obj.data.fg.xml_file = self.filepath
		
		#context.window_manager.fileselect_add(self)
		return {'FINISHED'}

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		debug_info( self.filepath )
		#return {'FINISHED'}
		return {'RUNNING_MODAL'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_select_file_jsb(bpy.types.Operator):
	bl_idname = "object.file_select_jsb"
	bl_label = ""

	#filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	filepath = bpy.props.StringProperty()
	filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})
	

	def execute(self, context):
		obj = context.active_object

		if obj.type == 'EMPTY':
			obj.fg.jsb_xml_file = self.filepath
		
		return {'FINISHED'}

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		debug_info( self.filepath )
		#return {'FINISHED'}
		return {'RUNNING_MODAL'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_write_xml(bpy.types.Operator):
	bl_idname = "view3d.write_xml"
	bl_label = "Write File"
	
	obj_name = bpy.props.StringProperty()
	
	#---------------------------------------------------------------------------
	def exist_in_text_editor(self, name ):
		for text in bpy.data.texts:
			if text.name == name:
				return True
		return False
	#---------------------------------------------------------------------------

	def creer_xml(self, filename):
		from ..xml import xml_manager

		new_filename = ""
		new_no = 0
		for xml_file, no in xml_manager.xml_files:
			if xml_file.name == filename:
				new_filename = filename
				new_no		 = no
				break;
		
		if new_filename == "":
			no = len(xml_manager.xml_files)
			xml_file = xml_manager.XML_FILE()
			new_filename = filename
			new_no		 = no
			xml_manager.add_xml_file( new_filename, new_no )

		obj = bpy.data.objects[self.obj_name]
		obj.data.fg.xml_file	= new_filename
		obj.data.fg.xml_file_no	= new_no
	#---------------------------------------------------------------------------

	def charge_xml(self, context, filename, no):
		from ..xml.xml_import import charge_xml
		from ..xml import xml_export
		from ..xml import xml_import

		debug_info( 'charge_xml "%s"' % filename )
		name = os.path.basename( filename )
		script_name = name
		
		if self.exist_in_text_editor( script_name ):
			bpy.data.texts[script_name].clear()
		else:
			bpy.data.texts.new( script_name )
	
		node = None
		obj = bpy.data.objects[self.obj_name]
		if obj.data.fg.bIncDiskFile:
			node = xml_import.charge_xml( filename )

		if node == None:
			node = xml.dom.minidom.Document()
			prop_list = node.createElement( 'PropertyList' )
			node.appendChild( prop_list )

		xml_export.write_animation_all( context, node, filename, no )
		bpy.data.texts[script_name].use_tabs_as_spaces = True
		bpy.data.texts[script_name].filepath = filename
		bpy.data.texts[script_name].write( node.toprettyxml() )
		
		debug_info( 'Filename "%s"' % filename )
		from ..props import props_armature
		if obj.data.fg.bWriteDisc:
			obj = bpy.data.objects[self.obj_name]
			f = open(filename, 'w')
			for line in bpy.data.texts[script_name].lines:
				debug_info( line.body )
				f.write( line.body )
				f.write( props_armature.endline() + '\n' )
			f.close()
		#bpy.data.texts[name].write( node.toxml() )
	#---------------------------------------------------------------------------
	def execute( self, context ):
		if self.filename != "":
			debug_info( self.filename )
			self.charge_xml( self.filename )
		return {'FINISHED'}

	#---------------------------------------------------------------------------

	def invoke(self, context, event):
		from ..xml import xml_manager
		
		debug_info( 'Save xml_file "%s"' % self.obj_name )
		obj = bpy.data.objects[self.obj_name]
		if obj.type == 'CAMERA':
			from ..xml import xml_camera
			filename = obj.data.fg.xml_file
			filename = bpy.path.abspath( filename )
			xml_camera.write_camera( context, filename )
			return {'FINISHED'}
		
		
		filename = obj.data.fg.xml_file
		filename = bpy.path.abspath(filename)
		no		 = obj.data.fg.xml_file_no
		debug_info( ' file = "%s"' % filename )
		#filename = self.filename
		if filename == "":
			bpy.ops.view3d.popup('INVOKE_DEFAULT', message="ERR003")
			return {'FINISHED'}
		
		if filename.find('Aircraft')!=-1:
			name_path = filename
		else:
			if not xml_manager.exist_xml_file( filename, no ):
				self.creer_xml( filename )
			name_path	= filename 
			no			= obj.data.fg.xml_file_no
		self.charge_xml( context, name_path, no )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_write_jsb(bpy.types.Operator):
	bl_idname = "view3d.write_jsb"
	bl_label = "Write File"
	
	#filename = bpy.props.StringProperty()
	obj_name = bpy.props.StringProperty()
	#objet = None
	
	#---------------------------------------------------------------------------
	def execute( self, context ):
		if self.filename != "":
			debug_info( self.filename )
			self.charge_xml( self.filename )
		return {'FINISHED'}

	#---------------------------------------------------------------------------

	def invoke(self, context, event):
		filename = bpy.data.objects[self.obj_name].fg.jsb_xml_file 
		filename = bpy.path.abspath( filename )
		debug_info( 'Save JSBsim "%s"' % filename )
		from ..xml import xml_jsbsim
		xml_jsbsim.write_jsbsim( context, filename )
		return {'FINISHED'}

#----------------------------------------------------------------------------------------------------------------------------------
#
#				REGISTER
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class( FG_OT_copy_xml_file)
	bpy.utils.register_class( FG_OT_select_file_xml )
	bpy.utils.register_class( FG_OT_select_file_jsb )
	bpy.utils.register_class( FG_OT_write_xml )
	bpy.utils.register_class( FG_OT_write_jsb )
	
def unregister():
	bpy.utils.unregister_class( FG_OT_copy_xml_file)
	bpy.utils.unregister_class( FG_OT_select_file_xml )
	bpy.utils.unregister_class( FG_OT_select_file_jsb )
	bpy.utils.unregister_class( FG_OT_write_xml )
	bpy.utils.unregister_class( FG_OT_write_jsb )

