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
#									AC_EXPORT.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import os
import bpy
import mathutils
from mathutils import Vector
from mathutils import Euler

from . import *





TEX_PATH		= False
APPLY_MODIFIERS 	= True
SELECT_ONLY		= True

list_material = []

parent = mathutils.Vector()
CG = mathutils.Vector( (0.0,0.0,0.0,0.0) )

path_name = ""
#DEBUG = False
DEBUG_VERTICE = True


#----------------------------------------------------------------------------------------------------------------------------------

def debug_info( aff):
	from ... import debug_ac3d_export

	if debug_ac3d_export:
		print( aff )
#----------------------------------------------------------------------------------------------------------------------------------

def extract_path(name_path):
	global path_name
	"""
	name = ""
	rep = name_path.split('/')
	
	for i in range(len(rep)-1):
		name += rep[i] + '/'

	path_name = name
	"""
	path_name = os.path.dirname(os.path.normpath(name_path))
	debug_info( "extract_path() : %s " % path_name )
#----------------------------------------------------------------------------------------------------------------------------------

def without_path(name_path):
	name = ""
	for c in reversed(name_path):
		if c != '/':
			name = c + name
		else:
			break
	return name
#----------------------------------------------------------------------------------------------------------------------------------

def write_some_data(filepath, s):
	f = open(filepath, 'a+')
	f.write("%s" % s)
	f.close()
#----------------------------------------------------------------------------------------------------------------------------------

def writeln_some_data(filepath, s):
	f = open(filepath, 'a+')
	f.write("%s\n" % s)
	f.close()
#----------------------------------------------------------------------------------------------------------------------------------

def write_file(fi, s):
	fi.write("%s" % s)
#----------------------------------------------------------------------------------------------------------------------------------

def writeln_file(fi, s):
	fi.write("%s\n" % s)
#----------------------------------------------------------------------------------------------------------------------------------


def new_file(filepath):
	f = open(filepath, 'w')
	f.close()
#----------------------------------------------------------------------------------------------------------------------------------

def significatif( st ):
	new_str = ""
	if st.find('.') == -1:
		return st
		
	decimal = st.find('.')
	entier = st[:decimal]
	mantisse = st[decimal:]
		
	sup = False
	
	for c in reversed(mantisse):
		if c != '0' and c!='.':
			new_str = c + new_str
			sup = True
		else:
			if sup:
				new_str = c + new_str

	if new_str !="":
		new_str = entier + new_str
	else:
		new_str = entier

	if new_str == '-':
		new_str = '0'
		
	#debug_info( "nombre %s %s   resultat %s" % (entier,mantisse,new_str) )
	return new_str
#----------------------------------------------------------------------------------------------------------------------------------

def write_edges( f, mesh ):
	nbEdges = len(mesh.edges)
	writeln_file( f, "numsurf " + str(nbEdges) )

	no = 1
	try:
		material = mesh.materials[0]
	except:
		no = 0

	if no ==1:
		matName = material.name
		try:
			no = list_material.index(matName)
		except:
			no = 0

	for i in range(nbEdges):
		edge = mesh.edges[i]
		
		nbVertices = len(edge.vertices)

		writeln_file( f, "SURF 0x02" )
		writeln_file( f, "mat %d" % no )
		writeln_file( f, "refs "+str(nbVertices) )
		
		for ed in edge.vertices:
			writeln_file( f, "%d 0 0" % ed )
		#writeln_file( f, "%d 0 0" % (edge.vertices[0]) )
		#writeln_file( f, "%d 0 0" % (edge.vertices[1]) )
		
	#writeln_file( f, "kids 0" )
#----------------------------------------------------------------------------------------------------------------------------------

def find_index( obj, mesh, idx):
	n_idx = 0 + idx
	_max = len(obj.data.vertices)
	debug_info( "Compare .. %d %d" % (n_idx, _max) )
	while( n_idx >= _max ):
		debug_info( "Conversion.." )
		n_idx = 0 + mesh.loops[n_idx].vertex_index
	debug_info( "Retour %d" % n_idx )
	return n_idx




#----------------------------------------------------------------------------------------------------------------------------------

def compute_material_number( obj ):
	mesh = obj.data
	no = 1
	try:
		material = mesh.materials[0]
	except:
		no = 0
	
	# found material use by face
	if no==1:
		matName = material.name
		try:
			no = list_material.index(matName)
		except:
			no = 0
	return no

