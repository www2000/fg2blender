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
# Contributors: René Nègre
#

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

#from io_utils import ExportHelper, ImportHelper
from bpy_extras.io_utils import ExportHelper, ImportHelper
from bpy.props import FloatProperty, StringProperty, BoolProperty, EnumProperty





class ImportFG(bpy.types.Operator, ImportHelper):
	'''This appears in the tooltip of the operator and in the generated docs'''
	bl_idname = "import.fg2blender"  # this is important since its how bpy.ops.export.some_data is constructed
	bl_label = "Import .xml"
	bl_options = {'PRESET'}	

	# ExportHelper mixin class uses this
	filename_ext = ".xml"

	filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})

	# List of operator properties, the attributes will be assigned
	# to the class instance from the operator settings before calling.
	#use_setting = BoolProperty(name="Example Boolean", description="Example Tooltip", default=True)
	#filepath = bpy.props.StringProperty(name="File Path", maxlen=1024, default="")

	smooth_all	= BoolProperty(name="Smooth all", description="Tools smooth", default=True)
	edge_split	= BoolProperty(name="Edge split", description="Object modifiers", default=True)
	split_angle	= FloatProperty(name="Split angle", description="Value of edge-spit", min=0.0, max=180.0, default=65.0 )


	def execute(self, context):
		from .import_xml import import_xml

		if self.edge_split:
			self.smooth_all=False
		import_xml(	self.filepath, 
								smooth_all=self.smooth_all,
								edge_split=self.edge_split,
								split_angle=self.split_angle,
								context=context )
		return {'FINISHED'}
		#return write_some_data(context, self.filepath, self.select_only)




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

#def menu_func_export(self, context):
#    self.layout.operator(ExportFG.bl_idname, text="Flightgear (.xml)")		# text=Title in the menu


def register():
    bpy.utils.register_class(ImportFG)
    #bpy.utils.register_class(ExportFG)

    bpy.types.INFO_MT_file_import.append(menu_func_import)
    #bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ImportAC)
    #bpy.utils.unregister_class(ExportAC)

    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    #bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
	try:
		unregister()
	except:
		pass
	register()
	
