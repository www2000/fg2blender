
bl_info = {
    "name": "AC3D Mr No",
    "description": "Import/Export meshs in .ac format.",
    "author": "Rene Negre",
    "version": (0,1),
    "blender": (2, 5, 7),
    "api": 31236,
    "location": "File > Import-Export",
    "warning": '', # used for warning icon and text in addons panel
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/"\
        "Scripts/My_Script",
    "tracker_url": "http://projects.blender.org/tracker/index.php?"\
        "func=detail&aid=<number>",
    "category": "Import-Export"}

if "bpy" in locals():
    import imp
    if "import_ac" in locals():
        imp.reload(import_ac)
    if "export_ac" in locals():
        imp.reload(export_ac)


import bpy

#from io_utils import ExportHelper, ImportHelper
from bpy_extras.io_utils import ExportHelper, ImportHelper
from bpy.props import FloatProperty, StringProperty, BoolProperty, EnumProperty



class ImportAC(bpy.types.Operator, ImportHelper):
	#bl_idname = "import.some_data"  # this is important since its how bpy.ops.export.some_data is constructed
	bl_idname = "import_scene.import_ac"  # this is important since its how bpy.ops.export.some_data is constructed
	
	bl_label = "Import .ac"
	bl_options = {'PRESET'}	

	# ExportHelper mixin class uses this
	filename_ext = ".ac"

	filter_glob = StringProperty(default="*.ac", options={'HIDDEN'})

	# List of operator properties, the attributes will be assigned
	# to the class instance from the operator settings before calling.
	#use_setting = BoolProperty(name="Example Boolean", description="Example Tooltip", default=True)
	#filepath = bpy.props.StringProperty(name="File Path", maxlen=1024, default="")

	#smooth_all	= BoolProperty(name="Smooth all", description="Tools smooth", default=True)
	edge_split	= BoolProperty(name="Edge Split", description="Object modifiers", default=False)
	#split_angle	= FloatProperty(name="Split angle", description="Value of edge-spit", min=0.0, max=180.0, default=30.0 )


	def execute(self, context):
		from . import import_ac
		#if self.edge_split:
		#	self.smooth_all=False
			
		#import_ac.read_ac( self.filepath, smooth_all=self.smooth_all, edge_split=self.edge_split, split_angle=self.split_angle )
		
		#import_ac.read_ac( self.filepath )
		import_ac.read_ac( self.filepath , context, self.edge_split)
		
		'''
		if self.edge_split:
			import_ac.edge_split( context, self.split_angle )
		if self.smooth_all and self.edge_split==False:
			import_ac.smooth_all( context )
		'''
		return {'FINISHED'}
		#return write_some_data(context, self.filepath, self.select_only)



class ExportAC(bpy.types.Operator, ExportHelper):
	bl_idname = "export_scene.export_ac"  # this is important since its how bpy.ops.export.some_data is constructed
	bl_label = "Export .ac"
	bl_options = {'PRESET'}	

	# ExportHelper mixin class uses this
	filename_ext = ".ac"

	filter_glob = StringProperty(default="*.ac", options={'HIDDEN'})

	# List of operator properties, the attributes will be assigned
	# to the class instance from the operator settings before calling.
	#use_setting = BoolProperty(name="Example Boolean", description="Example Tooltip", default=True)
	#filepath = bpy.props.StringProperty(name="File Path", maxlen=1024, default="")

	select_only 		= BoolProperty(name="Selection only", description="Export selected objects only", default=True)
	#tex_path			= BoolProperty(name="Path in texture name", description="Path name in texture name", default=False)
	apply_modifiers		= BoolProperty(name="Apply modifiers", description="Apply modifiers in meshes", default=False)

		
	@classmethod
	def poll(cls, context):
		return context.active_object != None

	def execute(self, context):
		from . import export_ac
		#export_ac.write_ac_file(context, self.filepath, select_only=self.select_only, tex_path=self.tex_path,apply_modifiers=self.apply_modifiers  )
		export_ac.write_ac_file(context, self.filepath, select_only=self.select_only, apply_modifiers=self.apply_modifiers  )
		return {'FINISHED'}



'''
====================================================================================================================



				REGISTER


====================================================================================================================
'''





# Only needed if you want to add into a dynamic menu



# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportAC.bl_idname, text="AC3D format (.ac)")		# text=Title in the menu

def menu_func_export(self, context):
    self.layout.operator(ExportAC.bl_idname, text="AC3D format (.ac)")		# text=Title in the menu


def register():
    bpy.utils.register_module(__name__)
    #bpy.utils.register_class(PanelOne)

    bpy.types.INFO_MT_file_import.append(menu_func_import)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)
    #bpy.utils.unregister_class(PanelOne)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
	try:
		unregister()
	except:
		pass
	register()
	