#----------------------------------------------------------------------------------------------------------------------------------

def write_faces2( filename, obj ):
	f = open(filename, 'a+')
	me = obj.data
	uv_layer = None
	if me.uv_layers:
		uv_layer = me.uv_layers.active.data

	writeln_file( f, "numsurf " + str(len(me.polygons)) )

	for poly in me.polygons:
		debug_info("Polygon index: %d, length: %d" % (poly.index, poly.loop_total))

		writeln_file( f, "SURF 0x10" )
		writeln_file( f, "mat %d" % compute_material_number(obj) )
		writeln_file( f, "refs "+str(poly.loop_total) )
		# range is used here to show how the polygons reference loops,
		# for convenience 'poly.loop_indices' can be used instead.
		for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
			debug_info("    Vertex: %d" % me.loops[loop_index].vertex_index)
			vIdx = me.loops[loop_index].vertex_index
			if uv_layer:
				debug_info("    UV: %r" % uv_layer[loop_index].uv)
				
				uv = (uv_layer[loop_index].uv[0], uv_layer[loop_index].uv[1] )
				writeln_file( f, "%d %s %s" % ( vIdx, significatif("%0.12f"%uv[0]), significatif("%0.12f"%uv[1]) ) )
			else:
				writeln_file( f, "%d" % ( vIdx ) )
	f.close()
#----------------------------------------------------------------------------------------------------------------------------------

def write_faces( filename, obj, mesh ):
	f = open(filename, 'a+')
	print_mesh( obj )
	#mesh.calc_tessface()
	nbFaces = len(mesh.tessfaces)
	debug_info( 'Mesh name : ' + mesh.name )
	debug_info( 'Nombre de face "%d"' % nbFaces )
	# if O face    mesh = edge
	if nbFaces == 0 :
		write_edges( f, mesh )
		f.close()
		return
		
	#  count face of mesh
	writeln_file( f, "numsurf " + str(nbFaces) )
	
	no = 1
	try:
		material = mesh.materials[0]
	except:
		no = 0
	
	# found material use by face
	if no==1:
		matName = material.name
		try:
			no = list_material.index(matName)
		except:
			no = 0
	
	j = 0

	debug_info( "Nb MeshLoop %d" % (len(mesh.loops)) )
	debug_info( "Nb polygons %d" % (len(mesh.polygons)) )
	debug_info( 'Nb UV "%d"' % len(mesh.uv_layers.active.data) )

	for idxLoop in range(len(mesh.loops)):
		loop = mesh.loops[idxLoop]
		IDX = loop.vertex_index
		str_debug =  ( '\tVertice %d idx %d' % (idxLoop, IDX) )
		debug_info( str_debug )


	# for each face
	for i in range(nbFaces):
		if len(mesh.materials) != 0:
			no = mesh.tessfaces[i].material_index
			matName = mesh.materials[no].name
			no = list_material.index(matName)
			debug_info( "Face no %d material %s no %d" % (i,matName,no) )
			debug_info( 'Indice face "%d"' % i )
	

		str_debug =  ( '\tLen polygon.loop_start %d ' % (mesh.polygons[i].loop_start) )
		str_debug =  str_debug + ( '\tloop_total %d ' % (mesh.polygons[i].loop_total) )
		debug_info( str_debug )

		for idxPolygon in range(mesh.polygons[i].loop_total):
			NO = mesh.polygons[i].vertices[idxPolygon]
			IDX = mesh.polygons[i].loop_indices
			str_debug =  ( '\t\tVertice index %d %s' % (NO, str(IDX)) )
			debug_info( str_debug )

		face = mesh.tessfaces[i]
		uv = []
		DEBUG_VERTICE = False
		meshUvLoop = mesh.uv_layers.active
		if meshUvLoop != None:
			if DEBUG_VERTICE:
				debug_info( '\tNb vertices      "%d"' %  len(mesh.tessfaces[i].vertices) )
				debug_info( '\tNb vertices_raw  "%d"' %  len(mesh.tessfaces[i].vertices_raw) )
			k = 0
			for idx in mesh.tessfaces[i].vertices:
				if DEBUG_VERTICE:
					str_debug =  ( '\tPt idx vertices %d vertices_raw %d \tUV Idx  "%d"' % (face.vertices[k],face.vertices_raw[k],j) ) + ( '\t\t "%s"' % str(meshUvLoop.data[idx].uv) )
					debug_info( str_debug )
					k += 1;
					#debug_info( '\tIndice  "%d"' % j )
					#debug_info( '\t\t UV "%s"' % str(meshUvLoop.data[idx].uv) )
				uv.append( meshUvLoop.data[j].uv[0] )
				uv.append( meshUvLoop.data[j].uv[1] )
				j = j + 1
		else:
			uv =[]
			for j in range(8):
				uv += [0.0]
				



		nbVertices = len(face.vertices)
		# face header
		writeln_file( f, "SURF 0x10" )
		writeln_file( f, "mat %d" % no)
		writeln_file( f, "refs "+str(nbVertices) )
		# write two first vertex
		vIdx = find_index( obj, mesh, face.vertices_raw[0] )
		writeln_file( f, "%d %s %s" % ( vIdx, significatif("%0.12f"%uv[0]), significatif("%0.12f"%uv[1]) ) )
		
		vIdx = find_index( obj, mesh, face.vertices_raw[1] )
		writeln_file( f, "%d %s %s" % ( vIdx, significatif("%0.12f"%uv[2]), significatif("%0.12f"%uv[3]) ) )
		# if triangle
		if nbVertices >= 3:
			vIdx = find_index( obj, mesh, face.vertices_raw[2] )
			writeln_file( f, "%d %s %s" % ( vIdx, significatif("%0.12f"%uv[4]), significatif("%0.12f"%uv[5]) ) )
		# if quad
		if nbVertices == 4:
			vIdx = find_index( obj, mesh, face.vertices_raw[3] )
			writeln_file( f, "%d %s %s" % ( vIdx, significatif("%0.12f"%uv[6]), significatif("%0.12f"%uv[7]) ) )
	
	#writeln_file( f, "kids 0" )
	f.close()
