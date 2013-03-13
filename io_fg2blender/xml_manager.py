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
import os

from mathutils import Vector
from mathutils import Euler

from . import *
from . import fg2bl

from .ac_manager import AC_FILE

#----------------------------------------------------------------------------------------------------------------------------------
add_on_path = ""

xml_files = []
xml_current = None
xml_current_no = 0

no_debug = 0

DEBUG = False
BIDOUILLE = True

#----------------------------------------------------------------------------------------------------------------------------------

def debug_info( aff):
	global DEBUG
	if DEBUG:
		print( aff )
#----------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------------
#		At loading
#----------------------------------------------------------------------------------------------------------------------------------
blender_path = os.getcwd()
addon_path = os.getcwd() + os.sep + str(bpy.app.version[0]) + '.' + str(bpy.app.version[1]) + os.sep + 'scripts' + os.sep + 'addons'
debug_info( 'Installation path ="%s"' % addon_path )

#----------------------------------------------------------------------------------------------------------------------------------
	

#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS XML_OPTION
#----------------------------------------------------------------------------------------------------------------------------------
#	Option for xml parser file
#----------------------------------------------------------------------------------------------------------------------------------

class XML_OPTION:
	def __init__(self):
		self.include			= False
		self.mesh_active_layer	= True
		self.mesh_layer_beg		= 1
		self.mesh_layer_end		= 20
		self.arma_active_layer	= True
		self.arma_layer_beg		= 1
		self.arma_layer_end		= 20

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
		self.name			= ""
		self.no				= 0
		self.ac_names			= []
		self.ac_files			= []
		self.offset			= Vector( (0.0, 0.0, 0.0) )
		self.eulerXYZ			= Vector( (0.0, 0.0, 0.0) )
		self.parent_offset		= Vector( (0.0, 0.0, 0.0) )
		self.parent_eulerXYZ		= Vector( (0.0, 0.0, 0.0) )
		self.anims			= []
		self.texts			= []
		self.file_offset		= ""

		
	def add_ac_file( self, ac_file = None ):
		if ac_file:
			self.ac_files.append( ac_file )
			self.ac_names.append( ac_file.name )
#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS ANIM
#----------------------------------------------------------------------------------------------------------------------------------
#	name				= "plane"							string	if transform name
#	type				= 0									1:Rotate 2:translate 3: group objects 4:pick 
#															5:light 6:shader 7: Spin
#	xml_file			= ""								string : xml  file
#	factor				= 0.0
#	property			= ""								string : flightgear property of transform
#	pos					= Vector( (0.0, 0.0, 0.0) )			bone location
#	vec					= Vector( (0.0, 0.0, 0.0) )			bone vector
#	objects				= []								objects list  ( name in xml file )
#	group_objects		= []								list : group_objects[0] name of group
#	layer				= 0									number of layer
#----------------------------------------------------------------------------------------------------------------------------------

