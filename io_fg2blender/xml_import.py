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
# Contributors: Clément
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									XML_IMPORT.PY
#
#----------------------------------------------------------------------------------------------------------------------------------
#!/usr/bin/env python3.2
import sys
import os
import time
import bpy
import xml.dom.minidom
import codecs

from . import *

from math import radians
from mathutils import Vector
from mathutils import Euler

from .ac_manager import AC_OPTION
from .ac_manager import AC_FILE
from .xml_manager import XML_OPTION
from .xml_manager import XML_FILE
#from .xml_manager import ANIM
from .xml_anim import ANIM
from .xml_anim import ANIM_ROTATE
from .xml_anim import ANIM_TRANSLATE
from .xml_anim import ANIM_SPIN
from .xml_anim import ANIM_SHADER
from .xml_anim import ANIM_LIGHT
from .xml_anim import ANIM_GROUPS
from .xml_anim import ANIM_PICK
from .xml_anim import ANIM_JSB

from .xml_manager import TEXT
#---------------------------------------------------------------------------------------------------------------------
niv = 0
path_model = ""
abs_path_model = ""
option_include = False
option_print_include = False
option_rotation = False
option_translation = False
option_animation = False
option_light = False
option_ac_file = False

option_mesh_rotate_layer = False
option_mesh_rotate_beg = 0
option_mesh_rotate_end = 9

option_arma_rotate_layer = False
option_arma_rotate_beg = 10
option_arma_rotate_end = 19

mesh_layer = -1
arma_layer = -1

DEBUG_INFO = True
#----------------------------------------------------------------------------------------------------------------------------------

def debug_info(aff):
	if DEBUG_INFO:
		print( aff )
#----------------------------------------------------------------------------------------------------------------------------------

def conversion(name_path):
	debug_info( "conversion de %s" % name_path )
	name = ""
	if os.sep == '\\':
		dirs = name_path.split("/")
		if dirs:
			for dir_item in dirs:
				if name == "":
					name = dir_item
				else:
					name = name + os.sep + dir_item
	else:
		dirs = name_path.split("\\")
		if dirs:
			for dir_item in dirs:
				if name == "":
					name = dir_item
				else:
					name = name + os.sep + dir_item

	debug_info( "reslutat %s" % name )

	return name
#---------------------------------------------------------------------------------------------------------------------

def tabs():
	global niv
	ret = ''
	for c in range(niv):
		ret += '\t'
	return ret
#---------------------------------------------------------------------------------------------------------------------

def sup_space( name ):
	ret = ''
	for c in name:
		if c==',':
			c = '.'
		if c!=' ' and c!= '\t':
			ret += c
	return ret
#---------------------------------------------------------------------------------------------------------------------

def read_center( node ):
	x0 = y0 = z0 = 'no'
	childs = node.getElementsByTagName('x-m')
	if childs:
		x0 = ret_text_value(childs[0])
	childs = node.getElementsByTagName('y-m')
	if childs:
		y0 = ret_text_value(childs[0])
	childs = node.getElementsByTagName('z-m')
	if childs:
		z0 = ret_text_value(childs[0])
		return "%s,%s,%s" % (x0,y0,z0)
	else:
		return ""
#---------------------------------------------------------------------------------------------------------------------

def read_vector_center( node ):
	v = Vector( (0.0,0.0,0.0) )
	childs = node.getElementsByTagName('x-m')
	if childs:
		v.x = ret_float_value(childs[0])
	childs = node.getElementsByTagName('y-m')
	if childs:
		v.y = ret_float_value(childs[0])
	childs = node.getElementsByTagName('z-m')
	if childs:
		v.z = ret_float_value(childs[0])

	childs = node.getElementsByTagName('x1-m')
	if childs:
		v.x = ret_float_value(childs[0])
	childs = node.getElementsByTagName('y1-m')
	if childs:
		v.y = ret_float_value(childs[0])
	childs = node.getElementsByTagName('z1-m')
	if childs:
		v.z = ret_float_value(childs[0])


	return v
#---------------------------------------------------------------------------------------------------------------------

def read_float_pitch_deg( node ):
	f = 0.0
	childs = node.getElementsByTagName('pitch-deg')
	if childs:
		f = radians( ret_float_value(childs[0]) )
	return f
#---------------------------------------------------------------------------------------------------------------------

def read_float_roll_deg( node ):
	f = 0.0
	childs = node.getElementsByTagName('roll-deg')
	if childs:
		f = radians( ret_float_value(childs[0]) )
	return f
#---------------------------------------------------------------------------------------------------------------------