#----------------------------------------------------------------------------------------------------------------------------------

def print_matrix( matrix, name ):
	debug_info( 'Matrix "%s"'  % name )
	for i in range(4):
		debug_info( 'Ligne no %d' % i )
		l = matrix[i]
		debug_info( "\t%f\t%f\t%f\t%f" % (l[0],l[1],l[2],l[3]) )
		debug_info( "matrix %f %f %f %f" % (l[0],l[1],l[2],l[3]) )
#----------------------------------------------------------------------------------------------------------------------------------

def extrait_translation_matrix( matrix ):
	t = matrix[3]
	ret = mathutils.Vector( (t[0],t[1],t[2]) )
	return ret
#----------------------------------------------------------------------------------------------------------------------------------

def write_vertice( filename, obj, _mesh ):
	global parent, CG
	
	f = open(filename, 'a+')

	location = obj.location
	debug_info( '---------------' )
	debug_info( 'write_vertice' )
	debug_info( '---------------' )
	debug_info( obj.name )
	mesh = obj.data
	debug_info( mesh.name )
	
	nbVertices = len( mesh.vertices )
	writeln_file( f, "numvert " + str(nbVertices) )
	
	m = obj.matrix_world
	# delta_location and delta euler use for offset xml
	# compute the invert matrix for euler
	# and subtract delta_location
	e = obj.delta_rotation_euler
	mat_euler = e.to_matrix()
	debug_info( 'Determinant matrice rotation euler %02f' % mat_euler.determinant() )
	i_delta = mat_euler.inverted()
	m_delta = i_delta.to_4x4()
	l_delta =  obj.delta_location
	
	debug_info( '\n%d points' % (len(mesh.vertices)) )
	i = 0;
	# for each vertex
	for v in mesh.vertices:
		vec3_vert = mathutils.Vector(v.co)
		vec3_resu = mathutils.Vector()

		vec3_resu = m * vec3_vert
		vec3_vert = vec3_resu - l_delta
		vec3_resu = m_delta * vec3_vert
		
		vec3_resu = vec3_resu - (mathutils.Vector(obj.location) + parent)

		str_x = significatif("%0.6f" % vec3_resu.x)
		str_y = significatif("%0.6f" % vec3_resu.z)
		str_z = significatif("%0.6f" % -vec3_resu.y)
		# write vertex into ac file
		writeln_file( f, str_x +' '+ str_y +' '+ str_z )		
		debug_info( '\t pt  %d  (%0.2f,%0.2f,%0.2f)' % (i, vec3_resu.x, vec3_resu.y, vec3_resu.z) )
		i += 1
		
	f.close()