class ANIM:
	def __init__(self):
		self.name				= ""
		self.type				= 0								# 1:Rotate 2:translate 3: group objects 4:pick 5:light 6:shader
		self.xml_file			= ""							# 7: Spin
		self.xml_file_no		= 0
		self.factor				= 1.0
		self.interpolation		= []
		self.property			= ""
		self.pos				= Vector( (0.0, 0.0, 0.0) )
		self.vec				= Vector( (0.0, 0.0, 0.0) )
		self.objects			= []
		self.group_objects		= []
		self.texture			= ""
		self.ac_file			= ""
		self.offset_deg			= 0.0
		self.layer				= 0						
		self.active_layer		= False
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
					elif value == 'light':
						self.type = 5
					elif value == 'shader':
						self.type = 6
					elif value == 'spin':
						debug_info( 'Spin animation' )
						self.type = 7
		else:
			childs = node.getElementsByTagName('name')
			if childs:
				self.type = 3
	#---------------------------------------------------------------------------------------------------------------------

	def extract_texture( self, node ):
		from .xml_import import ret_text_value
		from .xml_import import tabs
		from . import xml_import

		childs = node.getElementsByTagName('texture')
		if childs:
			self.texture = xml_import.conversion(  ret_text_value(childs[0]) )
			self.texture = os.getcwd() + os.sep + self.texture 
			debug_info( "\t%sTexture name %s" % (tabs(),self.texture) )
			ac_files = get_xml_file( self.xml_file, self.xml_file_no ).ac_files
			if len(ac_files)>0:
				self.ac_file = ac_files[0]
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

	def extract_offset_deg( self, node ):
		from .xml_import import ret_float_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('offset-deg')
		for child in childs:
			value = ret_float_value(child)
			self.offset_deg = value
			debug_info( "%s\tOffset-deg : %0.2f" % (tabs(),value) )
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
				debug_info( "%sAxe : %s" % (tabs(),str(self.vec)) )

		childs = node.getElementsByTagName('center')
		for child in childs:
			if child.hasChildNodes():
				self.pos = read_vector_center(child)
				debug_info( "%sCenter : %s" % (tabs(),str(self.pos)) )
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
			global no_debug
			from .xml_import import tabs

			debug_info( "%sExtract Rotate : %00d" % (tabs(),no_debug) )
			no_debug += 1
			self.extract_name( node )
			self.extract_property( node )
			self.extract_objects( node )
			self.extract_head_tail( node )
			self.extract_factor( node )
			self.extract_interpolation( node )
			self.extract_offset_deg( node )
			if self.type == 0:
				self.extract_group_objects( node )
		#---------------------------------------------------------------------------------------------------------------------

		def extract_anim_translate( node ):
			global no_debug
			from .xml_import import tabs

			debug_info( "%sExtract Translate : %00d" % (tabs(),no_debug) )
			no_debug += 1
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

		def extract_light( node ):
			from .xml_import import tabs

			debug_info( "%sExtract light :" % (tabs()) )
			self.extract_name( node )
			self.extract_objects( node )
		#---------------------------------------------------------------------------------------------------------------------

		def extract_empty( node ):
			from .xml_import import tabs

			debug_info( "%sExtract empty block:" % (tabs()) )
			self.extract_name( node )
			self.extract_objects( node )
		#---------------------------------------------------------------------------------------------------------------------

		def extract_shader( node ):
			from .xml_import import tabs

			debug_info( "%sExtract shader block:" % (tabs()) )
			self.extract_name( node )
			self.extract_objects( node )
			self.extract_texture( node )
		#---------------------------------------------------------------------------------------------------------------------

		def extract_spin( node ):
			global no_debug
			from .xml_import import tabs

			debug_info( "%sExtract spin : %00d" % (tabs(),no_debug) )
			no_debug += 1
			self.extract_name( node )
			self.extract_property( node )
			self.extract_objects( node )
			self.extract_head_tail( node )
			self.extract_factor( node )
			self.factor = 360.0
			self.extract_interpolation( node )
			if self.type == 0:
				self.extract_group_objects( node )
		#---------------------------------------------------------------------------------------------------------------------
		# pour recopier la valeur et non pas la référence
		from . import xml_import
		
		self.xml_file		= "" + xml_current.name
		self.xml_file_no	= 0 + xml_current.no
		self.layer			= 0 + xml_import.arma_layer
		self.active_layer	= xml_import.option_arma_rotate_layer

		self.extract_type( node )
		debug_info( '\tfg.data.xml_file = %d-"%s"' % (self.xml_file_no,self.xml_file) )
		
		if self.type == 1:
			extract_anim_rotate( node )
		elif self.type == 2:
			extract_anim_translate( node )
		elif self.type == 3:
			self.extract_group_objects( node )
		elif self.type == 4:
			extract_pick( node )
		elif self.type == 5:
			extract_light( node )
		elif self.type == 6:
			extract_shader( node )
		elif self.type == 7:
			extract_spin( node )
		elif self.type == 0:
			extract_empty( node )			#without type
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
		obj_armature = bpy.context.scene.objects.active
		if len(self.interpolation) != 0:
			_min = 0.0
			_max = 0.0
			for ind, dep in self.interpolation:
				if ind > _max:
					_max = ind
				if ind < _min:
					_min = ind
			debug_info( "Debut %0.2f" % obj_armature.data.fg.range_beg )
			debug_info( "Fin   %0.2f" % obj_armature.data.fg.range_end )
			#if self.interpolation[0][1] > self.interpolation[-1][1]:
			if obj_armature.data.fg.range_beg !=-999.0:
				if obj_armature.data.fg.range_beg <_min:
					_min = obj_armature.data.fg.range_beg
			else:
				obj_armature.data.fg.range_beg = obj_armature.data.fg.range_beg_ini = _min
				
			if obj_armature.data.fg.range_end !=-999.0:
				if obj_armature.data.fg.range_end >_max:
					_max = obj_armature.data.fg.range_beg
			else:
				obj_armature.data.fg.range_end = obj_armature.data.fg.range_end_ini = _max
					
			debug_info( obj_armature.name )
			debug_info( obj_armature.data.fg.property_value )
			debug_info( 'min=%0.2f max=%0.2f' % (_min,_max) )
				
			self.interpolation.reverse()
			for ind, dep in self.interpolation:
				coef = _max - _min
				if coef == 0.0:
					coef = 1.0
				frame = (( (ind-_min) / coef ) * 59.0) + 1.0 
				value = dep * self.factor
				self.insert_keyframe_rotation( int(round(frame)), value )
		else:
			self.insert_keyframe_rotation( 60, self.offset_deg + self.factor )
			self.insert_keyframe_rotation(  1, self.offset_deg + 0.0 )

		bpy.context.scene.frame_current = 1
		bpy.context.scene.frame_end = 60

		obj_armature = bpy.context.scene.objects.active

		'''
		debug_info( obj_armature.name )
		anim_data = obj_armature.animation_data_create()
		#anim_data = obj_armature.data.animation_data_create()
		debug_info( anim_data.action )
		if anim_data:
			debug_info( anim_data.action )
			anim_data.action = bpy.data.actions.new(obj_armature.name+'Action')
			#anim_data.action.fcurves.new('rotation_euler_x', action_group='Bone')
			#anim_data.action.fcurves.new('rotation_euler_y', action_group='Bone')
			#anim_data.action.fcurves.new('rotation_euler_Z', action_group='Bone')
			anim_data.action.groups.new('Bone')
			anim_data.action.id_root = 'OBJECT'
			anim_data.action.fcurves.new('pose.bones["Bone"].rotation_euler[0]', action_group='Bone')
			anim_data.action.fcurves.new('pose.bones["Bone"].rotation_euler[1]', action_group='Bone')
			anim_data.action.fcurves.new('pose.bones["Bone"].rotation_euler[2]', action_group='Bone')
			anim_data.action.fcurves.new('X Euler Rotation (Bone)', action_group='Bone')
			#anim_data.action.fcurves.new('pose.bones["Bone"].rotation_euler')
		return
		'''

		for fcurve in obj_armature.animation_data.action.fcurves:
			debug_info( fcurve.data_path )
			for keyframe in fcurve.keyframe_points:
				keyframe.interpolation = 'LINEAR'
		#obj_armature.animation_data.action.fcurves.new('pose.bones["Bone"].rotation_euler')
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
				self.insert_keyframe_translation( int(round(frame)), value )
				#self.insert_keyframe_translation(  frame, value )
		else:
			self.insert_keyframe_translation( 60, self.factor )
			self.insert_keyframe_translation(  1, 0.0 )

		bpy.context.scene.frame_current = 1
		bpy.context.scene.frame_end = 60

		obj_armature = bpy.context.scene.objects.active
		for fcurve in obj_armature.animation_data.action.fcurves:
			for keyframe in fcurve.keyframe_points:
				keyframe.interpolation = 'LINEAR'
	#---------------------------------------------------------------------------------------------------------------------
	
	def insert_keyframe_all( self ):
		debug_info( "self.insert_keyframe_all()  for %s" % self.name )
		debug_info( "self.insert_keyframe_all()" )
		if self.type == 1:
			bpy.context.scene.objects.active = bpy.data.objects[self.name]
			self.insert_keyframe_rotation_all()
		elif self.type == 2:
			bpy.context.scene.objects.active = bpy.data.objects[self.name]
			self.insert_keyframe_translation_all()
		elif self.type == 7:
			bpy.context.scene.objects.active = bpy.data.objects[self.name]
			self.insert_keyframe_rotation_all()
	#---------------------------------------------------------------------------------------------------------------------

	def create_property( self, obj ):
		from . import props_armature
		#------------------------------------------------------------

		def find_prop( obj, left, right, family, name ):
			for prop in family:
				left_prop = prop[0]
				right_prop = ''
				if prop[0].find('[') != -1:
					left_prop = prop[0].partition('[')[0]
					right_prop = prop[0].partition(']')[2]
			
				if left_prop == left and right_prop == right:
					debug_info( ' Bingo "%s"' , prop )
					obj.data.fg.family = name
					obj.data.fg.family_value = prop[0]
					if obj.data.fg.property_value.find('[') != -1:
						idx = obj.data.fg.property_value.partition('[')[2]
						idx = idx.partition(']')[0]
						obj.data.fg.property_idx = int(idx)

					if prop[1] != 'x':
						obj.data.fg.range_beg = prop[1]
						obj.data.fg.range_beg_ini = prop[1]
					if prop[2] != 'x':
						obj.data.fg.range_end = prop[2]
						obj.data.fg.range_end_ini = prop[2]
					
		#------------------------------------------------------------

		def find_in_family( obj, left, right ):
			find_prop( obj, left, right, props_armature.APUs, 'APU' )
			find_prop( obj, left, right, props_armature.anti_ices, 'anti_ice' )
			find_prop( obj, left, right, props_armature.armaments, 'armament' )
			find_prop( obj, left, right, props_armature.autoflights, 'autoflight' )
			find_prop( obj, left, right, props_armature.electrics, 'electric' )
			find_prop( obj, left, right, props_armature.engines, 'engine' )
			find_prop( obj, left, right, props_armature.flights, 'flight' )
			find_prop( obj, left, right, props_armature.fuels, 'fuel' )
			find_prop( obj, left, right, props_armature.consumables, 'consumable' )
			find_prop( obj, left, right, props_armature.gears, 'gear' )
		
		
		#------------------------------------------------------------

		if len(obj.data.fg.property_value) == 0:
			return
			

		if obj.data.fg.property_value[0] != '/':
			obj.data.fg.property_value = '/' + obj.data.fg.property_value
		debug_info( ' Recherche  property "%s"' % obj.data.fg.property_value )
		left = obj.data.fg.property_value
		right = ''
		if obj.data.fg.property_value.find('[') != -1:
			left = obj.data.fg.property_value.partition('[')[0]
			right = obj.data.fg.property_value.partition(']')[2]

		find_in_family( obj, left, right )
	#---------------------------------------------------------------------------------------------------------------------

	def create_armature_rotation( self ):
		bpy.ops.object.armature_add()

		#bpy.ops.object.move_to_layer( layers = layer(10) )
		
		armature = bpy.data.armatures[-1]
		debug_info( 'Create armature rotate : "%s"' % (armature.name) )
		debug_info( '\t\tFichier xml: "%s"' % os.path.basename(self.xml_file) )
		debug_info( '\t\t   no   xml: %d' % self.xml_file_no )
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
				obj_arma.data.fg.family = "custom"
				obj_arma.data.fg.property_value = "" + self.property
				obj_arma.data.fg.property_idx = -1
				obj_arma.data.fg.time = 60.0 / 24.0
				obj_arma.data.fg.range_beg = 0.0
				obj_arma.data.fg.range_end = 1.0
				obj_arma.data.fg.range_beg = -999.0
				obj_arma.data.fg.range_end = -999.0
				obj_arma.data.fg.range_beg_ini = -999.0
				obj_arma.data.fg.range_end_ini = -999.0
				obj_arma.data.fg.time_ini = 60.0 / 24.0
				obj_arma.data.fg.factor = 0.0 + self.factor
				obj_arma.data.fg.factor_ini = 0.0 + self.factor
				obj_arma.data.fg.offset_deg = 0.0 + self.offset_deg
				self.create_property( obj_arma )
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

		ac_manager.compute_extra_transforme( obj_arma, offset, euler )
		#obj_arma.delta_location = xml_current.offset
		#euler = xml_current.eulerXYZ
		#obj_arma.delta_rotation_euler = Euler( (euler.x, euler.y, euler.z) )
		#obj_arma.delta_location = xml_current.offset
		#obj_arma.delta_rotation_euler = Euler( (euler.x, euler.y, euler.z) )


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
		#bpy.ops.object.move_to_layer( layers = layer(10) )

		armature = bpy.data.armatures[-1]
		debug_info( 'Create armature translate : "%s"' % (armature.name) )
		debug_info( '\t\tFichier xml: "%s"' % os.path.basename(self.xml_file) )
		debug_info( '\t\t       no  : %d' % self.xml_file_no )
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
				obj_arma.data.fg.family = "custom"
				obj_arma.data.fg.property_value = "" + self.property
				obj_arma.data.fg.property_idx = -1
				obj_arma.data.fg.range_beg = 0.0
				obj_arma.data.fg.range_end = 1.0
				obj_arma.data.fg.time = 60.0 / 24.0
				obj_arma.data.fg.range_beg_ini = 0.0
				obj_arma.data.fg.range_end_ini = 1.0
				obj_arma.data.fg.time_ini = 60.0 / 24.0
				obj_arma.data.fg.factor = 0.0 + self.factor
				obj_arma.data.fg.factor_ini = 0.0 + self.factor
				self.create_property( obj_arma )
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

		ac_manager.compute_extra_transforme( obj_arma, offset, euler )
		#obj_arma.delta_location = xml_current.offset
		#euler = xml_current.eulerXYZ
		#obj_arma.delta_rotation_euler = Euler( (euler.x, euler.y, euler.z) )


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

	def create_light( self ):
		for xml_file, no in xml_files:
			if xml_file.name == self.xml_file and no == self.xml_file_no:
				break
		for obj_name_ac in self.objects:
			debug_info( 'Light' )
			debug_info( 'xml file no %d  -- "%s"' % (self.xml_file_no, os.path.basename(xml_file.name)) )
			debug_info( "Nb ac file : %d" % len(xml_file.ac_files) )
			
			if not obj_name_ac in xml_file.ac_files[0].dic_name_meshs:
				group_objects = find_group( obj_name_ac, xml_file )
				if group_objects:
					debug_info( '\tgroup : "%s"' % str(self.group_objects)  )
					for obj_name_bl in group_objects[1:]:
						debug_info( 'Create light : "%s"' % obj_name_bl )
						bpy.data.objects[obj_name_bl].draw_type = 'WIRE'
						#self.assign_pick( obj_name_bl )
				else:
					debug_info( '**** Erreur objet "%s" inconnu ***' % obj_name_ac )
					continue
			else:
				obj_name_bl = xml_file.ac_files[0].dic_name_meshs[obj_name_ac]
				debug_info( 'Create light : "%s"' % obj_name_bl )
				bpy.data.objects[obj_name_bl].draw_type = 'WIRE'
				#self.assign_pick( obj_name_bl )
	#----------------------------------------------------------------------------------------------------------------------------------

	def create_texture( self ):
		from . import xml_import
		img_name = os.path.basename(self.texture)
		if img_name == "":
			return
		
		debug_info( 'Creation de la texture "%s"' % img_name )
		debug_info( '              pathname "%s"' % self.texture )
		debug_info( '    repertoire courant "%s"' % os.getcwd() )
 		
		name_path = self.texture
	
		filenamepath = img_name
	
		debug_info( "create_texture()  name_path : %s" % (name_path) )
	
		for tex in bpy.data.textures:
			if tex.name==img_name:
				debug_info( "texture existante()  %s" % (img_name) )
				return tex
	
		try:
			img = bpy.data.images.load( name_path )
			
			
		except:
			debug_info( '*** erreur **** %s introuvale' % (name_path) )
			right_name = name_path.partition('Aircraft')[2]
			name_path = '/media/sauvegarde/fg-2.6/install/fgfs/fgdata/Aircraft' + right_name
			name_path = xml_import.conversion( name_path )
			img = bpy.data.images.load( name_path )
			debug_info( '*** bidouillle **** %s introuvale' % (name_path) )
			if BIDOUILLE:
				debug_info( "Bonjour" )
				#img = bpy.data.images.new(name='void', width=1024, height=1024, alpha=True, float_buffer=True)
			else:
				return None
	
		tex = bpy.data.textures.new( img_name, 'IMAGE')
		tex.image = img
		if bpy.app.version[0]==2 and bpy.app.version[1]<66:
			tex.use_alpha = True
		debug_info( '    Creation de la texture img="%s"  name="%s"' % (img_name, tex.name) )
		return tex
	#---------------------------------------------------------------------------------------------------------------------

	def create_pick( self ):
		for xml_file, no in xml_files:
			if xml_file.name == self.xml_file and no == self.xml_file_no:
				break
		for obj_name_ac in self.objects:
			debug_info( 'Pick' )
			debug_info( 'xml file no %d  -- "%s"' % (self.xml_file_no, os.path.basename(xml_file.name)) )
			debug_info( "Nb ac file : %d" % len(xml_file.ac_files) )
			
			if xml_file.ac_files:
				if not obj_name_ac in xml_file.ac_files[0].dic_name_meshs:
					group_objects = find_group( obj_name_ac, xml_file )
					if group_objects:
						debug_info( '\tgroup : "%s"' % str(self.group_objects)  )
						for obj_name_bl in group_objects[1:]:
							debug_info( 'Create Pick : "%s"' % obj_name_bl )
							self.assign_pick( obj_name_bl )
					else:
						debug_info( '**** Erreur objet "%s" inconnu ***' % obj_name_ac )
						continue
				else:
					obj_name_bl = xml_file.ac_files[0].dic_name_meshs[obj_name_ac]
					debug_info( 'Create Pick : "%s"' % obj_name_bl )
					self.assign_pick( obj_name_bl )
	#---------------------------------------------------------------------------------------------------------------------

	def create_armature( self ):
		if self.active_layer:
			bpy.context.scene.layers = layer( self.layer-2 )
			debug_info( "create_armature in layer %s" % str(self.layer-2) )
				
		if self.type == 1:
			self.create_armature_rotation()
			obj = bpy.context.scene.objects.active
			if obj:
				obj.data.fg.type_anim = 0 + self.type
		elif self.type == 2:
			self.create_armature_translation()
			obj = bpy.context.scene.objects.active
			if obj:
				obj.data.fg.type_anim = 0 + self.type
		elif self.type == 4:
			self.create_pick()
		elif self.type == 5:
			self.create_light()
		elif self.type == 6:
			tex = self.create_texture()
			self.assign_texture(tex)
		if self.type == 7:
			self.create_armature_rotation()
			obj = bpy.context.scene.objects.active
			if obj:
				obj.data.fg.type_anim = 0 + self.type
	#----------------------------------------------------------------------------------------------------------------------------------

	def assign_texture( self, tex ):
		if not tex:
			return
		if self.ac_file == "":
			return
		
		debug_info( str(self.objects) )
		for obj_name in self.objects:
			if obj_name in self.ac_file.dic_name_meshs:
				obj_name_bl = self.ac_file.dic_name_meshs[obj_name]
				obj_bl = bpy.data.objects[obj_name_bl]
			
				if obj_bl.type == 'MESH':
					mesh = obj_bl.data
					for texture_slot in mesh.materials[0].texture_slots:
						if texture_slot != None:
							if texture_slot.texture.name == tex.name:
								return

					debug_info( '    Assigne objet="%s"  texture="%s"' % (obj_bl.name, tex.name) )
					texture_slot = mesh.materials[0].texture_slots.add() 
					#mesh.materials[0].texture_slots.add() 
					texture_slot.texture = tex
					texture_slot.texture_coords	= 'REFLECTION'
					texture_slot.use_map_alpha	= True
					texture_slot.alpha_factor	= 0.1
				elif obj_bl.type == 'EMPTY':
					for obj in bpy.data.objects:
						if obj.parent == obj_bl:
							mesh = obj.data
							for texture_slot in mesh.materials[0].texture_slots:
								if texture_slot != None:
									if texture_slot.texture.name == tex.name:
										return

							debug_info( '    Assigne objet="%s"  texture="%s"' % (obj_bl.name, tex.name) )
							texture_slot = mesh.materials[0].texture_slots.add() 
							#mesh.materials[0].texture_slots.add() 
							texture_slot.texture = tex
							texture_slot.texture_coords	= 'REFLECTION'
							texture_slot.use_map_alpha	= True
							texture_slot.alpha_factor	= 0.1
	#---------------------------------------------------------------------------------------------------------------------

	def assign_pick( self, obj_name ):
		obj = get_object( obj_name )
		if obj:
			if obj.type == 'MESH':
				if not is_exist_matrial_pick(obj ):
					obj.data.materials.append( bpy.data.materials['Material_Pick'])
				obj.show_wire = True
				obj.show_transparent = True
