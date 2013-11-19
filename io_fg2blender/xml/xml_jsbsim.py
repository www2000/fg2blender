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
#									XML_JSBSIM.PY
#
#----------------------------------------------------------------------------------------------------------------------------------
import sys
import os
import time
import bpy
import xml.dom.minidom
import codecs

from math import degrees
from math import fabs

from mathutils import Vector
from mathutils import Euler

#---------------------------------------------------------------------------------------------------------------------

DEBUG_INFO = False
CG = Vector( (0.0,0.0,0.0) )


#----------------------------------------------------------------------------------------------------------------------------------

def debug_info( aff):
	from .. import debug_xml_jsbsim

	if debug_xml_jsbsim:
		print( aff )
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_cg( node_doc, obj ):
	global CG
	node_mass_balance = node_doc.getElementsByTagName('mass_balance')
	if node_mass_balance:
		node_location = node_mass_balance[0].getElementsByTagName('location')
		if node_location:
			x = node_location[0].getElementsByTagName( 'x' )[0].childNodes[0]
			x.nodeValue = '%0.4f' % (obj.location.x-CG.x)
			y = node_location[0].getElementsByTagName( 'y' )[0].childNodes[0]
			y.nodeValue = '%0.4f' % (obj.location.y-CG.y)
			z = node_location[0].getElementsByTagName( 'z' )[0].childNodes[0]
			z.nodeValue = '%0.4f' % (obj.location.z-CG.z)
			debug_info( node_location[0].toxml() )
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_left_gear( node_doc, obj ):
	global CG
	node_ground_reactions = node_doc.getElementsByTagName('ground_reactions')
	if node_ground_reactions:
		node_contacts = node_ground_reactions[0].getElementsByTagName('contact')
		if node_contacts:
			for node in node_contacts:
				if node.attributes['type'].value == 'BOGEY' and node.attributes['name'].value == 'LEFT_MAIN':
					debug_info( str(node.attributes['type'].value) )
					debug_info( str(node.attributes['name'].value) )
			
					node_location = node.getElementsByTagName('location')
					if node_location:
						x = node_location[0].getElementsByTagName( 'x' )[0].childNodes[0]
						x.nodeValue = '%0.4f' % (obj.location.x-CG.x)
						y = node_location[0].getElementsByTagName( 'y' )[0].childNodes[0]
						y.nodeValue = '%0.4f' % (obj.location.y-CG.y)
						z = node_location[0].getElementsByTagName( 'z' )[0].childNodes[0]
						z.nodeValue = '%0.4f' % (obj.location.z-CG.z)
						debug_info( node.toxml() )
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_right_gear( node_doc, obj ):
	global CG
	node_ground_reactions = node_doc.getElementsByTagName('ground_reactions')
	if node_ground_reactions:
		node_contacts = node_ground_reactions[0].getElementsByTagName('contact')
		if node_contacts:
			for node in node_contacts:
				if node.attributes['type'].value == 'BOGEY' and node.attributes['name'].value == 'RIGHT_MAIN':
					debug_info( str(node.attributes['type'].value) )
					debug_info( str(node.attributes['name'].value) )
			
					node_location = node.getElementsByTagName('location')
					if node_location:
						x = node_location[0].getElementsByTagName( 'x' )[0].childNodes[0]
						x.nodeValue = '%0.4f' % (obj.location.x-CG.x)
						y = node_location[0].getElementsByTagName( 'y' )[0].childNodes[0]
						y.nodeValue = '%0.4f' % (obj.location.y-CG.y)
						z = node_location[0].getElementsByTagName( 'z' )[0].childNodes[0]
						z.nodeValue = '%0.4f' % (obj.location.z-CG.z)
						debug_info( node.toxml() )
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_tail_gear( node_doc, obj ):
	global CG
	node_ground_reactions = node_doc.getElementsByTagName('ground_reactions')
	if node_ground_reactions:
		node_contacts = node_ground_reactions[0].getElementsByTagName('contact')
		if node_contacts:
			for node in node_contacts:
				if node.attributes['type'].value == 'BOGEY' and node.attributes['name'].value == 'TAIL':
					debug_info( str(node.attributes['type'].value) )
					debug_info( str(node.attributes['name'].value) )
			
					node_location = node.getElementsByTagName('location')
					if node_location:
						x = node_location[0].getElementsByTagName( 'x' )[0].childNodes[0]
						x.nodeValue = '%0.4f' % (obj.location.x-CG.x)
						y = node_location[0].getElementsByTagName( 'y' )[0].childNodes[0]
						y.nodeValue = '%0.4f' % (obj.location.y-CG.y)
						z = node_location[0].getElementsByTagName( 'z' )[0].childNodes[0]
						z.nodeValue = '%0.4f' % (obj.location.z-CG.z)
						debug_info( node.toxml() )
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_left_wing( node_doc, obj ):
	global CG
	node_ground_reactions = node_doc.getElementsByTagName('ground_reactions')
	if node_ground_reactions:
		node_contacts = node_ground_reactions[0].getElementsByTagName('contact')
		if node_contacts:
			for node in node_contacts:
				if node.attributes['type'].value == 'STRUCTURE' and node.attributes['name'].value == 'LEFT_WING':
					debug_info( str(node.attributes['type'].value) )
					debug_info( str(node.attributes['name'].value) )
			
					node_location = node.getElementsByTagName('location')
					if node_location:
						x = node_location[0].getElementsByTagName( 'x' )[0].childNodes[0]
						x.nodeValue = '%0.4f' % (obj.location.x-CG.x)
						y = node_location[0].getElementsByTagName( 'y' )[0].childNodes[0]
						y.nodeValue = '%0.4f' % (obj.location.y-CG.y)
						z = node_location[0].getElementsByTagName( 'z' )[0].childNodes[0]
						z.nodeValue = '%0.4f' % (obj.location.z-CG.z)
						debug_info( node.toxml() )
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_right_wing( node_doc, obj ):
	global CG
	node_ground_reactions = node_doc.getElementsByTagName('ground_reactions')
	if node_ground_reactions:
		node_contacts = node_ground_reactions[0].getElementsByTagName('contact')
		if node_contacts:
			for node in node_contacts:
				if node.attributes['type'].value == 'STRUCTURE' and node.attributes['name'].value == 'RIGHT_WING':
					debug_info( str(node.attributes['type'].value) )
					debug_info( str(node.attributes['name'].value) )
			
					node_location = node.getElementsByTagName('location')
					if node_location:
						x = node_location[0].getElementsByTagName( 'x' )[0].childNodes[0]
						x.nodeValue = '%0.4f' % (obj.location.x-CG.x)
						y = node_location[0].getElementsByTagName( 'y' )[0].childNodes[0]
						y.nodeValue = '%0.4f' % (obj.location.y-CG.y)
						z = node_location[0].getElementsByTagName( 'z' )[0].childNodes[0]
						z.nodeValue = '%0.4f' % (obj.location.z-CG.z)
						debug_info( node.toxml() )
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_tail_wing( node_doc, obj ):
	global CG
	node_ground_reactions = node_doc.getElementsByTagName('ground_reactions')
	if node_ground_reactions:
		node_contacts = node_ground_reactions[0].getElementsByTagName('contact')
		if node_contacts:
			for node in node_contacts:
				if node.attributes['type'].value == 'STRUCTURE' and node.attributes['name'].value == 'TAIL':
					#debug_info( str(node.attributes['type'].value) )
					#debug_info( str(node.attributes['name'].value) )
			
					node_location = node.getElementsByTagName('location')
					if node_location:
						x = node_location[0].getElementsByTagName( 'x' )[0].childNodes[0]
						x.nodeValue = '%0.4f' % (obj.location.x-CG.x)
						y = node_location[0].getElementsByTagName( 'y' )[0].childNodes[0]
						y.nodeValue = '%0.4f' % (obj.location.y-CG.y)
						z = node_location[0].getElementsByTagName( 'z' )[0].childNodes[0]
						z.nodeValue = '%0.4f' % (obj.location.z-CG.z)
						debug_info( node.toxml() )
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_cone_wing( node_doc, obj ):
	global CG
	node_ground_reactions = node_doc.getElementsByTagName('ground_reactions')
	if node_ground_reactions:
		node_contacts = node_ground_reactions[0].getElementsByTagName('contact')
		if node_contacts:
			for node in node_contacts:
				if node.attributes['type'].value == 'STRUCTURE' and node.attributes['name'].value == 'PROP_CONE':
					#debug_info( str(node.attributes['type'].value) )
					#debug_info( str(node.attributes['name'].value) )
			
					node_location = node.getElementsByTagName('location')
					if node_location:
						x = node_location[0].getElementsByTagName( 'x' )[0].childNodes[0]
						x.nodeValue = '%0.4f' % (obj.location.x-CG.x)
						y = node_location[0].getElementsByTagName( 'y' )[0].childNodes[0]
						y.nodeValue = '%0.4f' % (obj.location.y-CG.y)
						z = node_location[0].getElementsByTagName( 'z' )[0].childNodes[0]
						z.nodeValue = '%0.4f' % (obj.location.z-CG.z)
						debug_info( node.toxml() )
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_aerorp( node_doc, obj ):
	global CG
	node_metrics = node_doc.getElementsByTagName('metrics')
	if node_metrics:
		node_locations = node_metrics[0].getElementsByTagName('location')
		if node_locations:
			for node in node_locations:
				if node.attributes['name'].value == 'AERORP':
					#debug_info( str(node.attributes['name'].value) )
					if node:
						x = node.getElementsByTagName( 'x' )[0].childNodes[0]
						x.nodeValue = '%0.4f' % (obj.location.x-CG.x)
						y = node.getElementsByTagName( 'y' )[0].childNodes[0]
						y.nodeValue = '%0.4f' % (obj.location.y-CG.y)
						z = node.getElementsByTagName( 'z' )[0].childNodes[0]
						z.nodeValue = '%0.4f' % (obj.location.z-CG.z)
						#debug_info( node.toxml() )
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_propulsion( node_doc, obj ):
	global CG
	node_propulsions = node_doc.getElementsByTagName('propulsion')
	if node_propulsions:
		node_locations = node_propulsions[0].getElementsByTagName('location')
		if node_locations:
			for node in node_locations:
				if node:
					x = node.getElementsByTagName( 'x' )[0].childNodes[0]
					x.nodeValue = '%0.4f' % (obj.location.x-CG.x)
					y = node.getElementsByTagName( 'y' )[0].childNodes[0]
					y.nodeValue = '%0.4f' % (obj.location.y-CG.y)
					z = node.getElementsByTagName( 'z' )[0].childNodes[0]
					z.nodeValue = '%0.4f' % (obj.location.z-CG.z)
					#debug_info( node.toxml() )
		
