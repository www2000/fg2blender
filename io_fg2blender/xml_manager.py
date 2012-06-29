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
#									XML_MANAGER.PY
#
#----------------------------------------------------------------------------------------------------------------------------------
import xml.dom.minidom

from mathutils import Vector
from mathutils import Euler

from . import *

from .ac_manager import AC_FILE

#----------------------------------------------------------------------------------------------------------------------------------

xml_files = []
xml_current = None


DEBUG = False
BIDOUILLE = False
#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS XML_OPTION
#----------------------------------------------------------------------------------------------------------------------------------
#	Option for xml parser file
#----------------------------------------------------------------------------------------------------------------------------------

class XML_OPTION:
	def __init__(self):
		self.include		= False
		self.active_layer	= True
		self.layer_beg		= 1
		self.layer_end		= 20

#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS XML_FILE
#----------------------------------------------------------------------------------------------------------------------------------
#	name				= "plane.xml"						string	xml file name
#	ac_names			= [ fuse.ac" , "wings.ac" , ...]	List of string   ac name file
#	ac_files			= [ AC_FILE(), AC_FILE() , ... ]	List of ac_file object
#	offset				= ( 0.0 , 0.0 , 0.0 )				mathutils.Vector		
#	eulerXYZ			= ( 0.0 , 0.0 , 0.0 )				mathutils.Vector  for "euler" transform (for pich-deb,roll-deg, etc)
#	parent_offset		= ( 0.0 , 0.0 , 0.0 )				parent location
#	parent_eulerXYZ		= ( 0.0 , 0.0 , 0.0 )				parent rotation
#	file_offset 		= "include.xml"						strings    where xml define offset (parent file name)   (not use)
#	anims				= [ ANIM() , ANIM() , ... ]			List of ANIM  object
#----------------------------------------------------------------------------------------------------------------------------------

class XML_FILE:
	def __init__(self):
		self.name				= ""
		self.ac_names			= []
		self.ac_files			= []
		self.offset				= Vector( (0.0, 0.0, 0.0) )
		self.eulerXYZ			= Vector( (0.0, 0.0, 0.0) )
		self.parent_offset		= Vector( (0.0, 0.0, 0.0) )
		self.parent_eulerXYZ	= Vector( (0.0, 0.0, 0.0) )
		self.anims				= []
		self.file_offset		= ""

		
	def add_ac_file( self, ac_file = None ):
		if ac_file:
			self.ac_files.append( ac_file )
			self.ac_names.append( ac_file.name )
#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS ANIM
#----------------------------------------------------------------------------------------------------------------------------------
#	name				= "plane"							string	if transform name
#	type				= 0									1:Rotate  2:translate  3: group objects
#	xml_file			= ""								string : xml  file
#	factor				= 0.0
#	property			= ""								string : flightgear property of transform
#	pos					= Vector( (0.0, 0.0, 0.0) )			bone location
#	vec					= Vector( (0.0, 0.0, 0.0) )			bone vector
#	objects				= []								objects list  ( name in xml file )
#	group_objects		= []								list : group_objects[0] name of group
#----------------------------------------------------------------------------------------------------------------------------------