#----------------------------------------------------------------------------------------------------------------------------------
#
#							END CLASS ANIM
#
#----------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS TEXT
#----------------------------------------------------------------------------------------------------------------------------------
#	name				= "plane"						string	if transform name
#	type				= 0							1:Rotate 2:translate 3: group objects 4:pick 
#												5:light 6:shader 7: Spin
#	xml_file			= ""							string : xml  file
#	factor				= 0.0
#	property			= ""							string : flightgear property of transform
#	pos					= Vector( (0.0, 0.0, 0.0) )				bone location
#	vec					= Vector( (0.0, 0.0, 0.0) )				bone vector
#	objects				= []							objects list  ( name in xml file )
#	group_objects		= []							list : group_objects[0] name of group
#	layer				= 0							number of layer
#----------------------------------------------------------------------------------------------------------------------------------

class TEXT:
	def __init__(self):
		self.name			= ""
		self.type			= 0						# 1:literal 2:text-value 3:number-value
		self.xml_file			= ""
		self.xml_file_no		= 0
		self.factor			= 1.0
		self.property			= ""
		self.pos	    		= Vector( (0.0, 0.0, 0.0) )
		self.vec			= Vector( (0.0, 0.0, 0.0) )
		self.objects			= []
		self.group_objects		= []
		self.ac_file			= ""
		self.offset_deg			= 0.0
		self.layer			= 0						
		self.active_layer		= False
		self.offset				= Vector( (0.0, 0.0, 0.0) )
		self.eulerXYZ			= Vector( (0.0, 0.0, 0.0) )
		self.xml_offset			= Vector( (0.0, 0.0, 0.0) )
		self.xml_eulerXYZ		= Vector( (0.0, 0.0, 0.0) )
		self.xml_parent_offset	= Vector( (0.0, 0.0, 0.0) )
		self.xml_parent_eulerXYZ= Vector( (0.0, 0.0, 0.0) )

	#---------------------------------------------------------------------------------------------------------------------

	def extract_type( self, node ):
		from .xml_import import ret_text_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('type')
		if childs:
			for child in childs:
				if child.hasChildNodes():
					value = ret_text_value(child)
					if value == 'literal':
						self.type = 1
					elif value == 'text-value':
						self.type = 2
					elif value == 'number-value':
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

	def extract_text_value( self, node ):
		from .xml_import import ret_text_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('text')
		if childs:
			self.text = ret_text_value(childs[0])
			debug_info( "\t%sText %s" % (tabs(),self.text) )
	#---------------------------------------------------------------------------------------------------------------------

	def extract_character_size( self, node ):
		from .xml_import import ret_float_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('character-size')
		if childs:
			self.character_size = ret_float_value(childs[0])
			debug_info( "\t%sCharacter-size %s" % (tabs(),self.character_size) )
	#---------------------------------------------------------------------------------------------------------------------

	def extract_character_aspect_ratio( self, node ):
		from .xml_import import ret_float_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('character-aspect-ratio')
		if childs:
			self.character_aspect_ratio = ret_float_value(childs[0])
			debug_info( "\t%sCharacter-aspect-ratio %s" % (tabs(),self.character_aspect_ratio) )
	#---------------------------------------------------------------------------------------------------------------------

	def extract_max_height( self, node ):
		from .xml_import import ret_float_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('max-height')
		if childs:
			self.max_height = ret_float_value(childs[0])
			debug_info( "\t%sMax-height %s" % (tabs(),self.max_height) )
	#---------------------------------------------------------------------------------------------------------------------

	def extract_max_width( self, node ):
		from .xml_import import ret_float_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('max-width')
		if childs:
			self.max_width = ret_float_value(childs[0])
			debug_info( "\t%sMax-width %s" % (tabs(),self.max_width) )
	#---------------------------------------------------------------------------------------------------------------------

	def extract_text( self, node ):

		def extract_text_literal( node ):
			global no_debug
			from .xml_import import tabs

			debug_info( "%sExtract Text literal : %00d" % (tabs(),no_debug) )
			no_debug += 1
			self.extract_name( node )
			self.extract_text_value( node )
			self.extract_character_size( node )
			self.extract_character_aspect_ratio( node )
			self.extract_max_height( node )
			self.extract_max_width( node )
		#---------------------------------------------------------------------------------------------------------------------

		def extract_text_property( node ):
			global no_debug
			from .xml_import import tabs

			debug_info( "%sExtract Text property : %00d" % (tabs(),no_debug) )
			no_debug += 1
			self.extract_name( node )
			self.extract_property( node )
			self.extract_character_size( node )
			self.extract_character_aspect_ratio( node )
			self.extract_max_height( node )
			self.extract_max_width( node )
		#---------------------------------------------------------------------------------------------------------------------

		def extract_text_number( node ):
			global no_debug
			from .xml_import import tabs

			debug_info( "%sExtract Text number : %00d" % (tabs(),no_debug) )
			no_debug += 1
			self.extract_name( node )
			self.extract_property( node )
			self.extract_character_size( node )
			self.extract_character_aspect_ratio( node )
			self.extract_max_height( node )
			self.extract_max_width( node )
		#---------------------------------------------------------------------------------------------------------------------

		#---------------------------------------------------------------------------------------------------------------------
		# pour recopier la valeur et non pas la référence
		from . import xml_import
		
		self.xml_file		= "" + xml_current.name
		self.xml_file_no	= 0 + xml_current.no
		self.layer	    	= 0 + xml_import.arma_layer
		self.active_layer	= xml_import.option_arma_rotate_layer

		self.extract_type( node )
		debug_info( '\tfg.data.xml_file = %d-"%s"' % (self.xml_file_no,self.xml_file) )
		
		if self.type == 1:
			extract_text_literal( node )
		elif self.type == 2:
			extract_text_property( node )
		elif self.type == 3:
			extract_text_number( node )
	#---------------------------------------------------------------------------------------------------------------------

	def create_text_literal( self ):
		debug_info('############# WRITTING TEXT LITERAL ###########')
		bpy.ops.object.add(type="FONT")
		textObject = bpy.data.objects["Text"]
		textObject.data.body= self.text
		textObject.data.align= "CENTER"
		bpy.ops.transform.resize(value=(self.character_size*0.45, self.character_size*0.45, self.character_size*0.45))
		bpy.ops.transform.resize(value=(1, 1, self.character_aspect_ratio))

		bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, -1))
		bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0))
	#---------------------------------------------------------------------------------------------------------------------

	def create_text_property( self ):
		debug_info('############# WRITTING TEXT PROPERTY ###########')
		bpy.ops.object.add(type="FONT")
		textObject = bpy.data.objects["Text"]
		textObject.data.body= "#####"
		textObject.data.align= "CENTER"
		bpy.ops.transform.resize(value=(self.character_size*0.45, self.character_size*0.45, self.character_size*0.45))
		bpy.ops.transform.resize(value=(1, 1, self.character_aspect_ratio))

		bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, -1))
		bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0))
	#---------------------------------------------------------------------------------------------------------------------

	def create_text_number( self ):
		debug_info('############# WRITTING TEXT NUMBER ###########')
		bpy.ops.object.add(type="FONT")
		textObject = bpy.data.objects["Text"]
		textObject.data.body= "#####"
		textObject.data.align= "CENTER"		
		bpy.ops.transform.resize(value=(self.character_size*0.45, self.character_size*0.45, self.character_size*0.45))
		bpy.ops.transform.resize(value=(1, 1, self.character_aspect_ratio))

		bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, -1))
		bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0))
	#---------------------------------------------------------------------------------------------------------------------

	def create_text( self ):
		if self.type == 1:
			self.create_text_literal()
		elif self.type == 2:
			self.create_text_property()
		elif self.type == 3:
			self.create_text_number()
			
		textObject = bpy.data.objects["Text"]
		textObject.name= self.name
		textObject.delta_location = self.offset
		textObject.delta_rotation_euler = Euler( (self.eulerXYZ.x, self.eulerXYZ.y, self.eulerXYZ.z) )
	#---------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------

