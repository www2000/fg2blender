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
#									UI_SHORTCUT.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy

#----------------------------------------------------------------------------------------------------------------------------------

def register_shortcut():
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new('fg.exec', 'F', 'PRESS', ctrl=True)
    kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS')
    kmi.properties.name = 'VIEW3D_FG_root_menu' 
#----------------------------------------------------------------------------------------------------------------------------------

def unregister_shortcut():
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps["3D View"]
    for kmi in km.keymap_items:
        if kmi.idname == 'fg.exec':
            km.keymap_items.remove(kmi)
        if kmi.idname == 'wm.call_menu':
            km.keymap_items.remove(kmi)
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
    register_shortcut()

def unregister():
    unregister_shortcut()