class ANIM:
	def __init__(self):
		self.name				= ""
		self.type				= 0								# 1:Rotate 2:translate 3: group objects 4: pick
		self.xml_file			= ""
		self.factor				= 0.0
		self.interpolation		= []
		self.property			= ""
		self.pos				= Vector( (0.0, 0.0, 0.0) )
		self.vec				= Vector( (0.0, 0.0, 0.0) )
		self.objects			= []
		self.group_objects		= []
	#---------------------------------------------------------------------------------------------------------------------

	def extract_type( self, node ):
		from .xml_import import ret_text_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('type')
		if childs:
			for child in childs:
				if child.hasChildNodes():
					value = ret_text_value(child)
					if value == 'rotate':
						self.type = 1
					elif value == 'translate':
						self.type = 2
					elif value == 'pick':
						self.type = 4
		else:
			childs = node.getElementsByTagName('name')
			if childs:
				self.type = 3
	#---------------------------------------------------------------------------------------------------------------------

	def extract_name( self, node ):
		from .xml_import import ret_text_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('name')
		if childs:
			self.name = ret_text_value(childs[0])
			debug_info( "\t%sName %s" % (tabs(),self.name) )
	#---------------------------------------------------------------------------------------------------------------------

	def extract_property( self, node ):
		from .xml_import import ret_text_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('property')
		if childs:
			self.property = ret_text_value(childs[0])
			debug_info( "\t%sProperty %s" % (tabs(),self.property) )
	#---------------------------------------------------------------------------------------------------------------------

	def extract_objects( self, node ):
		from .xml_import import ret_text_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('object-name')
		for child in childs:
			value = ret_text_value(child)
			self.objects.append( value )
			debug_info( "%s\tAppend object-name : %s" % (tabs(),value) )
	#---------------------------------------------------------------------------------------------------------------------

	def extract_group_objects( self, node ):
		from .xml_import import ret_text_value
		from .xml_import import tabs

		debug_info( "%s\tExtract group :" % (tabs()) )
		self.type = 3
		childs = node.getElementsByTagName('name')
		if childs:
			value = ret_text_value(childs[0])
			self.group_objects.append( value )
			debug_info( "%s\t\tCreation du group %s" % (tabs(),value) )
			childs = node.getElementsByTagName('object-name')
			for child in childs:
				value = ret_text_value(child)
				debug_info( "%s\t\tAjout de %s" % (tabs(),value) )
				self.group_objects.append( value )
	#---------------------------------------------------------------------------------------------------------------------
			
	def extract_head_tail( self, node ):
		from .xml_import import read_vector_axis
		from .xml_import import read_vector_axis_points
		from .xml_import import read_vector_center
		from .xml_import import tabs
		childs = node.getElementsByTagName('axis')
		for child in childs:
			if child.hasChildNodes():
				self.vec = read_vector_axis(child)
				#print( "%sAxe : %s" % (tabs(),str(self.vec)) )

		childs = node.getElementsByTagName('center')
		for child in childs:
			if child.hasChildNodes():
				self.pos = read_vector_center(child)
				#print( "%sCenter : %s" % (tabs(),str(self.pos)) )
		childs = node.getElementsByTagName('x1-m')
		if childs:
			self.vec = read_vector_axis_points(node)
			self.pos = read_vector_center(node)
			
		debug_info( "\t\tPos %s" % str(self.pos) )
		debug_info( "\t\tVec %s" % str(self.vec) )
	#---------------------------------------------------------------------------------------------------------------------
			
	def extract_factor( self, node ):
		from .xml_import import ret_float_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('factor')
		if childs:
		#if child.hasChildNodes():
			self.factor = ret_float_value(childs[0])
			debug_info( "%s\tFactor : %s" % (tabs(),str(self.factor)) )
		else:
			self.factor = 1.0
			debug_info( "%s\tFactor default: %s" % (tabs(),str(self.factor)) )
	#---------------------------------------------------------------------------------------------------------------------
			
	def extract_interpolation( self, node ):
		from .xml_import import ret_float_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('interpolation')
		if childs:
			debug_info( "%s\tInterpolation" % tabs() )
			childs_ind = childs[0].getElementsByTagName('ind')
			childs_dep = childs[0].getElementsByTagName('dep')
			for no, child_ind in list(enumerate(childs_ind)):
				ind = ret_float_value(child_ind)
				dep = ret_float_value(childs_dep[no])
				debug_info( "%s\t\tind : %s" % (tabs(),str( (ind, dep) ) ) )
				self.interpolation.append( (ind,dep) )
				
	#---------------------------------------------------------------------------------------------------------------------

	def extract_anim( self, node ):
		#---------------------------------------------------------------------------------------------------------------------

		def extract_anim_rotate( node ):
			from .xml_import import tabs

			debug_info( "%sExtract Rotate :" % (tabs()) )
			self.extract_name( node )
			self.extract_property( node )
			self.extract_objects( node )
			self.extract_head_tail( node )
			self.extract_factor( node )
			self.extract_interpolation( node )
			if self.type == 0:
				self.extract_group_objects( node )
		#---------------------------------------------------------------------------------------------------------------------

		def extract_anim_translate( node ):
			from .xml_import import tabs

			debug_info( "%sExtract Translate :" % (tabs()) )
			self.extract_name( node )
			self.extract_property( node )
			self.extract_objects( node )
			self.extract_head_tail( node )
			self.extract_factor( node )
			self.extract_interpolation( node )
			if self.type == 0:
				self.extract_group_objects( node )
		#---------------------------------------------------------------------------------------------------------------------

		def extract_pick( node ):
			from .xml_import import tabs

			debug_info( "%sExtract Pick :" % (tabs()) )
			self.extract_name( node )
			self.extract_property( node )
			self.extract_objects( node )
		#---------------------------------------------------------------------------------------------------------------------
		# pour recopier la valeur et non pas la référence
		self.xml_file = "" + xml_current.name
		self.extract_type( node )
		if self.type == 1:
			extract_anim_rotate( node )
		elif self.type == 2:
			extract_anim_translate( node )
		elif self.type == 3:
			self.extract_group_objects( node )
		elif self.type == 4:
			extract_pick( node )
	#---------------------------------------------------------------------------------------------------------------------

	def insert_keyframe_rotation( self, frame, value ):
		obj_armature = bpy.context.scene.objects.active
		bpy.ops.object.posemode_toggle()
	
		bpy.context.scene.frame_current = frame
		bpy.ops.pose.select_all( action='SELECT' )
		obj_armature.pose.bones[-1].rotation_mode = 'XYZ'
		obj_armature.pose.bones[-1].rotation_euler = Euler( (0.0, radians(value), 0.0), 'XYZ' )
	
		try:
			bpy.ops.anim.keyframe_insert_menu( type='Rotation')
		except:
			bpy.ops.anim.keying_set_add()
			bpy.ops.anim.keying_set_active_set()
			bpy.ops.anim.keyframe_insert_menu( type='Rotation')

		bpy.ops.object.posemode_toggle()
	#---------------------------------------------------------------------------------------------------------------------

	def insert_keyframe_rotation_all( self ):

		if len(self.interpolation) != 0:
			_min = 0.0
			_max = 0.0
			for ind, dep in self.interpolation:
				if ind > _max:
					_max = ind
				if ind < _min:
					_min = ind
			#if self.interpolation[0][1] > self.interpolation[-1][1]:
			self.interpolation.reverse()
			for ind, dep in self.interpolation:
				coef = _max - _min
				frame = (( (ind-_min) / coef ) * 59.0) + 1.0 
				value = dep * self.factor
				self.insert_keyframe_rotation(  frame, value )
		else:
			self.insert_keyframe_rotation( 60, self.factor )
			self.insert_keyframe_rotation(  1, 0.0 )

		bpy.context.scene.frame_current = 1
		bpy.context.scene.frame_end = 60
	#---------------------------------------------------------------------------------------------------------------------

	def insert_keyframe_translation( self, frame, value ):
		obj_armature = bpy.context.scene.objects.active
		bpy.ops.object.posemode_toggle()
	
		bpy.context.scene.frame_current = frame
		bpy.ops.pose.select_all( action='SELECT' )
		
		tr = Vector( (0.0,value,0.0) )

		obj_armature.pose.bones[-1].location = tr
		try:
			bpy.ops.anim.keyframe_insert_menu( type='Location')
		except:
			bpy.ops.anim.keying_set_add()
			bpy.ops.anim.keying_set_active_set()
			bpy.ops.anim.keyframe_insert_menu( type='Location')

		bpy.ops.object.posemode_toggle()
	#---------------------------------------------------------------------------------------------------------------------

	def insert_keyframe_translation_all( self ):
		obj_armature = bpy.context.scene.objects.active

		if len(self.interpolation) != 0:
			_min = 0.0
			_max = 0.0
			for ind, dep in self.interpolation:
				if ind > _max:
					_max = ind
				if ind < _min:
					_min = ind
			#if self.interpolation[0][1] > self.interpolation[-1][1]:
			self.interpolation.reverse()
			for ind, dep in self.interpolation:
				coef = _max - _min
				frame = (( (ind-_min) / coef ) * 59.0) + 1.0 
				value = dep * self.factor
				self.insert_keyframe_translation(  frame, value )
		else:
			self.insert_keyframe_translation( 60, self.factor )
			self.insert_keyframe_translation(  1, 0.0 )

		bpy.context.scene.frame_current = 1
		bpy.context.scene.frame_end = 60
	#---------------------------------------------------------------------------------------------------------------------

	def create_armature_rotation( self ):
		#print( "Context : %s" % bpy.context.mode )
		bpy.ops.object.armature_add()

		#print( "Context : %s" % bpy.context.mode )
		#bpy.context.scene.layers = layer( 10 )
		#bpy.context.scene.active_layer = 10
		bpy.ops.object.move_to_layer( layers = layer(10) )
		
		#armature = bpy.data.armatures.new( 'Armature')
		armature = bpy.data.armatures[-1]
		print( 'Create armature rotate : "%s"' % armature.name )
		debug_info( '\t\tFichier xml: "%s"' % os.path.basename(self.xml_file) )
		debug_info( "\t\tFactor %0.4f" % self.factor )
		debug_info( '\t\tProperty : "%s"' % self.property )
		debug_info( "\t\tPos %s" % str(self.pos) )
		debug_info( "\t\tVec %s" % str(self.vec) )
		debug_info( "\t\tObjects %s" % str(self.objects) )

		armature_name = armature.name 
        
		for obj in bpy.data.objects:
			if obj.type != 'ARMATURE':
				continue
			if obj.data.name == armature_name:
				obj_arma = obj_armature = obj

				break;

		if self.name != "":
			self.name = obj_arma.name
			#obj_arma.name = self.name
		else:
			self.name = obj_arma.name
				
		offset = Vector( (0.0,0.0,0.0) ) + xml_current.offset
		euler  = Vector( (0.0,0.0,0.0) ) + xml_current.eulerXYZ
				
		vec = self.vec /10.0
		#head = self.pos
		#tail = self.pos + vec
		head = Vector( (0.0,0.0,0.0) )
		tail = Vector( (0.0,0.0,0.0) ) + vec
		obj_arma.location = self.pos
		
		bpy.ops.object.editmode_toggle()

		bpy.context.object.data.edit_bones["Bone"].head = head #Vector( (0.0,0.0,0.0) ) #self.head
		bpy.context.object.data.edit_bones["Bone"].tail = tail #self.vec /10.0

		bpy.ops.object.editmode_toggle()

		obj_arma.delta_location = xml_current.offset
		obj_arma.delta_rotation_euler = Euler( (euler.x, euler.y, euler.z) )


		bpy.ops.object.posemode_toggle()
		bpy.ops.pose.select_all( action='SELECT' )
		bpy.ops.pose.constraint_add(type='LIMIT_ROTATION')

		bpy.data.objects[obj.name].pose.bones[-1].rotation_mode = 'XYZ'
		limit_rotation = bpy.data.objects[obj.name].pose.bones[-1].constraints[-1]
		limit_rotation.use_limit_x = True
		limit_rotation.use_limit_y = False
		limit_rotation.use_limit_z = True
		limit_rotation.owner_space = 'LOCAL'
		bpy.ops.object.posemode_toggle()
		
	#---------------------------------------------------------------------------------------------------------------------

	def create_armature_translation( self ):
		bpy.ops.object.armature_add()
		#bpy.context.scene.layers = layer( 10 )
		#bpy.context.scene.active_layer = 10
		bpy.ops.object.move_to_layer( layers = layer(10) )

		armature = bpy.data.armatures[-1]
		print( 'Create armature translate : "%s"' % armature.name )
		debug_info( '\t\tFichier xml: "%s"' % os.path.basename(self.xml_file) )
		debug_info( "\t\tFactor %0.4f" % self.factor )
		debug_info( '\t\tProperty : "%s"' % self.property )
		debug_info( "\t\tPos %s" % str(self.pos) )
		debug_info( "\t\tVec %s" % str(self.vec) )
		debug_info( "\t\tObjects %s" % str(self.objects) )

		armature_name = armature.name 
        
		for obj in bpy.data.objects:
			if obj.type != 'ARMATURE':
				continue
			if obj.data.name == armature_name:
				obj_arma = obj_armature = obj

				break;

		if self.name != "":
			self.name = obj_arma.name
			#obj_arma.name = self.name
		else:
			self.name = obj_arma.name
				
		offset = Vector( (0.0,0.0,0.0) ) + xml_current.offset
		euler  = Vector( (0.0,0.0,0.0) ) + xml_current.eulerXYZ
				
		vec = self.vec /10.0
		#head = self.pos
		#tail = self.pos + vec
		head = Vector( (0.0,0.0,0.0) )
		tail = Vector( (0.0,0.0,0.0) ) + vec
		obj_arma.location = self.pos
				
		bpy.ops.object.editmode_toggle()

		bpy.context.object.data.edit_bones["Bone"].head = head #Vector( (0.0,0.0,0.0) ) #self.head
		bpy.context.object.data.edit_bones["Bone"].tail = tail #self.vec /10.0

		bpy.ops.object.editmode_toggle()

		obj_arma.delta_location = xml_current.offset
		obj_arma.delta_rotation_euler = Euler( (euler.x, euler.y, euler.z) )


		bpy.ops.object.posemode_toggle()
		bpy.ops.pose.select_all( action='SELECT' )
		bpy.ops.pose.constraint_add(type='LIMIT_LOCATION')

		bpy.data.objects[obj.name].pose.bones[-1].rotation_mode = 'XYZ'
		limit_rotation = bpy.data.objects[obj.name].pose.bones[-1].constraints[-1]
		limit_rotation.use_min_x = True
		limit_rotation.use_min_y = False
		limit_rotation.use_min_z = True
		limit_rotation.use_max_x = True
		limit_rotation.use_max_y = False
		limit_rotation.use_max_z = True
		limit_rotation.owner_space = 'LOCAL'
		bpy.ops.object.posemode_toggle()
		
	#---------------------------------------------------------------------------------------------------------------------
	
	def insert_keyframe_all( self ):
		if self.type == 1:
			bpy.context.scene.objects.active = bpy.data.objects[self.name]
			self.insert_keyframe_rotation_all()
		elif self.type == 2:
			bpy.context.scene.objects.active = bpy.data.objects[self.name]
			self.insert_keyframe_translation_all()
	#---------------------------------------------------------------------------------------------------------------------

	def create_armature( self ):
		if self.type == 1:
			self.create_armature_rotation()
		if self.type == 2:
			self.create_armature_translation()
		if self.type == 4:
			self.create_pick()
	#---------------------------------------------------------------------------------------------------------------------
	def assign_pick( self, obj_name_bl ):
		obj = get_object( obj_name_bl )
		if obj:
			if obj.type == 'MESH':
				if not is_exist_matrial_pick(obj ):
					obj.data.materials.append( bpy.data.materials['Material_Pick'])
				obj.show_wire = True
				obj.show_transparent = True


	def create_pick( self ):
		for xml_file, no in xml_files:
			if xml_file.name == self.xml_file:
				break
		for obj_name_ac in self.objects:
			#print( 'xml file "%s"' % os.path.basename(xml_file.name) )
			#print( "Nb ac file : %d" % len(xml_file.ac_files) )
			
			if not obj_name_ac in xml_file.ac_files[0].dic_name_meshs:
				group_objects = find_group( obj_name_ac, xml_file )
				if group_objects:
					debug_info( '\tgroup : "%s"' % str(self.group_objects)  )
					for obj_name_bl in group_objects[1:]:
						print( 'Create Pick : "%s"' % obj_name_bl )
						self.assign_pick( obj_name_bl )
				else:
					print( '**** Erreur objet "%s" inconnu ***' % obj_name )
					continue
			else:
				obj_name_bl = xml_file.ac_files[0].dic_name_meshs[obj_name_ac]
				print( 'Create Pick : "%s"' % obj_name_bl )
				self.assign_pick( obj_name_bl )
