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
# Contributors: Clément de l'Hamaide
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									__INIT__.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

bl_info = {
    "name": "Flightgear",
    "description": "Import/Export flightgear xml (plane description)",
    "author": "Rene Negre, Alexis Laillé, Clément de l'Hamaide",
    "version": (0,1),
    "blender": (2, 63, 0),
    "api": 31236,
    "location": "File > Import-Export",
    "warning": '', # used for warning icon and text in addons panel
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/"\
        "Scripts/My_Script",
    "tracker_url": "http://projects.blender.org/tracker/index.php?"\
        "func=detail&aid=<number>",
    "category": "Import-Export"}


import bpy
import os
import time
#from . import *

from math import radians
from math import degrees

from bpy_extras.io_utils import ExportHelper
from bpy_extras.io_utils import ImportHelper

from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import CollectionProperty

from .meshes.ac3d.ac_manager import AC_OPTION
from .xml.xml_manager import XML_OPTION



DEBUG = False

debug_file_debug		= False
debug_xml_manager		= False
debug_xml_import		= False
debug_xml_export		= False
debug_xml_camera		= False
debug_xml_jsbsim		= False
debug_xml_armement		= False
debug_xml_anim			= False
debug_ac3d_import		= False
debug_ac3d_export		= False
debug_fg2bl		        = False
debug_props_armature	= False
debug_props_camera		= False
debug_props_empty		= False
debug_props_meshes		= False
debug_ops_unwrap		= False
debug_ops_flightgear	= False
debug_ops_ac3d			= False
debug_ops_xml			= False
debug_ops_tools			= False
debug_ops_armature		= False
debug_unwrap			= False


#----------------------------------------------------------------------------------------------------------------------------------

def debug_info( aff):
	global DEBUG
	if DEBUG:
		print( aff )

#----------------------------------------------------------------------------------------------------------------------------------
#
#							ImportFG CLASS
#
#----------------------------------------------------------------------------------------------------------------------------------

class ImportFG(bpy.types.Operator, ImportHelper):
	'''FlightGear XML Import'''
	bl_idname = "import.fg2blender"  # this is important since its how bpy.ops.export.some_data is constructed
	bl_label = "Import FlightGear"
	bl_options = {'PRESET'}	

	# ExportHelper mixin class uses this
	filename_ext = ".xml"
	filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})
	
	files = CollectionProperty( name="File Path", description="File path used for importing " "xml file", type=bpy.types.OperatorFileListElement)
	directory = StringProperty()

	include		= BoolProperty(name="Include file", description="Read file include", default=True)

	mesh_active_layer	= BoolProperty(name="Active layer", description="Read file include", default=False)
	mesh_rotate_layer_0	= IntProperty(name="Begin", description="Read file include", min=1, max=20, default=1)
	mesh_rotate_layer_1	= IntProperty(name="End", description="Read file include", min=1, max=20, default=9)

	armature_active_layer	= BoolProperty(name="Active layer", description="Read file include", default=False)
	armature_rotate_layer_0	= IntProperty(name="Begin", description="Read file include", min=1, max=20, default=11)
	armature_rotate_layer_1	= IntProperty(name="End", description="Read file include", min=1, max=20, default=19)

	def draw(self, context):
		scn = context.scene
		layout = self.layout
		row = layout.row()
		row.label( text = "Option AC3D" )

		box_option_ac = layout.box()
		row = box_option_ac.column()
		row.prop( self, "mesh_active_layer" )
		if not self.mesh_active_layer:
			row.prop( self, "mesh_rotate_layer_0" )
			row.prop( self, "mesh_rotate_layer_1" )

		row = layout.row()
		row.label( text = "Option XML" )
		box_option_xml = layout.box()
		row = box_option_xml.column()
		#row.label( text = "Option xml" )
		row.prop( self, "include" )
		row.prop( self, "armature_active_layer" )
		if not self.armature_active_layer:
			row.prop( self, "armature_rotate_layer_0" )
			row.prop( self, "armature_rotate_layer_1" )


	def execute(self, context):

		paths = [os.path.join(self.directory, name.name)	for name in self.files]
			
		from .xml.xml_import import import_xml
		for filename in paths:
			debug_info( filename )
			ac_option = AC_OPTION()
		
			xml_option = XML_OPTION()
			xml_option.include				= self.include
			xml_option.mesh_active_layer	= self.mesh_active_layer
			xml_option.mesh_layer_beg		= self.mesh_rotate_layer_0
			xml_option.mesh_layer_end		= self.mesh_rotate_layer_1
			xml_option.arma_active_layer	= self.armature_active_layer
			xml_option.arma_layer_beg		= self.armature_rotate_layer_0
			xml_option.arma_layer_end		= self.armature_rotate_layer_1
			
			global debug_file_debug
			if debug_file_debug:
				print( "Write /tmp/script-fg2bl" )
				f = open('/tmp/script-fg2bl', mode='w')
				f.write( filename )
				f.close()
			print( "*********" )
			import_xml(	filename, ac_option, xml_option )
			bpy.context.scene.layers = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------
#
#							ImportAC CLASS
#
#----------------------------------------------------------------------------------------------------------------------------------

