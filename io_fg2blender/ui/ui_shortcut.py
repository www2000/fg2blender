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
    kmi = km.keymap_items.new('fg.exec2', 'X', 'PRESS', ctrl=True)
    kmi = km.keymap_items.new('view3d.create_anim', 'C', 'PRESS', alt=True)
    #kmi = km.keymap_items.new('wm.mouse_position', 'J', 'PRESS')
    kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS')
    kmi.properties.name = 'VIEW3D_FG_root_menu' 
    #kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS')
    #kmi.properties.name = 'VIEW3D_FG_root_menu' 
    kmi = km.keymap_items.new('fg.only_render', 'R', 'PRESS', ctrl=True)
    
    # for "edit mode" because F key is use
    #km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    #kmi = km.keymap_items.new('wm.call_menu', 'M', 'PRESS')
    #kmi.properties.name = 'VIEW3D_FG_root_menu' 
#----------------------------------------------------------------------------------------------------------------------------------

def unregister_shortcut():
	kc = bpy.context.window_manager.keyconfigs.addon
	km = kc.keymaps["3D View"]
	for kmi in km.keymap_items:
		print( "Suppression de kmi : " + kmi.idname )
		if kmi.idname == "fg.exec":
			km.keymap_items.remove(kmi)
		elif kmi.idname == "fg.exec2":
			km.keymap_items.remove(kmi)
		elif kmi.idname == 'wm.call_menu':
			km.keymap_items.remove(kmi)
		elif kmi.idname == 'fg.only_render':
			km.keymap_items.remove(kmi)
		#if kmi.idname == 'wm.mouse_position':
		#    km.keymap_items.remove(kmi)
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