#----------------------------------------------------------------------------------------------------------------------------------

def extrait_crease( obj, mesh ):
	pi = 3.141592653589793238462643383279502884197
	if len(obj.modifiers)!=0:
		for mod in obj.modifiers:
			if mod.type=='EDGE_SPLIT':
				return mod.split_angle/pi*180.0
	if mesh.use_auto_smooth:	
		if mesh.auto_smooth_angle!=0.0:
			return mesh.auto_smooth_angle/pi*180.0
	else:
		return -1.0
	
	return 30.0
#----------------------------------------------------------------------------------------------------------------------------------

def write_header_mesh( filename, obj, mesh ):
	global path_name
	global CG
	
	f = open(filename, 'a+')

	try:
		#n = mesh.tessfaces[0].material_index
		n = obj.data.polygons[0].material_index
		#tex_name = mesh.materials[n].texture_slots[0].texture.image.filepath
		tex_name = obj.data.materials[n].texture_slots[0].texture.image.filepath
		if tex_name.find('glass_shader') != -1:
			tex_name = ""
	except:
		print( 'Error: Unload texture name for "%s"' % obj.name )
		tex_name = ''
		pass

	vec3_locat	= mathutils.Vector(obj.location) + parent - CG
		
	writeln_file( f, "OBJECT poly" )
	writeln_file( f, 'name "' + obj.name + '"' )
	
	str_x = significatif("%0.6f" % vec3_locat.x)
	str_y = significatif("%0.6f" % vec3_locat.z)
	str_z = significatif("%0.6f" % -vec3_locat.y)
	
	writeln_file( f, "loc %s %s %s" % (str_x, str_y, str_z) )
	writeln_file( f, 'data %d'%len(obj.name) )
	writeln_file( f, obj.name )
	
	if tex_name != "":
		path = os.path.dirname( bpy.path.abspath(tex_name) )
		relpath = os.path.relpath( path, path_name )
		debug_info( 'Texture name (tex_name) "%s"' % tex_name )
		debug_info( 'Path  (tex_name) "%s"' % path )
		debug_info( 'RelPath  (tex_name) "%s"' % relpath )
		if relpath == '.':
			relative_name_tex = os.path.basename( tex_name )
		else:
			relative_name_tex = relpath + os.sep + os.path.basename( tex_name )
		debug_info( 'Chemin relatif "%s" ' % relative_name_tex )
		writeln_file( f, 'texture "%s"' % relative_name_tex )
		
	writeln_file( f, 'texrep 1 1' )
	cr = extrait_crease(obj,mesh)
	if cr != -1.0:
		writeln_file( f, 'crease %0.6f' % extrait_crease(obj,mesh) )

 
	f.close()
#----------------------------------------------------------------------------------------------------------------------------------

def write_material( filename, sel_obj ):
	global list_material

	list_material = []
	
	f = open(filename, 'a+')
	
	
	for obj in sel_obj:
		if obj.type != 'MESH':
			continue
		if len(obj.data.materials)==0:
			continue
			
		for material in obj.data.materials:
			if material == None:
				continue
			name = material.name
			if name == 'Material_Pick':
				continue 

			try:
				no = list_material.index(name)
			except:
				# first use material -> write into ac file
				list_material += [name]

				write_file( f, 'MATERIAL "%s"' % str(name) )
				# color
				color = material.diffuse_color
				str_color = significatif("%0.6f"%color[0]) +' '+ significatif("%0.6f"%color[1]) +' '+ significatif("%0.6f"%color[2])
				write_file( f, " rgb %s" % str_color )
				# amb
				amb = significatif( "%0.6f"% material.ambient )
				debug_info( str(name) + " Ambient = " + amb)
				write_file( f, " amb %s %s %s"%(amb,amb,amb) )
				# emit
				emit = significatif( "%0.6f"%material.emit)
				write_file( f, " emis %s %s %s"%(emit,emit,emit) )
				# specular
				spec = material.specular_color
				str_spec = significatif( "%0.6f"%spec[0]) +' '+ significatif( "%0.6f"%spec[1]) +' '+ significatif( "%0.6f"%spec[2])
				write_file( f, " spec %s" % str_spec )
				# shininess
				write_file( f, " shi %d" % material.specular_hardness )
				# transparent
				value = material.alpha
				if len(material.texture_slots)>=1:
					if material.texture_slots[0] != None:
						if material.texture_slots[0].use_map_alpha and obj.show_transparent == False:
							value = 1.0
							#write_file( f, " trans %s" % significatif("%0.6f" % (0.0) ) )

				write_file( f, " trans %s" % significatif("%0.6f" % (1.0-value)) )
	
				writeln_file( f, "" )
	f.close()
