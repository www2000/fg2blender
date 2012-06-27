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

		row = layout.row()
		row.label( text = "Option xml" )
		box_option_xml = layout.box()
		row = box_option_xml.column()
		#row.label( text = "Option xml" )
		row.prop( self, "include" )


	def execute(self, context):

		paths = [os.path.join(self.directory, name.name)	for name in self.files]
			
		from .xml_import import import_xml
		for filename in paths:
			print( filename )
			ac_option = AC_OPTION()
			ac_option.smooth_all	= self.smooth_all
			ac_optionedge_split		= self.edge_split
			ac_optionsplit_angle	= self.split_angle
		
			xml_option = XML_OPTION()
			xml_option.include		= self.include
		
			f = open('/home/rene/tmp/blender/script-fg2bl', mode='w')
			f.write( filename )
			#f.write( '\n' )
			f.close()

			import_xml(	filename, ac_option, xml_option )
		
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
	include		= BoolProperty(name="Include file", description="Read file include", default=True)

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
		'''
		row = layout.row()
		row.label( text = "Option xml" )
		box_option_xml = layout.box()
		row = box_option_xml.column()
		#row.label( text = "Option xml" )
		row.prop( self, "include" )
		'''

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
		
			f = open('~/tmp/blender/script-fg2bl', 'w')
			f.write( filename )
			t.close()
			
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


#----------------------------------------------------------------------------------------------------------------------------------
#
#							Register shortcut
#
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_translate(bpy.types.Operator):
	'''Add armature type translate '''
	bl_idname = "view3d.create_translate"
	bl_label = "Create Translate"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return True
		return context.active_object != None

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians

		print( "Create_translate : " )
		armature = bpy.ops.object.armature_add( view_align=True )
		armature = bpy.data.armatures[-1]
		print( armature.name )
		for obj in bpy.data.objects:
			if obj.type != 'ARMATURE':
				continue
			if obj.data.name == armature.name:
				break 
		if obj.type == 'ARMATURE':
			print( "\tSelecion de : %s" %(obj.name) )
			#bpy.ops.object.select_pattern(pattern=obj.name)
			context.scene.objects.active = obj

			bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

			print("\tActivation Pose Mode")
			bpy.ops.object.posemode_toggle()
			bpy.ops.pose.select_all( action='SELECT' )
			print("\tAjout limite location")
			bpy.ops.pose.constraint_add(type='LIMIT_LOCATION')

			print("\tActivation des limites en local")
			limit_translate = bpy.data.objects[obj.name].pose.bones[-1].constraints[-1]
			limit_translate.use_min_x = True
			limit_translate.use_max_x = True
			limit_translate.use_min_y = False
			limit_translate.use_max_y = False
			limit_translate.use_min_z = True
			limit_translate.use_max_z = True
			limit_translate.owner_space = 'LOCAL'
			bpy.ops.object.posemode_toggle()

			print("\tDesactivation Pose Mode")
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_rotate(bpy.types.Operator):
	'''Add armature type rotate '''
	bl_idname = "view3d.create_rotate"
	bl_label = "Create Rotate"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return True
		return context.active_object != None

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians

		print( "Create_rotate : " )
		armature = bpy.ops.object.armature_add( view_align=True )
		armature = bpy.data.armatures[-1]
		print( armature.name )
		for obj in bpy.data.objects:
			if obj.type != 'ARMATURE':
				continue
			if obj.data.name == armature.name:
				break 
		if obj.type == 'ARMATURE':
			print( "\tSelecion de : %s" %(obj.name) )
			#bpy.ops.object.select_pattern(pattern=obj.name)
			context.scene.objects.active = obj

			#bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

			print("\tActivation Pose Mode")
			bpy.ops.object.posemode_toggle()
			bpy.ops.pose.select_all( action='SELECT' )
			print("\tAjout limite rotation")
			bpy.ops.pose.constraint_add(type='LIMIT_ROTATION')

			print("\tMatrice en mode EulerXYZ")
			bpy.data.objects[obj.name].pose.bones[-1].rotation_mode = 'XYZ'
			print("\tActivation des limites en local")
			limit_rotation = bpy.data.objects[obj.name].pose.bones[-1].constraints[-1]
			limit_rotation.use_limit_x = True
			limit_rotation.use_limit_y = False
			limit_rotation.use_limit_z = True
			limit_rotation.owner_space = 'LOCAL'
			bpy.ops.object.posemode_toggle()

			print("\tDesactivation Pose Mode")
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_create_anim(bpy.types.Operator):
	'''Add armature type rotate '''
	bl_idname = "view3d.create_anim"
	bl_label = "Create Annimation"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		xml_manager.create_anims()
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_assign_anim(bpy.types.Operator):
	'''Add armature type rotate '''
	bl_idname = "view3d.assign_anim"
	bl_label = "Assign animation"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		xml_manager.assign_anims()
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_edges_split(bpy.types.Operator):
	'''Add edge split sor select object '''
	bl_idname = "view3d.edge_split"
	bl_label = "Edge split"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type == 'MESH'#None

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians

		print( "Smooth Object : " )
		list_objects = context.selected_objects
		active_object =	context.scene.objects.active
		for obj in bpy.data.objects:
			obj.select = False

		for obj in list_objects:
			if obj.type == 'MESH':
				obj.select = True
				context.scene.objects.active = obj
				angle = obj.data.auto_smooth_angle
				print( "\tObject : %s    angle=%0.2f" % (obj.name,degrees(angle)) )

				try:
					bpy.ops.object.modifier_add( type='EDGE_SPLIT')	
					for mod in obj.modifiers:
						if mod.type=='EDGE_SPLIT':
							mod.split_angle = angle
				except:
					print( "Erreur modifier_add Edge-split" )

				obj.select = False

		for obj in list_objects:
			obj.select = True
		context.scene.objects.active = active_object

				
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_root_menu(bpy.types.Menu):
    bl_label = "Flightgear Tools Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        #layout.menu("VIEW3D_FG_root_menu")
        layout.separator()
        layout.operator("view3d.edge_split",		text='Edge-split' )
        layout.operator("view3d.create_anim",		text='Creation animations' )
        #layout.operator("view3d.assign_anim",		text='Assigne animations' )
        layout.separator()
        layout.operator("view3d.create_rotate",		text='Define Rotation' )
        layout.operator("view3d.create_translate",	text='Define Translation' )
        layout.separator()
