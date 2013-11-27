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
#									OPS_ARMATURE.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy

from . import *

from mathutils import Vector
from mathutils import Euler

from math import radians

from bpy.props import StringProperty

from ..ui.ui_lang import lang
#--------------------------------------------------------------------------------------------------------------------------------

def debug_info(aff):
	from .. import debug_ops_armature

	if debug_ops_armature:
		print(aff)
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_translate(bpy.types.Operator):
	'''Create armature type translate'''
	bl_idname = "view3d.create_translate"
	bl_label = ""
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


			obj.data.fg.type_anim		= 'translate'
			obj.data.fg.xml_file		= ""
			obj.data.fg.xml_file_no		= 0
			obj.data.fg.family		= "custom"
			obj.data.fg.family_value	= "error"
			obj.data.fg.property_value	= ""
			obj.data.fg.property_idx	= -1
			obj.data.fg.time		= 100.0/bpy.data.scenes[0].render.fps
			obj.data.fg.time_ini		= 100.0/bpy.data.scenes[0].render.fps
			obj.data.fg.range_beg		= 0.0
			obj.data.fg.range_beg_ini	= 0.0
			obj.data.fg.range_end		= 1.0
			obj.data.fg.range_end_ini	= 1.0
			obj.data.fg.factor		= 1.0
			obj.data.fg.factor_ini		= 1.0
			obj.data.fg.offset_deg		= 0.0

			debug_info("\tDesactivation Pose Mode")
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_translate_axis(bpy.types.Operator):
	'''Create armature type translate on selected axis'''
	bl_idname = "view3d.create_translate_axis"
	bl_label = ""
	bl_description = lang['DOC013']
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
			
			
				obj.data.fg.type_anim		= 'translate'
				obj.data.fg.xml_file		= ""
				obj.data.fg.xml_file_no		= 0
				obj.data.fg.family		= "custom"
				obj.data.fg.family_value	= "error"
				obj.data.fg.property_value	= ""
				obj.data.fg.property_idx	= -1
				obj.data.fg.time		= 100.0/bpy.data.scenes[0].render.fps
				obj.data.fg.time_ini		= 100.0/bpy.data.scenes[0].render.fps
				obj.data.fg.range_beg		= 0.0
				obj.data.fg.range_beg_ini	= 0.0
				obj.data.fg.range_end		= 1.0
				obj.data.fg.range_end_ini	= 1.0
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
				
			create_rotate( vec )

		debug_info( self.axis )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_rotate(bpy.types.Operator):
	'''Create armature type rotate'''
	bl_idname = "view3d.create_rotate"
	bl_label = ""
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
			
			obj.data.fg.type_anim		= 'rotate'
			obj.data.fg.xml_file		= ""
			obj.data.fg.xml_file_no		= 0
			obj.data.fg.family		= "custom"
			obj.data.fg.family_value	= "error"
			obj.data.fg.property_value	= ""
			obj.data.fg.property_idx	= -1
			obj.data.fg.time		= 100.0/bpy.data.scenes[0].render.fps
			obj.data.fg.time_ini		= 100.0/bpy.data.scenes[0].render.fps
			obj.data.fg.range_beg		= 0.0
			obj.data.fg.range_beg_ini	= 0.0
			obj.data.fg.range_end		= 1.0
			obj.data.fg.range_end_ini	= 1.0
			obj.data.fg.factor		= 1.0
			obj.data.fg.factor_ini		= 1.0
			obj.data.fg.offset_deg		= 0.0

			debug_info("\tDesactivation Pose Mode")
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_rotate_axis(bpy.types.Operator):
	'''Create armature type rotate on selected axis'''
	bl_idname = "view3d.create_rotate_axis"
	bl_label = ""
	bl_description = lang['DOC014']
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
			
				obj.data.fg.type_anim		= 'rotate'
				obj.data.fg.xml_file		= ""
				obj.data.fg.xml_file_no		= 0
				obj.data.fg.family		= "custom"
				obj.data.fg.family_value	= "error"
				obj.data.fg.property_value	= ""
				obj.data.fg.property_idx	= -1
				obj.data.fg.time		= 100.0/bpy.data.scenes[0].render.fps
				obj.data.fg.time_ini		= 100.0/bpy.data.scenes[0].render.fps
				obj.data.fg.range_beg		= 0.0
				obj.data.fg.range_beg_ini	= 0.0
				obj.data.fg.range_end		= 1.0
				obj.data.fg.range_end_ini	= 1.0
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
				
			create_rotate( vec )

		debug_info( self.axis )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_spin(bpy.types.Operator):
	'''Create armature type spin on selected axis'''
	bl_idname = "view3d.create_spin"
	bl_label = ""
	bl_description = lang['DOC015']
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
			
				obj.data.fg.type_anim		= 'spin'
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
	'''Compute XML animations loaded from the XML import'''
	bl_idname = "view3d.create_anim"
	bl_label = ""
	bl_description = lang['DOC016']
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