#----------------------------------------------------------------------------------------------------------------------------------
#
#							END CLASS ANIM
#
#----------------------------------------------------------------------------------------------------------------------------------
# because blender problem    bpy.ops.object.select_pattern( obj_name )
def get_object( obj_name ):
	for obj in bpy.data.objects:
		if obj.name == obj_name:
			#print( 'pick "%s" == "%s"' % (obj.name, obj_name) )
			return obj
	return None
#----------------------------------------------------------------------------------------------------------------------------------

def is_exist_matrial_pick( obj ):
	for material in obj.data.materials:
		if material.name == 'Material_Pick':
			return True
	return False
#----------------------------------------------------------------------------------------------------------------------------------

def debug_info( aff):
	global DEBUG
	if DEBUG:
		print( aff )
#----------------------------------------------------------------------------------------------------------------------------------
# xml_files  = tule ( xml_file, no_include )
def add_xml_file( xml_file, no ):
	if xml_file:
		xml_files.append( (xml_file,no) )
#----------------------------------------------------------------------------------------------------------------------------------

def set_current_xml( xml_file=None ):
	global xml_current
	
	if xml_file:
		xml_current = xml_file
#----------------------------------------------------------------------------------------------------------------------------------

def get_current_xml():
	global xml_current
	
	return  xml_current