def read_float_heading_deg( node ):
	f = 0.0
	childs = node.getElementsByTagName('heading-deg')
	if childs:
		f = radians( ret_float_value(childs[0]) )
	return f

#---------------------------------------------------------------------------------------------------------------------

def read_color_vecteur( node ):
	r = g = b = a = 'no'
	childs = node.getElementsByTagName('r')
	if childs:
		r = ret_text_value(childs[0])
	childs = node.getElementsByTagName('g')
	if childs:
		g = ret_text_value(childs[0])
	childs = node.getElementsByTagName('b')
	if childs:
		b = ret_text_value(childs[0])
	childs = node.getElementsByTagName('a')
	if childs:
		a = ret_text_value(childs[0])
	return "%s,%s,%s,%s" % (r,g,b,a)
#---------------------------------------------------------------------------------------------------------------------

def read_axis_vecteur( node ):
	x = y = z = 'no'
	childs = node.getElementsByTagName('x')
	if childs:
		x = ret_text_value(childs[0])
	childs = node.getElementsByTagName('y')
	if childs:
		y = ret_text_value(childs[0])
	childs = node.getElementsByTagName('z')
	if childs:
		z = ret_text_value(childs[0])
	return "%s,%s,%s" % (x,y,z)
#---------------------------------------------------------------------------------------------------------------------

def read_vector_axis_vecteur( node ):
	v = Vector( (0.0,0.0,0.0) )
	childs = node.getElementsByTagName('x')
	if childs:
		v.x = ret_float_value(childs[0])
	childs = node.getElementsByTagName('y')
	if childs:
		v.y = ret_float_value(childs[0])
	childs = node.getElementsByTagName('z')
	if childs:
		v.z = ret_float_value(childs[0])
	return v
#---------------------------------------------------------------------------------------------------------------------

def read_axis_points( node ):
	x1 = y1 =z1 = x2 = y2 =z2 = 'no'
	childs = node.getElementsByTagName('x1-m')
	if childs:
		x1 = ret_text_value(childs[0])
	childs = node.getElementsByTagName('y1-m')
	if childs:
		y1 = ret_text_value(childs[0])
	childs = node.getElementsByTagName('z1-m')
	if childs:
		z1 = ret_text_value(childs[0])

	childs = node.getElementsByTagName('x2-m')
	if childs:
		x2 = ret_text_value(childs[0])
	childs = node.getElementsByTagName('y2-m')
	if childs:
		y2 = ret_text_value(childs[0])
	childs = node.getElementsByTagName('z2-m')
	if childs:
		z2 = ret_text_value(childs[0])

	return "pt1 %s,%s,%s   pt2 %s,%s,%s" % (x1,y1,z1 , x2,y2,z2)
#---------------------------------------------------------------------------------------------------------------------

def read_vector_axis_points( node ):
	p1 = Vector( (0.0,0.0,0.0) )
	p2 = Vector( (0.0,0.0,0.0) )
	childs = node.getElementsByTagName('x1-m')
	if childs:
		p1.x = ret_float_value(childs[0])
	childs = node.getElementsByTagName('y1-m')
	if childs:
		p1.y = ret_float_value(childs[0])
	childs = node.getElementsByTagName('z1-m')
	if childs:
		p1.z = ret_float_value(childs[0])

	childs = node.getElementsByTagName('x2-m')
	if childs:
		p2.x = ret_float_value(childs[0])
	childs = node.getElementsByTagName('y2-m')
	if childs:
		p2.y = ret_float_value(childs[0])
	childs = node.getElementsByTagName('z2-m')
	if childs:
		p2.z = ret_float_value(childs[0])
	v = p2 - p1
	return v
#---------------------------------------------------------------------------------------------------------------------

def read_axis( node ):
	childs = node.getElementsByTagName('x1-m')
	if childs:
		return read_axis_points( node )
	childs = node.getElementsByTagName('y1-m')
	if childs:
		return read_axis_points( node )
	childs = node.getElementsByTagName('z1-m')
	if childs:
		return read_axis_points( node )
	childs = node.getElementsByTagName('x')
	if childs:
		return read_axis_vecteur( node )
	childs = node.getElementsByTagName('y')
	if childs:
		return read_axis_vecteur( node )
	childs = node.getElementsByTagName('z')
	if childs:
		return read_axis_vecteur( node )
#---------------------------------------------------------------------------------------------------------------------

