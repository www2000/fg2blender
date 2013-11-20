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
#									XML_CAMERA.PY
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
	from .. import debug_xml_camera

	if debug_xml_camera:
		print( aff )
#----------------------------------------------------------------------------------------------------------------------------------
		
def find_view( doc, n_view ):
	node_views = doc.getElementsByTagName('view')

	if node_views:
		for node in node_views:
			n = int(node.getAttribute("n") )
			if n == n_view:
				return node
	return None
#----------------------------------------------------------------------------------------------------------------------------------
		
def create_view( doc, n_view ):
	global CG
	
	node_view = find_view( doc, n_view )
	if not node_view:
		debug_info( "Create node view" )
		node_view = doc.getElementsByTagName('view')
		new_view = node_view[0].cloneNode(True)
		new_view.setAttribute( "n", str(n_view) )

		nodePropertyList = doc.getElementsByTagName('PropertyList')
		nodePropertyList[0].appendChild( new_view )
	else:
		debug_info( "***** vue existe !! ****" )
	
		
	
			
		
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_view( doc, obj, n_view ):
	global CG
	
	node_view = find_view( doc, n_view )

	if node_view:
		node_config = node_view.getElementsByTagName('config')
		if node_config:
			x = node_config[0].getElementsByTagName( 'z-offset-m' )[0].childNodes[0]
			x.nodeValue = '%0.4f' % (obj.location.x-CG.x)
			y = node_config[0].getElementsByTagName( 'x-offset-m' )[0].childNodes[0]
			y.nodeValue = '%0.4f' % (obj.location.y-CG.y)
			z = node_config[0].getElementsByTagName( 'y-offset-m' )[0].childNodes[0]
			z.nodeValue = '%0.4f' % (obj.location.z-CG.z)

			x = node_config[0].getElementsByTagName( 'roll-offset-deg' )[0].childNodes[0]
			x.nodeValue = '%0.4f' % (degrees(obj.rotation_euler.x) - 90 )
			y = node_config[0].getElementsByTagName( 'pitch-offset-deg' )[0].childNodes[0]
			y.nodeValue = '%0.4f' % (degrees(obj.rotation_euler.y))
			z = node_config[0].getElementsByTagName( 'heading-offset-deg' )[0].childNodes[0]
			z.nodeValue = '%0.4f' % (degrees(obj.rotation_euler.z) - 90)
	
			node_fov = node_config[0].getElementsByTagName('default-field-of-view-deg')
			if node_fov:
				node_fov[0].childNodes[0].nodeValue = '%0.2f' % degrees(obj.data.angle)
				
		node_view.setAttribute( "n", str(n_view) )
		#node_property[0].appendChild( node_view )

		
#----------------------------------------------------------------------------------------------------------------------------------
		
def write_camera( context, filename  ):
	from . import xml_manager
	from . import xml_import
	from . import xml_export

	global CG
	
	CG = Vector( (0.0,0.0,0.0) )
	#search CG point
	for obj in bpy.data.objects:
		if obj.type == 'EMPTY' and obj.fg.jsb_attr == 'CG':
			CG = obj.location
 	
	debug_info( 'xml_camera.write_camera() Write xml_file "%s"' % filename )
	basename = os.path.basename( filename )
	template = xml_manager.addon_path + os.sep + 'io_fg2blender' + os.sep + 'templates' + os.sep + 'view_template.xml'
	debug_info( 'xml_export.write_camera() xml_file "%s"' % template )
	debug_info( 'xml_export.write_camera() xml_file "%s"' % basename )

	if os.path.isfile(filename):
		debug_info( "File exist : " + filename )
		doc = xml_import.charge_xml( filename )
		xml_export.cleanDoc(doc,"\t","\n\r")
	else:
		doc = xml_import.charge_xml( template )
		xml_export.cleanDoc(doc,"\t","\n\r")

	xml_export.cleanDoc(doc,"\t","\n\r")
	
	n_view = 100;
	
	for obj in bpy.data.objects:
		if obj.type == 'CAMERA':
			#if obj.name.lower().find( 'cg') != -1:
			if obj.data.fg.type_view == 'COCKPIT_VIEW':
				debug_info( '--- Cockpit view' )
				create_view( doc, 0 )
				append_view( doc, obj, 0 )
			elif obj.data.fg.type_view == 'EXTRA_VIEW':
				debug_info( '--- Extra  view' )
				create_view( doc, n_view )
				append_view( doc, obj, n_view )
				n_view += 1
			#else:
				#debug_info( '--- view' )
				#append_view( doc, obj )

	node_property = doc.getElementsByTagName( 'PropertyList' )
	list_node_views = node_property[0].getElementsByTagName('view')
	#node_property[0].removeChild( list_node_views[0] )
	#---------------------------------------------------------------------------

	def exist_in_text_editor(name ):
		for text in bpy.data.texts:
			if text.name == name:
				return True
		return False
	#---------------------------------------------------------------------------

	if exist_in_text_editor( basename ):
		bpy.data.texts[basename].clear()
	else:
		bpy.data.texts.new( basename )


	bpy.data.texts[basename].use_tabs_as_spaces = True
	bpy.data.texts[basename].filepath = filename
	bpy.data.texts[basename].write( doc.toprettyxml() )

	
