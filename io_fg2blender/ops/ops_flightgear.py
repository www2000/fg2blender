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
#									OPS_FLIGHTGEAR.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy

from . import *

from bpy.props import StringProperty

#--------------------------------------------------------------------------------------------------------------------------------

STACK_SAVE_PARENT = []

#--------------------------------------------------------------------------------------------------------------------------------
class SAVE_PARENT:
	def __init__(self):
		self.object_name			= ""
		self.parent_name			= ""

#--------------------------------------------------------------------------------------------------------------------------------

def debug_info(aff):
	from .. import debug_ops_flightgear

	if debug_ops_flightgear:
		print(aff)
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_freeze_armature(bpy.types.Operator):
	'''Freeze selected armatures'''
	bl_idname = "view3d.freeze_armature"
	bl_label = "Freeze an armature"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object == None:
			return False
		return context.scene.objects.active.type == 'ARMATURE'

	def execute(self, context):
		from ..xml import xml_export

		debug_info( 'bpy.ops.view3d.freeze_armature()' )
		obj = context.scene.objects.active
		current_frame = context.scene.frame_current
		armature = obj#obj.data

		if armature.animation_data != None:
			for armature in context.selected_objects:
				if armature.type != 'ARMATURE':
					continue

				if len(armature.data.fg.keyframes) != 0:
					#debug_info( '\tFreeze exist on "%s"' % armature.name )
					#bpy.ops.view3d.popup('INVOKE_DEFAULT', message="ERR005")
					continue
					#return {'FINISHED'}
		
				value = 0.0

				if armature.animation_data != None:
					yFcurve = None
					n = 0
					for fcurve in armature.animation_data.action.fcurves:
						if armature.data.fg.type_anim in [1,7]:
							if fcurve.data_path.find( "euler" ) != -1:
								n = n + 1
							if n == 2:
								yFcurve = fcurve
								value = xml_export.compute_rotation_angle_current( armature )
						elif armature.data.fg.type_anim in [2]:
							if fcurve.data_path.find( "location" ) != -1:
								n = n + 1
							if n == 2:
								yFcurve = fcurve
								value = xml_export.compute_translation_current( armature )
						else:
							continue
			
					if yFcurve == None:
						continue
						#return {'FINISHED'}

					for point in yFcurve.keyframe_points:
						key = armature.data.fg.keyframes.add()
						key.x = 0.0 + point.co.x
						key.y = 0.0 + point.co.y
						point.co.y = value

			
				context.scene.frame_current = current_frame
				debug_info( '\tFreeze armature : "%s"' % ( obj.name ) )
		else:
			bpy.ops.view3d.popup('INVOKE_DEFAULT', message="ERR006")
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_unfreeze_armature(bpy.types.Operator):
	'''Unfreeze selected armatures'''
	bl_idname = "view3d.unfreeze_armature"
	bl_label = "Unfreeze selected armatures"
	bl_options = {'REGISTER', 'UNDO'}

	object_name = bpy.props.StringProperty()

	#-----------------------------------------------------------------------------------------------------------------------------
	@classmethod
	def poll(cls, context):
		for armature in bpy.data.armatures:
			if len(armature.fg.keyframes) != 0:
				return True
		return False

	#-----------------------------------------------------------------------------------------------------------------------------
	def execute(self, context):
		#-------------------------------------------------------------------------------------------------------------------------
		def unfreeze_armature( armature ):
			n = 0
			if armature.animation_data != None:
				yFcurve = None			
				for fcurve in armature.animation_data.action.fcurves:
					if armature.data.fg.type_anim in [1,7]:
						if fcurve.data_path.find( "euler" ) != -1:
							n = n + 1
						if n == 2:
							yFcurve = fcurve
					elif armature.data.fg.type_anim in [2]:
						if fcurve.data_path.find( "location" ) != -1:
							n = n + 1
						if n == 2:
							yFcurve = fcurve
					else:
						continue
			
				if yFcurve == None:
					return
								
				#for i in range(len(yFcurve.keyframe_points)):
				#	yFcurve.keyframe_points.remove(0)
				
				for i,point in enumerate(yFcurve.keyframe_points):
					point.co.x = armature.data.fg.keyframes[i].x
					point.co.y = armature.data.fg.keyframes[i].y

				for point in yFcurve.keyframe_points:
					armature.data.fg.keyframes.remove(0)
				

		#-------------------------------------------------------------------------------------------------------------------------

		debug_info( 'bpy.ops.view3d.unfreeze_armature()' )
		#obj = context.scene.objects.active
		current_frame = context.scene.frame_current

		if self.object_name == "All":
			for obj in bpy.data.objects:
				if obj.type != 'ARMATURE':
					continue
				if len(obj.data.fg.keyframes) != 0:
					unfreeze_armature(obj)			
		else:
			unfreeze_armature(bpy.data.objects[self.object_name])			
		
		context.scene.frame_current = current_frame		
		#debug_info( '\tUnfreeze armature : "%s"' % ( obj.name ) )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_select_by_file(bpy.types.Operator):
	'''Select by file'''
	bl_idname = "view3d.select_by_file"
	bl_label = "Unfreeze selected armatures"
	bl_options = {'REGISTER', 'UNDO'}

	filename = bpy.props.StringProperty()

	#-----------------------------------------------------------------------------------------------------------------------------
	def execute(self, context):
		debug_info( 'bpy.ops.view3d.select_by_file()' )
		for obj in bpy.data.objects:
			if obj.type == 'ARMATURE' and obj.data.fg.xml_file == self.filename:
				obj.select = True
			elif obj.type == 'MESH' and obj.data.fg.ac_file == self.filename:
				obj.select = True

		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_save_keyframe(bpy.types.Operator):
	'''???????????'''
	bl_idname = "view3d.save_keyframe"
	bl_label = "Save animation keyframe"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object == None:
			return False
		return context.scene.objects.active.type == 'ARMATURE'

	def execute(self, context):
		from ..xml import xml_export

		debug_info( 'bpy.ops.view3d.freeze_armature()' )
		obj = context.scene.objects.active
		current_frame = context.scene.frame_current
		armature = obj#obj.data

		if armature.animation_data != None:
			for armature in context.selected_objects:
				if armature.type != 'ARMATURE':
					continue

				if len(armature.data.fg.keyframes) != 0:
					#debug_info( '\tFreeze exist on "%s"' % armature.name )
					#bpy.ops.view3d.popup('INVOKE_DEFAULT', message="ERR005")
					continue
					#return {'FINISHED'}
		
				value = 0.0

				if armature.animation_data != None:
					yFcurve = None
					n = 0
					for fcurve in armature.animation_data.action.fcurves:
						if armature.data.fg.type_anim in [1,7]:
							if fcurve.data_path.find( "euler" ) != -1:
								n = n + 1
							if n == 2:
								yFcurve = fcurve
						elif armature.data.fg.type_anim in [2]:
							if fcurve.data_path.find( "location" ) != -1:
								n = n + 1
							if n == 2:
								yFcurve = fcurve
						else:
							continue
			
					if yFcurve == None:
						continue
						#return {'FINISHED'}

					for point in yFcurve.keyframe_points:
						key = armature.data.fg.keyframes.add()
						key.x = 0.0 + point.co.x
						key.y = 0.0 + point.co.y
						point.co.y = value

			
				context.scene.frame_current = current_frame
				debug_info( '\tFreeze armature : "%s"' % ( obj.name ) )
		else:
			bpy.ops.view3d.popup('INVOKE_DEFAULT', message="ERR006")
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_save_parent(bpy.types.Operator):
	'''?????????'''
	bl_idname = "view3d.save_parent"
	bl_label = "Save parent"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object == None:
			return False
		return context.scene.objects.active.type in ('MESH','ARMATURE','EMPTY')

	def execute(self, context):
		from ..xml import xml_manager
		global STACK_SAVE_PARENT

		debug_info( 'bpy.ops.view3d.save_parent()' )
		obj = context.scene.objects.active
		
		list_objects = context.selected_objects
		for obj in list_objects:
			obj.select = False
		
		
		for obj in list_objects:
			if not obj.type in ('MESH','ARMATURE','EMPTY'):
				continue

			for sp in STACK_SAVE_PARENT:
				if sp.object_name == obj.name:
					debug_info( '\tSave exist on "%s"' % obj.name )
					continue
		
			save_parent = SAVE_PARENT()
			save_parent.object_name = obj.name
			if obj.parent != None:
				save_parent.parent_name = obj.parent.name
			else:
				save_parent.parent_name = ''
				
			obj.select = True
			context.scene.objects.active = obj
			bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
			#bpy.ops.object.parent_clear(type='CLEAR')
			obj.select = False
			#obj.parent = None
		
			STACK_SAVE_PARENT.append( save_parent )		
			debug_info( '\tSave for "%s" parent "%s"' % ( obj.name, save_parent.parent_name ) )

		for obj in list_objects:
			obj.select = True
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_restore_parent(bpy.types.Operator):
	'''????????'''
	bl_idname = "view3d.restore_parent"
	bl_label = "Restore parent"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object == None:
			return False
		return context.scene.objects.active.type in ('MESH','ARMATURE','EMPTY')

	def execute(self, context):
		from ..xml import xml_manager
		global STACK_SAVE_PARENT

		debug_info( 'bpy.ops.view3d.restore_parent()' )
		obj = context.scene.objects.active
		for obj in context.selected_objects:
			if not obj.type in ('MESH','ARMATURE','EMPTY'):
				continue
			
			save_parent = None		
			for sp in STACK_SAVE_PARENT:
				if sp.object_name == obj.name:
					save_parent = sp
				
			if save_parent == None:
				debug_info( '\tRestore "%s" : had not save' % obj.name )
				continue

			if save_parent.parent_name != '':
				obj.parent = bpy.data.objects[save_parent.parent_name]
				if obj.parent.type == 'ARMATURE':
					obj.parent_bone = 'Bone'
					obj.parent_type = 'BONE'
		
			debug_info( '\tRestore "%s" parent "%s"' % ( obj.name, save_parent.parent_name ) )
			STACK_SAVE_PARENT.remove( save_parent )		
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_copy_property(bpy.types.Operator):
	'''Assign FG property from active object to selected objects'''
	bl_idname = "view3d.copy_property"
	bl_label = "Copy FG property"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object == None:
			return False
		return context.scene.objects.active.type == 'ARMATURE'
		#return True

	def execute(self, context):
		from ..xml import xml_manager

		debug_info( 'bpy.ops.view3d.copy_property()' )

		active_obj = context.scene.objects.active
		debug_info( "Copy de %s" % active_obj.data.fg.property_value )
		family			= active_obj.data.fg.family
		family_value	= active_obj.data.fg.family_value
		property_value	= active_obj.data.fg.property_value
		property_idx	= active_obj.data.fg.property_idx
		factor			= active_obj.data.fg.factor
		factor_ini		= active_obj.data.fg.factor_ini
		range_beg		= active_obj.data.fg.range_beg
		range_end		= active_obj.data.fg.range_end
		range_beg_ini	= active_obj.data.fg.range_beg_ini
		range_end_ini	= active_obj.data.fg.range_end_ini
		time			= active_obj.data.fg.time
		time_ini		= active_obj.data.fg.time_ini
		debug_info( '\tActive object : "%s"' % active_obj.name )
		debug_info( '\tValue : "%s"' % str(property_value) )

		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				continue
			debug_info( '\t\tOn object "%s"' % obj.name )
			obj.data.fg.family			= family
			obj.data.fg.family_value	= family_value
			obj.data.fg.property_value	= property_value
			obj.data.fg.property_idx	= property_idx
			obj.data.fg.factor			= factor
			obj.data.fg.factor_ini		= factor_ini
			obj.data.fg.range_beg		= range_beg
			obj.data.fg.range_end		= range_end
			obj.data.fg.range_beg_ini	= range_beg_ini
			obj.data.fg.range_end_ini	= range_end_ini
			obj.data.fg.time			= time
			obj.data.fg.time_ini		= time_ini
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_select_property(bpy.types.Operator):
	'''Select all objects with same property than active object'''
	bl_idname = "view3d.select_property"
	bl_label = "Select property"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type in( 'MESH','ARMATURE')

	def execute(self, context):
		import bpy
		import mathutils
		#-------------------------------------------------------------------
		def select_childs( parent ):
			for obj in bpy.data.objects:
				if not obj.parent:
					continue
				if obj.parent.name == parent.name:
					o = obj
					o.select=True
					select_childs( o )
		#-------------------------------------------------------------------
		def find_armature( obj ):
			o = obj
			while o.parent:
				if o.parent.type == 'ARMATURE':
					return o.parent
				o = o.parent
			return None
		#-------------------------------------------------------------------
		debug_info( '--- Select property  ---' )
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				obj = find_armature( obj )
				if not obj:
					continue
			if obj.type != 'ARMATURE':
				continue
			property_name =  obj.data.fg.property_value
			debug_info( property_name )
			for o in bpy.data.objects:
				if o.type == 'ARMATURE':
					if o.data.fg.property_value == property_name:
						
						select_childs( o )
						o.select = True
				
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_show_animation(bpy.types.Operator):
	'''Show all objects with the same property and hide other'''
	bl_idname = "view3d.show_animation"
	bl_label = "Show animated objects"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type in( 'MESH','ARMATURE')

	def execute(self, context):
		import bpy
		import mathutils
		bpy.ops.view3d.select_property()
		bpy.ops.object.select_all(action='INVERT')
		bpy.ops.object.hide_view_set(unselected=False)
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_show_all(bpy.types.Operator):
	'''Show all objects'''
	bl_idname = "view3d.show_all"
	bl_label = "Show all objects"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type in( 'MESH','ARMATURE')

	def execute(self, context):
		import bpy
		import mathutils
		bpy.ops.object.hide_view_clear()
		bpy.ops.object.select_all(action='INVERT')
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_insertion_keyframe_rotate(bpy.types.Operator):
	'''Insert keyframe rotate with linear interpolation '''
	bl_idname = "view3d.insert_keyframe_rotate"
	bl_label = "Insert keyframe rotate"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.mode != 'POSE':
			return False
		if context.active_object == None:
			return False
		if context.active_object.type != 'ARMATURE':
			return False
		if context.active_object.data.fg.type_anim != 1:
			return False
		return True

	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		active_obj = context.active_object
		bpy.ops.anim.keyframe_insert_menu( type='Rotation', confirm_success=False, always_prompt=False )

		for fcurve in active_obj.animation_data.action.fcurves:
			for keyframe in fcurve.keyframe_points:
				keyframe.interpolation = 'LINEAR'
		
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_insertion_keyframe_translate(bpy.types.Operator):
	'''Insert keyframe rotate with linear interpolation '''
	bl_idname = "view3d.insert_keyframe_translate"
	bl_label = "Insert keyframe rotate"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.mode != 'POSE':
			return False
		if context.active_object == None:
			return False
		if context.active_object.type != 'ARMATURE':
			return False
		if context.active_object.data.fg.type_anim != 2:
			return False
		return True

	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		active_obj = context.active_object
		bpy.ops.anim.keyframe_insert_menu( type='Location', confirm_success=False, always_prompt=False )

		for fcurve in active_obj.animation_data.action.fcurves:
			for keyframe in fcurve.keyframe_points:
				keyframe.interpolation = 'LINEAR'
		
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_select_by_property(bpy.types.Operator):
	'''Select all armatures with same flightgear property'''
	bl_idname = "view3d.select_by_property"					
	bl_label = "Select all armatures with same flightgear property"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		for obj in bpy.context.selected_objects:
		    return obj.type == 'ARMATURE'

	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		from ..xml import xml_export
		active_object = context.active_object
		if active_object and active_object.type == 'ARMATURE':
			property_value = xml_export.build_property_name( active_object )
			
			for obj in bpy.data.objects:
				if obj.type != 'ARMATURE':
					continue
				if xml_export.build_property_name(obj) == property_value:
					debug_info( "%s : %s == %s" % (obj.name, xml_export.build_property_name(obj),property_value) )
					obj.select = True
					
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------
class FG_OT_select_object_by_armature(bpy.types.Operator):
	'''????????????'''
	bl_idname = "view3d.select_object_by_armature"					
	bl_label = "???????????"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		for obj in bpy.context.selected_objects:
		    return obj.type == 'ARMATURE'

	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		def find_son( parent_obj ):
		    for obj in bpy.data.objects:
		        if obj.parent == parent_obj:
		            if obj.type == 'MESH':
		                obj.select = True
		            find_son( obj )

		for obj in bpy.context.selected_objects:
		    if obj.type != 'ARMATURE':
		        continue
		    obj.select = False
		    find_son( obj )
		
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------
#
#				REGISTER
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class( FG_OT_freeze_armature)
	bpy.utils.register_class( FG_OT_unfreeze_armature)
	bpy.utils.register_class( FG_OT_save_keyframe)
	bpy.utils.register_class( FG_OT_save_parent)
	bpy.utils.register_class( FG_OT_restore_parent)
	bpy.utils.register_class( FG_OT_select_property)
	bpy.utils.register_class( FG_OT_copy_property)
	bpy.utils.register_class( FG_OT_show_animation )
	bpy.utils.register_class( FG_OT_show_all )
	bpy.utils.register_class( FG_OT_insertion_keyframe_rotate )
	bpy.utils.register_class( FG_OT_insertion_keyframe_translate )
	bpy.utils.register_class( FG_OT_select_by_property )
	bpy.utils.register_class( FG_OT_select_object_by_armature )
	bpy.utils.register_class( FG_OT_select_by_file )

def unregister():
	bpy.utils.unregister_class( FG_OT_freeze_armature)
	bpy.utils.unregister_class( FG_OT_unfreeze_armature)
	bpy.utils.unregister_class( FG_OT_save_keyframe)
	bpy.utils.unregister_class( FG_OT_save_parent)
	bpy.utils.unregister_class( FG_OT_restore_parent)
	bpy.utils.unregister_class( FG_OT_select_property)
	bpy.utils.unregister_class( FG_OT_copy_property)
	bpy.utils.unregister_class( FG_OT_show_animation )
	bpy.utils.unregister_class( FG_OT_show_all )
	bpy.utils.unregister_class( FG_OT_insertion_keyframe_rotate )
	bpy.utils.unregister_class( FG_OT_insertion_keyframe_translate )
	bpy.utils.unregister_class( FG_OT_select_by_property )
	bpy.utils.unregister_class( FG_OT_select_object_by_armature )
	bpy.utils.unregister_class( FG_OT_select_by_file )