#----------------------------------------------------------------------------------------------------------------------------------
		
def write_jsbsim( context, filename  ):
	from . import xml_manager
	from . import xml_import
	global CG

	CG = Vector( (0.0,0.0,0.0) )
	#search CG point
	for obj in bpy.data.objects:
		if obj.type != 'EMPTY':
			continue
		if obj.fg.jsb_attr != 'CG':
			continue
		CG = obj.location


	debug_info( "Save : " + filename )
	template = xml_manager.addon_path + os.sep + 'io_fg2blender' + os.sep + 'templates' + os.sep + 'jsbsim_template.xml'
	debug_info( 'xml_export.write_JSBSIM() Recherche xml_file "%s"' % template )
	if os.path.isfile(filename):
		debug_info( "File exist : " + filename )
		doc = xml_import.charge_xml( filename )
	else:
		doc = xml_import.charge_xml( template )

	for obj in bpy.data.objects:
		if obj.type == 'EMPTY' and filename.find(bpy.path.abspath(obj.fg.jsb_xml_file )) != -1 and obj.fg.jsb_xml_file != "" :
			if obj.fg.jsb_attr == 'CG':
				debug_info( '--- Tranformation cg' )
				append_cg( doc, obj )
			elif obj.fg.jsb_attr == 'LEFT_GEAR':
				debug_info( '--- Tranformation left gear' )
				append_left_gear( doc, obj )
			elif obj.fg.jsb_attr == 'RIGHT_GEAR':
				debug_info( '--- Tranformation right gear' )
				append_right_gear( doc, obj )
			elif obj.fg.jsb_attr == 'TAIL_GEAR':
				debug_info( '--- Tranformation right gear' )
				append_tail_gear( doc, obj )
			elif obj.fg.jsb_attr == 'LEFT_CONTACT':
				debug_info( '--- Tranformation left wing' )
				append_left_wing( doc, obj )
			elif obj.fg.jsb_attr == 'RIGHT_CONTACT':
				debug_info( '--- Tranformation right wing' )
				append_right_wing( doc, obj )
			elif obj.fg.jsb_attr == 'TAIL_CONTACT':
				debug_info( '--- Tranformation tail wing' )
				append_tail_wing( doc, obj )
			elif obj.fg.jsb_attr == 'NOSE_CONTACT':
				debug_info( '--- Tranformation prop cone' )
				append_cone_wing( doc, obj )
			elif obj.fg.jsb_attr == 'AERO_CENTER':
				debug_info( '--- Tranformation aerorp' )
				append_aerorp( doc, obj )
			elif obj.fg.jsb_attr == 'ENGINE':
				debug_info( '--- Tranformation propulsion' )
				append_propulsion( doc, obj )

	#---------------------------------------------------------------------------
	def exist_in_text_editor(name ):
		for text in bpy.data.texts:
			if text.name == name:
				return True
		return False
	#---------------------------------------------------------------------------
	basename = os.path.basename( filename )

	if exist_in_text_editor( basename ):
		bpy.data.texts[basename].clear()
	else:
		bpy.data.texts.new( basename )


	bpy.data.texts[basename].use_tabs_as_spaces = True
	bpy.data.texts[basename].filepath = filename
	bpy.data.texts[basename].write( doc.toxml() )

	#
	# write to disk
	#

	f = open(filename, 'w')
	for line in bpy.data.texts[basename].lines:
		debug_info( line.body )
		f.write( line.body )
		f.write( '\n' )
	f.close()