#----------------------------------------------------------------------------------------------------------------------------------

class VIEW3D_FG_sub_menu_0(bpy.types.Menu):
    bl_label = "Assign Material"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        for material_name in bpy.data.materials.keys():
            layout.operator("view3d.assign_material",
                text=material_name,
                icon='MATERIAL_DATA').matname = material_name

        layout.operator("view3d.assign_material",
                        text="Add New",
                        icon='ZOOMIN')
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_exec(bpy.types.Operator):
	global path
	global nLayer, nLayerBone
	
	bl_idname = "fg.exec"
	bl_label = "fg.exec"

	#from io_scene_xplane import layer
	
	def execute(self, context ):
		from .ac_manager import AC_OPTION
		from .xml_manager import XML_OPTION
		from .xml_import import import_xml

		ac_option = AC_OPTION()
		ac_option.smooth_all	= True
		ac_optionedge_split		= True
		ac_optionsplit_angle	= True
	
		xml_option = XML_OPTION()
		xml_option.include		= True
	
			
		f = open('/home/rene/tmp/blender/script-fg2bl', mode='r')
		filename = f.readline()
		f.close()
		
		import_xml( filename, ac_option, xml_option )
			 
		return {'FINISHED'}
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
    km = kc.keymaps["3D_View_xplane"]
    for kmi in km.keymap_items:
        if kmi.idname == 'fg.exec':
            km.keymap_items.remove(kmi)
        if kmi.idname == 'fg.exec':
            km.keymap_items.remove(kmi)
            #if kmi.properties.name ==  "XPLANE_OT_exec":
            #    break
#----------------------------------------------------------------------------------------------------------------------------------


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

#def menu_func_export(self, context):
#    self.layout.operator(ExportFG.bl_idname, text="Flightgear (.xml)")		# text=Title in the menu


def register():
    bpy.utils.register_class(ImportFG)
    bpy.utils.register_class(ImportAC)
    bpy.utils.register_class(FG_OT_exec)
    bpy.utils.register_class(VIEW3D_FG_root_menu)
    bpy.utils.register_class(FG_OT_edges_split)
    bpy.utils.register_class(FG_OT_create_anim)
    bpy.utils.register_class(FG_OT_assign_anim)
    bpy.utils.register_class(FG_OT_create_rotate)
    bpy.utils.register_class(FG_OT_create_translate)
    register_shortcut()
    #bpy.utils.register_class(ExportFG)

    bpy.types.INFO_MT_file_import.append(menu_func_import)
    #bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ImportFG)
    bpy.utils.unregister_class(ImportAC)
    bpy.utils.unregister_class(FG_OT_exec)
    bpy.utils.unregister_class(VIEW3D_FG_root_menu)
    bpy.utils.unregister_class(FG_OT_edges_split)
    bpy.utils.unregister_class(FG_OT_create_anim)
    bpy.utils.unregister_class(FG_OT_assign_anim)
    bpy.utils.unregister_class(FG_OT_create_rotate)
    bpy.utils.unregister_class(FG_OT_create_translate)
    unregister_shortcut()
    #bpy.utils.unregister_class(ExportAC)

    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    #bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
	try:
		unregister()
	except:
		pass
	register()
	
