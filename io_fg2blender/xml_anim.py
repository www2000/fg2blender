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
# Script copyright (C) Clément de l'Hamaide
# Contributors: 
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									XML_ANIM.PY
#
#----------------------------------------------------------------------------------------------------------------------------------
import xml.dom.minidom
import os
import bpy

from mathutils import Vector
from mathutils import Euler

from math import radians

from . import ac_manager

DEBUG = True

#----------------------------
def debug_info( aff):
	global DEBUG
	if DEBUG:
		print( aff )
#----------------------------


#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM:

	def __init__( self ):
		self.name			= ""
		self.type			= 0				# 1:Rotate 2:translate 3: group objects 4:pick 5:light 6:shader 7: Spin
		self.xml_file			= ""					
		self.xml_file_no		= 0
		self.factor			= 1.0
		self.interpolation		= []
		self.property			= ""
		self.pos			= Vector( (0.0, 0.0, 0.0) )
		self.vec			= Vector( (0.0, 0.0, 0.0) )
		self.objects			= []
		self.group_objects		= []
		self.texture			= ""
		self.ac_file			= ""
		self.offset_deg			= 0.0
		self.layer			= 0						
		self.active_layer		= False

	#----------------------------------------------
	# extract_texture( self, node)
	#----------------------------------------------
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


	#----------------------------------------------
	# extract_name( self, node)
	#----------------------------------------------
	def extract_name( self, node ):
		from .xml_import import ret_text_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('name')
		if childs:
			self.name = ret_text_value(childs[0])
			debug_info( "\t%sName %s" % (tabs(),self.name) )


	#----------------------------------------------
	# extract_property( self, node)
	#----------------------------------------------
	def extract_property( self, node ):
		from .xml_import import ret_text_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('property')
		if childs:
			self.property = ret_text_value(childs[0])
			debug_info( "\t%sProperty %s" % (tabs(),self.property) )


	#----------------------------------------------
	# extract_objects( self, node)
	#----------------------------------------------
	def extract_objects( self, node ):
		from .xml_import import ret_text_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('object-name')
		for child in childs:
			value = ret_text_value(child)
			self.objects.append( value )
			debug_info( "%s\tAppend object-name : %s" % (tabs(),value) )


	#----------------------------------------------
	# extract_offset_deg( self, node)
	#----------------------------------------------
	def extract_offset_deg( self, node ):
		from .xml_import import ret_float_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('offset-deg')
		for child in childs:
			value = ret_float_value(child)
			self.offset_deg = value
			debug_info( "%s\tOffset-deg : %0.2f" % (tabs(),value) )


	#----------------------------------------------
	# extract_head_tail( self, node)
	#----------------------------------------------
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


	#----------------------------------------------
	# extract_factore( self, node)
	#----------------------------------------------
	def extract_factor( self, node ):
		from .xml_import import ret_float_value
		from .xml_import import tabs

		childs = node.getElementsByTagName('factor')
		if childs:
			self.factor = ret_float_value(childs[0])
			debug_info( "%s\tFactor : %s" % (tabs(),str(self.factor)) )
		else:
			self.factor = 1.0
			debug_info( "%s\tFactor default: %s" % (tabs(),str(self.factor)) )


	#----------------------------------------------
	# extract_interpolation( self, node)
	#----------------------------------------------
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


	#----------------------------------------------
	# create_armature( self )
	#----------------------------------------------
	def create_armature( self ):
		pass



























	#----------------------------------------------
	# insert_keyframe_rotation( self, frame, value )
	#----------------------------------------------
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

	#----------------------------------------------
	# insert_keyframe_rotation_all( self )
	#----------------------------------------------
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


	#----------------------------------------------
	# insert_keyframe_translation( self, frame, value )
	#----------------------------------------------
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


	#----------------------------------------------
	# insert_keyframe_translation_all( self )
	#----------------------------------------------
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


	#----------------------------------------------
	# insert_keyframe_all( self )
	#----------------------------------------------	
	def insert_keyframe_all( self ):
		pass
	'''
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
	'''

	#----------------------------------------------
	# create_property( self, obj )
	#----------------------------------------------
	def create_property( self, obj ):
		from . import props_armature

		#----------------------------------------------
		# extract_interpolation( self, node)
		#----------------------------------------------
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
					

		#----------------------------------------------
		# extract_interpolation( self, node)
		#----------------------------------------------
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

















#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_ROTATE(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_ROTATE(ANIM):

	def __init__( self, node ):
		ANIM.__init__( self )
		self.type = "rotate"
		self.extract_name( node )
		self.extract_property( node )
		self.extract_objects( node )
		self.extract_head_tail( node )
		self.extract_factor( node )
		self.extract_interpolation( node )
		self.extract_offset_deg( node )


	#----------------------------------------------
	# create_armature( self ) ROTATE
	#----------------------------------------------
	def create_armature( self, xml_current ):
		bpy.ops.object.armature_add()

		#bpy.ops.object.move_to_layer( layers = layer(10) )
		
		armature = bpy.data.armatures[-1]
		debug_info( 'Create armature rotate : "%s"' % (armature.name) )
		debug_info( '\t\tFichier xml: "%s"' % os.path.basename(xml_current.name) )
		debug_info( '\t\t   no   xml: %d' % xml_current.no )
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
				obj_arma.data.fg.type_anim = 1
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

	#----------------------------------------------
	# insert_keyframe_all( self )
	#----------------------------------------------	
	def insert_keyframe_all( self ):
		debug_info( "self.insert_keyframe_all()  for %s" % self.name )
		debug_info( "self.insert_keyframe_all()" )

		bpy.context.scene.objects.active = bpy.data.objects[self.name]
		self.insert_keyframe_rotation_all()

		
