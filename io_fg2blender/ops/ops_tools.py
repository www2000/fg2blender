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
#									OPS_TOOLS.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy

from . import *

from ..ui.ui_lang import lang

#----------------------------------------------------------------------------------------------------------------------------------

def debug_info(aff):
	from .. import debug_ops_tools

	if debug_ops_tools:
		print(aff)
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_edges_split(bpy.types.Operator):
	'''Apply edge split to selected object(s)'''
	bl_idname = "view3d.edge_split"
	bl_label = ""
	bl_description = lang['DOC010']
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if context.active_object == None:
			return False
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
		from math import degrees

		debug_info( "Smooth Object : " )
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
					debug_info( "\tObject : %s    angle=%0.2f" % (obj.name,degrees(angle)) )

					try:
						bpy.ops.object.modifier_add( type='EDGE_SPLIT')	
						for mod in obj.modifiers:
							if mod.type=='EDGE_SPLIT':
								mod.split_angle = angle
					except:
						debug_info( "Erreur modifier_add Edge-split" )

					obj.select = False

		for obj in list_objects:
			obj.select = True
		context.scene.objects.active = active_object

				
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_only_render(bpy.types.Operator):
	'''??????????????????'''
	bl_idname = "fg.only_render"
	bl_label = ""
	bl_description = "???????????????????"

	def execute(self, context):
		debug_info( self.filepath)
		return {'FINISHED'}

	def invoke(self, context, event):
		debug_info( context.space_data.type )
		if context.space_data.type=='VIEW_3D':
			context.space_data.show_only_render = not  context.space_data.show_only_render
		#return {'FINISHED'}
		return {'RUNNING_MODAL'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_time_2x(bpy.types.Operator):
	'''Increase speed animation x2'''
	bl_idname = "view3d.time_2x"
	bl_label = ""
	bl_description = lang['DOC011']

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
	'''Decrease speed animation x2'''
	bl_idname = "view3d.time_0_5x"
	bl_label = ""
	bl_description = lang['DOC012']

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

class FG_OT_relpath(bpy.types.Operator):
	'''Change all files path to relative path'''
	bl_idname = "object.relpath"					
	bl_label = ""
	bl_options = {'REGISTER', 'UNDO'}
	'''
	@classmethod
	def poll(cls, context):
		return True
	'''
	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		# ce que l'on veut faire
		debug_info( "HelloWord" )
		from .. import fg2bl
		fg2bl.path.change_all_to_relatif()
		return {'FINISHED'}
		

#----------------------------------------------------------------------------------------------------------------------------------
class FG_OT_abspath(bpy.types.Operator):
	'''Change all files path to absolute path'''
	bl_idname = "object.abspath"					
	bl_label = ""
	bl_options = {'REGISTER', 'UNDO'}
	'''
	@classmethod
	def poll(cls, context):
		return True
	'''
	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		# ce que l'on veut faire
		debug_info( "HelloWord" )
		from .. import fg2bl
		fg2bl.path.change_all_to_abs()
		return {'FINISHED'}
       
        
#----------------------------------------------------------------------------------------------------------------------------------
# Sample : simple operator
#----------------------------------------------------------------------------------------------------------------------------------
class FG_OT_exemple(bpy.types.Operator):
	'''C'est un exemple d'operateur blender'''
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
		debug_info( "HelloWord" )
		return {'FINISHED'}

#----------------------------------------------------------
# Sample
#----------------------------------------------------------
# from api-doc  blender.org
#----------------------------------------------------------
class SimpleMouseOperator(bpy.types.Operator):
    """ This operator shows the mouse location,
        this string is used for the tooltip and API docs
    """
    bl_idname = "wm.mouse_position"
    bl_label = "Mouse location"
 
    x = bpy.props.IntProperty()
    y = bpy.props.IntProperty()
 
    def execute(self, context):
        # rather then printing, use the report function,
        # this way the message appears in the header,
        self.report({'INFO'}, "Mouse coords are %d %d" % (self.x, self.y))
        return {'FINISHED'}
 
    def invoke(self, context, event):
        self.x = event.mouse_x
        self.y = event.mouse_y
        return self.execute(context)
 
#
#    Panel in tools region
#
class MousePanel(bpy.types.Panel):
    bl_label = "Mouse"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_PROPS"
 
    def draw(self, context):
        self.layout.operator("wm.mouse_position")
 
#
#	Registration
#   Not really necessary to register the class, because this happens
#   automatically when the module is registered. OTOH, it does not hurt either.
#bpy.utils.register_class(SimpleMouseOperator)
#bpy.utils.register_class(MousePanel)
 
# Automatically display mouse position on startup
#bpy.ops.wm.mouse_position('INVOKE_DEFAULT')
 
# Another test call, this time call execute() directly with pre-defined settings.
#bpy.ops.wm.mouse_position('EXEC_DEFAULT', x=20, y=66)
#----------------------------------------------------------------------------------------------------------------------------------
#
#				REGISTER
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class( FG_OT_edges_split)
	bpy.utils.register_class( FG_OT_exemple)
	bpy.utils.register_class( FG_OT_only_render )
	bpy.utils.register_class( FG_OT_time_0_5x )
	bpy.utils.register_class( FG_OT_time_2x )
	bpy.utils.register_class( FG_OT_relpath )
	bpy.utils.register_class( FG_OT_abspath )
	
def unregister():
	bpy.utils.unregister_class( FG_OT_edges_split)
	bpy.utils.unregister_class( FG_OT_exemple)
	bpy.utils.unregister_class( FG_OT_only_render )
	bpy.utils.unregister_class( FG_OT_time_0_5x )
	bpy.utils.unregister_class( FG_OT_time_2x )
	bpy.utils.unregister_class( FG_OT_relpath )
	bpy.utils.unregister_class( FG_OT_abspath )

