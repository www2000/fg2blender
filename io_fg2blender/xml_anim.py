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

from mathutils import Vector
from mathutils import Euler

DEBUG = False

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


#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_ROTATE(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_ROTATE(ANIM):

	def __init__( self, node ):
		ANIM.__init__( self )
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

		
#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_TRANSLATE(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_TRANSLATE(ANIM):

	def __init__( self ):
		ANIM.__init__( self )
		self.extract_name( node )
		self.extract_property( node )
		self.extract_objects( node )
		self.extract_head_tail( node )
		self.extract_factor( node )
		self.extract_interpolation( node )


	#----------------------------------------------
	# create_armature( self ) TRANSLATE
	#----------------------------------------------
	def create_armature( self ):
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
	

#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_PICK(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_PICK(ANIM):

	def __init__( self ):
		ANIM.__init__( self )
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
	
#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_SPIN(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_SPIN(ANIM):

	def __init__( self ):
		ANIM.__init__( self )
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
	

#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_LIGHT(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_LIGHT(ANIM):

	def __init__( self ):
		ANIM.__init__( self )
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
						#self.assign_pick( obj_name_bl )
				else:
					debug_info( '**** Erreur objet "%s" inconnu ***' % obj_name_ac )
					continue
			else:
				obj_name_bl = xml_file.ac_files[0].dic_name_meshs[obj_name_ac]
				debug_info( 'Create light : "%s"' % obj_name_bl )
				bpy.data.objects[obj_name_bl].draw_type = 'WIRE'
				#self.assign_pick( obj_name_bl )


#----------------------------------------------------------------------------------------------------------------------------------------------
# ANIM_SHADER(ANIM)
#----------------------------------------------------------------------------------------------------------------------------------------------

class ANIM_SHADER(ANIM):

	def __init__( self ):
		ANIM.__init__( self )
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
		self.extract_name( node )
		self.extract_objects( node )

	#----------------------------------------------
	# create_armature( self ) GROUPS
	#----------------------------------------------
	def create_armature( self ):
		pass


