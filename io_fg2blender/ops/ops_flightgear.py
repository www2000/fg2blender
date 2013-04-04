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
import xml.dom.minidom
import os


from . import *

from mathutils import Vector
from mathutils import Matrix
from mathutils import Euler

from math import radians
from math import degrees
from math import acos


from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import CollectionProperty

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

class FG_OT_create_translate(bpy.types.Operator):
	'''Add armature type translate '''
	bl_idname = "view3d.create_translate"
	bl_label = "Create Translate"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return True
		return context.active_object != None

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians

		debug_info( "Create_translate : " )
		armature = bpy.ops.object.armature_add( view_align=True )
		armature = bpy.data.armatures[-1]
		debug_info( armature.name )
		for obj in bpy.data.objects:
			if obj.type != 'ARMATURE':
				continue
			if obj.data.name == armature.name:
				break 
		if obj.type == 'ARMATURE':
			debug_info( "\tSelecion de : %s" %(obj.name) )
			#bpy.ops.object.select_pattern(pattern=obj.name)
			context.scene.objects.active = obj

			bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

			debug_info("\tActivation Pose Mode")
			bpy.ops.object.posemode_toggle()
			bpy.ops.pose.select_all( action='SELECT' )
			debug_info("\tAjout limite location")
			bpy.ops.pose.constraint_add(type='LIMIT_LOCATION')

			debug_info("\tActivation des limites en local")
			limit_translate = bpy.data.objects[obj.name].pose.bones[-1].constraints[-1]
			limit_translate.use_min_x = True
			limit_translate.use_max_x = True
			limit_translate.use_min_y = False
			limit_translate.use_max_y = False
			limit_translate.use_min_z = True
			limit_translate.use_max_z = True
			limit_translate.owner_space = 'LOCAL'
			#obj.lock_location = ( True, False, True )
			bpy.ops.object.posemode_toggle()


			obj.data.fg.type_anim		= 2
			obj.data.fg.xml_file		= ""
			obj.data.fg.xml_file_no		= 0
			obj.data.fg.family			= "custom"
			obj.data.fg.family_value	= "error"
			obj.data.fg.property_value	= ""
			obj.data.fg.property_idx	= -1
			obj.data.fg.time			= 100.0/bpy.data.scenes[0].render.fps
			obj.data.fg.time_ini		= 100.0/bpy.data.scenes[0].render.fps
			obj.data.fg.range_beg		= 0.0
			obj.data.fg.range_beg_ini	= 0.0
			obj.data.fg.range_end		= 1.0
			obj.data.fg.range_end_ini	= 1.0
			obj.data.fg.factor			= 1.0
			obj.data.fg.factor_ini		= 1.0
			obj.data.fg.offset_deg		= 0.0

			debug_info("\tDesactivation Pose Mode")
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_translate_axis(bpy.types.Operator):
	'''Add armature type translate axis '''
	bl_idname = "view3d.create_translate_axis"
	bl_label = "Create Translate axis"
	bl_options = {'REGISTER', 'UNDO'}
	
	axis = StringProperty(default="")

	@classmethod
	def poll(cls, context):
		return context.mode == 'OBJECT'

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians
		
		def create_rotate( vec ):
			debug_info( "Create_translate : " )
			bpy.ops.object.armature_add( view_align=False )
			vec = vec / 10.0
			#vec = Vector(( 0.0, 0.1, 0.0) )
			head = Vector( (0.0,0.0,0.0) )
			tail = Vector( (0.0,0.0,0.0) ) + vec
		
			bpy.ops.object.editmode_toggle()

			bpy.context.object.data.edit_bones["Bone"].head = head #Vector( (0.0,0.0,0.0) ) #self.head
			bpy.context.object.data.edit_bones["Bone"].tail = tail #self.vec /10.0

			bpy.ops.object.editmode_toggle()
		
			obj = context.active_object
			debug_info( obj.name )
			
			if obj.type == 'ARMATURE':
				debug_info( "\tSelecion de : %s" %(obj.name) )
				#bpy.ops.object.select_pattern(pattern=obj.name)
				context.scene.objects.active = obj

				#bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
				debug_info("\tActivation Pose Mode")
				bpy.ops.object.posemode_toggle()

				bpy.ops.pose.select_all( action='SELECT' )
				debug_info("\tAjout limite location")
				bpy.ops.pose.constraint_add(type='LIMIT_LOCATION')

				debug_info("\tActivation des limites en local")
				limit_translate = bpy.data.objects[obj.name].pose.bones[-1].constraints[-1]
				limit_translate.use_min_x = True
				limit_translate.use_max_x = True
				limit_translate.use_min_y = False
				limit_translate.use_max_y = False
				limit_translate.use_min_z = True
				limit_translate.use_max_z = True
				limit_translate.owner_space = 'LOCAL'
				obj.pose.bones[-1].lock_location = ( True, False, True )
				bpy.ops.object.posemode_toggle()
			
			
				obj.data.fg.type_anim		= 2
				obj.data.fg.xml_file		= ""
				obj.data.fg.xml_file_no		= 0
				obj.data.fg.family			= "custom"
				obj.data.fg.family_value	= "error"
				obj.data.fg.property_value	= ""
				obj.data.fg.property_idx	= -1
				obj.data.fg.time			= 100.0/bpy.data.scenes[0].render.fps
				obj.data.fg.time_ini		= 100.0/bpy.data.scenes[0].render.fps
				obj.data.fg.range_beg		= 0.0
				obj.data.fg.range_beg_ini	= 0.0
				obj.data.fg.range_end		= 1.0
				obj.data.fg.range_end_ini	= 1.0
				obj.data.fg.factor			= 1.0
				obj.data.fg.factor_ini		= 1.0
				obj.data.fg.offset_deg		= 0.0

				debug_info("\tDesactivation Pose Mode")
				
		for ax in self.axis:
			if ax =='X':
				vec = Vector((1.0,0.0,0.0))
			elif ax =='Y':
				vec = Vector((0.0,1.0,0.0))
			elif ax =='Z':
				vec = Vector((0.0,0.0,1.0))
			elif ax =='x':
				vec = Vector((-1.0,0.0,0.0))
			elif ax =='y':
				vec = Vector((0.0,-1.0,0.0))
			elif ax =='z':
				vec = Vector((0.0,0.0,-1.0))
				
			create_rotate( vec )

		debug_info( self.axis )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_rotate(bpy.types.Operator):
	'''Add armature type rotate '''
	bl_idname = "view3d.create_rotate"
	bl_label = "Create Rotate"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return True
		return context.active_object != None

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians

		debug_info( "Create_rotate : " )
		armature = bpy.ops.object.armature_add( view_align=True )
		armature = bpy.data.armatures[-1]
		debug_info( armature.name )
		for obj in bpy.data.objects:
			if obj.type != 'ARMATURE':
				continue
			if obj.data.name == armature.name:
				break 
		if obj.type == 'ARMATURE':
			debug_info( "\tSelecion de : %s" %(obj.name) )
			#bpy.ops.object.select_pattern(pattern=obj.name)
			context.scene.objects.active = obj

			#bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
			debug_info("\tActivation Pose Mode")
			bpy.ops.object.posemode_toggle()

			bpy.ops.pose.select_all( action='SELECT' )
			debug_info("\tAjout limite rotation")
			bpy.ops.pose.constraint_add(type='LIMIT_ROTATION')

			debug_info("\tMatrice en mode EulerXYZ")
			debug_info("\tActivation des limites en local")
			limit_rotation = bpy.data.objects[obj.name].pose.bones[-1].constraints[-1]
			limit_rotation.use_limit_x = True
			limit_rotation.use_limit_y = False
			limit_rotation.use_limit_z = True
			limit_rotation.owner_space = 'LOCAL'

			bpy.data.objects[obj.name].pose.bones[-1].rotation_mode = 'XYZ'
			bpy.data.objects[obj.name].pose.bones[-1].lock_rotation = ( True, False, True )
			bpy.ops.object.posemode_toggle()
			
			obj.lock_rotation = ( True, False, True )
			
			obj.data.fg.type_anim		= 1
			obj.data.fg.xml_file		= ""
			obj.data.fg.xml_file_no		= 0
			obj.data.fg.family			= "custom"
			obj.data.fg.family_value	= "error"
			obj.data.fg.property_value	= ""
			obj.data.fg.property_idx	= -1
			obj.data.fg.time			= 100.0/bpy.data.scenes[0].render.fps
			obj.data.fg.time_ini		= 100.0/bpy.data.scenes[0].render.fps
			obj.data.fg.range_beg		= 0.0
			obj.data.fg.range_beg_ini	= 0.0
			obj.data.fg.range_end		= 1.0
			obj.data.fg.range_end_ini	= 1.0
			obj.data.fg.factor			= 1.0
			obj.data.fg.factor_ini		= 1.0
			obj.data.fg.offset_deg		= 0.0

			debug_info("\tDesactivation Pose Mode")
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_rotate_axis(bpy.types.Operator):
	'''Add armature type rotate axis '''
	bl_idname = "view3d.create_rotate_axis"
	bl_label = "Create Rotate axis"
	bl_options = {'REGISTER', 'UNDO'}
	
	axis = StringProperty(default="")

	@classmethod
	def poll(cls, context):
		return context.mode == 'OBJECT'

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians
		
		def create_rotate( vec ):
			debug_info( "Create_rotate : " )
			bpy.ops.object.armature_add( view_align=False )
			vec = vec / 10.0
			#vec = Vector(( 0.0, 0.1, 0.0) )
			head = Vector( (0.0,0.0,0.0) )
			tail = Vector( (0.0,0.0,0.0) ) + vec
		
			bpy.ops.object.editmode_toggle()

			bpy.context.object.data.edit_bones["Bone"].head = head #Vector( (0.0,0.0,0.0) ) #self.head
			bpy.context.object.data.edit_bones["Bone"].tail = tail #self.vec /10.0

			bpy.ops.object.editmode_toggle()
		
			obj = context.active_object
			debug_info( obj.name )

			if obj.type == 'ARMATURE':
				debug_info( "\tSelecion de : %s" %(obj.name) )
				#bpy.ops.object.select_pattern(pattern=obj.name)
				context.scene.objects.active = obj

				#bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
				debug_info("\tActivation Pose Mode")
				bpy.ops.object.posemode_toggle()

				bpy.ops.pose.select_all( action='SELECT' )
				debug_info("\tAjout limite rotation")
				bpy.ops.pose.constraint_add(type='LIMIT_ROTATION')

				debug_info("\tMatrice en mode EulerXYZ")
				debug_info("\tActivation des limites en local")
				limit_rotation = bpy.data.objects[obj.name].pose.bones[-1].constraints[-1]
				limit_rotation.use_limit_x = True
				limit_rotation.use_limit_y = False
				limit_rotation.use_limit_z = True
				limit_rotation.owner_space = 'LOCAL'

				bpy.data.objects[obj.name].pose.bones[-1].rotation_mode = 'XYZ'
				bpy.data.objects[obj.name].pose.bones[-1].lock_rotation = ( True, False, True )
				bpy.ops.object.posemode_toggle()
			
				#obj.pose.bones[-1].rotation_mode = lock_location = ( True, False, True )
				#obj.lock_rotation = ( True, False, True )
			
				obj.data.fg.type_anim		= 1
				obj.data.fg.xml_file		= ""
				obj.data.fg.xml_file_no		= 0
				obj.data.fg.family			= "custom"
				obj.data.fg.family_value	= "error"
				obj.data.fg.property_value	= ""
				obj.data.fg.property_idx	= -1
				obj.data.fg.time			= 100.0/bpy.data.scenes[0].render.fps
				obj.data.fg.time_ini		= 100.0/bpy.data.scenes[0].render.fps
				obj.data.fg.range_beg		= 0.0
				obj.data.fg.range_beg_ini	= 0.0
				obj.data.fg.range_end		= 1.0
				obj.data.fg.range_end_ini	= 1.0
				obj.data.fg.factor			= 1.0
				obj.data.fg.factor_ini		= 1.0
				obj.data.fg.offset_deg		= 0.0

				debug_info("\tDesactivation Pose Mode")
				
		for ax in self.axis:
			if ax =='X':
				vec = Vector((1.0,0.0,0.0))
			elif ax =='Y':
				vec = Vector((0.0,1.0,0.0))
			elif ax =='Z':
				vec = Vector((0.0,0.0,1.0))
			elif ax =='x':
				vec = Vector((-1.0,0.0,0.0))
			elif ax =='y':
				vec = Vector((0.0,-1.0,0.0))
			elif ax =='z':
				vec = Vector((0.0,0.0,-1.0))
				
			create_rotate( vec )

		debug_info( self.axis )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_spin(bpy.types.Operator):
	'''Add armature type spin '''
	bl_idname = "view3d.create_spin"
	bl_label = "Create spin"
	bl_options = {'REGISTER', 'UNDO'}
	
	axis = StringProperty(default="")

	@classmethod
	def poll(cls, context):
		return context.mode == 'OBJECT'

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians
		
		def create_spin( vec ):
			debug_info( "Create_spin : " )
			bpy.ops.object.armature_add( view_align=False )
			vec = vec / 10.0
			#vec = Vector(( 0.0, 0.1, 0.0) )
			head = Vector( (0.0,0.0,0.0) )
			tail = Vector( (0.0,0.0,0.0) ) + vec
		
			bpy.ops.object.editmode_toggle()

			bpy.context.object.data.edit_bones["Bone"].head = head #Vector( (0.0,0.0,0.0) ) #self.head
			bpy.context.object.data.edit_bones["Bone"].tail = tail #self.vec /10.0

			bpy.ops.object.editmode_toggle()
		
			obj = context.active_object
			debug_info( obj.name )

			if obj.type == 'ARMATURE':
				debug_info( "\tSelecion de : %s" %(obj.name) )
				#bpy.ops.object.select_pattern(pattern=obj.name)
				context.scene.objects.active = obj

				#bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
				debug_info("\tActivation Pose Mode")
				bpy.ops.object.posemode_toggle()

				bpy.ops.pose.select_all( action='SELECT' )
				debug_info("\tAjout limite rotation")
				bpy.ops.pose.constraint_add(type='LIMIT_ROTATION')

				debug_info("\tMatrice en mode EulerXYZ")
				debug_info("\tActivation des limites en local")
				limit_rotation = bpy.data.objects[obj.name].pose.bones[-1].constraints[-1]
				limit_rotation.use_limit_x = True
				limit_rotation.use_limit_y = False
				limit_rotation.use_limit_z = True
				limit_rotation.owner_space = 'LOCAL'

				bpy.data.objects[obj.name].pose.bones[-1].rotation_mode = 'XYZ'
				bpy.data.objects[obj.name].pose.bones[-1].lock_rotation = ( True, False, True )
				bpy.ops.object.posemode_toggle()
			
				#obj.pose.bones[-1].rotation_mode = lock_location = ( True, False, True )
				#obj.lock_rotation = ( True, False, True )
			
				obj.data.fg.type_anim		= 7
				obj.data.fg.xml_file		= ""
				obj.data.fg.xml_file_no		= 0
				obj.data.fg.family		= "custom"
				obj.data.fg.family_value	= "error"
				obj.data.fg.property_value	= ""
				obj.data.fg.property_idx	= -1
				obj.data.fg.time		= 100.0/bpy.data.scenes[0].render.fps
				obj.data.fg.time_ini		= 100.0/bpy.data.scenes[0].render.fps
				obj.data.fg.range_beg		= -999
				obj.data.fg.range_beg_ini	= -999
				obj.data.fg.range_end		= 999
				obj.data.fg.range_end_ini	= 999
				obj.data.fg.factor		= 1.0
				obj.data.fg.factor_ini		= 1.0
				obj.data.fg.offset_deg		= 0.0

				debug_info("\tDesactivation Pose Mode")
				
		for ax in self.axis:
			if ax =='X':
				vec = Vector((1.0,0.0,0.0))
			elif ax =='Y':
				vec = Vector((0.0,1.0,0.0))
			elif ax =='Z':
				vec = Vector((0.0,0.0,1.0))
			elif ax =='x':
				vec = Vector((-1.0,0.0,0.0))
			elif ax =='y':
				vec = Vector((0.0,-1.0,0.0))
			elif ax =='z':
				vec = Vector((0.0,0.0,-1.0))
				
			create_spin( vec )

		debug_info( self.axis )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_anim(bpy.types.Operator):
	'''???????????'''
	bl_idname = "view3d.create_anim"
	bl_label = "Create Animation"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		from ..xml import xml_manager
		xml_manager.create_anims()
		xml_manager.create_texts()
		# change orgin for all objects
		bpy.ops.object.select_all(action='SELECT')
		bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY',center='MEDIAN')
		bpy.ops.object.select_all(action='DESELECT')
		return {'FINISHED'}
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

