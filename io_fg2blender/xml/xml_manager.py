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
import bpy
import xml.dom.minidom
import os
import time

from mathutils import Vector
from mathutils import Euler

from . import *
from .. import fg2bl

from ..meshes.ac3d.ac_manager import AC_FILE

#----------------------------------------------------------------------------------------------------------------------------------
#add_on_path = ""

xml_files = []
xml_current = None
xml_current_no = 0

no_debug = 0

#----------------------------------------------------------------------------------------------------------------------------------
#		At loading
#----------------------------------------------------------------------------------------------------------------------------------
def debug_info( aff ):
	from .. import debug_xml_manager
	
	if debug_xml_manager:
		print( aff )
#----------------------------------------------------------------------------------------------------------------------------------

blender_path = os.getcwd()
addon_path = os.getcwd() + os.sep + str(bpy.app.version[0]) + '.' + str(bpy.app.version[1]) + os.sep + 'scripts' + os.sep + 'addons'
#debug_info( 'Installation path ="%s"' % addon_path )

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
	from ..props import props_armature
	
	props_armature.bLock_update = True
	
	debug_info( '------' )
	print( "Create animations" )
	time_deb = time.time()
	# Save active layers
	save_active_layers = [ b for b in bpy.context.scene.layers ]

	bpy.context.scene.frame_end = 24
	#
	#	Create material Pick an groupd (ac filename)
	#
	#********************************************
	# Laisse un affichage mini
	print( "  -Create new materials")
	#********************************************
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
	#	Change anim time 
	#
	#********************************************
	# Laisse un affichage mini
	print( "  -Change anim time from jsbsim")
	#********************************************
	for xml_file, no in xml_files:
		for anim in xml_file.anims:
			if  anim.type == 'jsb':
				set_current_xml( xml_file, no )
				anim.change_time_animation( xml_current )
	#
	#	Create Anim
	#
	#********************************************
	# Laisse un affichage mini
	print( "  -Create animations")
	#********************************************
	for xml_file, no in xml_files:
		set_current_xml( xml_file, no )
		debug_info( '------' )
		debug_info( xml_file.name )
		for anim in xml_file.anims:
			debug_info( 'Animation type = %s' % anim.type )
			if anim.type in [ 'jsb' ]:
				continue
			anim.create_armature( xml_current )
			if not anim.type in [ "rotate", "translate", "spin" ]:
				continue
			obj = bpy.context.scene.objects.active
			if obj:
				debug_info( 'Modif xml_file="%s" obj="%s"' % (xml_file.name,obj.name) )
				debug_info( xml_file.name )
				#obj.data.fg.xml_file = "//../" + xml_file.name
				obj.data.fg.xml_file = "" + xml_file.name
				debug_info( "FILENAME %s" % obj.data.fg.xml_file )
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
	#********************************************
	# Laisse un affichage mini
	print( "  -Assign objects to animations")
	#********************************************
	bpy.context.scene.layers = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
	assign_obj_to_anim()
	#
	#	Insert keyframe
	#
	#********************************************
	# Laisse un affichage mini
	print( "  -Insert keyframe")
	#********************************************
	for xml_file, no in xml_files:
		set_current_xml( xml_file, no )
		for anim in xml_file.anims:
			if anim.name=="":
				continue
			debug_info( 'insertion keyframe : "%s"' % anim.name )
			anim.insert_keyframe_all()

	#restore active layer
	bpy.context.scene.layers = save_active_layers

	time_end = time.time()
	debug_info( "Create animations in  %0.2f sec" % (time_end-time_deb) )

	props_armature.bLock_update = False
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

		from .. import debug_xml_manager
		if debug_xml_manager:
			print_dic_name( xml_file, dic_name )
		
		for anim in xml_file.anims:
			#if anim.type != 1 and anim.type != 2:
			if not anim.type in [ "rotate", "translate", "spin" ]:
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