def read_vector_axis( node ):
	v = Vector( (0.0,0.0,0.0) )
	childs = node.getElementsByTagName('x1-m')
	if childs:
		return read_vector_axis_points( node )
	childs = node.getElementsByTagName('y1-m')
	if childs:
		return read_vector_axis_points( node )
	childs = node.getElementsByTagName('z1-m')
	if childs:
		return read_vector_axis_points( node )
	childs = node.getElementsByTagName('x')
	if childs:
		return read_vector_axis_vecteur( node )
	childs = node.getElementsByTagName('y')
	if childs:
		return read_vector_axis_vecteur( node )
	childs = node.getElementsByTagName('z')
	if childs:
		return read_vector_axis_vecteur( node )
#---------------------------------------------------------------------------------------------------------------------

def ret_text( node ):
	s = ""
	if node.nodeType == 3:
		if node.nodeValue[0] != '\n':
			s = node.nodeValue
	return s
#---------------------------------------------------------------------------------------------------------------------

def ret_text_value( node ):
	s = ""
	if node.hasChildNodes():
		child = node.childNodes[0]
		if child.nodeType == 3:
			if child.nodeValue[0] != '\n':
				s = child.nodeValue
	return s
#---------------------------------------------------------------------------------------------------------------------

def ret_float_value( node ):
	s = 0.0
	if node.hasChildNodes():
		child = node.childNodes[0]
		if child.nodeType == 3:
			if child.nodeValue[0] != '\n':
				s = float( sup_space( child.nodeValue ) )
	return s
#---------------------------------------------------------------------------------------------------------------------

def print_element_to_xml( node ):
	debug_info( node.toxml() )
#---------------------------------------------------------------------------------------------------------------------

def print_element( node, extra ):
	if extra!= "":
		debug_info( "%s<%s>%s" % (tabs(),node.nodeName,extra) )
	else:
		debug_info( "%s<%s>" % (tabs(),node.nodeName) )
#---------------------------------------------------------------------------------------------------------------------