def create_texts():
	global xml_files
	# Save active layers
	save_active_layers = [ b for b in bpy.context.scene.layers ]

	#
	#	Create Anim
	#
	for xml_file, no in xml_files:
		set_current_xml( xml_file, no )
		debug_info( '------' )
		debug_info( xml_file.name )
		for text in xml_file.texts:
			if text.type != 0:
				debug_info( 'Text type = %d' % text.type )
				text.create_text()

#----------------------------------------------------------------------------------------------------------------------------------
		

#----------------------------------------------------------------------------------------------------------------------------------
#
#							END CLASS TEXT
#
#----------------------------------------------------------------------------------------------------------------------------------

# because blender problem    bpy.ops.object.select_pattern( obj_name )
def get_object( obj_name ):
	for obj in bpy.data.objects:
		if obj.name == obj_name:
			debug_info( 'pick "%s" == "%s"' % (obj.name, obj_name) )
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
		debug_info( aff )
#----------------------------------------------------------------------------------------------------------------------------------
# xml_files  = tule ( xml_file, no_include )
def add_xml_file( xml_file, no ):
	if xml_file:
		xml_files.append( (xml_file,no) )
#----------------------------------------------------------------------------------------------------------------------------------
# xml_files  = tule ( xml_file, no_include )
def exist_xml_file( xml_file, no ):
	if (xml_file,no) in xml_files:
		return True
	else:
		return False
