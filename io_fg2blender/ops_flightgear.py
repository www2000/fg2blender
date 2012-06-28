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
#									OPS_FLIGHTGEAR.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy

from math import radians
from math import degrees


from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import CollectionProperty

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
			bpy.ops.object.posemode_toggle()

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
			bpy.data.objects[obj.name].pose.bones[-1].rotation_mode = 'XYZ'
			print("\tActivation des limites en local")
			limit_rotation = bpy.data.objects[obj.name].pose.bones[-1].constraints[-1]
			limit_rotation.use_limit_x = True
			limit_rotation.use_limit_y = False
			limit_rotation.use_limit_z = True
			limit_rotation.owner_space = 'LOCAL'
			bpy.ops.object.posemode_toggle()

			print("\tDesactivation Pose Mode")
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_anim(bpy.types.Operator):
	'''Add armature type rotate '''
	bl_idname = "view3d.create_anim"
	bl_label = "Create Annimation"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		from . import xml_manager
		xml_manager.create_anims()
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_edges_split(bpy.types.Operator):
	'''Add edge split sor select object '''
	bl_idname = "view3d.edge_split"
	bl_label = "Edge split"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type == 'MESH'#None

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
    bpy.utils.register_class(FG_OT_edges_split)
    bpy.utils.register_class(FG_OT_create_anim)
    bpy.utils.register_class(FG_OT_create_rotate)
    bpy.utils.register_class(FG_OT_create_translate)
    bpy.utils.register_class(FG_OT_exemple)


def unregister():
    bpy.utils.unregister_class(FG_OT_edges_split)
    bpy.utils.unregister_class(FG_OT_create_anim)
    bpy.utils.unregister_class(FG_OT_create_rotate)
    bpy.utils.unregister_class(FG_OT_create_translate)
    bpy.utils.unregister_class(FG_OT_exemple)