class FG_OT_init_rotation(bpy.types.Operator):
	'''???????????'''
	bl_idname = "view3d.init_rotation"
	bl_label = "?????????????"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object == None:
			return False
		return context.scene.objects.active.type == 'ARMATURE'
		#return True

	def execute(self, context):
		from ..xml import xml_manager
		
		#-------------------------------------------------------------------------------------------
		def insert_keyframe_rotation( obj_armature, frame, value ):
			bpy.context.scene.objects.active = obj_armature
			bpy.ops.object.posemode_toggle()
	
			bpy.context.scene.frame_current = frame
			bpy.ops.pose.select_all( action='SELECT' )
			obj_armature.pose.bones[-1].rotation_mode = 'XYZ'
			obj_armature.pose.bones[-1].rotation_euler = Euler( (0.0, radians(value), 0.0), 'XYZ' )
	
			try:
				bpy.ops.anim.keyframe_insert_menu( type='Rotation')
			except:
				bpy.ops.anim.keying_set_add()
				bpy.ops.anim.keying_set_active_set()
				bpy.ops.anim.keyframe_insert_menu( type='Rotation')

			bpy.ops.object.posemode_toggle()

		#-------------------------------------------------------------------------------------------
		save_active = bpy.context.scene.objects.active

		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				continue

			debug_info( "Insert keyframe sur %s" % obj.name )
			
			if obj.data.fg.range_beg != -999.0:
				insert_keyframe_rotation( obj, 1, obj.data.fg.range_beg * obj.data.fg.factor )
			else:
				insert_keyframe_rotation( obj, 1, 0.0 )

			if obj.data.fg.range_end != -999.0:
				frame = obj.data.fg.time / bpy.data.scenes[0].render.fps
				insert_keyframe_rotation( obj, frame, obj.data.fg.range_end * obj.data.fg.factor )
			else:
				insert_keyframe_rotation( obj, 1, 0.0 )


			for fcurve in obj.animation_data.action.fcurves:
				for keyframe in fcurve.keyframe_points:
					keyframe.interpolation = 'LINEAR'


		bpy.context.scene.objects.active = save_active
			
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_init_rotation_zero(bpy.types.Operator):
	'''???????????????'''
	bl_idname = "view3d.init_rotation_zero"
	bl_label = "????????????"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object == None:
			return False
		return context.scene.objects.active.type == 'ARMATURE'
		#return True

	def execute(self, context):
		from ..xml import xml_manager
		
		#-------------------------------------------------------------------------------------------
		def insert_keyframe_rotation( obj_armature, frame, value ):
			bpy.context.scene.objects.active = obj_armature
			bpy.ops.object.posemode_toggle()
	
			bpy.context.scene.frame_current = frame
			bpy.ops.pose.select_all( action='SELECT' )
			obj_armature.pose.bones[-1].rotation_mode = 'XYZ'
			obj_armature.pose.bones[-1].rotation_euler = Euler( (0.0, radians(value), 0.0), 'XYZ' )
	
			try:
				bpy.ops.anim.keyframe_insert_menu( type='Rotation')
			except:
				bpy.ops.anim.keying_set_add()
				bpy.ops.anim.keying_set_active_set()
				bpy.ops.anim.keyframe_insert_menu( type='Rotation')

			bpy.ops.object.posemode_toggle()

		#-------------------------------------------------------------------------------------------
		save_active = bpy.context.scene.objects.active

		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				continue

			debug_info( "Insert keyframe sur %s" % obj.name )
			
			insert_keyframe_rotation( obj, 1, 0.0 )
			frame = obj.data.fg.time / bpy.data.scenes[0].render.fps
			insert_keyframe_rotation( obj, frame, 0.0 )

			for fcurve in obj.animation_data.action.fcurves:
				for keyframe in fcurve.keyframe_points:
					keyframe.interpolation = 'LINEAR'


		bpy.context.scene.objects.active = save_active
			
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
		from math import radians
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