#----------------------------------------------------------------------------------------------------------------------------------

def is_defined( filename ):
	global xml_files
	
	for xml_file,no in xml_files:
		if xml_file.name == filename:
			return True
	return False
#----------------------------------------------------------------------------------------------------------------------------------

def isnot_defined( filename ):
	return not is_defined( filename )
#----------------------------------------------------------------------------------------------------------------------------------

def get_xml_file( filename, no_include ):
	global xml_files
	
	for xml_file, no in xml_files:
		if xml_file.name == filename and no_include == no:
			return xml_file
	return None
#----------------------------------------------------------------------------------------------------------------------------------

def is_load_ac( filename ):
	global xml_files

	for xml_file, no in xml_files:
		for ac_name in xml_file.ac_names:
			if ac_name == filename:
				return True
	return False
#----------------------------------------------------------------------------------------------------------------------------------

def get_ac_file( filename ):
	global xml_files

	for xml_file, no in xml_files:
		for ac_file in xml_file.ac_files:
			if ac_file.name == filename:
				return ac_file
	return None
#----------------------------------------------------------------------------------------------------------------------------------

def layer( No ):
	list_layer = []
	for i in range(20):
		if No == i:
			list_layer.append( True )
		else:
			list_layer.append( False )
	return list_layer
#----------------------------------------------------------------------------------------------------------------------------------