#----------------------------------------------------------------------------------------------------------------------------------

def test_son( list_objects, obj,name_parent ):
	if obj.parent!=None:
		if obj.parent.type == 'ARMATURE':
			name_parent == 'world'
			return True
		if obj.parent.name == name_parent:
			return True
	elif name_parent == 'world':
		return True

	return False
#----------------------------------------------------------------------------------------------------------------------------------

def count_son( list_objects, name_parent ):
	nb = 0
	for obj in list_objects:
			if obj.parent!=None:
				if obj.parent.type == 'ARMATURE' and name_parent == 'world':
					nb += 1
					continue
				if obj.parent.type != 'MESH':
					continue
					#name_parent == 'world'
					#nb += 1
				if obj.parent.name == name_parent:
					nb += 1
			elif name_parent == 'world':
				nb += 1
				
	debug_info( '"%s"  %d childs' % (name_parent, nb) )
	return nb
#----------------------------------------------------------------------------------------------------------------------------------

def recurs_son( filename, context, list_objects, obj ):
	debug_info( "Ecriture de %s" % obj.name )

	if obj.type == 'MESH':
		mesh_local = obj.to_mesh( context.scene, APPLY_MODIFIERS, 'PREVIEW' )
		#write_header_mesh( filename, obj, mesh )
		#write_faces( filename, mesh )
		#write_vertice( filename, obj, mesh )
		
		write_header_mesh( filename, obj, obj.data )
		write_vertice( filename, obj, obj.data )
		#write_faces( filename, obj, mesh_local )
		write_faces2( filename, obj )
	elif obj.type == 'EMPTY':
		writeln_some_data( filename, "OBJECT group" )
		writeln_some_data( filename, 'name "' + obj.name + '"' )
		vec3_locat	= mathutils.Vector(obj.location)
		str_x = significatif("%0.6f" % vec3_locat.x)
		str_y = significatif("%0.6f" % vec3_locat.z)
		str_z = significatif("%0.6f" % -vec3_locat.y)
		writeln_some_data( filename, "loc %s %s %s" % (str_x, str_y, str_z) )
		
		


	nb = count_son(list_objects, obj.name)
	writeln_some_data( filename, "kids %d" % nb )
	debug_info( "%d enfants" % nb )
	
	if nb != 0:
		for obj_ in list_objects:
			if test_son( list_objects, obj_, obj.name ):
				recurs_son( filename, context, list_objects, obj_ )
	debug_info ( " fin enfant de %s" % obj.name )
#----------------------------------------------------------------------------------------------------------------------------------

def write_ac_file( context, filename, object_list, select_only, tex_path, apply_modifiers ):
	global	SELECT_ONLY, TEX_PATH, APPLY_MODIFIERS
	global CG
	
	SELECT_ONLY		= select_only
	TEX_PATH		= tex_path
	APPLY_MODIFIERS = apply_modifiers

	extract_path( filename )
	new_file( filename )
	writeln_some_data( filename, "AC3Db" )
	
	list_objects = object_list
	
	# create dictionnary for mesh order
	dic_obj_meshs = {}
	for obj in list_objects:
		if obj.type == 'MESH' or obj.type == 'EMPTY':
			dic_obj_meshs[obj.name] = obj
			
	list_objects_sort = []
	for name in sorted(dic_obj_meshs.keys()):
		list_objects_sort.append( dic_obj_meshs[name] )
	
	
	# write materials	
	write_material( filename, list_objects )
	# Header
	# object world
	writeln_some_data( filename, "OBJECT world" )
	writeln_some_data( filename, "kids %d" % count_son(list_objects, 'world' ) )
	
	CG = mathutils.Vector( (0.0,0.0,0.0) )
	#search CG point
	for obj in bpy.data.objects:
		if obj.type == 'EMPTY' and obj.fg.jsb_attr == 'CG':
			CG = obj.location

	debug_info( 'Gravity center "%s"' % str(CG) )
	
	for obj in list_objects_sort:
		debug_info( "Object : %s" % obj.name )
		if test_son(list_objects, obj, 'world' ):
			recurs_son( filename, context, list_objects, obj )
	
	return

