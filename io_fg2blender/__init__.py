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
#									__INIT__.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

bl_info = {
    "name": "Flightgear",
    "description": "Import/Export flightgear xml (plane description)",
    "author": "Rene Negre, PAF",
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

from .ac_manager import AC_OPTION
from .xml_manager import XML_OPTION

from . import *



#----------------------------------------------------------------------------------------------------------------------------------
#
#							ImportFG CLASS
#
#----------------------------------------------------------------------------------------------------------------------------------

class ImportFG(bpy.types.Operator, ImportHelper):
	'''This appears in the tooltip of the operator and in the generated docs'''
	bl_idname = "import.fg2blender"  # this is important since its how bpy.ops.export.some_data is constructed
	bl_label = "Import .xml"
	bl_options = {'PRESET'}	

	# ExportHelper mixin class uses this
	filename_ext = ".xml"
	filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})


	files = CollectionProperty(	name="File Path",
								description="File path used for importing " "xml file",
								type=bpy.types.OperatorFileListElement)
	directory = StringProperty()


	smooth_all	= BoolProperty(name="Smooth all", description="Tools smooth", default=True)
	edge_split	= BoolProperty(name="Edge split", description="Object modifiers", default=True)
	split_angle	= FloatProperty(name="Split angle", description="Value of edge-spit", min=0.0, max=180.0, default=65.0 )
	include		= BoolProperty(name="Include file", description="Read file include", default=True)

	mesh_active_layer	= BoolProperty(name="Active layer", description="Read file include", default=False)
	mesh_rotate_layer_0	= IntProperty(name="Begin", description="Read file include", min=1, max=20, default=1)
	mesh_rotate_layer_1	= IntProperty(name="End", description="Read file include", min=1, max=20, default=10)

	armature_active_layer	= BoolProperty(name="Active layer", description="Read file include", default=False)
	armature_rotate_layer_0	= IntProperty(name="Begin", description="Read file include", min=1, max=20, default=11)
	armature_rotate_layer_1	= IntProperty(name="End", description="Read file include", min=1, max=20, default=20)

	def draw(self, context):
		scn = context.scene
		layout = self.layout
		row = layout.row()
		row.label( text = "Option AC3D" )

		box_option_ac = layout.box()
		row = box_option_ac.column()
		row.prop( self, "smooth_all" )
		row.prop( self, "edge_split" )
		row.prop( self, "split_angle" )
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
			
		from .xml_import import import_xml
		for filename in paths:
			print( filename )
			ac_option = AC_OPTION()
			ac_option.smooth_all			= self.smooth_all
			ac_option.edge_split			= self.edge_split
			ac_option.split_angle			= self.split_angle
		
			xml_option = XML_OPTION()
			xml_option.include				= self.include
			xml_option.mesh_active_layer	= self.mesh_active_layer
			xml_option.mesh_layer_beg		= self.mesh_rotate_layer_0
			xml_option.mesh_layer_end		= self.mesh_rotate_layer_1
			xml_option.arma_active_layer	= self.armature_active_layer
			xml_option.arma_layer_beg		= self.armature_rotate_layer_0
			xml_option.arma_layer_end		= self.armature_rotate_layer_1
		
			if xml_manager.BIDOUILLE :
				f = open('/home/rene/tmp/script-fg2bl', mode='w')
				f.write( filename )
				f.close()
				#xml_option = XML_OPTION()
				#xml_option.include		= False
				#xml_option.active_layer	= False
				#xml_option.layer_beg	= 1
				#xml_option.layer_end	= 10

			import_xml(	filename, ac_option, xml_option )
			#bpy.context.scene.layers = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
			#bpy.ops.view3d.create_anim()
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------
#
#							ImportAC CLASS
#
#----------------------------------------------------------------------------------------------------------------------------------