def create_material_pick():
	for material in bpy.data.materials:
		if material.name == "Material_Pick":
			return
		bl_mat = bpy.data.materials.new( 'Material_Pick' )

		bl_mat.emit				= 0.2
		bl_mat.type				= 'WIRE'
		bl_mat.use_transparency = True
		bl_mat.alpha			= 0.0
#----------------------------------------------------------------------------------------------------------------------------------

def create_anims():
	global xml_files
	
	create_material_pick()
	bpy.ops.view3d.layers( nr=11, extend=True, toggle = True )
	if not bpy.context.scene.layers[10]:
		bpy.ops.view3d.layers( nr=11, extend=True, toggle = True )

	#print( str(bpy.context) )
	for xml_file, no in xml_files:
		set_current_xml( xml_file )
		debug_info( xml_file.name )
		for anim in xml_file.anims:
			if anim.type != 1 and anim.type != 2 and anim.type != 4:
				continue
			anim.create_armature()

	for xml_file, no in xml_files:
		for ac_file in xml_file.ac_files:
			#debug_info( "\tCreation de groups %s" % os.path.basename(ac_file.name) )
			debug_info( 'Creation de groups "%s"' % os.path.basename(ac_file.name) )
			ac_file.create_group_ac()

	assign_obj_to_anim()

	for xml_file, no in xml_files:
		set_current_xml( xml_file )
		for anim in xml_file.anims:
			if anim.name=="":
				continue
			debug_info( 'insertion keyframe : "%s"' % anim.name )
			anim.insert_keyframe_all()

	bpy.context.scene.layers = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