#----------------------------------------------------------------------------------------------------------------------------------

def set_current_xml( xml_file=None, no=0 ):
	global xml_current
	global xml_current_no
	
	if xml_file:
		xml_current = xml_file
		xml_current_no = no
#----------------------------------------------------------------------------------------------------------------------------------

def get_current_xml():
	global xml_current
	
	return  xml_current
#----------------------------------------------------------------------------------------------------------------------------------

def get_current_xml_no():
	global xml_current_no
	
	return  xml_current_no
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

	if no_include == -1:
		no_include = 0
	for xml_file, no in xml_files:
		debug_info( xml_file.name )
		#print ( no )
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
	debug_info( '------' )
	# Save active layers
	save_active_layers = [ b for b in bpy.context.scene.layers ]

	#
	#	Create material Pick an groupd (ac filename)
	#
	create_material_pick()
	# Change layer
	#bpy.ops.view3d.layers( nr=11, extend=True, toggle = True )
	#if not bpy.context.scene.layers[10]:
	#	bpy.ops.view3d.layers( nr=11, extend=True, toggle = True )
	# Create group	
	for xml_file, no in xml_files:
		for ac_file in xml_file.ac_files:
			debug_info( 'Creation de groups "%s"' % os.path.basename(ac_file.name) )
			ac_file.create_group_ac()

	bpy.context.scene.objects.active = None
	#
	#	Create Anim
	#
	for xml_file, no in xml_files:
		set_current_xml( xml_file, no )
		debug_info( '------' )
		debug_info( xml_file.name )
		for anim in xml_file.anims:
			debug_info( 'Animation type = %d' % anim.type )
			if anim.type in [ 0 ]:
				continue
			anim.create_armature()
			if not anim.type in [ 1,2,7 ]:
				continue
			obj = bpy.context.scene.objects.active
			if obj:
				debug_info( 'Modif xml_file="%s" obj="%s"' % (xml_file.name,obj.name) )
				debug_info( xml_file.name )
				#obj.data.fg.xml_file = "//../" + xml_file.name
				obj.data.fg.xml_file = "" + xml_file.name
				debug_info( "FILENAME %s" % fg2bl.path.rel_from(obj.data.fg.xml_file, "" ) )
				obj.data.fg.xml_file_no = 0 + no
				#fg2bl.path.print_filename( obj.data.fg.xml_file )
				#Assign group ac_file to armature
				if len(xml_file.ac_files)>0:
					ac_file = xml_file.ac_files[0]
					if ac_file:
						ac_name = os.path.basename( ac_file.name )
						if ac_name in bpy.data.groups:
							bpy.ops.object.group_link( group = ac_name)
							debug_info( 'Assign group group : "%s"' % ac_name )
	#
	#	Assign objct to anim
	#
	bpy.context.scene.layers = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
	assign_obj_to_anim()
	#
	#	Insert keyframe
	#
	for xml_file, no in xml_files:
		set_current_xml( xml_file, no )
		for anim in xml_file.anims:
			if anim.name=="":
				continue
			debug_info( 'insertion keyframe : "%s"' % anim.name )
			anim.insert_keyframe_all()

	#restore active layer
	bpy.context.scene.layers = save_active_layers