class ImportAC(bpy.types.Operator, ImportHelper):
	'''AC3D Import'''
	bl_idname = "import.ac_file"  # this is important since its how bpy.ops.export.some_data is constructed
	bl_label = "Import .ac"
	bl_options = {'PRESET'}	

	# ExportHelper mixin class uses this
	filename_ext = ".ac"
	filter_glob = StringProperty(default="*.ac", options={'HIDDEN'})


	files = CollectionProperty(	name="File Path",
								description="File path used for importing " "xml file",
								type=bpy.types.OperatorFileListElement)
	directory = StringProperty()

	mesh_active_layer	= BoolProperty(name="Active layer", description="Read file include", default=True)
	mesh_rotate_layer_0	= IntProperty(name="Begin", description="Read file include", min=1, max=20, default=0)
	mesh_rotate_layer_1	= IntProperty(name="End", description="Read file include", min=1, max=20, default=20)

	def draw(self, context):
		scn = context.scene
		layout = self.layout
		row = layout.row()
		row.label( text = "Option AC3D" )

		box_option_ac = layout.box()
		row = box_option_ac.column()

		row.prop( self, "mesh_active_layer" )
		if not self.mesh_active_layer:
			row.prop( self, "mesh_rotate_layer_0" )
			row.prop( self, "mesh_rotate_layer_1" )

	def execute(self, context):

		paths = [os.path.join(self.directory, name.name)	for name in self.files]
			
		from .meshes.ac3d.ac_import import read_ac
		for filename in paths:
			debug_info( filename )
			ac_option = AC_OPTION()
			ac_option.context		= context
			print ("import ac : %s" % os.path.basename(filename) )
			global debug_file_debug
			if debug_file_debug:
				f = open('/tmp/script-fg2bl', mode='w')
				f.write( filename )
				f.close()
			
			read_ac( filename, ac_option )
			
		
		return {'FINISHED'}

#====================================================================================================================
#
#
#
#				REGISTER
#
#
#====================================================================================================================
# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportFG.bl_idname, text="Flightgear (.xml)")		# text=Title in the menu
    self.layout.operator(ImportAC.bl_idname, text="Flightgear (.ac)")		# text=Title in the menu

def register():
	from .ops import ops_flightgear
	from .ops import ops_ac3d
	from .ops import ops_tools
	from .ops import ops_xml
	from .ops import ops_popup
	from .ops import ops_unwrap
	from .ops import ops_armature
	from .props import props_armature
	from .props import props_meshes
	from .props import props_empty
	from .props import props_camera
	from .ui import ui_menu
	from .ui import ui_panel_armature
	from .ui import ui_panel_object
	from .ui import ui_panel_empty
	from .ui import ui_panel_camera
	from .ui import ui_shortcut
	from .ui import ui_button

	bpy.utils.register_class(ImportFG)
	bpy.utils.register_class(ImportAC)
	bpy.types.INFO_MT_file_import.append(menu_func_import)

	ops_flightgear.register()
	ops_ac3d.register()
	ops_tools.register()
	ops_xml.register()
	ops_popup.register()
	ops_unwrap.register()
	ops_armature.register()
	props_armature.register()
	props_meshes.register()
	props_empty.register()
	props_camera.register()
	ui_menu.register()
	ui_panel_armature.register()
	ui_panel_object.register()
	ui_panel_empty.register()
	ui_panel_camera.register()
	ui_shortcut.register()
	ui_button.register()

	if not os.path.isfile('/tmp/script-fg2bl'):
		print( "Run script without debug info" )
	else:
		print( "Run script with debug info" )
		global	debug_xml_manager
		global	debug_xml_import
		global	debug_xml_export
		global	debug_xml_camera
		global	debug_xml_jsbsim
		global	debug_xml_armement
		global	debug_xml_anim
		global	debug_ac3d_import
		global	debug_ac3d_export
		global	debug_fg2bl
		global	DEBUG
		global	debug_file_debug
		global	debug_ops_unwrap
		global	debug_ops_flightgear
		global	debug_ops_ac3d
		global	debug_ops_tools
		global	debug_ops_xml
		global	debug_ops_armature
		global  debug_props_armature
		
		debug_file_debug	= True
		DEBUG			= True
		debug_info( "File debug OK" )

		debug_fg2bl		     	= True
		debug_xml_manager		= False
		debug_xml_import		= False
		debug_xml_export		= False
		debug_xml_camera		= False
		debug_xml_jsbsim		= False
		debug_xml_armement		= True
		debug_xml_anim			= False
		debug_ac3d_import		= False
		debug_ac3d_export		= False
		debug_props_armature	= False
		debug_ops_unwrap		= False
		debug_ops_flightgear	= False
		debug_ops_ac3d			= False
		debug_ops_tools			= False
		debug_ops_xml			= True
		debug_ops_armature		= False
	
def unregister():
	from .ops import ops_flightgear
	from .ops import ops_ac3d
	from .ops import ops_tools
	from .ops import ops_xml
	from .ops import ops_popup
	from .ops import ops_unwrap
	from .ops import ops_armature
	from .props import props_armature
	from .props import props_meshes
	from .props import props_empty
	from .props import props_camera
	from .ui import ui_menu
	from .ui import ui_panel_armature
	from .ui import ui_panel_object
	from .ui import ui_panel_empty
	from .ui import ui_panel_camera
	from .ui import ui_shortcut
	from .ui import ui_button

	bpy.utils.unregister_class(ImportFG)
	bpy.utils.unregister_class(ImportAC)
	bpy.types.INFO_MT_file_import.remove(menu_func_import)

	ops_flightgear.unregister()
	ops_ac3d.unregister()
	ops_tools.unregister()
	ops_xml.unregister()
	ops_popup.unregister()
	ops_unwrap.unregister()
	ops_armature.unregister()
	props_armature.unregister()
	props_meshes.unregister()
	props_empty.unregister()
	props_camera.unregister()
	ui_menu.unregister()
	ui_panel_armature.unregister()
	ui_panel_object.unregister()
	ui_panel_empty.unregister()
	ui_panel_camera.unregister()
	ui_shortcut.unregister()
	ui_button.unregister()

	
if __name__ == "__main__":
	try:
		unregister()
	except:
		pass
	register()

