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
	from .. import debug_xml_armement

	if debug_xml_armement:
		print( aff )
		
#----------------------------------------------------------------------------------------------------------------------------------
		
def create_gun_node(doc, obj_name):
	from . import xml_manager
	from . import xml_import
	from . import xml_export
	
	node_property_list = doc.getElementsByTagName('PropertyList')

	template = xml_manager.addon_path + os.sep + 'io_fg2blender' + os.sep + 'templates' + os.sep + 'gun_template.xml'
	debug_info( 'xml_export.create_gun() from template gun_template.xml' )


	doc_gun = xml_import.charge_xml( template )
	xml_export.cleanDoc(doc_gun,"\t","\n\r")
	node_submodel = doc_gun.getElementsByTagName('submodel')
	
	txt = doc.createComment( obj_name )
	nodePropertyList = doc.getElementsByTagName('PropertyList')
	nodePropertyList[0].appendChild( txt )

	node_property_list[0].appendChild( node_submodel[0] )
	
	return 	node_submodel

		
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_gun( node_doc, obj, number ):
	global CG

	node_submodel = node_doc.getElementsByTagName('submodel')

	if number >= len(node_submodel):
		node_submodel = create_gun_node(node_doc, obj.name)
		number = 0
		debug_info( 'Node submodel' + str(node_submodel) )
		if not node_submodel:
			print( "Error : create gun xml_jsbsim line 270:" )
			return
		else:
			print( str(node_submodel) )
	
	node_x = node_submodel[number].getElementsByTagName('x-offset')
	if node_x:
		x = node_x[0].childNodes[0]
		x.nodeValue = '%0.4f' % (3.281*(obj.location.x-CG.x))
		
	node_y = node_submodel[number].getElementsByTagName('y-offset')
	if node_y:
		y = node_y[0].childNodes[0]
		y.nodeValue = '%0.4f' % (3.281*(obj.location.y-CG.y))
		
	node_z = node_submodel[number].getElementsByTagName('z-offset')
	if node_z:
		z = node_z[0].childNodes[0]
		z.nodeValue = '%0.4f' % (3.281*(obj.location.z-CG.z))
					#debug_info( node.toxml() )
		

#----------------------------------------------------------------------------------------------------------------------------------
		
def write_armement( context, filename  ):
	from . import xml_manager
	from . import xml_import
	from . import xml_export
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
	template = xml_manager.addon_path + os.sep + 'io_fg2blender' + os.sep + 'templates' + os.sep + 'armement_template.xml'
	debug_info( 'xml_export.write_JSBSIM() Recherche xml_file "%s"' % template )

	if os.path.isfile(filename):
		debug_info( "File exist : " + filename )
		doc = xml_import.charge_xml( filename )
		xml_export.cleanDoc(doc,"\t","\n\r")
	else:
		doc = xml_import.charge_xml( template )
		xml_export.cleanDoc(doc,"\t","\n\r")
		

	for obj in bpy.data.objects:
		if obj.type == 'EMPTY' and filename.find(bpy.path.abspath(obj.fg.jsb_xml_file )) != -1 and obj.fg.jsb_xml_file != "" :
			if obj.fg.jsb_attr in ['GUN0','GUN1','GUN2','GUN3','GUN4','GUN5','GUN6','GUN7','GUN8','GUN9']:

				debug_info( '--- Save ' + obj.fg.jsb_attr )
				number = int( obj.fg.jsb_attr[3:] )
				debug_info( 'Number : ' + str(number) )
				append_gun( doc, obj, number )

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


	#
	# write in script window of blender
	#
	bpy.data.texts[basename].use_tabs_as_spaces = True
	bpy.data.texts[basename].filepath = filename
	bpy.data.texts[basename].write( doc.toprettyxml() )
	#node.toprettyxml()


	
