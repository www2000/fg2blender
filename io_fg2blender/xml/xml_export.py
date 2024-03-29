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
from mathutils import Matrix

from ..ui.ui_lang import lang
#from . import *
#from .__init__ import debug_xml_export as DEBUG

#---------------------------------------------------------------------------------------------------------------------

CG = Vector( (0.0,0.0,0.0) )
indent = ""


#----------------------------------------------------------------------------------------------------------------------------------

def debug_info( aff):
	from .. import debug_xml_export
	global indent

	if debug_xml_export:
		print( indent + aff )
#----------------------------------------------------------------------------------------------------------------------------------

def indentPlus():
	global indent
	
	indent = indent + "\t"
#----------------------------------------------------------------------------------------------------------------------------------

def indentMoins():
	global indent

	if len(indent) >= 1:
		indent = indent[:-1]
		
#---------------------------------------------------------------------------
def find_yFcurve( armature ):
	n = 0
	
	if armature.data.fg.type_anim in ['rotate','spin']:
		search_string = 'euler'
	if armature.data.fg.type_anim == 'translate':
		search_string = 'location'
		
	yFcurve = None
	if armature.animation_data and armature.animation_data.action:
		for fcurve in armature.animation_data.action.fcurves:
			debug_info( fcurve.data_path )
			if fcurve.data_path.find( search_string ) != -1:
				n = n + 1
			if n == 2:
				yFcurve = fcurve
				break
	return yFcurve
	
#----------------------------------------------------------------------------------------------------------------------------------

def compute_rotation_angle_current( armature ):
	yFcurve = find_yFcurve(armature)
	if yFcurve == None:
		return 0.0
	
	angle = yFcurve.evaluate( bpy.context.scene.frame_current )
	#print( "Fcurve ; %s" % yFcurve.data_path )
	#print( "%s Angle %.2f pour la frame : %.2f" % (armature.name,angle, bpy.context.scene.frame_current) ) 
	return angle
#---------------------------------------------------------------------------

def compute_translation_current( armature ):
	yFcurve = find_yFcurve(armature)
	if yFcurve == None:
		return 0.0
	
	value = yFcurve.evaluate( bpy.context.scene.frame_current ) * armature.scale.y
	debug_info( "Fcurve ; %s" % yFcurve.data_path )
	debug_info( "%s Angle %.2f pour la frame : %.2f" % (armature.name,value, bpy.context.scene.frame_current) ) 
	return value
#------------------------------------------------------------------------------------------------------------------------------------