class FG_OT_init_rotation(bpy.types.Operator):
	'''???????????'''
	bl_idname = "view3d.init_rotation"
	bl_label = ""
	bl_description = lang['DOC017']
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object == None:
			return False
		if context.mode != 'POSE' and context.mode != 'OBJECT':
			return False
		return context.scene.objects.active.type == 'ARMATURE'
		#return True

	def execute(self, context):
		from ..xml import xml_manager
		
		#-------------------------------------------------------------------------------------------
		def insert_keyframe_rotation( obj_armature, frame, value ):
			bpy.context.scene.objects.active = obj_armature
			if context.mode != 'POSE':
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
			
			frame = bpy.context.scene.frame_start
			if obj.data.fg.range_beg != -999.0:
				#insert_keyframe_rotation( obj, frame, obj.data.fg.range_beg * obj.data.fg.factor )
				insert_keyframe_rotation( obj, frame, obj.data.fg.range_beg )
			else:
				insert_keyframe_rotation( obj, frame, 0.0 )

			frame = bpy.context.scene.frame_end
			if obj.data.fg.range_end != -999.0:
				#frame = obj.data.fg.time / bpy.data.scenes[0].render.fps
				#insert_keyframe_rotation( obj, frame, obj.data.fg.range_end * obj.data.fg.factor )
				insert_keyframe_rotation( obj, frame, obj.data.fg.range_end )
			else:
				insert_keyframe_rotation( obj, frame, 0.0 )


			for fcurve in obj.animation_data.action.fcurves:
				for keyframe in fcurve.keyframe_points:
					keyframe.interpolation = 'LINEAR'


		bpy.context.scene.objects.active = save_active
			
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_init_rotation_zero(bpy.types.Operator):
	'''???????????????'''
	bl_idname = "view3d.init_rotation_zero"
	bl_label = ""
	bl_description = lang['DOC018']
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

class FG_OT_transforme_to_rotate(bpy.types.Operator):
	'''Transform selected armature(s) as armature type rotate'''
	bl_idname = "view3d.transform_to_rotate"
	bl_label = ""
	bl_description = lang['DOC019']
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type == 'ARMATURE'

	def execute(self, context):
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				continue
			obj.data.fg.type_anim = 'rotate'
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_transforme_to_translate(bpy.types.Operator):
	'''Transform selected armature(s) as armature type translate'''
	bl_idname = "view3d.transform_to_translate"
	bl_label = ""
	bl_description = lang['DOC020']
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type == 'ARMATURE'

	def execute(self, context):
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				continue
			obj.data.fg.type_anim = 'translate'
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_transforme_to_spin(bpy.types.Operator):
	'''Transform selected armature(s) as armature type spin'''
	bl_idname = "view3d.transform_to_spin"
	bl_label = ""
	bl_description = lang['DOC021']
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type == 'ARMATURE'

	def execute(self, context):
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				continue
			obj.data.fg.type_anim = 'spin'
		return {'FINISHED'}

#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_reset_all_armatures(bpy.types.Operator):
	'''Transform selected armature(s) as armature type spin'''
	bl_idname = "view3d.reset_all_armatures"
	bl_label = ""
	bl_description = lang['DOC059']
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return True
		#if not context.active_object:
		#	return False
		#return context.active_object.type == 'ARMATURE'

	def execute(self, context):
		for anim in bpy.data.objects:
			if anim.type != 'ARMATURE':
				continue

			anim.pose.bones["Bone" ].rotation_euler.y = 0.0
			anim.pose.bones["Bone" ].location.y = 0.0

		return {'FINISHED'}

#----------------------------------------------------------------------------------------------------------------------------------
#
#				REGISTER
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class( FG_OT_init_rotation_zero)
	bpy.utils.register_class( FG_OT_init_rotation)
	bpy.utils.register_class( FG_OT_create_anim)
	bpy.utils.register_class( FG_OT_create_rotate)
	bpy.utils.register_class( FG_OT_create_rotate_axis)
	bpy.utils.register_class( FG_OT_create_spin)
	bpy.utils.register_class( FG_OT_create_translate)
	bpy.utils.register_class( FG_OT_create_translate_axis)
	bpy.utils.register_class( FG_OT_transforme_to_rotate )
	bpy.utils.register_class( FG_OT_transforme_to_translate )
	bpy.utils.register_class( FG_OT_transforme_to_spin )
	bpy.utils.register_class( FG_OT_reset_all_armatures )

def unregister():
	bpy.utils.unregister_class( FG_OT_init_rotation_zero)
	bpy.utils.unregister_class( FG_OT_init_rotation)
	bpy.utils.unregister_class( FG_OT_create_anim)
	bpy.utils.unregister_class( FG_OT_create_rotate)
	bpy.utils.unregister_class( FG_OT_create_rotate_axis)
	bpy.utils.unregister_class( FG_OT_create_spin)
	bpy.utils.unregister_class( FG_OT_create_translate)
	bpy.utils.unregister_class( FG_OT_create_translate_axis)
	bpy.utils.unregister_class( FG_OT_transforme_to_rotate )
	bpy.utils.unregister_class( FG_OT_transforme_to_translate )
	bpy.utils.unregister_class( FG_OT_transforme_to_spin )
	bpy.utils.unregister_class( FG_OT_reset_all_armatures )

