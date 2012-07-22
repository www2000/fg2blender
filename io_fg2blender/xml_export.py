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
#									XML_EXPORT.PY
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


#----------------------------------------------------------------------------------------------------------------------------------

def build_property_name( armature ):
	prop_name = armature.data.fg.familly_value
	if prop_name.find('%d')!=-1:
		idx = armature.data.fg.property_idx
		left  = prop_name.partition('[')[0]
		right = prop_name.partition(']')[2]
		return left + '[' +  str(armature.data.fg.property_idx) + ']' + right
	return prop_name
#----------------------------------------------------------------------------------------------------------------------------------

def write_animation( context, node, obj ):
	from .xml_import import charge_xml
	#---------------------------------------------------------------------------

	def create_node( key ):
		return node.createElement( key )
	#---------------------------------------------------------------------------

	def create_node_value( key, value ):
		x = node.createElement( key )
		txt = node.createTextNode( value) 
		x.appendChild( txt )
		return x
	#---------------------------------------------------------------------------

	def test_need_interpolation( armature ):
		if armature.animation_data == None:
			return True
		fcurve = armature.animation_data.action.fcurves[1]
		if len(fcurve.keyframe_points) != 2:
			return True
		
		keyframe = fcurve.keyframe_points[0]
		x = keyframe.co.x
		y = keyframe.co.y
		x = (x -1.0)/59.0
		if t == 1:
			y = degrees(y) / armature.data.fg.factor
		if t == 2:
			y = (y) / armature.data.fg.factor
		#print( 'ind=%0.2f dep=%0.2f' % (x, y) )

		str_x = "%0.4f" % fabs(x)
		str_y = "%0.4f" % fabs(y)
		if str_x != "0.0000" or str_y!="0.0000":
			return True
			
		keyframe = fcurve.keyframe_points[1]
		x = keyframe.co.x
		y = keyframe.co.y
		x = (x -1.0)/59.0
		if t == 1:
			y = degrees(y) / armature.data.fg.factor
		if t == 2:
			y = (y) / armature.data.fg.factor
		#print( 'ind=%0.2f dep=%0.2f' % (x, y) )

		str_x = "%0.4f" % x
		str_y = "%0.4f" % y
		if str_x != "1.0000" or str_y!="1.0000":
			return True
			
		return False
	#---------------------------------------------------------------------------

	def append_interpolation( node_animation, armature, t ):
		if armature.animation_data == None:
			return True
		if not test_need_interpolation(armature):
			return
		fcurve = armature.animation_data.action.fcurves[1]

		interpolation = create_node('interpolation')
		#print( fcurve.data_path )
		for keyframe in fcurve.keyframe_points:
			entry = create_node( 'entry' )
			x = keyframe.co.x
			y = keyframe.co.y
			#print( 'x=%0.2f y=%0.2f' % (x, y) )
			x = (x -1.0)/59.0
			if t == 1:	#rotation
				y = degrees(y) / armature.data.fg.factor
			if t == 2:	#translation
				y = (y) / armature.data.fg.factor
			ind = create_node_value( 'ind', '%0.4f' % x )
			dep = create_node_value( 'dep', '%0.4f' % y )
			entry.appendChild( ind )
			entry.appendChild( dep )
			interpolation.appendChild( entry )
			
		node_animation.appendChild( interpolation )
	#---------------------------------------------------------------------------

	def append_objects( node_animation, armature ):
		#print( 'Append_object pour "%s"' % armature.name )
		for obj in bpy.data.objects:
			if 	obj.parent:
				if obj.parent.name == armature.name:
					#print( 'child object pour "%s"' % obj.name )
					if obj.type == 'MESH':
						name = obj.data.fg.name_ac
						if name == "":
							name = obj.name
					elif obj.type in [ 'EMPTY', 'ARMATURE' ]:
						#print( '-Append_object recursion sur "%s"' % obj.name )
						append_objects( node_animation, obj )
						continue
					else:
						name = obj.name
					#print( 'Append_object "%s" pour "%s"' % (name,armature.name) )
					o = create_node_value( 'object-name', name )
					node_animation.appendChild( o )
	#---------------------------------------------------------------------------

	def append_axis( node_animation, armature ):
		axis = create_node( 'axis' )
		node_animation.appendChild( axis )
		head = armature.data.bones["Bone"].head
		tail = armature.data.bones["Bone"].tail
		
		m = armature.matrix_basis
		ht = m * head
		tt = m * tail
		v = tt - ht
		v.normalize()


		x_value = create_node_value( 'x', '%0.4f' % (v.x) )
		y_value = create_node_value( 'y', '%0.4f' % (v.y) )
		z_value = create_node_value( 'z', '%0.4f' % (v.z) )
		
		axis.appendChild( x_value )
		axis.appendChild( y_value )
		axis.appendChild( z_value )
	#---------------------------------------------------------------------------

	def append_center( node_animation, armature ):
		center = create_node( 'center' )
		node_animation.appendChild( center )
		head = armature.data.bones["Bone"].head

		m = armature.matrix_basis
		v = m * head
 		
		x_value = create_node_value( 'x-m', '%0.4f' % (v.x) )
		y_value = create_node_value( 'y-m', '%0.4f' % (v.y) )
		z_value = create_node_value( 'z-m', '%0.4f' % (v.z) )
		
		center.appendChild( x_value )
		center.appendChild( y_value )
		center.appendChild( z_value )
	#---------------------------------------------------------------------------

	def append_property( node_animation, armature ):
		obj_ctx = bpy.context.scene.objects.active
		bpy.context.scene.objects.active = armature

		value = armature.data.fg.familly
		#print( 'objet "%s"' % obj.name )
		#print( 'Familly "%s"' % obj.data.fg.familly )
		#print( 'Familly_value "%s"' % obj.data.fg.familly_value )
		#print( 'Property_value "%s"' % obj.data.fg.property_value )
		if value == "custom":
			value = armature.data.fg.property_value
		else:
			value = armature.data.fg.familly_value

		print( 'Value "%s"' % value )
	
		if value != "error" and value != '':
			if value.find('%d')!=-1:
				value = build_property_name( armature )
			prop = create_node_value( 'property', value )
			node_animation.appendChild( prop )
		bpy.context.scene.objects.active = obj_ctx
	#---------------------------------------------------------------------------
	
	nodePropertyList = node.getElementsByTagName( 'PropertyList' )
	#print( obj.name )
	txt = node.createComment( obj.name ) 
	nodePropertyList[0].appendChild( txt )

	animation = create_node( 'animation' )
	t = obj.data.fg.type_anim
	#--- Type ------------
	if t == 1:
		type_anim = create_node_value( 'type', 'rotate' )
		animation.appendChild( type_anim )
	elif t == 2:
		type_anim = create_node_value( 'type', 'translate' )
		animation.appendChild( type_anim )
	elif t == 7:
		type_anim = create_node_value( 'type', 'spin' )
		animation.appendChild( type_anim )
	#--- Object-name ------------
	append_objects( animation, obj )
	#--- Property ------------
	append_property( animation, obj )
	#--- Factor ------------
	value = '%0.6f' % obj.data.fg.factor
	if t == 7:
		value = '1.0'
	factor = create_node_value( 'factor', value )
	animation.appendChild( factor )
	#--- Center ------------
	if t in [1,7]:
		append_center( animation, obj )
	#--- Axis ------------
	if t in [1,2,7]:
		append_axis( animation, obj )
	#--- Interpolation ------------
	if t in [1,2]:
		append_interpolation( animation, obj, t  )
	nodePropertyList[0].appendChild( animation  )
