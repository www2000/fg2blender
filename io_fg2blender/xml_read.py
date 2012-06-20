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

#!/usr/bin/env python3.2
import sys
import os

import xml.dom.minidom
import bpy
#---------------------------------------------------------------------------------------------------------------------
niv = 0
path_model = ""
option_include = False
option_print_include = False
option_rotation = False
option_translation = False
option_animation = False
option_ac_file = False

#---------------------------------------------------------------------------------------------------------------------

def tabs():
	global niv
	ret = ''
	for c in range(niv):
		ret += '\t'
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

def read_axis( node ):
	childs = node.getElementsByTagName('x1-m')
	if childs:
		return read_axis_points( node )
	childs = node.getElementsByTagName('x')
	if childs:
		return read_axis_vecteur( node )
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

def print_element_to_xml( node ):
	print( node.toxml() )
#---------------------------------------------------------------------------------------------------------------------

def print_element( node, extra ):
	if extra!= "":
		print( "%s<%s>%s" % (tabs(),node.nodeName,extra) )
	else:
		print( "%s<%s>" % (tabs(),node.nodeName) )
#---------------------------------------------------------------------------------------------------------------------

def print_rotate( node ):
	global niv
	
	niv += 1
	childs = node.getElementsByTagName('property')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			print( "%sProperty : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('object-name')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			print( "%sObject : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('axis')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_axis(child)
			print( "%sAxe : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('center')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_center(child)
			print( "%sCenter : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('factor')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			print( "%sFactor : %s" % (tabs(),value) )
	niv -= 1
#---------------------------------------------------------------------------------------------------------------------

def print_translate( node ):
	global niv
	niv += 1
	childs = node.getElementsByTagName('property')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			print( "%sProperty : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('object-name')
	for child in childs:
		if child.hasChildNodes():
			value = ret_text(child.childNodes[0])
			print( "%sObject : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('axis')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_axis(child)
			print( "%sAxe : %s" % (tabs(),value) )

	childs = node.getElementsByTagName('center')
	for child in childs:
		if child.hasChildNodes():
			#print_element_to_xml(child)
			value = read_center(child)
			print( "%sCenter : %s" % (tabs(),value) )
	niv -= 1
#---------------------------------------------------------------------------------------------------------------------

def print_animation( node ):
	global option_rotation
	global option_translation
	global option_animation
	global niv
	#child = node.find( 'type' )
	childs = node.getElementsByTagName('type')
	if childs:
		for child in childs:
			if child.hasChildNodes():
				value = ret_text_value(child)
				if value == 'rotate':
					if option_rotation:
						print( "%sAnimation rotate : %s" % (tabs(),value) )
						#print( node.toxml() )
						print_rotate( node )
				elif value == 'translate':
					if option_translation:
						print( "%sAnimation translate : %s" % (tabs(),value) )
						#print( node.toxml() )
						print_translate( node )
				else:
					if option_animation:
						print( "%sAnimation type : %s" % (tabs(),value) )
	else:
		name = node.getElementsByTagName('name')
		if name:
			if option_animation:
				print( "%sAnimation name" % tabs() )
				niv += 1
				value = ret_text_value(name[0])
				print( "%sname : %s" % (tabs(),value) )

				childs = node.getElementsByTagName('object-name')
				for child in childs:
					value = ret_text_value(child)
					print( "%sobject-name : %s" % (tabs(),value) )
				niv -= 1
			
		elif option_animation:
			print( "%sAnimation sans type" % tabs() )
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
					print( "%sOffset : %s" % (tabs(),value) )
				roll = child.getElementsByTagName('roll-deg')
				if roll:
					print( "%sroll-deg : %s" % (tabs(),ret_text_value(roll[0])) )
				pitch = child.getElementsByTagName('pitch-deg')
				if pitch:
					print( "%spitch-deg : %s" % (tabs(),ret_text_value(pitch[0])) )
				heading = child.getElementsByTagName('heading-deg')
				if heading:
					print( "%sheading-deg : %s" % (tabs(),ret_text_value(heading[0])) )
	else:
		print( "%sPas d'offset" % tabs() )
#---------------------------------------------------------------------------------------------------------------------

def parcour_child( node, file_name ):
	global niv
	global option_include
	global option_print_include
	global option_ac_file

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
					ret_list +=  [ filename ]
					if option_print_include:
						print( "%s%s include=%s" %(tabs(),node.nodeName,filename) )


		if node.nodeName == 'path':
			if node.hasChildNodes():
				if ret_text(node.childNodes[0]).find('.xml')!=-1:
					ret_list +=  [ ret_text(node.childNodes[0]) ]
					if option_print_include:
						niv -= 1
						print( "%sinclude : %s" % ( tabs(),ret_text(node.childNodes[0]) ) )
						niv += 1
						if node.parentNode:
							if node.parentNode.nodeName == 'model':
								print_offset_path( node.parentNode )

				elif ret_text(node.childNodes[0]).find('.ac')!=-1:
					if option_ac_file:
						dir_name  = os.path.normpath( os.path.dirname(  file_name ) )
						file_ac = dir_name + os.sep + ret_text(node.childNodes[0])

						print( "%sFichier AC3D <path>: %s" % (tabs(),file_ac) )

						from .import_ac import read_ac
						read_ac(	filename 	= file_ac,
									smooth_all	= True,
									edge_split	= True,
									split_angle	= 65,
									context		= bpy.context )
						#print_element_to_xml( node )
						if node.parentNode:
							#print( node.parentNode.nodeName )
							if node.parentNode.nodeName == 'model':
								print_offset_path( node.parentNode )
		elif node.nodeName == 'animation':
			print_animation( node )
	#Attribut nodeType =2
	elif node.nodeType == 2:
		print( "%sATTR:%s = %s" % (tabs(),node.nodeName, node.nodeValue) )
	# ni texte ni commentaire    nodeType=3 ou nodeType=8
	elif node.nodeType != 3 and node.nodeType != 8:
		print( "%sIndefini %d" % (tabs(), node.nodeType) )
		
		
	niv += 1
	for n in node.childNodes:
		ret_list += parcour_child( n, file_name )
	niv -= 1
	return ret_list
#---------------------------------------------------------------------------------------------------------------------

def lit_fichier( filename ):
	global niv 
	global path_model
	global option_include
	
	file_includes = []
	niv = 0
	print( "--- Lecture du fichier : %s " % filename )
	if os.path.isfile(filename):
		fsock = open(filename)
		xmldoc = xml.dom.minidom.parse(fsock) 
		fsock.close()                 
		node = xmldoc.documentElement

		if node.getElementsByTagName('animation'):
			print( filename )

		file_includes = parcour_child( node, filename )
	else:
		print( "Fichier introuvable : %s" % filename  )
	
	if option_include:
		for file_include in file_includes:
			if file_include.find( path_model ) == -1:
				file_include = path_model + file_include
			lit_fichier( file_include )
#---------------------------------------------------------------------------------------------------------------------
#
#							ENTRY function
#
#---------------------------------------------------------------------------------------------------------------------

def read_file_xml( name ):
	global path_model
	global option_include
	global option_print_include
	global option_rotation
	global option_translation
	global option_animation
	global option_ac_file
	
	path_model = ""
	option_include = True
	option_print_include = True
	option_rotation = False
	option_translation = False
	option_animation = True
	option_ac_file = True

	current_path = os.getcwd()
	slach = os.sep

	path_name = current_path + slach + name

	base_name = os.path.basename( name )
	dir_name  = os.path.normpath( os.path.dirname(  name ) )

	print( "Name : %s" % name )
	print( "current_path : %s" % current_path )
	print( "BaseName : %s" % base_name )
	print( "DirName  : %s" % dir_name )

	if dir_name.find( 'Aircraft' )!=-1:
		right_path = dir_name.partition( 'Aircraft'+slach )[2]

		if right_path != "":
			if len(right_path.split(slach)) >= 1:
				path_model = 'Aircraft' + slach + right_path.split(slach)[0] + slach
			else :
				path_model = 'Aircraft' + slach + right_path + slach

			file_name = name
			#print( base_name )
			print( path_model )
			print( file_name )
			#print( "Lit fichier : %s" %( file_name) )			
			os.chdir( dir_name.partition('Aircraft')[0] )
			#print( "Lecture du fichier : %s " % file_name )
			lit_fichier( (file_name) )			
	
		else:
			print( "Erreur : fichier 	 n'appartient pas a un avion " )
	else:
		print( "Erreur : fichier 	 n'appartient pas a un avion " )

	os.chdir( current_path )