#bpy.ops.view3d.layers( nr=2, extend=True, toggle = True )
#----------------------------------------------------------------------------------------------------------------------------------

def print_dic_name( xml_file, dic_name ):
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
		set_current_xml( xml_file, no )
		debug_info( '-----------------------------------' )
		debug_info( 'assign_obj_to_anim()  in "%s"' % os.path.basename(xml_file.name) )
		debug_info( xml_file.name )
		debug_info( 'assign_to_anim() make dictionnary' )
		dic_name = {}
		for ac_file in xml_file.ac_files:
			debug_info( 'assign_to_anim() add to dictionnary "%s"' % os.path.basename(ac_file.name) )
			dic_name.update( ac_file.dic_name_meshs )
			
		if len(dic_name) == 0:
			continue

		if DEBUG:
			print_dic_name( xml_file, dic_name )
		
		for anim in xml_file.anims:
			#if anim.type != 1 and anim.type != 2:
			if not anim.type in [ 1, 2, 7 ]:
				continue
			debug_info( '\tassign_obj_to_anim() pour l armature "%s"' % anim.name )
			for obj_name in anim.objects:
				debug_info( '\tRecherche object : "%s" ' % obj_name )
				if obj_name in dic_name:
					debug_info( '\t\tObject : "%s"   (blender:"%s")' % (obj_name, dic_name[obj_name]) )
				else:
					debug_info( '\t\tObject : "%s" pas contenu dans le dictionnary)' % (obj_name) )
					
			for obj_name in anim.objects:
				#if anim.name == "":
				#	continue
				#obj = bpy.data.objects[obj_name]
				if not obj_name in dic_name:
					assign_group_obj_to_anim( xml_file, obj_name, anim, dic_name )
					debug_info( "**** Erreur objet %s inconnu ***" % obj_name )
					#continue
				else:
					obj_name_bl = dic_name[obj_name]
					#obj = bpy.data.objects[obj_name_bl]
					#obj = find_object(obj_name_bl)
					obj = bpy.data.objects[obj_name_bl]
					debug_info( "\tObj name %s" % obj.name )
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

