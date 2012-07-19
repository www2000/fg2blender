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
#									OPS_FLIGHTGEAR.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy
import xml.dom.minidom

from . import *

from mathutils import Vector

from math import radians
from math import degrees
from math import acos


from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import CollectionProperty

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
			obj.lock_location = ( True, False, True )
			bpy.ops.object.posemode_toggle()


			obj.data.fg.type_anim		= 2
			obj.data.fg.xml_file		= ""
			obj.data.fg.xml_file_no		= 0
			obj.data.fg.familly			= "custom"
			obj.data.fg.familly_value	= "error"
			obj.data.fg.property_value	= ""
			obj.data.fg.property_idx	= -1
			obj.data.fg.time			= 2.5
			obj.data.fg.range_beg		= 0.0
			obj.data.fg.range_beg_ini	= 0.0
			obj.data.fg.range_end		= 1.0
			obj.data.fg.range_end_ini	= 1.0
			obj.data.fg.factor			= 1.0
			obj.data.fg.factor_ini		= 1.0
			obj.data.fg.offset_deg		= 0.0

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
			print("\tActivation des limites en local")
			limit_rotation = bpy.data.objects[obj.name].pose.bones[-1].constraints[-1]
			limit_rotation.use_limit_x = True
			limit_rotation.use_limit_y = False
			limit_rotation.use_limit_z = True
			limit_rotation.owner_space = 'LOCAL'

			bpy.data.objects[obj.name].pose.bones[-1].rotation_mode = 'XYZ'
			bpy.data.objects[obj.name].pose.bones[-1].lock_rotation = ( True, False, True )
			bpy.ops.object.posemode_toggle()
			
			obj.lock_rotation = ( True, False, True )
			
			obj.data.fg.type_anim		= 1
			obj.data.fg.xml_file		= ""
			obj.data.fg.xml_file_no		= 0
			obj.data.fg.familly			= "custom"
			obj.data.fg.familly_value	= "error"
			obj.data.fg.property_value	= ""
			obj.data.fg.property_idx	= -1
			obj.data.fg.time			= 2.5
			obj.data.fg.range_beg		= 0.0
			obj.data.fg.range_beg_ini	= 0.0
			obj.data.fg.range_end		= 1.0
			obj.data.fg.range_end_ini	= 1.0
			obj.data.fg.factor			= 1.0
			obj.data.fg.factor_ini		= 1.0
			obj.data.fg.offset_deg		= 0.0

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
		from . import xml_manager
		xml_manager.create_anims()
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