def build_property_name( armature ):
	prop_name = "" + str(armature.data.fg.family_value)
	#prop_name = "" + str(armature.data.fg.property_value)
	#print( "%s : %s" % (armature.name,prop_name) )
	if prop_name.find('%d')!=-1:
		if armature.data.fg.property_idx == -1:
			left  = prop_name.partition('[')[0]
			right = prop_name.partition(']')[2]
			prop_name = "" + left + right
		else:
			idx = armature.data.fg.property_idx
			left  = prop_name.partition('[')[0]
			right = prop_name.partition(']')[2]
			prop_name = "" + left + '[' +  str(armature.data.fg.property_idx) + ']' + right
	elif armature.data.fg.family == 'custom':
		prop_name = "" + armature.data.fg.property_value
	elif prop_name == 'error':
		prop_name = "" + armature.data.fg.property_value
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
		txt = node.createTextNode( value ) 
		x.appendChild( txt )
		
		return x
	#---------------------------------------------------------------------------

	def test_need_interpolation( armature ):
		if armature.animation_data == None:
			return False
		n = 0
		
		if armature.data.fg.type_anim == 'rotate':
			search_string = 'euler'
		if armature.data.fg.type_anim == 'translate':
			search_string = 'location'
		
		if not armature.animation_data.action:
			return False
			
		for fcurve in armature.animation_data.action.fcurves:
			debug_info( fcurve.data_path )
			if fcurve.data_path.find( search_string ) != -1:
				n = n + 1
			if n == 2:
				break

		if len(fcurve.keyframe_points) != 2:
			return False
		
		keyframe = fcurve.keyframe_points[0]
		x = keyframe.co.x
		y = keyframe.co.y
		tFrame = armature.data.fg.time * bpy.data.scenes[0].render.fps - 1
		x = (x -1.0)/tFrame
		if t == 1:
			y = degrees(y) / armature.data.fg.factor
		if t == 2:
			y = (y) / armature.data.fg.factor


		str_x = "%0.4f" % x
		str_y = "%0.4f" % y
		debug_info( 'Range	deb="%s" fin="%s"' % ("%0.4f"%armature.data.fg.range_beg, "%0.4f"%armature.data.fg.range_end) )
		debug_info( 'Test interpolation ind="%s" dep="%s"' % (str_x, str_y) )

		if str_x == "-0.0000":
			str_x = "0.0000"
		if str_y == "-0.0000":
			str_y = "0.0000"

		debug_info( 'Value 	str_x="%s" str_y="%s"' % (str_x, str_y) )

		bDeb = False
		if str_x == "0.0000" and str_y==("%0.4f"%armature.data.fg.range_beg):
			bDeb = True
			
			
		#x = (x -1.0)/59.0
		beg = armature.data.fg.range_beg
		end = armature.data.fg.range_end
		
		coef = end - beg
		x = ( x * coef ) + beg
			
		str_x = "%0.4f" % fabs(x)
		str_y = "%0.4f" % fabs(y)
		
		keyframe = fcurve.keyframe_points[1]
		x = keyframe.co.x
		y = keyframe.co.y
		x = (x -1.0)/tFrame
		if t == 1:
			y = degrees(y) / armature.data.fg.factor
		if t == 2:
			y = (y) / armature.data.fg.factor

		str_x = "%0.4f" % x
		str_y = "%0.4f" % y
		debug_info( 'Test interpolation ind="%s" dep="%s"' % (str_x, str_y) )

		bFin = False
		if str_x == "1.0000" and str_y==("%0.4f"%armature.data.fg.range_end):
			bFin = True

		debug_info( 'ind=%0.2f dep=%0.2f' % (x, y) )
		#x = (x -1.0)/59.0
		beg = armature.data.fg.range_beg
		end = armature.data.fg.range_end
		
		coef = end - beg
		x = ( x * coef ) + beg

		str_x = "%0.4f" % x
		str_y = "%0.4f" % y
			
		if bDeb and bFin:
			return True
			
		return False
	#---------------------------------------------------------------------------
	def append_interpolation( node_animation, armature, t ):
		indentMoins()
		debug_info( 'append_interpolation' )
		indentPlus()
		if armature.animation_data == None:
			return True
		
		indentPlus()
		if test_need_interpolation(armature):
			indentMoins()
			return
		indentMoins()
		
		yFcurve = find_yFcurve(armature)
		if yFcurve == None:
			return
		interpolation = create_node('interpolation')
		debug_info( "Extraction des keyframes de : " + yFcurve.data_path )
		for keyframe in yFcurve.keyframe_points:
			entry = create_node( 'entry' )
			x = keyframe.co.x
			y = keyframe.co.y
			#y = y * armature.scale.y
			debug_info( 'x=%0.2f y=%0.2f scale.y=%0.2f' % (x, y,armature.scale.y) )
			tFrame = armature.data.fg.time * bpy.data.scenes[0].render.fps - 1
			x = (x -1.0)/tFrame
			beg = armature.data.fg.range_beg
			end = armature.data.fg.range_end
			
			if end != -999.0 and beg != -999.0:
				coef = end - beg
				x = ( x * coef ) + beg
			
			if t in ['rotate','spin']:	#rotation
				y = degrees(y) / armature.data.fg.factor
			elif t == 'translate':	#translation
				y = (y) / armature.data.fg.factor * armature.scale.y
			else:
				return

			debug_info( 'Factor "%0.2f"' % armature.data.fg.factor )
			debug_info( '      x="%0.2f", y="%0.2f"' % (x,y) )
			
			ind = create_node_value( 'ind', '%0.4f' % x )
			dep = create_node_value( 'dep', '%0.4f' % y )
			entry.appendChild( ind )
			entry.appendChild( dep )
			interpolation.appendChild( entry )
			
		node_animation.appendChild( interpolation )
	#---------------------------------------------------------------------------

	def append_objects( node_animation, armature ):
		#debug_info( 'Append_object pour "%s"' % armature.name )
		for obj in bpy.data.objects:
			if 	obj.parent:
				if obj.parent.name == armature.name:
					#debug_info( 'child object pour "%s"' % obj.name )
					if obj.type == 'MESH':
						name = obj.data.fg.name_ac
						if name == "":
							name = obj.name
					elif obj.type in [ 'EMPTY', 'ARMATURE' ]:
						#debug_info( '-Append_object recursion sur "%s"' % obj.name )
						append_objects( node_animation, obj )
						continue
					else:
						name = obj.name
					# for obj file
					#name = name + '_' + name + '.mesh'
					debug_info( 'Append_object-name "%s" pour "%s"' % (name,armature.name) )
					o = create_node_value( 'object-name', name )
					node_animation.appendChild( o )
	#---------------------------------------------------------------------------

	def get_tail( armature ):
		tail = armature.data.bones["Bone"].tail

		m = armature.matrix_world
		e = armature.delta_rotation_euler
		m_euler = e.to_matrix()
		i_delta = m_euler.inverted()
		m_delta = i_delta.to_4x4()
		l_delta =  armature.delta_location
		
		tt = m * tail
		tt0 = tt - l_delta
		tt = m_delta * tt0

		return tt
	#---------------------------------------------------------------------------

	def get_tail_local( armature ):
		tail = armature.data.bones["Bone"].tail
		return tail
	#---------------------------------------------------------------------------

	def get_head( armature ):
		head = armature.data.bones["Bone"].head

		m = armature.matrix_world
		e = armature.delta_rotation_euler
		m_euler = e.to_matrix()
		i_delta = m_euler.inverted()
		m_delta = i_delta.to_4x4()
		l_delta =  armature.delta_location
		
		ht = m * head
		ht0 = ht - l_delta
		ht = m_delta * ht0
		
		return ht
	#---------------------------------------------------------------------------

	def get_head_local( armature ):
		head = armature.data.bones["Bone"].head
		return head
	#---------------------------------------------------------------------------

	def compute_rotation_axis( armature ):
		tail = get_tail(armature)
		head = get_head(armature)

		v = tail - head
		v.normalize()
		return v
	#---------------------------------------------------------------------------

	def compute_rotation_matrix( armature ):
		angle		= compute_rotation_angle_current(armature)
		axis		= compute_rotation_axis(armature)
		location	= get_head(armature)

		rot  = Matrix.Rotation(angle, 4, axis)
		tr_n = Matrix.Translation( -location )
		tr_p = Matrix.Translation( location )

		m_ret = tr_p * rot * tr_n

		return m_ret
	#---------------------------------------------------------------------------

	def compute_translation_matrix( armature ):
		value		= compute_translation_current(armature)
		axis		= compute_rotation_axis(armature)
		axis		= value * axis

		m_ret  = Matrix.Translation( axis)

		return m_ret
	#---------------------------------------------------------------------------

	def compute_parent_matrix( armature ):
		obj = armature
		M = Matrix.Identity(4)
		while ( obj.parent != None ):
			if obj.parent.data.fg.type_anim == 'rotate':
				matrix = compute_rotation_matrix( obj.parent )
				M0 = M * matrix
				M = M0
			elif obj.parent.data.fg.type_anim == 'translate':
				matrix = compute_translation_matrix( obj.parent )
				M0 = M * matrix
				M = M0
			obj = obj.parent
			
		return M
	#---------------------------------------------------------------------------

	def append_axis( node_animation, armature ):
		axis = create_node( 'axis' )
		node_animation.appendChild( axis )

		#for evaluate transformation in current frame
		m_parent_transform = compute_parent_matrix( armature )

		M = m_parent_transform.inverted() * armature.matrix_world
		v = (M * get_tail_local(armature)) - (M * get_head_local(armature))
		#v.normalize()

		x_value = create_node_value( 'x', '%0.4f' % (v.x) )
		y_value = create_node_value( 'y', '%0.4f' % (v.y) )
		z_value = create_node_value( 'z', '%0.4f' % (v.z) )
		debug_info(  'Append_axis %0.2f %0.2f %0.2f' % (v.x, v.y, v.z) )

		axis.appendChild( x_value )
		axis.appendChild( y_value )
		axis.appendChild( z_value )
	#---------------------------------------------------------------------------

	def append_center( node_animation, armature ):
		global CG
		center = create_node( 'center' )
		node_animation.appendChild( center )

		m_parent_transform = compute_parent_matrix( armature )
		M = m_parent_transform.inverted() * armature.matrix_world
		v = M * get_head_local(armature)

		v = v - CG
 		
		loc = armature.delta_location
 		
		x_value = create_node_value( 'x-m', '%0.4f' % (v.x) )
		y_value = create_node_value( 'y-m', '%0.4f' % (v.y) )
		z_value = create_node_value( 'z-m', '%0.4f' % (v.z) )
		debug_info(  'Append_center %0.2f %0.2f %0.2f' % (v.x, v.y, v.z) )
		
		center.appendChild( x_value )
		center.appendChild( y_value )
		center.appendChild( z_value )
	#---------------------------------------------------------------------------

	def append_property( node_animation, armature ):
		obj_ctx = bpy.context.scene.objects.active
		bpy.context.scene.objects.active = armature

		value = armature.data.fg.family
		if value == "custom":
			value = armature.data.fg.property_value
		else:
			value = armature.data.fg.family_value

		debug_info( '<property>"%s"</property>' % value )
		indentPlus()
		debug_info( 'obj.name                    : "%s"' % obj.name )
		debug_info( 'obj.data.fg.family          : "%s"' % obj.data.fg.family )
		debug_info( 'obj.data.fg.family_value    : "%s"' % obj.data.fg.family_value )
		debug_info( 'obj.data.fg.property_value  : "%s"' % obj.data.fg.property_value )
		indentMoins()
	
		if value != "error" and value != '':
			if value.find('%d')!=-1:
				value = build_property_name( armature )
				debug_info( value)
			if value[0]=="/":
				value = value[1:]
			prop = create_node_value( 'property', value )
			node_animation.appendChild( prop )
		bpy.context.scene.objects.active = obj_ctx
	#---------------------------------------------------------------------------
	if obj.data.fg.factor == 0.0:
		return
	
	debug_info( 'Write Armature "%s"' % obj.name )
	nodePropertyList = node.getElementsByTagName( 'PropertyList' )

	txt = node.createComment( obj.name ) 
	nodePropertyList[0].appendChild( txt )

	animation = create_node( 'animation' )
	t = obj.data.fg.type_anim
	#--- Type ------------
	if t == 'rotate':
		type_anim = create_node_value( 'type', 'rotate' )
		animation.appendChild( type_anim )
		debug_info( 'Type = Rotate'  )
	elif t == 'translate':
		type_anim = create_node_value( 'type', 'translate' )
		animation.appendChild( type_anim )
		debug_info( 'Type = Translate'  )
	elif t == 'spin':
		type_anim = create_node_value( 'type', 'spin' )
		animation.appendChild( type_anim )
		debug_info( 'Type = Spin'  )
	#--- Object-name ------------
	append_objects( animation, obj )
	#--- Property ------------
	append_property( animation, obj )
	#--- Factor ------------
	value = '%0.6f' % obj.data.fg.factor
	#if t == 'spin':
	#	value = '1.0'
	factor = create_node_value( 'factor', value )
	animation.appendChild( factor )
	#--- Center ------------
	if t in [ 'rotate', 'spin' ]:
		append_center( animation, obj )
		append_axis( animation, obj )
	#--- Axis ------------
	if t in [ 'translate' ]:
		append_center( animation, obj )
		append_axis( animation, obj )
	#--- Interpolation ------------
	if t in [ 'rotate', 'translate' ]:
		indentPlus()
		append_interpolation( animation, obj, t  )
		indentMoins()
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
	debug_info( 'Write animation "%s"' % obj.name )
	indentPlus()
	write_animation( context, node, obj )
	indentMoins()
	lst = find_child(obj)
	for objet in lst:
		if objet.type != 'ARMATURE':
			continue
		debug_info( 'Write animation list "%s"' % objet.name )

		#write_animation( context, node, objet )
		if objet.parent!= None:
			write_animation_recurs( context, node, objet)