#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_TRANSLATE(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_TRANSLATE(ANIM):

	def __init__( self ):
		ANIM.__init__( self )
		self.type = "translate"
		self.extract_name( node )
		self.extract_property( node )
		self.extract_objects( node )
		self.extract_head_tail( node )
		self.extract_factor( node )
		self.extract_interpolation( node )


	#----------------------------------------------
	# create_armature( self ) TRANSLATE
	#----------------------------------------------
	def create_armature( self, xml_current ):
		bpy.ops.object.armature_add()
		#bpy.context.scene.layers = layer( 10 )
		#bpy.context.scene.active_layer = 10
		#bpy.ops.object.move_to_layer( layers = layer(10) )

		armature = bpy.data.armatures[-1]
		debug_info( 'Create armature translate : "%s"' % (armature.name) )
		debug_info( '\t\tFichier xml: "%s"' % os.path.basename(xml_current.name) )
		debug_info( '\t\t       no  : %d' % self.xml_file.no )
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
				obj_arma.data.fg.type_anim = 2
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
	
	#----------------------------------------------
	# insert_keyframe_all( self )
	#----------------------------------------------	
	def insert_keyframe_all( self ):
		debug_info( "self.insert_keyframe_all()  for %s" % self.name )
		debug_info( "self.insert_keyframe_all()" )

		bpy.context.scene.objects.active = bpy.data.objects[self.name]
		self.insert_keyframe_translation_all()


#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_PICK(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_PICK(ANIM):

	def __init__( self ):
		ANIM.__init__( self )
		self.type = "pick"
		self.extract_name( node )
		self.extract_property( node )
		self.extract_objects( node )


	#----------------------------------------------
	# create_armature( self ) PICK
	#----------------------------------------------
	def create_armature( self ):
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


	#----------------------------------------------
	# assign_pick( self ) PICK
	#----------------------------------------------
	def assign_pick( self, obj_name ):
		obj = get_object( obj_name )
		if obj:
			if obj.type == 'MESH':
				if not is_exist_matrial_pick(obj ):
					obj.data.materials.append( bpy.data.materials['Material_Pick'])
				obj.show_wire = True
				obj.show_transparent = True
	
#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_SPIN(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_SPIN(ANIM):

	def __init__( self ):
		ANIM.__init__( self )
		self.type = "spin"
		self.extract_name( node )
		self.extract_property( node )
		self.extract_objects( node )
		self.extract_head_tail( node )
		self.factor = 360.0
		self.extract_interpolation( node )


	#----------------------------------------------
	# create_armature( self ) SPIN
	#----------------------------------------------
	def create_armature( self ):
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
				obj_arma.data.fg.type_anim = 7
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
	
	#----------------------------------------------
	# insert_keyframe_all( self )
	#----------------------------------------------	
	def insert_keyframe_all( self ):
		debug_info( "self.insert_keyframe_all()  for %s" % self.name )
		debug_info( "self.insert_keyframe_all()" )

		bpy.context.scene.objects.active = bpy.data.objects[self.name]
		self.insert_keyframe_rotation_all()

		

#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_LIGHT(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_LIGHT(ANIM):

	def __init__( self ):
		ANIM.__init__( self )
		self.type = "light"
		self.extract_name( node )
		self.extract_objects( node )


	#----------------------------------------------
	# create_armature( self ) LIGHT
	#----------------------------------------------
	def create_armature( self ):
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
				else:
					debug_info( '**** Erreur objet "%s" inconnu ***' % obj_name_ac )
					continue
			else:
				obj_name_bl = xml_file.ac_files[0].dic_name_meshs[obj_name_ac]
				debug_info( 'Create light : "%s"' % obj_name_bl )
				bpy.data.objects[obj_name_bl].draw_type = 'WIRE'


#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_SHADER(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_SHADER(ANIM):

	def __init__( self ):
		ANIM.__init__( self )
		self.type = "shader"
		self.extract_name( node )
		self.extract_objects( node )
		self.extract_texture( node )


	#----------------------------------------------
	# create_armature( self ) SHADER
	#----------------------------------------------
	def create_armature( self ):
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
	

#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_GROUP(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_GROUPS(ANIM):

	def __init__( self ):
		ANIM.__init__( self )
		self.type = "groups"
		self.extract_name( node )
		self.extract_objects( node )

	#----------------------------------------------
	# create_armature( self ) GROUPS
	#----------------------------------------------
	def create_armature( self ):
		pass


