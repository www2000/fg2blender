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
# Script copyright (C) Clément de l'Hamaide
# Contributors: René Nègre
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									OPS_POPUP.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy


#----------------------------------------------------------------------------------------------------------------------------------
class FG_OT_popup(bpy.types.Operator):
	bl_idname = "view3d.popup"
	bl_label = "FG2Blender error"

	message = bpy.props.StringProperty()

	def execute(self, context):
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def draw(self, context):
		from ..ui.ui_lang import lang
		self.layout.label(lang[self.message])

#----------------------------------------------------------------------------------------------------------------------------------
class FG_OT_insert_keyframe_rotate_at(bpy.types.Operator):
	bl_idname = "view3d.insert_keyframe_rotate_at"
	bl_label = "Insert keyframe at"
	
	float_value = bpy.props.FloatProperty()

	@classmethod
	def poll(cls, context):
		if context.mode != 'POSE':
			return False
		if context.active_object == None:
			return False
		if context.active_object.type != 'ARMATURE':
			return False
		if context.active_object.data.fg.type_anim != 'rotate':
			return False
		return True

	def execute(self, context):
		active_object = context.active_object

		if not active_object and active_object.type != 'ARMATURE' and active_object.data.fg.type_anim != 'rotate':
			return {'FINISHED'}

		print( "Value = %0.2f" % self.float_value )

		if self.float_value > active_object.data.fg.range_end or self.float_value < active_object.data.fg.range_beg:
			bpy.ops.view3d.popup('INVOKE_DEFAULT', message="ERR008")
			return {'FINISHED'}

		rg = float(bpy.context.scene.frame_end - bpy.context.scene.frame_start)
		coef = (self.float_value-active_object.data.fg.range_beg) /(active_object.data.fg.range_end-active_object.data.fg.range_beg) 
		pos_float = bpy.context.scene.frame_start + rg * coef
		pos = int(pos_float)
		
		bpy.context.scene.frame_current = pos
		bpy.ops.view3d.insert_keyframe_rotate()
		
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE' and obj.data.fg.type_anim != 'rotate':
				continue

			print( "Insert keyframe sur %s" % obj.name )

			if obj.animation_data.action:
				for fcurve in obj.animation_data.action.fcurves:
					print( "data_path %s" % fcurve.data_path )
					if fcurve.data_path.find('rotation_euler') == -1:
						continue		

					for keyframe in fcurve.keyframe_points:
						keyframe.interpolation = 'LINEAR'
						
						if keyframe.co.x == pos:
							keyframe.co.x = pos_float
							print( "co  %s" % str(keyframe.co) )

		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def draw(self, context):
		from ..ui.ui_lang import lang
		
		active_object = context.active_object
		mess = "Error"
		if active_object and active_object.type == 'ARMATURE' and active_object.data.fg.type_anim == 'rotate':
			mess = lang['UI031'] % ( active_object.data.fg.range_beg, active_object.data.fg.range_end )
		self.layout.label(mess)

		box = self.layout.box()
		row = box.row()
		row.prop(self, "float_value" )
		#row.prop( self.float_value,  "Value" )

#----------------------------------------------------------------------------------------------------------------------------------
class FG_OT_insert_keyframe_translate_at(bpy.types.Operator):
	bl_idname = "view3d.insert_keyframe_translate_at"
	bl_label = "Insert keyframe at"
	
	float_value = bpy.props.FloatProperty()

	@classmethod
	def poll(cls, context):
		if context.mode != 'POSE':
			return False
		if context.active_object == None:
			return False
		if context.active_object.type != 'ARMATURE':
			return False
		if context.active_object.data.fg.type_anim != 'translate':
			return False
		return True

	def execute(self, context):
		active_object = context.active_object

		if not active_object and active_object.type != 'ARMATURE' and active_object.data.fg.type_anim != 'translate':
			return {'FINISHED'}

		print( "Value = %0.2f" % self.float_value )

		if self.float_value > active_object.data.fg.range_end or self.float_value < active_object.data.fg.range_beg:
			bpy.ops.view3d.popup('INVOKE_DEFAULT', message="ERR008")
			return {'FINISHED'}

		rg = float(bpy.context.scene.frame_end - bpy.context.scene.frame_start)
		coef = (self.float_value-active_object.data.fg.range_beg) /(active_object.data.fg.range_end-active_object.data.fg.range_beg) 
		pos_float = bpy.context.scene.frame_start + rg * coef
		pos = int(pos_float)
		
		bpy.context.scene.frame_current = pos
		bpy.ops.view3d.insert_keyframe_translate()
		
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE' and obj.data.fg.type_anim != 'translate':
				continue

			print( "Insert keyframe sur %s" % obj.name )

			if obj.animation_data.action:
				for fcurve in obj.animation_data.action.fcurves:
					print( "data_path %s" % fcurve.data_path )
					if fcurve.data_path.find('location') == -1:
						continue		

					for keyframe in fcurve.keyframe_points:
						keyframe.interpolation = 'LINEAR'
						
						if keyframe.co.x == pos:
							keyframe.co.x = pos_float
							print( "co  %s" % str(keyframe.co) )

		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def draw(self, context):
		from ..ui.ui_lang import lang
		
		active_object = context.active_object
		mess = "Error"
		if active_object and active_object.type == 'ARMATURE' and active_object.data.fg.type_anim == 'translate':
			mess = lang['UI032'] % ( active_object.data.fg.range_beg, active_object.data.fg.range_end )
		self.layout.label(mess)

		box = self.layout.box()
		row = box.row()
		row.prop(self, "float_value" )
		#row.prop( self.float_value,  "Value" )


#----------------------------------------------------------------------------------------------------------------------------------
def register():
	bpy.utils.register_class( FG_OT_popup )
	bpy.utils.register_class( FG_OT_insert_keyframe_rotate_at )
	bpy.utils.register_class( FG_OT_insert_keyframe_translate_at )

#----------------------------------------------------------------------------------------------------------------------------------
def unregister():
	bpy.utils.unregister_class( FG_OT_popup )
	bpy.utils.unregister_class( FG_OT_insert_keyframe_rotate_at )
	bpy.utils.unregister_class( FG_OT_insert_keyframe_translate_at )