class FG_OT_select_property(bpy.types.Operator):
	'''Add edge split sor select object '''
	bl_idname = "view3d.select_property"
	bl_label = "Edge split"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type in( 'MESH','ARMATURE')

	def execute(self, context):
		import bpy
		import mathutils
		from math import radians
		#-------------------------------------------------------------------
		def select_childs( parent ):
			for obj in bpy.data.objects:
				if not obj.parent:
					continue
				if obj.parent.name == parent.name:
					o = obj
					o.select=True
					select_childs( o )
		#-------------------------------------------------------------------
		def find_armature( obj ):
			o = obj
			while o.parent:
				if o.parent.type == 'ARMATURE':
					return o.parent
				o = o.parent
			return None
		#-------------------------------------------------------------------
		print( '--- Select property  ---' )
		for obj in context.selected_objects:
			if obj.type != 'ARMATURE':
				obj = find_armature( obj )
				if not obj:
					continue
			if obj.type != 'ARMATURE':
				continue
			property_name =  obj.data.fg.property_value
			print( property_name )
			for o in bpy.data.objects:
				if o.type == 'ARMATURE':
					if o.data.fg.property_value == property_name:
						
						select_childs( o )
						o.select = True
				
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_select_file(bpy.types.Operator):
	bl_idname = "object.file_select"
	bl_label = ""

	#filepath = bpy.props.StringProperty(subtype="FILE_PATH")
	filepath = bpy.props.StringProperty()
	filter_glob = StringProperty(default="*.xml", options={'HIDDEN'})
	

	def execute(self, context):
		obj = context.active_object

		if obj.type == 'ARMATURE':
			obj.data.fg.xml_file = self.filepath
		
		#context.window_manager.fileselect_add(self)
		return {'FINISHED'}

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		#print( self.filepath )
		#return {'FINISHED'}
		return {'RUNNING_MODAL'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_only_render(bpy.types.Operator):
	bl_idname = "fg.only_render"
	bl_label = ""

	def execute(self, context):
		#print( self.filepath)
		return {'FINISHED'}

	def invoke(self, context, event):
		#print( context.space_data.type )
		if context.space_data.type=='VIEW_3D':
			context.space_data.show_only_render = not  context.space_data.show_only_render
		#return {'FINISHED'}
		return {'RUNNING_MODAL'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_time_2x(bpy.types.Operator):
	bl_idname = "view3d.time_2x"
	bl_label = ""

	def invoke(self, context, event):
		end = context.scene.frame_end
		old = context.scene.render.frame_map_old
		new = context.scene.render.frame_map_new
		if new == 100.0:
			end = context.scene.frame_end = 60.0
			old = context.scene.render.frame_map_old = 60.0
			new = context.scene.render.frame_map_new = 60.0

		context.scene.frame_end = new *0.5
		context.scene.render.frame_map_old = old
		context.scene.render.frame_map_new = new *0.5
		return {'FINISHED'}
		return {'RUNNING_MODAL'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_time_0_5x(bpy.types.Operator):
	bl_idname = "view3d.time_0_5x"
	bl_label = ""

	def invoke(self, context, event):
		end = context.scene.frame_end
		old = context.scene.render.frame_map_old
		new = context.scene.render.frame_map_new
		if new == 100.0:
			end = context.scene.frame_end = 60.0
			old = context.scene.render.frame_map_old = 60.0
			new = context.scene.render.frame_map_new = 60.0

		context.scene.frame_end = new *2.0
		context.scene.render.frame_map_old = old
		context.scene.render.frame_map_new = new * 2.0
		return {'FINISHED'}
		return {'RUNNING_MODAL'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_write_xml(bpy.types.Operator):
	bl_idname = "view3d.write_xml"
	bl_label = "Write File"
	
	#filename = bpy.props.StringProperty()
	obj_name = bpy.props.StringProperty()
	#objet = None
	
	#---------------------------------------------------------------------------
	def exist_in_text_editor(self, name ):
		for text in bpy.data.texts:
			if text.name == name:
				return True
		return False
	#---------------------------------------------------------------------------

	def creer_xml(self, filename):
		new_filename = ""
		new_no = 0
		for xml_file, no in xml_manager.xml_files:
			if xml_file.name == filename:
				new_filename = filename
				new_no		 = no
				break;
		
		if new_filename == "":
			no = len(xml_manager.xml_files)
			xml_file = xml_manager.XML_FILE()
			new_filename = filename
			new_no		 = no
			xml_manager.add_xml_file( new_filename, new_no )

		obj = bpy.data.objects[self.obj_name]
		obj.data.fg.xml_file	= new_filename
		obj.data.fg.xml_file_no	= new_no
	#---------------------------------------------------------------------------

	def charge_xml(self, context, filename, no):
		from .xml_import import charge_xml
		from . import xml_export
		from . import xml_import

		#if len(xml_manager.xml_files)<1:
		#	return
			
		name = os.path.basename( filename )
		script_name = name +'.script'
		
		if self.exist_in_text_editor( script_name ):
			bpy.data.texts[script_name].clear()
		else:
			#bpy.ops.text.new( name )
			bpy.data.texts.new( script_name )

		node = xml_import.charge_xml( filename )

		if node == None:
			node = xml.dom.minidom.Document()
			prop_list = node.createElement( 'PropertyList' )
			node.appendChild( prop_list )
			print( name )
			print( script_name )
			#return
		xml_export.write_animation_all( context, node, name, no )
		bpy.data.texts[script_name].use_tabs_as_spaces = True
		bpy.data.texts[script_name].write( node.toprettyxml() )
		#bpy.data.texts[name].write( node.toxml() )
	#---------------------------------------------------------------------------
	def execute( self, context ):
		if self.filename != "":
			print( self.filename )
			self.charge_xml( self.filename )
		return {'FINISHED'}

	#---------------------------------------------------------------------------

	def invoke(self, context, event):
		print( self.obj_name )
		obj = bpy.data.objects[self.obj_name]
		filename = obj.data.fg.xml_file
		no		 = obj.data.fg.xml_file_no
		print( filename )
		#filename = self.filename
		if filename == "":
			filename = xml_manager.xml_files[0][0].name
		
		if filename.find('Aircraft')!=-1:
			right_name = filename.partition('Aircraft')[2]
			name_path = '/media/sauvegarde/fg-2.6/install/fgfs/fgdata/Aircraft/' + right_name
		else:
			if not xml_manager.exist_xml_file( filename, no ):
				self.creer_xml( filename )
			name_path	= filename 
			no			= obj.data.fg.xml_file_no
		self.charge_xml( context, name_path, no )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_unwrap_4_faces(bpy.types.Operator):
	'''C'est un exemple d'operateur blender '''
	bl_idname = "view3d.unwrap_4_faces"					# sera appelé par bpy.ops.view3d.exemple()
	bl_label = "Exemple d'operateur"
	bl_options = {'REGISTER', 'UNDO'}


	#---------------------------------------------------------------------------
	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type in( 'MESH')

	#---------------------------------------------------------------------------

	def invoke(self, context, event):
		#---------------------------------------------------------------------------

		def compute_uv_up( indices, vertices, uvtex, idx, mat, bb, dim, coef,  _max, decal ):
			dim = m * dim
			
			w = dim
			print( "dimension x=%0.2f y=%0.2f z=%0.2f" % (w.x,w.y,w.z) )
			for i in range(8):
				w = Vector( (bb[i][0],bb[i][1],bb[i][2]) )
				print( "ind  %d      bb x=%0.2f y=%0.2f z=%0.2f" % (i, w.x,w.y,w.z) )

			b = Vector( (bb[0][0],bb[0][1],bb[0][2]) )
			w = Vector( (bb[6][0],bb[6][1],bb[6][2]) )

			b = m * b
			w = m * w

			j = 0
			for i in indices:
				v = vertices[i].co
				w = m * v
				print( "vertice x=%0.2f y=%0.2f z=%0.2f" % (v.x,v.y,v.z) )
				u = (w.x-b.x)/coef
				v = (w.y-b.y)/coef
				print( "uv  u=%0.2f v=%0.2f" % (u,v) )
				if u >decal:
					decal = u
				
				uvtex.data[idx+j].uv = ( 0.0+u + _max, v )
				j = j + 1
			return decal
		#---------------------------------------------------------------------------

		def compute_uv_down( indices, vertices, uvtex, idx, mat, bb, dim, coef,  _max, decal  ):
			dim = m * dim
			
			w = dim

			b = Vector( (bb[0][0],bb[0][1],bb[0][2]) )
			w = Vector( (bb[6][0],bb[6][1],bb[6][2]) )

			b = m * b
			w = m * w

			j = 0
			for i in indices:
				v = vertices[i].co
				w = m * v
				print( "vertice x=%0.2f y=%0.2f z=%0.2f" % (v.x,v.y,v.z) )
				u = (w.x-b.x)/coef
				v = (w.y-b.y)/coef
				print( "uv  u=%0.2f v=%0.2f" % (u,v) )
				if u >decal:
					decal = u
				
				uvtex.data[idx+j].uv = ( 0.0+u + _max, v )
				j = j + 1
			return decal
		#---------------------------------------------------------------------------
		
		def compute_uv_left( indices, vertices, uvtex, idx, mat, bb, dim, coef,  _max, decal  ):
			dim = m * dim
			
			w = dim

			b = Vector( (bb[0][0],bb[0][1],bb[0][2]) )
			w = Vector( (bb[6][0],bb[6][1],bb[6][2]) )

			b = m * b
			w = m * w

			j = 0
			for i in indices:
				v = vertices[i].co
				w = m * v
				print( "vertice x=%0.2f y=%0.2f z=%0.2f" % (v.x,v.y,v.z) )
				u = -(w.z-b.z)/coef
				v = (w.y-b.y)/coef
				print( "uv  u=%0.2f v=%0.2f" % (u,v) )
				if u >decal:
					decal = u
				
				uvtex.data[idx+j].uv = ( 0.0+u + _max, v )
				j = j + 1
			return decal
		#---------------------------------------------------------------------------

		def compute_uv_right( indices, vertices, uvtex, idx, mat, bb, dim, coef,  _max, decal  ):
			dim = m * dim
			
			w = dim

			b = Vector( (bb[0][0],bb[0][1],bb[0][2]) )
			w = Vector( (bb[6][0],bb[6][1],bb[6][2]) )

			b = m * b
			w = m * w
			

			j = 0
			for i in indices:
				v = vertices[i].co
				w = m * v
				print( "vertice x=%0.2f y=%0.2f z=%0.2f" % (v.x,v.y,v.z) )
				u = -(w.z-b.z)/coef
				v = (w.y-b.y)/coef
				print( "uv  u=%0.2f v=%0.2f" % (u,v) )
				if u >decal:
					decal = u
				
				uvtex.data[idx+j].uv = ( 0.0+u + _max, v )
				j = j + 1
			return decal
	#---------------------------------------------------------------------------

		_max = 0
		
		obj = context.active_object
		up		= Vector( (0.0,0.0,1.0) )
		front	= Vector( (1.0,0.0,0.0) )
		m = obj.matrix_world

		mesh = obj.data
		mesh.uv_textures.new()
		uvtex = mesh.uv_layers.active
		bb = obj.bound_box
		dim = obj.dimensions
		#bb = m * bb
		#dim = m * dim
		idx = 0

		coef = dim.x
		if dim.y > coef:
			coef = dim.y
		if dim.z > coef:
			coef = dim.z
		
		coef = -coef
		decal = 0		
		for polygon in obj.data.polygons:
			if not polygon.select:
				idx = idx + len(polygon.vertices)
				continue
			n = Vector( (0.0,0.0,0.0) ) + polygon.normal
			n.normalize()
			v = m * n
			#v.normalize()
			#v = n
			angle =  degrees( up.angle(v) )
			
			uv = Vector( (0.0,0.0) )
			if angle < 45:# or angle >= 360-45:
				print( "------------------------------------" )
				print( "Normal x=%0.2f y=%0.2f z=%0.2f" % (v.x,v.y,v.z) )
				print( "dot=%0.2f" % angle )
				decal = compute_uv_up( polygon.vertices, mesh.vertices, uvtex, idx, m, bb, dim, coef,  _max, decal )
				print( 'Up decal %0.2f' % decal )
			idx = idx + len(polygon.vertices)
				
		_max = _max + decal
		
		idx = 0
		decal = 0		
		for polygon in obj.data.polygons:
			if not polygon.select:
				idx = idx + len(polygon.vertices)
				continue
			n = Vector( (0.0,0.0,0.0) ) + polygon.normal
			n.normalize()
			v = m * n
			#v.normalize()
			#v = n
			angle =  degrees( up.angle(v) )
			
			uv = Vector( (0.0,0.0) )
			
			if 135 < angle and angle <= 225:
				print( "------------------------------------" )
				print( "Normal x=%0.2f y=%0.2f z=%0.2f" % (v.x,v.y,v.z) )
				print( "dot=%0.2f" % angle )
				decal = compute_uv_down( polygon.vertices, mesh.vertices, uvtex, idx, m, bb, dim, coef,  _max, decal )
				print( 'Down decal %0.2f' % decal )
			idx = idx + len(polygon.vertices)

		
		_max = _max + decal
		idx = 0
		decal = 0		
		for polygon in obj.data.polygons:
			if not polygon.select:
				idx = idx + len(polygon.vertices)
				continue
			n = Vector( (0.0,0.0,0.0) ) + polygon.normal
			n.normalize()
			v = m * n
			angle =  degrees( up.angle(v) )
			
			uv = Vector( (0.0,0.0) )
			if angle < 45 or angle > 360-45:
				idx = idx + len(polygon.vertices)
				continue
			elif 135 < angle and angle < 225 :
				idx = idx + len(polygon.vertices)
				continue
			else:
				angle = degrees( front.angle(v) )
				if angle < 90 and angle >= 0:
					decal = compute_uv_right( polygon.vertices, mesh.vertices, uvtex, idx, m, bb, dim, coef,  _max, decal )
					print( "dot=%0.2f" % angle )
					print( 'Right' )
			idx = idx + len(polygon.vertices)
		
		_max = _max + decal
		idx = 0
		decal = 0		
		for polygon in obj.data.polygons:
			if not polygon.select:
				idx = idx + len(polygon.vertices)
				continue
			n = Vector( (0.0,0.0,0.0) ) + polygon.normal
			n.normalize()
			v = m * n
			#v.normalize()
			#v = n
			angle =  degrees( up.angle(v) )
			
			if angle < 45 or angle > 360-45:
				idx = idx + len(polygon.vertices)
				continue
			elif angle < 225 and angle > 135:
				idx = idx + len(polygon.vertices)
				continue
			else:
				angle = degrees( front.angle(v) )
				if angle < 90 and angle >= 0:
					idx = idx + len(polygon.vertices)
					continue
				else:
					compute_uv_left( polygon.vertices, mesh.vertices, uvtex, idx, m, bb, dim, coef,  _max, decal )
					print( "dot=%0.2f" % angle )
					print( 'Left' )
			idx = idx + len(polygon.vertices)

		#bpy.data.objects['Cube'].data.polygons[1].normal
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_exemple(bpy.types.Operator):
	'''C'est un exemple d'operateur blender '''
	bl_idname = "view3d.exemple"					# sera appelé par bpy.ops.view3d.exemple()
	bl_label = "Exemple d'operateur"
	bl_options = {'REGISTER', 'UNDO'}
	'''
	@classmethod
	def poll(cls, context):
		return True
	'''
	def execute(self, context):						# executé lors de l'appel par bpy.ops.view3d.exemple()
		# ce que l'on veut faire
		print( "HelloWord" )
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class( FG_OT_edges_split)
	bpy.utils.register_class( FG_OT_select_property)
	bpy.utils.register_class( FG_OT_create_anim)
	bpy.utils.register_class( FG_OT_create_rotate)
	bpy.utils.register_class( FG_OT_create_translate)
	bpy.utils.register_class( FG_OT_exemple)
	bpy.utils.register_class( FG_OT_select_file )
	bpy.utils.register_class( FG_OT_only_render )
	bpy.utils.register_class( FG_OT_time_0_5x )
	bpy.utils.register_class( FG_OT_time_2x )
	bpy.utils.register_class( FG_OT_write_xml )
	bpy.utils.register_class( FG_OT_unwrap_4_faces )

def unregister():
	bpy.utils.unregister_class( FG_OT_edges_split)
	bpy.utils.unregister_class( FG_OT_select_property)
	bpy.utils.unregister_class( FG_OT_create_anim)
	bpy.utils.unregister_class( FG_OT_create_rotate)
	bpy.utils.unregister_class( FG_OT_create_translate)
	bpy.utils.unregister_class( FG_OT_exemple)
	bpy.utils.unregister_class( FG_OT_select_file )
	bpy.utils.unregister_class( FG_OT_only_render )
	bpy.utils.unregister_class( FG_OT_time_0_5x )
	bpy.utils.unregister_class( FG_OT_time_2x )
	bpy.utils.unregister_class( FG_OT_write_xml )
	bpy.utils.unregister_class( FG_OT_unwrap_4_faces )