class ImportAC(bpy.types.Operator, ImportHelper):
	'''This appears in the tooltip of the operator and in the generated docs'''
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


	smooth_all	= BoolProperty(name="Smooth all", description="Tools smooth", default=True)
	edge_split	= BoolProperty(name="Edge split", description="Object modifiers", default=True)
	split_angle	= FloatProperty(name="Split angle", description="Value of edge-spit", min=0.0, max=180.0, default=65.0 )

	mesh_active_layer	= BoolProperty(name="Active layer", description="Read file include", default=True)
	mesh_rotate_layer_0	= IntProperty(name="Begin", description="Read file include", min=1, max=20, default=0)
	mesh_rotate_layer_1	= IntProperty(name="End", description="Read file include", min=1, max=20, default=20)

	def draw(self, context):
		scn = context.scene
		layout = self.layout
		row = layout.row()
		row.label( text = "Option ac" )

		box_option_ac = layout.box()
		row = box_option_ac.column()
		row.prop( self, "smooth_all" )
		row.prop( self, "edge_split" )
		row.prop( self, "split_angle" )

		row.prop( self, "mesh_active_layer" )
		if not self.mesh_active_layer:
			row.prop( self, "mesh_rotate_layer_0" )
			row.prop( self, "mesh_rotate_layer_1" )

	def execute(self, context):

		paths = [os.path.join(self.directory, name.name)	for name in self.files]
			
		from .ac_import import read_ac
		for filename in paths:
			#print( filename )
			ac_option = AC_OPTION()
			ac_option.smooth_all	= self.smooth_all
			ac_option.edge_split	= self.edge_split
			ac_option.split_angle	= self.split_angle
			ac_option.context		= context
			
			if xml_manager.BIDOUILLE:
				f = open('/home/rene/tmp/script-fg2bl', mode='w')
				f.write( filename )
				f.close()
			
			read_ac( filename, ac_option )
			
		
		return {'FINISHED'}



'''
class ExportFG(bpy.types.Operator, ExportHelper):
	bl_idname = "export.fg2blender"  # this is important since its how bpy.ops.export.some_data is constructed
	bl_label = "Export .xml"
	bl_options = {'PRESET'}	

	# ExportHelper mixin class uses this
	filename_ext = ".xml"

	filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})

	# List of operator properties, the attributes will be assigned
	# to the class instance from the operator settings before calling.
	#use_setting = BoolProperty(name="Example Boolean", description="Example Tooltip", default=True)
	#filepath = bpy.props.StringProperty(name="File Path", maxlen=1024, default="")

	select_only 		= BoolProperty(name="Selection only", description="Export selected objects only", default=True)
	tex_path			= BoolProperty(name="Path in texture name", description="Path name in texture name", default=False)
	apply_modifiers		= BoolProperty(name="Apply modifiers", description="Apply modifiers in meshes", default=True)


	
		
	@classmethod
	def poll(cls, context):
		return context.active_object != None

	def execute(self, context):
		from . import export_xml
		export_xml.write_file(	context, 
									self.filepath, 
									select_only=self.select_only, 
									tex_path=self.tex_path,
									apply_modifiers=self.apply_modifiers  )
		return {'FINISHED'}

'''
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
#    self.layout.operator(ImportAC.bl_idname, text="Flightgear (.ac)")		# text=Title in the menu

#def menu_func_export(self, context):
#    self.layout.operator(ExportFG.bl_idname, text="Flightgear (.xml)")		# text=Title in the menu


def register():
	from . import ops_flightgear
	from . import ops_unwrap
	from . import props_armature
	from . import ui_menu
	from . import ui_panel_armature
	from . import ui_panel_object
	from . import ui_shortcut
	from . import ui_button

	bpy.utils.register_class(ImportFG)
	bpy.utils.register_class(ImportAC)
	bpy.types.INFO_MT_file_import.append(menu_func_import)

	ops_flightgear.register()
	ops_unwrap.register()
	props_armature.register()
	ui_menu.register()
	ui_panel_armature.register()
	ui_panel_object.register()
	ui_shortcut.register()
	ui_button.register()

	if not os.path.isfile('/home/rene/tmp/script-fg2bl'):
		print( "N'existe pas" )
		xml_manager.BIDOUILLE = False
	else:
		print( "Existe" )

	
	
def unregister():
	from . import ops_flightgear
	from . import ops_unwrap
	from . import props_armature
	from . import ui_menu
	from . import ui_panel_armature
	from . import ui_panel_object
	from . import ui_shortcut
	from . import ui_button

	bpy.utils.unregister_class(ImportFG)
	bpy.utils.unregister_class(ImportAC)
	bpy.types.INFO_MT_file_import.remove(menu_func_import)

	ops_flightgear.unregister()
	ops_unwrap.unregister()
	props_armature.unregister()
	ui_menu.unregister()
	ui_panel_armature.unregister()
	ui_panel_object.unregister()
	ui_shortcut.unregister()
	ui_button.unregister()

	
	
if __name__ == "__main__":
	try:
		unregister()
	except:
		pass
	register()
	