#bpy.ops.view3d.layers( nr=2, extend=True, toggle = True )
#----------------------------------------------------------------------------------------------------------------------------------

def print_dic_name( xml_file ):
	global xml_files

	dic_name = {}
	for ac_file in xml_file.ac_files:
		dic_name.update( ac_file.dic_name_meshs )
		
	debug_info( "\tDictionnary     : (xml name) to (blender name)" )
	for key,value in dic_name.items():
		debug_info( '\t\tkey : "%s"  value : "%s"' % ( key, value ) )
		
#----------------------------------------------------------------------------------------------------------------------------------

def find_object( obj_name):

	for obj in bpy.data.objects:
		if obj.name == obj_name:
			return obj
	return None
#----------------------------------------------------------------------------------------------------------------------------------

def assign_obj_to_anim():
	global xml_files

	for xml_file, no in xml_files:
		set_current_xml( xml_file )
		print( 'assign_obj_to_anim()  in "%s"' % os.path.basename(xml_file.name) )
		#print( xml_file.name )
		debug_info( 'assign_to_anim() make dictionnary' )
		dic_name = {}
		for ac_file in xml_file.ac_files:
			debug_info( 'assign_to_anim() add to dictionnary "%s"' % os.path.basename(ac_file.name) )
			dic_name.update( ac_file.dic_name_meshs )
			
		if len(dic_name) == 0:
			continue

		if DEBUG:
			print_dic_name( xml_file )
		
		for anim in xml_file.anims:
			if anim.type != 1 and anim.type != 2:
				continue
			debug_info( '\tassign_obj_to_anim() pour l armature "%s"' % anim.name )
			for obj_name in anim.objects:
				if obj_name in dic_name:
					debug_info( '\tObject : "%s"   (blender:"%s")' % (obj_name, dic_name[obj_name]) )
				else:
					debug_info( '\tObject : "%s" pas contenu dans le dictionnary)' % (obj_name) )
					
			for obj_name in anim.objects:
				#if anim.name == "":
				#	continue
				#obj = bpy.data.objects[obj_name]
				if not obj_name in dic_name:
					assign_group_obj_to_anim( xml_file, obj_name, anim, dic_name )
					#print( "**** Erreur objet %s inconnu ***" % obj_name )
					#continue
				else:
					obj_name_bl = dic_name[obj_name]
					#obj = bpy.data.objects[obj_name_bl]
					#obj = find_object(obj_name_bl)
					obj = bpy.data.objects[obj_name_bl]
					#debug_info( "\tObj name %s" % obj.name )
					obj_armature = bpy.data.objects[anim.name]
					parent_set( obj, obj_armature )