def find_obj_in_empty_animation( obj_name ):
	global xml_files
	
	debug_info( '\tRecherche in empty <animation> : "%s"' % obj_name )
	for xml_file, no in  xml_files:
		for ac_file in xml_file.ac_files:
			for objet in ac_file.meshs:
				if objet == obj_name:
					debug_info( 'Find obj="%s" in "%s"' % (obj_name , os.path.basename(xml_file.name)) )
					debug_info( 'Find obj="%s" in "%s"' % (obj_name , os.path.basename(ac_file.name)) )
					obj_name_bl = ac_file.dic_name_meshs[obj_name]
					return obj_name_bl
	return None
#----------------------------------------------------------------------------------------------------------------------------------

def assign_group_obj_to_anim( xml_file, group_name, anim, dic_name ):
	global xml_files

	debug_info( '\tRecherche de group name : "%s"' % group_name )
	group_objects = find_group( group_name, xml_file )
	if group_objects:
		debug_info( '\tgroup : "%s"' % str(group_objects)  )
		for obj_name in group_objects[1:]:
			if not obj_name in dic_name:
				obj_name_bl = find_obj_in_empty_animation(obj_name)
				if obj_name_bl:
					obj = bpy.data.objects[obj_name_bl]
					obj_armature = bpy.data.objects[anim.name]
					parent_set( obj, obj_armature )
				else:
					debug_info( '**** Erreur objet "%s" inconnu ***' % obj_name )
				continue
			else:
				obj_name_bl = dic_name[obj_name]
				obj = bpy.data.objects[obj_name_bl]
				obj_armature = bpy.data.objects[anim.name]
				parent_set( obj, obj_armature )
		return

	obj_name_bl = find_obj_in_empty_animation(group_name)
	if obj_name_bl:
		obj = bpy.data.objects[obj_name_bl]
		obj_armature = bpy.data.objects[anim.name]
		parent_set( obj, obj_armature )
	else:
		debug_info( '**** xm file "%s"  ***' % xml_file.name )
		debug_info( '**** Erreur objet "%s" inconnu ***' % group_name )
