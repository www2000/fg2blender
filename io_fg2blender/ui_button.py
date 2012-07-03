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
#									UI_PANEL_BUTTON.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy


#--------------------------------------------------------------------------------------------------------------------------------
#   Button
class FG_OT_button_select(bpy.types.Operator):
	bl_idname = "fg.button_select"
	bl_label = "Select"

	object_name = bpy.props.StringProperty()

	def execute(self, context):	
		for obj in bpy.data.objects:
			obj.select = False
		obj = bpy.data.objects[self.object_name]
		obj.select = True
		bpy.context.scene.objects.active = obj
		return{'FINISHED'}    
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class(FG_OT_button_select)
#--------------------------------------------------------------------------------------------------------------------------------

def unregister():
	bpy.utils.unregister_class(FG_OT_button_select)