#----------------------------------------------------------------------------------------------------------------------------------
		
def find_child( obj ):
	lst = []
	for objet in bpy.data.objects:
		if objet.parent == obj:
			lst += [objet]
	return lst
#----------------------------------------------------------------------------------------------------------------------------------
		
def write_animation_recurs( context, node, obj ):
	print( 'Write animation "%s"' % obj.name )
	write_animation( context, node, obj )
	lst = find_child(obj)
	for objet in lst:
		if objet.type != 'ARMATURE':
			continue
		print( 'Write animation list "%s"' % objet.name )

		#write_animation( context, node, objet )
		if objet.parent!= None:
			write_animation_recurs( context, node, objet)
#----------------------------------------------------------------------------------------------------------------------------------
		
def write_animation_all( context, node, filename, no ):
	#---------------------------------------------------------------------------

	def remove_animation( node, doc ):
		from .xml_import import ret_text_value

		node_list = node.getElementsByTagName( 'animation' )
		for child in node_list:
			for _child in child.childNodes:
				if _child.nodeType == node.COMMENT_NODE:
					child.removeChild( _child )
			for _type in child.getElementsByTagName( 'type' ):
				name = ret_text_value(_type)
				if  name in ['rotate','translate','spin']:
					txt = doc.createComment( '\n'+child.toprettyxml()+'\n' )
					node.appendChild( txt )
					node.removeChild( child )
	#---------------------------------------------------------------------------
	 
	def cleanNode(currentNode,indent,newl):
		filter=indent+newl
		if currentNode.hasChildNodes:
		    for node in currentNode.childNodes:
		        if node.nodeType == 3:
		            node.nodeValue = node.nodeValue.lstrip(' ').lstrip(filter).strip(filter).rstrip(' ')
		            #node.nodeValue = node.nodeValue.lstrip(' ').lstrip(filter).strip(filter).rstrip(' ').strip('--')
		            #node.nodeValue = node.nodeValue.lstrip(filter).strip(filter)
		            if node.nodeValue == "":
		                currentNode.removeChild(node)
		    for node in currentNode.childNodes:
		        cleanNode(node,indent,newl)
	#---------------------------------------------------------------------------

	def cleanDoc(document,indent="",newl=""):
		node=document.documentElement
		cleanNode(node,indent,newl)
	#---------------------------------------------------------------------------
 	
	print( 'xml_export.write_animation_all() Recherche xml_file "%s"' % filename )
	cleanDoc(node,"\t","\n\r")
	#return
	nodePropertyList = node.getElementsByTagName( 'PropertyList' )

	
	txt = node.createComment( "\n\n\t\tScript fg2blender v0.1 alpha  (c)paf http://gitorious.org/paf/fg2blender\n\t\thttp://equipe-flightgear.forumactif.com\n\n") 
	nodePropertyList[0].appendChild( txt )

	#remove_animation( nodePropertyList[0], node )

	for obj in bpy.data.objects:
		if obj.type != 'ARMATURE':
			continue
		#print( obj.name )
		#print( obj.parent.name )
		if obj.parent != None:
			if obj.parent.type != 'EMPTY':
				continue
		if obj.data.fg.xml_file.find( filename ) != -1 and obj.data.fg.xml_file_no == no:
			print( obj.name )
			write_animation_recurs( context, node, obj )
		
	
