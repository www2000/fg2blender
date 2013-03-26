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
# Contributors:
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									OPS_POPUP.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy


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
		self.layout.label(self.message)
		row = self.layout.split(0.25)


def register():
	bpy.utils.register_class( FG_OT_popup )

def unregister():
	bpy.utils.unregister_class( FG_OT_popup )