#----------------------------------------------------------------------------------------------------------------------------------

def find_group( group_name, xml_file ):
	global xml_files
	
	for anim in  xml_file.anims:
		if anim.group_objects:
			if anim.group_objects[0] == group_name:
				return anim.group_objects
	return None

#----------------------------------------------------------------------------------------------------------------------------------

def assign_group_obj_to_anim( xml_file, group_name, anim, dic_name ):
	global xml_files

	debug_info( '\tRecherche de group name : "%s"' % group_name )
	group_objects = find_group( group_name, xml_file )
	if group_objects:
		debug_info( '\tgroup : "%s"' % str(anim.group_objects)  )
		for obj_name in group_objects[1:]:
			if not obj_name in dic_name:
				print( '**** Erreur objet "%s" inconnu ***' % obj_name )
				continue
			obj_name_bl = dic_name[obj_name]
			obj = bpy.data.objects[obj_name_bl]
			obj_armature = bpy.data.objects[anim.name]
			parent_set( obj, obj_armature )
	else:
		print( '**** xm file "%s"  ***' % xml_file.name )
		print( '**** Erreur objet "%s" inconnu ***' % group_name )
	
#----------------------------------------------------------------------------------------------------------------------------------

def is_obj_link_armature( obj ):
	objet = bpy.data.objects[obj.name]
	#debug_info( "\tObj name %s" % objet.name )
	if objet.parent!= None:
		#while( objet.parent != None ):
		objet = objet.parent
		if objet.type == 'ARMATURE':
			return objet
		else:
			debug_info( "**** Clear Transform *****" )
			bpy.ops.object.select_all(action='DESELECT')
			obj.select = True
			bpy.context.scene.objects.active = obj
			obj_parent = obj.parent
			bpy.ops.object.parent_clear( type='CLEAR_KEEP_TRANSFORM' )
			obj.parent = obj_parent
			return None
	else:
		return None
#----------------------------------------------------------------------------------------------------------------------------------

def parent_set( obj, armature ):
	debug_info( '\t\tCreation parenté d objet "%s" sur "%s"' % (obj.name, armature.name) )
	parent_armature = is_obj_link_armature( obj )
	if parent_armature:
		parent_set_armature( parent_armature, armature )
		#return

	bpy.ops.object.select_all(action='DESELECT')
	obj = get_object( obj.name )
	obj.select = True
	#bpy.ops.object.select_pattern(pattern=obj.name)
	bpy.ops.object.select_pattern(pattern=armature.name)
	bpy.context.scene.objects.active = armature
	bpy.ops.object.parent_set(type='BONE')

#----------------------------------------------------------------------------------------------------------------------------------

def parent_set_armature( parent, child ):
	debug_info( '\t\t\tCreation parenté d armature "%s" sur "%s"' % (child.name, parent.name) )

	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.select_pattern(pattern=child.name)
	bpy.ops.object.select_pattern(pattern=parent.name)
	bpy.context.scene.objects.active = parent
	bpy.ops.object.parent_set(type='BONE')