def print_rotate( node ):
	global niv
	
	niv += 1
	childs = node.getElementsByTagName('property')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sProperty : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('object-name')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sObject : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('axis')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_axis(child)
			debug_info( "%sAxe : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('center')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_center(child)
			debug_info( "%sCenter : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('factor')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sFactor : %s" % (tabs(),value) )
	niv -= 1
#---------------------------------------------------------------------------------------------------------------------

def print_translate( node ):
	global niv
	niv += 1
	childs = node.getElementsByTagName('property')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sProperty : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('object-name')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sObject : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('axis')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_axis(child)
			debug_info( "%sAxe : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('center')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_center(child)
			debug_info( "%sCenter : %s" % (tabs(),value) )
	niv -= 1
#---------------------------------------------------------------------------------------------------------------------

def print_light( node ):
	global niv
	niv += 1
	childs = node.getElementsByTagName('light-type')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sLight type : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('object-name')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sObject : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('position')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_vector_axis_vecteur(child)
			debug_info( "%sPosition : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('direction')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_vector_axis_vecteur(child)
			debug_info( "%sDirection : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('ambient')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_color_vecteur(child)
			debug_info( "%sAmbiente : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('diffuse')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_color_vecteur(child)
			debug_info( "%sDiffuse : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('specular')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_color_vecteur(child)
			debug_info( "%sSpecular : %s" % (tabs(),value) )
	niv -= 1

#---------------------------------------------------------------------------------------------------------------------

def print_text( node ):
	global niv
	niv += 1
	childs = node.getElementsByTagName('type')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sType : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('name')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sName : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('axis-alignment')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sAxis-alignment : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('text')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sText : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('property')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sProperty : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('format')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sFormat : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('layout')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sLayout : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('character-size')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sCharacter-size : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('character-aspect-ratio')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sCharacter-aspect-ratio : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('max-height')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sMax-height : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('max-width')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sMax-width : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('alignment')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			debug_info( "%sAlignment : %s" % (tabs(),value) )
	niv -= 1
#---------------------------------------------------------------------------------------------------------------------

def print_animation( node ):
	global option_rotation
	global option_translation
	global option_animation
	global option_light
	global niv

	childs = node.getElementsByTagName('type')
	if childs:
		for child in childs:
			if child.hasChildNodes():
				value = ret_text_value(child)
				if value == 'rotate':
					#bpy.ops.view3d.create_rotate()
					if option_rotation:
						debug_info( "%sAnimation rotate : %s" % (tabs(),value) )
						#debug_info( node.toxml() )
						print_rotate( node )
				elif value == 'translate':
					if option_translation:
						debug_info( "%sAnimation translate : %s" % (tabs(),value) )
						#debug_info( node.toxml() )
						print_translate( node )
				elif value == 'light':
					if option_light:
						debug_info( "%sAnimation light : %s" % (tabs(),value) )
						#debug_info( node.toxml() )
						print_light( node )
				else:
					if option_animation:
						debug_info( "%sAnimation type : %s" % (tabs(),value) )
	else:
		name = node.getElementsByTagName('name')
		if name:
			if option_animation:
				debug_info( "%sAnimation name" % tabs() )
				niv += 1
				value = ret_text_value(name[0])
				debug_info( "%sname : %s" % (tabs(),value) )

				childs = node.getElementsByTagName('object-name')
				for child in childs:
					value = ret_text_value(child)
					debug_info( "%sobject-name : %s" % (tabs(),value) )
				niv -= 1
			
		elif option_animation:
			debug_info( "%sAnimation sans type" % tabs() )
#---------------------------------------------------------------------------------------------------------------------

def print_offset_path( node ):
	#print_element_to_xml(node)
	childs = node.getElementsByTagName('offsets')
	if childs:
		#childs = node.getElementsByTagName('center')
		for child in childs:
			if child.hasChildNodes():
				translations = child.getElementsByTagName('x-m')
				if translations:
					value = read_center(child)
					debug_info( "%sOffset : %s" % (tabs(),value) )
					#xml_manager.xml_current.offset = read_center(child)
				roll = child.getElementsByTagName('roll-deg')
				if roll:
					debug_info( "%sroll-deg : %s" % (tabs(),ret_text_value(roll[0])) )
				pitch = child.getElementsByTagName('pitch-deg')
				if pitch:
					debug_info( "%spitch-deg : %s" % (tabs(),ret_text_value(pitch[0])) )
				heading = child.getElementsByTagName('heading-deg')
				if heading:
					debug_info( "%sheading-deg : %s" % (tabs(),ret_text_value(heading[0])) )
	else:
		if DEBUG_INFO:
			debug_info( "%sPas d'offset" % tabs() )
#---------------------------------------------------------------------------------------------------------------------

def read_rotation_path( node, xml_file ):
	xml_parent = xml_manager.get_current_xml()
	xml_file.parent_eulerXYZ	= Vector( (0.0,0.0,0.0) ) + xml_parent.eulerXYZ
	xml_file.eulerXYZ			= Vector( (0.0,0.0,0.0) )
	
	childs = node.getElementsByTagName('offsets')
	
	if childs:
		#childs = node.getElementsByTagName('center')
		for child in childs:
			if child.hasChildNodes():
				roll = child.getElementsByTagName('roll-deg')
				if roll:
					xml_file.eulerXYZ.x = xml_file.eulerXYZ.x + read_float_roll_deg(child)
				pitch = child.getElementsByTagName('pitch-deg')
				if pitch:
					xml_file.eulerXYZ.y = xml_file.eulerXYZ.y + read_float_pitch_deg(child)
				heading = child.getElementsByTagName('heading-deg')
				if heading:
					xml_file.eulerXYZ.z = xml_file.eulerXYZ.z + read_float_heading_deg(child)
	else:
		if DEBUG_INFO:
			debug_info( "%sPas de rotation" % tabs() )
#---------------------------------------------------------------------------------------------------------------------

def read_offset_path( node, xml_file ):
	xml_parent = xml_manager.get_current_xml()
	xml_file.parent_offset	= Vector( (0.0,0.0,0.0) ) + xml_parent.offset
	xml_file.offset			= Vector( (0.0,0.0,0.0) )
	
	childs = node.getElementsByTagName('offsets')
	if childs:
		for child in childs:
			if child.hasChildNodes():
				translations = child.getElementsByTagName('x-m')
				if translations:
					value = read_center(child)
					xml_file.offset = Vector( (0.0,0.0,0.0) )  + read_vector_center(child)
					
	else:
		if DEBUG_INFO:
			debug_info( "%sPas d'offset" % tabs() )
#---------------------------------------------------------------------------------------------------------------------

def read_rotation_text( node, text ):
	xml_file = xml_manager.get_current_xml()
	text.xml_offset = xml_file.offset
	text.xml_eulerXYZ = xml_file.eulerXYZ
	text.xml_parent_offset = xml_file.parent_offset
	text.xml_parent_eulerXYZ = xml_file.parent_eulerXYZ
	
	childs = node.getElementsByTagName('offsets')
	
	if childs:
		#childs = node.getElementsByTagName('center')
		for child in childs:
			if child.hasChildNodes():
				roll = child.getElementsByTagName('roll-deg')
				if roll:
					text.eulerXYZ.x = xml_file.eulerXYZ.x + read_float_roll_deg(child)
				pitch = child.getElementsByTagName('pitch-deg')
				if pitch:
					text.eulerXYZ.y = xml_file.eulerXYZ.y + read_float_pitch_deg(child)
				heading = child.getElementsByTagName('heading-deg')
				if heading:
					text.eulerXYZ.z = xml_file.eulerXYZ.z + read_float_heading_deg(child)
	else:
		if DEBUG_INFO:
			debug_info( "%sPas de rotation" % tabs() )
#---------------------------------------------------------------------------------------------------------------------

def read_offset_text( node, text ):
	xml_parent = xml_manager.get_current_xml()
	xml_file = xml_manager.get_current_xml()
	text.xml_offset = xml_file.offset
	text.xml_eulerXYZ = xml_file.eulerXYZ
	text.xml_parent_offset = xml_file.parent_offset
	text.xml_parent_eulerXYZ = xml_file.parent_eulerXYZ
	
	
	childs = node.getElementsByTagName('offsets')
	if childs:
		for child in childs:
			if child.hasChildNodes():
				translations = child.getElementsByTagName('x-m')
				if translations:
					value = read_center(child)
				text.offset = Vector( (0.0,0.0,0.0) )  + read_vector_center(child)
					
	else:
		if DEBUG_INFO:
			debug_info( "%sPas d'offset" % tabs() )
#---------------------------------------------------------------------------------------------------------------------

def compute_offset_text( text ):
	
	e = text.xml_eulerXYZ
	eleur  = Euler( (e.x, e.y, e.z) )

	mat4 = eleur.to_matrix().to_4x4()
	pos = mat4 * text.offset
	
	#tr = xml_file.offset - pos
	text.offset = text.xml_offset + pos
	text.eulerXYZ = text.eulerXYZ + text.xml_eulerXYZ
#---------------------------------------------------------------------------------------------------------------------

def compute_offset( xml_file ):
	
	e = xml_file.parent_eulerXYZ
	eleur  = Euler( (e.x, e.y, e.z) )

	mat4 = eleur.to_matrix().to_4x4()
	pos = mat4 * xml_file.offset
	
	#tr = xml_file.offset - pos
	xml_file.offset = xml_file.parent_offset + pos
	xml_file.eulerXYZ = xml_file.eulerXYZ + xml_file.parent_eulerXYZ
#---------------------------------------------------------------------------------------------------------------------

def absolute_path( filename ):
	global path_model
	
	if filename.find( path_model ) == -1:
		filename = abs_path_model + path_model + filename
	else:
		pos = filename.find(path_model)
		debug_info( "absolute_path pos path_model %d" %pos )
		debug_info( "    %s" % filename[len(path_model):] )
		filename = abs_path_model + path_model +filename[len(path_model):]
		
	return filename
#---------------------------------------------------------------------------------------------------------------------

no_include = 0;

def parse_node( node, file_name ):
	global niv
	global option_include
	global option_print_include
	global option_ac_file
	global no_include
	global mesh_layer
	global arma_layer
	

	ret_list = []
	value = ""
	extra = ""
	# Element   nodeType =1
	if node.nodeType == 1:
		extra = ""
		if node.hasChildNodes():
			extra += ret_text(node.childNodes[0])
		if node.hasAttributes():
			for i in range(node.attributes.length):
				extra += " attr:"+node.attributes.item(i).name + "=" + node.attributes.item(i).value +"  "
				if node.attributes.item(i).name == 'include':
					filename =  str(node.attributes.item(i).value)
					ret_list +=  [ (filename, no_include)  ]
					no_include += 1
					if option_print_include:
						debug_info( "%s%s include=%s" %(tabs(),node.nodeName,filename) )


		if node.nodeName == 'path':
			if node.hasChildNodes():
				if ret_text(node.childNodes[0]).find('.xml')!=-1:
					ret_list +=  [ (ret_text(node.childNodes[0]), no_include) ]
					no_include +=1
					niv -= 1
					if option_print_include:
						debug_info( "%sinclude : %s" % ( tabs(),ret_text(node.childNodes[0]) ) )
					niv += 1
					if node.parentNode:
						if node.parentNode.nodeName == 'model':
							xml_file = XML_FILE()
							debug_info( "***** CREATION OBJET XML_FILE() *****" )
							xml_file.name = absolute_path( conversion(ret_text(node.childNodes[0])) )
							debug_info( "filename = %s" % xml_file.name )
							no_include -= 1
							xml_file.no = no_include
							xml_manager.add_xml_file( xml_file, no_include )
							no_include += 1 
							if option_print_include:
								print_offset_path( node.parentNode )
							read_offset_path( node.parentNode, xml_file )
							read_rotation_path( node.parentNode, xml_file )
							compute_offset( xml_file )

				elif ret_text(node.childNodes[0]).find('.ac')!=-1:
					if option_ac_file:
						dir_name  = os.path.normpath( os.path.dirname(  file_name ) )
						file_ac = ret_text(node.childNodes[0])
						dir_name_ac = os.path.dirname(file_ac)
						
						if dir_name.find(dir_name_ac) != -1:
							file_ac = os.path.basename( file_ac )

						file_ac = dir_name + os.sep + file_ac

						if file_ac.find(os.getcwd()) == -1:
							file_ac = os.getcwd() + os.sep + file_ac
						
						if xml_manager.is_load_ac( file_ac ):
							ac_manager.clone_ac(	xml_manager.get_ac_file(file_ac),
													xml_manager.xml_current )
							xml_manager.xml_current.add_ac_file( ac_manager.get_ac_file() )
							mesh_layer = mesh_layer + 1
							arma_layer = arma_layer + 1
						else:
							if os.path.isfile(file_ac):
								from .ac_import import read_ac
								ac_option = AC_OPTION()
								ac_option.smooth_all	= True
								ac_option.edge_split	= True
								ac_option.split_angle	= 60.0
								ac_option.context		= bpy.context
								
								read_ac(	filename 	= conversion(file_ac),
											ac_option	= ac_option,
											extra		= xml_manager.xml_current )
								mesh_layer = mesh_layer + 1
								arma_layer = arma_layer + 1
								ac_file = ac_manager.get_ac_file()
								xml_manager.xml_current.add_ac_file( ac_file )
							else:
								debug_info( "xml_import:parse_node() Fichier introuvable : %s" % file_ac  )
						if node.parentNode:
							if node.parentNode.nodeName == 'model':
								xml_file = XML_FILE()
								xml_file.name = absolute_path( conversion(ret_text(node.childNodes[0])) )
								xml_file.no = no_include
								xml_manager.add_xml_file( xml_file, no_include )
								no_include += 1
								if option_print_include:
									print_offset_path( node.parentNode )
								read_offset_path( node.parentNode, xml_file )
								read_offset_path( node.parentNode, xml_file )
								read_rotation_path( node.parentNode, xml_file )
								compute_offset( xml_file )


		elif node.nodeName == 'animation':

			from .xml_import import ret_text_value
			#from .xml_import import tabs
			anim = None
			childs = node.getElementsByTagName('type')
			if childs:
				for child in childs:
					if child.hasChildNodes():
						value = ret_text_value(child)
						if value == 'rotate':
							anim = ANIM_ROTATE( node )
						elif value == 'translate':
							anim = ANIM_TRANSLATE( node )
						elif value == 'pick':
							anim = ANIM_PICK( node )
						elif value == 'light':
							anim = ANIM_LIGHT( node )
						elif value == 'shader':
							anim = ANIM_SHADER( node )
						elif value == 'spin':
							anim = ANIM_SPIN( node )
			else:
				childs = node.getElementsByTagName('name')
				if childs:
					anim = ANIM_GROUPS(node)

			#anim = ANIM()
			#anim.extract_anim( node )
			if anim != None:
				xml_manager.get_current_xml().anims.append( anim )
				print_animation( node )

		elif node.nodeName == 'fdm_config':
			debug_info( "Creation ANIM_JSB()" )
			anim = ANIM_JSB( node )
			xml_manager.get_current_xml().anims.append( anim )


		elif node.nodeName == 'text':
			text = TEXT()
			text.extract_text( node )
			read_offset_text(node, text)
			read_rotation_text(node, text)
			compute_offset_text( text )
			xml_manager.get_current_xml().texts.append( text )
			print_text( node )

		elif node.nodeName == 'aero':
			xml_file = XML_FILE()
			xml_file.name = absolute_path( conversion(ret_text(node.childNodes[0])) )
			xml_file.name = xml_file.name + '.xml'
			debug_info( "Node aero - filename : %s" % xml_file.name ) 
			xml_file.no = no_include
			xml_manager.add_xml_file( xml_file, no_include )
			ret_list +=  [ (os.path.basename(xml_file.name), xml_file.no) ]
			no_include += 1

	#Attribut nodeType =2
	elif node.nodeType == 2:
		debug_info( "%sATTR:%s = %s" % (tabs(),node.nodeName, node.nodeValue) )
	# ni texte ni commentaire    nodeType=3 ou nodeType=8
	elif node.nodeType != 3 and node.nodeType != 8:
		debug_info( "%sIndefini %d" % (tabs(), node.nodeType) )
		
		
	niv += 1
	for n in node.childNodes:
		ret_list += parse_node( n, file_name )
	niv -= 1
	return ret_list
#---------------------------------------------------------------------------------------------------------------------

def parse_file( filename, no_inc ):
	global niv 
	global path_model
	global abs_path_model
	global option_include
	global no_include
	global mesh_layer
	global option_mesh_rotate_layer
	global option_mesh_rotate_beg
	global option_mesh_rotate_end
	global arma_layer
	global option_arma_rotate_layer
	global option_arma_rotate_beg
	global option_arma_rotate_end


	if option_mesh_rotate_layer:
		#mesh_layer = mesh_layer + 1
		if mesh_layer < option_mesh_rotate_beg:
			mesh_layer = option_mesh_rotate_beg
		if mesh_layer > option_mesh_rotate_end:
			mesh_layer = option_mesh_rotate_beg
		if DEBUG_INFO:
			print ( 'mesh_layer %d' % mesh_layer )	
			
		bpy.context.scene.layers = xml_manager.layer( mesh_layer-1 )
			
	if option_arma_rotate_layer:
		#arma_layer = arma_layer + 1
		if arma_layer < option_arma_rotate_beg:
			arma_layer = option_arma_rotate_beg
		if arma_layer > option_arma_rotate_end:
			arma_layer = option_arma_rotate_beg

		if DEBUG_INFO:
			print ( 'arma_layer %d' % arma_layer )	
		#bpy.context.scene.layers = xml_manager.layer( mesh_layer-1 )
			
	
	#xml_file = XML_FILE()
	if no_inc == -1:
		xml_file = XML_FILE()
		no_include = 0
	else:
		xml_file = xml_manager.get_xml_file( filename, no_inc )
		if not xml_file:
			xml_file = XML_FILE()

	#xml_file.name = abs_path_model + filename
	xml_file.name = filename
	debug_info( "******** Nom de fichier  : %s" % xml_file.name )
	xml_file.no = no_inc
	if no_inc == -1:
		xml_manager.add_xml_file( xml_file, no_include )
	xml_manager.set_current_xml( xml_file=xml_file, no=no_include )
	
	file_includes = []
	niv = 0
	debug_info( "xml_import:parse_file()  %s " % filename )
	if os.path.isfile(filename):
		fsock = open(filename)
		try:
			xmldoc = xml.dom.minidom.parse(fsock)
		except:
			fsock.close()                 
			fsock = codecs.open(filename, 'r+', 'iso-8859-1' )
			debug_info( " **********************************************************************************" )
			debug_info( " ***************        CODEC  utf-8 invalide !!!!                  ***************" )
			debug_info( " **********************************************************************************" )
			debug_info( " ***************  Changement de Codec ; Ah les messieurs iso-8859-1 ***************" )
			debug_info( " **********************************************************************************" )
			xmldoc = xml.dom.minidom.parse(fsock)

		fsock.close()                 
		node = xmldoc.documentElement

		file_includes = parse_node( node, filename )
	else:
		debug_info( "xml_import:parse_file() Fichier introuvable : %s" % filename  )
	
	if option_include:
		debug_info( "files_includes %s" % str(file_includes)  )
		for file_include, no in file_includes:
			debug_info(  file_include )
			debug_info( path_model )
			file_include = absolute_path( conversion(file_include) )
			parse_file( conversion(file_include), no )
#---------------------------------------------------------------------------------------------------------------------

def read_file_xml( name ):
	global path_model
	global abs_path_model
	global option_include
	global option_print_include
	global option_rotation
	global option_translation
	global option_animation
	global option_ac_file

	
	current_path = os.getcwd()
	slach = os.sep

	path_name = current_path + slach + name

	base_name = os.path.basename( name )
	dir_name  = os.path.normpath( os.path.dirname(  name ) )

	debug_info( "Name : %s" % name )
	debug_info( "current_path : %s" % current_path )
	debug_info( "BaseName : %s" % base_name )
	debug_info( "DirName  : %s" % dir_name )

	if dir_name.find( 'Aircraft' )!=-1:
		right_path = dir_name.partition( 'Aircraft'+slach )[2]
		left_path = dir_name.partition( 'Aircraft'+slach )[0]

		if right_path != "":
			if len(right_path.split(slach)) >= 1:
				path_model = 'Aircraft' + slach + right_path.split(slach)[0] + slach
			else :
				path_model = 'Aircraft' + slach + right_path + slach
			abs_path_model = left_path
			file_name = name
			debug_info( base_name )
			debug_info( "path_model : %s" % path_model )
			debug_info( "abs_path_model : %s" % abs_path_model )
			debug_info( "filename : %s" % file_name )
			debug_info( "Lit fichier : %s" %( file_name) )			
			os.chdir( dir_name.partition('Aircraft')[0] )
			debug_info( "Lecture du fichier : %s " % file_name )
			parse_file( conversion(file_name), -1 )			
	
		else:
			debug_info( "Erreur : fichier 	 n'appartient pas a un avion " )
	else:
		debug_info( "Erreur : fichier 	 n'appartient pas a un avion " )

	os.chdir( current_path )
#---------------------------------------------------------------------------------------------------------------------

def charge_xml( filename ):
	global option_include
	global option_print_include
	global option_rotation
	global option_translation
	global option_animation
	global option_ac_file
	global option_light
	global option_mesh_rotate_layer
	global option_mesh_rotate_beg
	global option_mesh_rotate_end
	global option_arma_rotate_layer
	global option_arma_rotate_beg
	global option_arma_rotate_end

	option_include = False
	option_print_include = False
	option_rotation = False
	option_translation = False
	option_animation = False
	option_ac_file = False
	option_light = False
	option_mesh_rotate_layer = False
	option_mesh_rotate_beg = 0
	option_mesh_rotate_end = 10
	
	xmldoc = None
	debug_info( "xml_import:charge_xml()  %s " % filename )
	if os.path.isfile(filename):
		fsock = open(filename)
		try:
			xmldoc = xml.dom.minidom.parse(fsock)
		except:
			fsock.close()                 
			fsock = codecs.open(filename, 'r+', 'iso-8859-1' )
			debug_info( " **********************************************************************************" )
			debug_info( " ***************        CODEC  utf-8 invalide !!!!                  ***************" )
			debug_info( " **********************************************************************************" )
			debug_info( " ***************  Changement de Codec ; Ah les messieurs iso-8859-1 ***************" )
			debug_info( " **********************************************************************************" )
			xmldoc = xml.dom.minidom.parse(fsock)

		fsock.close()                 
		#node = xmldoc.documentElement
	else:
		debug_info( "*** xml_import.charge_xml( filename ) Erreur: Fichier inconnu ***" )
	return xmldoc
#---------------------------------------------------------------------------------------------------------------------
#
#							ENTRY function
#
#---------------------------------------------------------------------------------------------------------------------
def import_xml(filename, ac_option, xml_option):
	global option_include
	global option_print_include
	global option_rotation
	global option_translation
	global option_animation
	global option_ac_file
	global option_light
	global option_mesh_rotate_layer
	global option_mesh_rotate_beg
	global option_mesh_rotate_end
	global option_arma_rotate_layer
	global option_arma_rotate_beg
	global option_arma_rotate_end


	time_deb = time.time()

	option_include = xml_option.include
	option_mesh_rotate_layer = not xml_option.mesh_active_layer
	option_mesh_rotate_beg = xml_option.mesh_layer_beg
	option_mesh_rotate_end = xml_option.mesh_layer_end

	option_arma_rotate_layer = not xml_option.arma_active_layer
	option_arma_rotate_beg = xml_option.arma_layer_beg
	option_arma_rotate_end = xml_option.arma_layer_end

	option_print_include = False
	option_rotation = False
	option_translation = False
	option_animation = False
	option_ac_file = True
	option_light = False

	if DEBUG_INFO:		
		option_print_include = True
		option_rotation = True
		option_translation = True
		option_animation = True
		option_ac_file = True
		option_light = True



	# Save active layers
	save_active_layers = bpy.context.scene.layers

	read_file_xml( conversion(filename) )

	#restore active layer
	bpy.context.scene.layers = save_active_layers

	time_end = time.time()
	debug_info( "Import %s in %0.2f sec" % (os.path.basename(filename),(time_end-time_deb) ) )
	nb_rotate = 0
	nb_translate = 0
	nb_pick = 0
	nb_light = 0
	nb_shader = 0
	nb_spin = 0
	nb_xml = 0
	for xml_file, no in xml_manager.xml_files:
		for anim in xml_file.anims:
			if anim.type == 1:
				nb_rotate = nb_rotate + 1
			elif anim.type == 2:
				nb_translate = nb_translate + 1
			elif anim.type == 4:
				nb_pick = nb_pick + 1
			elif anim.type == 5:
				nb_light = nb_light + 1
			elif anim.type == 6:
				nb_shader = nb_shader + 1
			elif anim.type == 7:
				nb_spin = nb_spin + 1
		nb_xml = nb_xml + 1
	debug_info( "\tNb xml file   : %d" % nb_xml )
	debug_info( "\tNb rotate     : %d" % nb_rotate )
	debug_info( "\tNb translate  : %d" % nb_translate )
	debug_info( "\tNb pick       : %d" % nb_pick )
	debug_info( "\tNb light      : %d" % nb_light )
	debug_info( "\tNb shader     : %d" % nb_shader )
	debug_info( "\tNb spin       : %d" % nb_spin )
	