#----------------------------------------------------------------------------------------------------------------------------------

def is_obj_link_armature( obj ):
	objet = bpy.data.objects[obj.name]
	debug_info( "\tObj name %s" % objet.name )
	if objet.parent!= None:
		#while( objet.parent != None ):
		objet = objet.parent
		if objet.type == 'ARMATURE':
			return objet
		'''
		else:
			debug_info( "**** Clear Transform *****" )
			bpy.ops.object.select_all(action='DESELECT')
			obj.select = True
			bpy.context.scene.objects.active = obj
			obj_parent = obj.parent
			bpy.ops.object.parent_clear( type='CLEAR_KEEP_TRANSFORM' )
			#obj.parent = obj_parent
			return None
		'''
	else:
		return None
#----------------------------------------------------------------------------------------------------------------------------------

def is_obj_link_empty( obj ):
	objet = bpy.data.objects[obj.name]
	debug_info( "\tObj name %s" % objet.name )
	if objet.parent!= None:
		objet = objet.parent
		if objet.type == 'EMPTY':
			debug_info( "**** Clear Transform *****" )
			bpy.ops.object.select_all(action='DESELECT')
			obj.select = True
			bpy.context.scene.objects.active = obj
			obj_parent = obj.parent
			bpy.ops.object.parent_clear( type='CLEAR_KEEP_TRANSFORM' )
			return objet
	else:
		return None
#----------------------------------------------------------------------------------------------------------------------------------

def parent_set( obj, armature ):
	debug_info( '\t\tCreation parenté d objet "%s" sur "%s"' % (obj.name, armature.name) )
	parent_armature = is_obj_link_armature( obj )
	if parent_armature:
		parent_set_armature( parent_armature, armature )
	parent_empty = is_obj_link_empty( obj )
	if parent_empty:
		parent_set_armature_simple( parent_empty, armature )
		#return

	bpy.ops.object.select_all(action='DESELECT')
	obj = get_object( obj.name )
	obj.select = True
	#bpy.ops.object.select_pattern(pattern=obj.name)
	bpy.ops.object.select_pattern(pattern=armature.name,case_sensitive=True)
	bpy.context.scene.objects.active = armature
	bpy.ops.object.parent_set(type='BONE')

#----------------------------------------------------------------------------------------------------------------------------------

def parent_set_armature( parent, child ):
	debug_info( '\t\t\tCreation parenté d armature "%s" sur "%s"' % (child.name, parent.name) )

	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.select_pattern(pattern=child.name,case_sensitive=True)
	bpy.ops.object.select_pattern(pattern=parent.name,case_sensitive=True)
	bpy.context.scene.objects.active = parent
	bpy.ops.object.parent_set(type='BONE')
#----------------------------------------------------------------------------------------------------------------------------------

def parent_set_armature_simple( parent, child ):
	debug_info( '\t\t\tCreation parenté simple de "%s" sur "%s"' % (child.name, parent.name) )

	bpy.ops.object.select_all(action='DESELECT')
	bpy.ops.object.select_pattern(pattern=child.name,case_sensitive=True)
	bpy.ops.object.select_pattern(pattern=parent.name,case_sensitive=True)
	bpy.context.scene.objects.active = parent
	bpy.ops.object.parent_set(type='OBJECT')


