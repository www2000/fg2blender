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

STACK_SAVE_KEYFRAMES = []

class SAVE_KEYFRAME:
	def __init__(self):
		self.armature_name			= ""
		self.keyframe				= []

#
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

		print( "Create_translate : " )
		armature = bpy.ops.object.armature_add( view_align=True )
		armature = bpy.data.armatures[-1]
		print( armature.name )
		for obj in bpy.data.objects:
			if obj.type != 'ARMATURE':
				continue
			if obj.data.name == armature.name:
				break 
		if obj.type == 'ARMATURE':
			print( "\tSelecion de : %s" %(obj.name) )
			#bpy.ops.object.select_pattern(pattern=obj.name)
			context.scene.objects.active = obj

			bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

			print("\tActivation Pose Mode")
			bpy.ops.object.posemode_toggle()
			bpy.ops.pose.select_all( action='SELECT' )
			print("\tAjout limite location")
			bpy.ops.pose.constraint_add(type='LIMIT_LOCATION')

			print("\tActivation des limites en local")
			limit_translate = bpy.data.objects[obj.name].pose.bones[-1].constraints[-1]
			limit_translate.use_min_x = True
			limit_translate.use_max_x = True
			limit_translate.use_min_y = False
			limit_translate.use_max_y = False
			limit_translate.use_min_z = True
			limit_translate.use_max_z = True
			limit_translate.owner_space = 'LOCAL'
			obj.lock_location = ( True, False, True )
			bpy.ops.object.posemode_toggle()


			obj.data.fg.type_anim		= 2
			obj.data.fg.xml_file		= ""
			obj.data.fg.xml_file_no		= 0
			obj.data.fg.familly			= "custom"
			obj.data.fg.familly_value	= "error"
			obj.data.fg.property_value	= ""
			obj.data.fg.property_idx	= -1
			obj.data.fg.time			= 2.5
			obj.data.fg.range_beg		= 0.0
			obj.data.fg.range_beg_ini	= 0.0
			obj.data.fg.range_end		= 1.0
			obj.data.fg.range_end_ini	= 1.0
			obj.data.fg.factor			= 1.0
			obj.data.fg.factor_ini		= 1.0
			obj.data.fg.offset_deg		= 0.0

			print("\tDesactivation Pose Mode")
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

		print( "Create_rotate : " )
		armature = bpy.ops.object.armature_add( view_align=True )
		armature = bpy.data.armatures[-1]
		print( armature.name )
		for obj in bpy.data.objects:
			if obj.type != 'ARMATURE':
				continue
			if obj.data.name == armature.name:
				break 
		if obj.type == 'ARMATURE':
			print( "\tSelecion de : %s" %(obj.name) )
			#bpy.ops.object.select_pattern(pattern=obj.name)
			context.scene.objects.active = obj

			#bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
			print("\tActivation Pose Mode")
			bpy.ops.object.posemode_toggle()

			bpy.ops.pose.select_all( action='SELECT' )
			print("\tAjout limite rotation")
			bpy.ops.pose.constraint_add(type='LIMIT_ROTATION')

			print("\tMatrice en mode EulerXYZ")
			print("\tActivation des limites en local")
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
			obj.data.fg.familly			= "custom"
			obj.data.fg.familly_value	= "error"
			obj.data.fg.property_value	= ""
			obj.data.fg.property_idx	= -1
			obj.data.fg.time			= 2.5
			obj.data.fg.range_beg		= 0.0
			obj.data.fg.range_beg_ini	= 0.0
			obj.data.fg.range_end		= 1.0
			obj.data.fg.range_end_ini	= 1.0
			obj.data.fg.factor			= 1.0
			obj.data.fg.factor_ini		= 1.0
			obj.data.fg.offset_deg		= 0.0

			print("\tDesactivation Pose Mode")
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_rotate_axis(bpy.types.Operator):
	'''Add armature type rotate '''
	bl_idname = "view3d.create_rotate_axis"
	bl_label = "Create Rotate"
	bl_options = {'REGISTER', 'UNDO'}
	
	axis = StringProperty(default="")

	@classmethod
	def poll(cls, context):
		return True
		return context.active_object != None

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians
		
		def create_rotate( vec ):
			print( "Create_rotate : " )
			armature = bpy.ops.object.armature_add( view_align=False )
			vec = vec / 10.0
			#vec = Vector(( 0.0, 0.1, 0.0) )
			head = Vector( (0.0,0.0,0.0) )
			tail = Vector( (0.0,0.0,0.0) ) + vec
		
			bpy.ops.object.editmode_toggle()

			bpy.context.object.data.edit_bones["Bone"].head = head #Vector( (0.0,0.0,0.0) ) #self.head
			bpy.context.object.data.edit_bones["Bone"].tail = tail #self.vec /10.0

			bpy.ops.object.editmode_toggle()
		
			armature = bpy.data.armatures[-1]
			print( armature.name )
			for obj in bpy.data.objects:
				if obj.type != 'ARMATURE':
					continue
				if obj.data.name == armature.name:
					break 
			if obj.type == 'ARMATURE':
				print( "\tSelecion de : %s" %(obj.name) )
				#bpy.ops.object.select_pattern(pattern=obj.name)
				context.scene.objects.active = obj

				#bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
				print("\tActivation Pose Mode")
				bpy.ops.object.posemode_toggle()

				bpy.ops.pose.select_all( action='SELECT' )
				print("\tAjout limite rotation")
				bpy.ops.pose.constraint_add(type='LIMIT_ROTATION')

				print("\tMatrice en mode EulerXYZ")
				print("\tActivation des limites en local")
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
				obj.data.fg.familly			= "custom"
				obj.data.fg.familly_value	= "error"
				obj.data.fg.property_value	= ""
				obj.data.fg.property_idx	= -1
				obj.data.fg.time			= 2.5
				obj.data.fg.range_beg		= 0.0
				obj.data.fg.range_beg_ini	= 0.0
				obj.data.fg.range_end		= 1.0
				obj.data.fg.range_end_ini	= 1.0
				obj.data.fg.factor			= 1.0
				obj.data.fg.factor_ini		= 1.0
				obj.data.fg.offset_deg		= 0.0

				print("\tDesactivation Pose Mode")
				
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

		print( self.axis )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_anim(bpy.types.Operator):
	'''Add armature type rotate '''
	bl_idname = "view3d.create_anim"
	bl_label = "Create Animation"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		from . import xml_manager
		xml_manager.create_anims()
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_save_keyframe(bpy.types.Operator):
	'''Add armature type rotate '''
	bl_idname = "view3d.save_keyframe"
	bl_label = "Create Animation"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.scene.objects.active.type == 'ARMATURE'

	def execute(self, context):
		from . import xml_manager
		global STACK_SAVE_KEYFRAMES

		obj = context.scene.objects.active
		
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				continue

			for skf in STACK_SAVE_KEYFRAMES:
				if skf.name == obj.name:
					print( "Deja sauvegardé" )
					continue
		
			save_keyframe = SAVE_KEYFRAME()
			save_keyframe.name = obj.name
		
			armature = obj#obj.data
			if armature.animation_data != None:
				print( " Sauvegarde " )
				for fcurve in armature.animation_data.action.fcurves:
					print( ' Fcurve  ' )
					for point in fcurve.keyframe_points:
						x = 0.0 + point.co.x
						y = 0.0 + point.co.y
						co = ( x, y )
						print( " Point %s" % str(co) )
						save_keyframe.keyframe.append( co )
						point.co.y = 0.0
				
		
			STACK_SAVE_KEYFRAMES.append( save_keyframe )		
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_restore_keyframe(bpy.types.Operator):
	'''Add armature type rotate '''
	bl_idname = "view3d.restore_keyframe"
	bl_label = "Create Animation"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.scene.objects.active.type == 'ARMATURE'

	def execute(self, context):
		from . import xml_manager
		global STACK_SAVE_KEYFRAMES

		obj = context.scene.objects.active
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				continue
			
			save_keyframe = None		
			for skf in STACK_SAVE_KEYFRAMES:
				if skf.name == obj.name:
					save_keyframe = skf
				
			if save_keyframe == None:
				print( '"%s" non sauvegarde' % obj.name )
				continue
		
			armature = obj
			if armature.animation_data != None:
				idx = 0
				for fcurve in armature.animation_data.action.fcurves:
					for point in fcurve.keyframe_points:
						print( str(save_keyframe.keyframe[idx]) )
						point.co.y = save_keyframe.keyframe[idx][1]
						idx = idx + 1
				
		
			STACK_SAVE_KEYFRAMES.remove( save_keyframe )		
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_copy_xml_file(bpy.types.Operator):
	'''Add armature type rotate '''
	bl_idname = "view3d.copy_xml_file"
	bl_label = "Copy xml file"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.scene.objects.active.type == 'ARMATURE'
		#return True

	def execute(self, context):
		from . import xml_manager

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
			
			if active_obj.delta_location != obj.delta_location:
				obj.location = obj.location - active_obj.delta_location
				obj.delta_location = obj.delta_location + active_obj.delta_location
			if active_obj.delta_rotation_euler != obj.delta_rotation_euler:
				obj.rotation_euler = obj.rotation_euler - active_obj.delta_rotation_euler
				obj.delta_rotation_euler = obj.delta_rotation_euler + active_obj.delta_rotation_euler
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_copy_property(bpy.types.Operator):
	'''Add armature type rotate '''
	bl_idname = "view3d.copy_property"
	bl_label = "Copy property"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.scene.objects.active.type == 'ARMATURE'
		#return True

	def execute(self, context):
		from . import xml_manager

		active_obj = context.scene.objects.active
		print( "Copy de %s" % active_obj.data.fg.property_value )
		familly			= active_obj.data.fg.familly
		familly_value	= active_obj.data.fg.familly_value
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

		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				continue
			print( "Copy sur %s" % obj.name )
			print( "	Copy de  %s" % str(property_value) )
			obj.data.fg.familly			= familly
			obj.data.fg.familly_value	= familly_value
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
	'''Add armature type rotate '''
	bl_idname = "view3d.init_rotation"
	bl_label = "Copy property"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.scene.objects.active.type == 'ARMATURE'
		#return True

	def execute(self, context):
		from . import xml_manager
		
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

			print( "Insert keyframe sur %s" % obj.name )
			
			if obj.data.fg.range_beg != -999.0:
				insert_keyframe_rotation( obj, 1, obj.data.fg.range_beg * obj.data.fg.factor )
			else:
				insert_keyframe_rotation( obj, 1, 0.0 )

			if obj.data.fg.range_end != -999.0:
				insert_keyframe_rotation( obj, 60, obj.data.fg.range_end * obj.data.fg.factor )
			else:
				insert_keyframe_rotation( obj, 1, 0.0 )


			for fcurve in obj.animation_data.action.fcurves:
				for keyframe in fcurve.keyframe_points:
					keyframe.interpolation = 'LINEAR'


		bpy.context.scene.objects.active = save_active
			
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_init_rotation_zero(bpy.types.Operator):
	'''Add armature type rotate '''
	bl_idname = "view3d.init_rotation_zero"
	bl_label = "Copy property"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.scene.objects.active.type == 'ARMATURE'
		#return True

	def execute(self, context):
		from . import xml_manager
		
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

			print( "Insert keyframe sur %s" % obj.name )
			
			insert_keyframe_rotation( obj, 1, 0.0 )
			insert_keyframe_rotation( obj, 60, 0.0 )

			for fcurve in obj.animation_data.action.fcurves:
				for keyframe in fcurve.keyframe_points:
					keyframe.interpolation = 'LINEAR'


		bpy.context.scene.objects.active = save_active
			
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_edges_split(bpy.types.Operator):
	'''Add edge split sor select object '''
	bl_idname = "view3d.edge_split"
	bl_label = "Edge split"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		bModifier = False
		for obj in context.selected_objects:
			if obj.type != 'MESH':
				continue
			bObjModifier = False
			for modifier in obj.modifiers:
				if modifier.type == 'EDGE_SPLIT':
					bObjModifier = True

			if bObjModifier == False:
				bModifier = True
		
		return bModifier
					
					

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians

		print( "Smooth Object : " )
		list_objects = context.selected_objects
		active_object =	context.scene.objects.active
		for obj in bpy.data.objects:
			obj.select = False

		for obj in list_objects:
			if obj.type == 'MESH':
				bModifier = True
				for modifier in obj.modifiers:
					if modifier.type == 'EDGE_SPLIT':
						bModifier = False

				if bModifier:
					obj.select = True
					context.scene.objects.active = obj
					angle = obj.data.auto_smooth_angle
					print( "\tObject : %s    angle=%0.2f" % (obj.name,degrees(angle)) )

					try:
						bpy.ops.object.modifier_add( type='EDGE_SPLIT')	
						for mod in obj.modifiers:
							if mod.type=='EDGE_SPLIT':
								mod.split_angle = angle
					except:
						print( "Erreur modifier_add Edge-split" )

					obj.select = False

		for obj in list_objects:
			obj.select = True
		context.scene.objects.active = active_object

				
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_select_property(bpy.types.Operator):
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
		print( '--- Select property  ---' )
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				obj = find_armature( obj )
				if not obj:
					continue
			if obj.type != 'ARMATURE':
				continue
			property_name =  obj.data.fg.property_value
			print( property_name )
			for o in bpy.data.objects:
				if o.type == 'ARMATURE':
					if o.data.fg.property_value == property_name:
						
						select_childs( o )
						o.select = True
				
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_select_armature_property(bpy.types.Operator):
	bl_idname = "view3d.select_armature_property"
	bl_label = "Select property"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.active_object.type == 'ARMATURE'

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians

		property_name =  context.active_object.data.fg.property_value
		print( property_name )
		
		for obj in bpy.data.objects:
			if obj.type != 'ARMATURE':
				continue
			if obj.data.fg.property_value == property_name:
				obj.select = True
				
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------
class FG_OT_show_animation(bpy.types.Operator):
	'''Show all object used by the same property and hid other '''
	bl_idname = "view3d.show_animation"
	bl_label = "Show animate objects"
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
	'''Show all object used by the same property and hid other '''
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
class FG_OT_select_file(bpy.types.Operator):
	bl_idname = "object.file_select"
	bl_label = ""

	#filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	filepath = bpy.props.StringProperty()
	filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})
	

	def execute(self, context):
		obj = context.active_object

		if obj.type == 'ARMATURE':
			obj.data.fg.xml_file = self.filepath
		
		#context.window_manager.fileselect_add(self)
		return {'FINISHED'}

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		#print( self.filepath )
		#return {'FINISHED'}
		return {'RUNNING_MODAL'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_only_render(bpy.types.Operator):
	bl_idname = "fg.only_render"
	bl_label = ""

	def execute(self, context):
		#print( self.filepath)
		return {'FINISHED'}

	def invoke(self, context, event):
		#print( context.space_data.type )
		if context.space_data.type=='VIEW_3D':
			context.space_data.show_only_render = not  context.space_data.show_only_render
		#return {'FINISHED'}
		return {'RUNNING_MODAL'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_time_2x(bpy.types.Operator):
	bl_idname = "view3d.time_2x"
	bl_label = ""

	def invoke(self, context, event):
		end = context.scene.frame_end
		old = context.scene.render.frame_map_old
		new = context.scene.render.frame_map_new
		if new == 100.0:
			end = context.scene.frame_end = 60.0
			old = context.scene.render.frame_map_old = 60.0
			new = context.scene.render.frame_map_new = 60.0

		context.scene.frame_end = new *0.5
		context.scene.render.frame_map_old = old
		context.scene.render.frame_map_new = new *0.5
		return {'FINISHED'}
		return {'RUNNING_MODAL'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_time_0_5x(bpy.types.Operator):
	bl_idname = "view3d.time_0_5x"
	bl_label = ""

	def invoke(self, context, event):
		end = context.scene.frame_end
		old = context.scene.render.frame_map_old
		new = context.scene.render.frame_map_new
		if new == 100.0:
			end = context.scene.frame_end = 60.0
			old = context.scene.render.frame_map_old = 60.0
			new = context.scene.render.frame_map_new = 60.0

		context.scene.frame_end = new *2.0
		context.scene.render.frame_map_old = old
		context.scene.render.frame_map_new = new * 2.0
		return {'FINISHED'}
		return {'RUNNING_MODAL'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_write_xml(bpy.types.Operator):
	bl_idname = "view3d.write_xml"
	bl_label = "Write File"
	
	#filename = bpy.props.StringProperty()
	obj_name = bpy.props.StringProperty()
	#objet = None
	
	#---------------------------------------------------------------------------
	def exist_in_text_editor(self, name ):
		for text in bpy.data.texts:
			if text.name == name:
				return True
		return False
	#---------------------------------------------------------------------------

	def creer_xml(self, filename):
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
		from .xml_import import charge_xml
		from . import xml_export
		from . import xml_import

		#if len(xml_manager.xml_files)<1:
		#	return
			
		name = os.path.basename( filename )
		script_name = name +'.script'
		
		if self.exist_in_text_editor( script_name ):
			bpy.data.texts[script_name].clear()
		else:
			#bpy.ops.text.new( name )
			bpy.data.texts.new( script_name )

		node = xml_import.charge_xml( filename )

		if node == None:
			node = xml.dom.minidom.Document()
			prop_list = node.createElement( 'PropertyList' )
			node.appendChild( prop_list )
			print( name )
			print( script_name )
			#return
		xml_export.write_animation_all( context, node, name, no )
		bpy.data.texts[script_name].use_tabs_as_spaces = True
		bpy.data.texts[script_name].write( node.toprettyxml() )
		#bpy.data.texts[name].write( node.toxml() )
	#---------------------------------------------------------------------------
	def execute( self, context ):
		if self.filename != "":
			print( self.filename )
			self.charge_xml( self.filename )
		return {'FINISHED'}

	#---------------------------------------------------------------------------

	def invoke(self, context, event):
		print( self.obj_name )
		obj = bpy.data.objects[self.obj_name]
		filename = obj.data.fg.xml_file
		no		 = obj.data.fg.xml_file_no
		print( filename )
		#filename = self.filename
		if filename == "":
			filename = xml_manager.xml_files[0][0].name
		
		if filename.find('Aircraft')!=-1:
			right_name = filename.partition('Aircraft')[2]
			name_path = '/media/sauvegarde/fg-2.6/install/fgfs/fgdata/Aircraft/' + right_name
		else:
			if not xml_manager.exist_xml_file( filename, no ):
				self.creer_xml( filename )
			name_path	= filename 
			no			= obj.data.fg.xml_file_no
		self.charge_xml( context, name_path, no )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_exemple(bpy.types.Operator):
	'''C'est un exemple d'operateur blender '''
	bl_idname = "view3d.exemple"					# sera appelé par bpy.ops.view3d.exemple()
	bl_label = "Exemple d'operateur"
	bl_options = {'REGISTER', 'UNDO'}
	'''
	@classmethod
	def poll(cls, context):
		return True
	'''
	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		# ce que l'on veut faire
		print( "HelloWord" )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class( FG_OT_save_keyframe)
	bpy.utils.register_class( FG_OT_restore_keyframe)
	bpy.utils.register_class( FG_OT_edges_split)
	bpy.utils.register_class( FG_OT_select_property)
	bpy.utils.register_class( FG_OT_select_armature_property)
	bpy.utils.register_class( FG_OT_copy_xml_file)
	bpy.utils.register_class( FG_OT_copy_property)
	bpy.utils.register_class( FG_OT_init_rotation_zero)
	bpy.utils.register_class( FG_OT_init_rotation)
	bpy.utils.register_class( FG_OT_create_anim)
	bpy.utils.register_class( FG_OT_create_rotate)
	bpy.utils.register_class( FG_OT_create_rotate_axis)
	bpy.utils.register_class( FG_OT_create_translate)
	bpy.utils.register_class( FG_OT_exemple)
	bpy.utils.register_class( FG_OT_select_file )
	bpy.utils.register_class( FG_OT_show_animation )
	bpy.utils.register_class( FG_OT_show_all )
	bpy.utils.register_class( FG_OT_only_render )
	bpy.utils.register_class( FG_OT_time_0_5x )
	bpy.utils.register_class( FG_OT_time_2x )
	bpy.utils.register_class( FG_OT_write_xml )

def unregister():
	bpy.utils.unregister_class( FG_OT_save_keyframe)
	bpy.utils.unregister_class( FG_OT_restore_keyframe)
	bpy.utils.unregister_class( FG_OT_edges_split)
	bpy.utils.unregister_class( FG_OT_select_property)
	bpy.utils.unregister_class( FG_OT_select_armature_property)
	bpy.utils.unregister_class( FG_OT_copy_xml_file)
	bpy.utils.unregister_class( FG_OT_copy_property)
	bpy.utils.unregister_class( FG_OT_init_rotation_zero)
	bpy.utils.unregister_class( FG_OT_init_rotation)
	bpy.utils.unregister_class( FG_OT_create_anim)
	bpy.utils.unregister_class( FG_OT_create_rotate)
	bpy.utils.unregister_class( FG_OT_create_rotate_axis)
	bpy.utils.unregister_class( FG_OT_create_translate)
	bpy.utils.unregister_class( FG_OT_exemple)
	bpy.utils.unregister_class( FG_OT_select_file )
	bpy.utils.unregister_class( FG_OT_show_animation )
	bpy.utils.unregister_class( FG_OT_show_all )
	bpy.utils.unregister_class( FG_OT_only_render )
	bpy.utils.unregister_class( FG_OT_time_0_5x )
	bpy.utils.unregister_class( FG_OT_time_2x )
	bpy.utils.unregister_class( FG_OT_write_xml )