#----------------------------------------------------------------------------------------------------------------------------------
		
def append_path( nodeDoc, node, filename, no ):
	debug_info( 'append_path()' )
	for obj in bpy.data.objects:
		if obj.type != 'MESH':
			continue
		debug_info( obj.name )
		if obj.parent:
			debug_info( obj.parent.name )
		#if obj.parent != None:
			if obj.parent.type == 'ARMATURE':
				obj_armature = obj.parent
				if bpy.path.abspath(obj_armature.data.fg.xml_file).find( filename ) != -1 and obj_armature.data.fg.xml_file_no == no:
					from .. import fg2bl 
					
					debug_info( "Armature : %s" % obj_armature.name )
					if obj.data.fg.ac_file == "":
						bpy.ops.view3d.popup('INVOKE_DEFAULT', message="ERR007")
						return
					ac_file = "" + fg2bl.path.rel_from( obj.data.fg.ac_file, filename  )
					#ac_file = fg2bl.path.compute_path( obj.data.fg.ac_file, filename  )
					path = nodeDoc.createElement( 'path' )
					txt  = nodeDoc.createTextNode( ac_file )
					path.appendChild( txt )
					node.appendChild( path )
					return
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
	global CG
	CG = Vector( (0.0,0.0,0.0) )
	#search CG point
	for obj in bpy.data.objects:
		if obj.type != 'EMPTY':
			continue
		if obj.fg.jsb_attr != 'CG':
			continue
		CG = obj.location
 	
	debug_info( 'xml_export.write_animation_all() Recherche xml_file "%s"' % filename )
	debug_info( 'xml_export.write_animation_all() Recherche xml_file "%s"' % filename )
	cleanDoc(node,"\t","\n\r")

	nodePropertyList = node.getElementsByTagName( 'PropertyList' )

	
	txt = node.createComment( "\n\n\t***********************************************************\n\t***********************************************************\n\t\tPart of this file was generating by a blender script\n\n\t\tScript fg2blender v0.1 alpha  (c)paf\n\t\tdownload: http://gitorious.org/paf/fg2blender\n\t\tcontacts: http://equipe-flightgear.forumactif.com\n\t\tdoc:      http://wiki.flightgear.org/Fr/fg2blender\n\t***********************************************************\n\t***********************************************************\n\n\t") 
	nodePropertyList[0].appendChild( txt )
	
	append_path( node, nodePropertyList[0], filename, no )
	filename = os.path.basename( filename )

	#remove_animation( nodePropertyList[0], node )

	for obj in bpy.data.objects:
		if obj.type != 'ARMATURE':
			continue
		debug_info( "------------" )
		debug_info( "Export : %s" %obj.name )
		if obj.parent:
			debug_info( obj.parent.name )
		if obj.parent != None:
			if obj.parent.type != 'EMPTY':
				continue
		obj_filename = bpy.path.abspath(obj.data.fg.xml_file)
		debug_info( 'Obj "%s"  filename "%s"' % ( obj.name, obj_filename) )
		if bpy.path.abspath(obj.data.fg.xml_file).find( filename ) != -1 and obj.data.fg.xml_file_no == no:
			debug_info( obj.name )
			write_animation_recurs( context, node, obj )
	