class FG_OT_select_armature_property(bpy.types.Operator):
	'''????????????'''
	bl_idname = "view3d.select_armature_property"
	bl_label = "??????????"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object == None:
			return False
		return context.active_object.type == 'ARMATURE'

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians

		property_name =  context.active_object.data.fg.property_value
		debug_info( property_name )
		
		for obj in bpy.data.objects:
			if obj.type != 'ARMATURE':
				continue
			if obj.data.fg.property_value == property_name:
				obj.select = True
				
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
		from math import radians
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
		from math import radians
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

class FG_OT_transforme_to_rotate(bpy.types.Operator):
	'''C'est un exemple d'operateur blender '''
	bl_idname = "view3d.transform_to_rotate"					# sera appelé par bpy.ops.view3d.exemple()
	bl_label = "Exemple d'operateur"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type == 'ARMATURE'

	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				continue
			obj.data.fg.type_anim = 1
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_transforme_to_translate(bpy.types.Operator):
	'''C'est un exemple d'operateur blender '''
	bl_idname = "view3d.transform_to_translate"					# sera appelé par bpy.ops.view3d.exemple()
	bl_label = "Exemple d'operateur"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type == 'ARMATURE'

	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				continue
			obj.data.fg.type_anim = 2
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_transforme_to_spin(bpy.types.Operator):
	'''C'est un exemple d'operateur blender '''
	bl_idname = "view3d.transform_to_spin"					# sera appelé par bpy.ops.view3d.exemple()
	bl_label = "Exemple d'operateur"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type == 'ARMATURE'

	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				continue
			obj.data.fg.type_anim = 7
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_select_by_property(bpy.types.Operator):
	'''C'est un exemple d'operateur blender '''
	bl_idname = "view3d.select_by_property"					
	bl_label = "Select alla armatures with same flightgear property"
	bl_options = {'REGISTER', 'UNDO'}
	'''
	@classmethod
	def poll(cls, context):
		return True
	'''
	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		from ..xml import xml_export
		active_object = context.active_object
		if active_object and active_object.type == 'ARMATURE':
			property_value = xml_export.build_property_name( active_object )
			#print( "Actif %s %s" % (active_object.name, property_value) )
			
			for obj in bpy.data.objects:
				if obj.type != 'ARMATURE':
					continue
				#bpy.ops.object.posemode_toggle()
				if xml_export.build_property_name(obj) == property_value:
					obj.select = True
				#print( "%s %s %s - %s %s" % (obj.name, obj.data.fg.family, obj.data.fg.family_value, xml_export.build_property_name(obj), obj.select) )
					
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------
class FG_OT_select_object_by_armature(bpy.types.Operator):
	'''C'est un exemple d'operateur blender '''
	bl_idname = "view3d.select_object_by_armature"					
	bl_label = "Select alla armatures with same flightgear property"
	bl_options = {'REGISTER', 'UNDO'}
	'''
	@classmethod
	def poll(cls, context):
		return True
	'''
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
		    print( obj.name )
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
	bpy.utils.register_class( FG_OT_select_armature_property)
	bpy.utils.register_class( FG_OT_copy_property)
	bpy.utils.register_class( FG_OT_init_rotation_zero)
	bpy.utils.register_class( FG_OT_init_rotation)
	bpy.utils.register_class( FG_OT_create_anim)
	bpy.utils.register_class( FG_OT_create_rotate)
	bpy.utils.register_class( FG_OT_create_rotate_axis)
	bpy.utils.register_class( FG_OT_create_spin)
	bpy.utils.register_class( FG_OT_create_translate)
	bpy.utils.register_class( FG_OT_create_translate_axis)
	bpy.utils.register_class( FG_OT_show_animation )
	bpy.utils.register_class( FG_OT_show_all )
	bpy.utils.register_class( FG_OT_insertion_keyframe_rotate )
	bpy.utils.register_class( FG_OT_insertion_keyframe_translate )
	bpy.utils.register_class( FG_OT_transforme_to_rotate )
	bpy.utils.register_class( FG_OT_transforme_to_translate )
	bpy.utils.register_class( FG_OT_transforme_to_spin )
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
	bpy.utils.unregister_class( FG_OT_select_armature_property)
	bpy.utils.unregister_class( FG_OT_copy_property)
	bpy.utils.unregister_class( FG_OT_init_rotation_zero)
	bpy.utils.unregister_class( FG_OT_init_rotation)
	bpy.utils.unregister_class( FG_OT_create_anim)
	bpy.utils.unregister_class( FG_OT_create_rotate)
	bpy.utils.unregister_class( FG_OT_create_rotate_axis)
	bpy.utils.unregister_class( FG_OT_create_spin)
	bpy.utils.unregister_class( FG_OT_create_translate)
	bpy.utils.unregister_class( FG_OT_create_translate_axis)
	bpy.utils.unregister_class( FG_OT_show_animation )
	bpy.utils.unregister_class( FG_OT_show_all )
	bpy.utils.unregister_class( FG_OT_insertion_keyframe_rotate )
	bpy.utils.unregister_class( FG_OT_insertion_keyframe_translate )
	bpy.utils.unregister_class( FG_OT_transforme_to_rotate )
	bpy.utils.unregister_class( FG_OT_transforme_to_translate )
	bpy.utils.unregister_class( FG_OT_transforme_to_spin )
	bpy.utils.unregister_class( FG_OT_select_by_property )
	bpy.utils.unregister_class( FG_OT_select_object_by_armature )
	bpy.utils.unregister_class( FG_OT_select_by_file )

