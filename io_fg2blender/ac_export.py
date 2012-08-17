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

import os
import bpy
import mathutils







TEX_PATH		= False
APPLY_MODIFIERS = True
SELECT_ONLY		= True

list_material = []


parent = mathutils.Vector()


path_name = ""
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
	#print( "extract_path() : %s " % path_name )






def without_path(name_path):
	name = ""
	for c in reversed(name_path):
		if c != '/':
			name = c + name
		else:
			break
	return name





def write_some_data(filepath, s):
	f = open(filepath, 'a+')
	f.write("%s" % s)
	f.close()

def writeln_some_data(filepath, s):
	f = open(filepath, 'a+')
	f.write("%s\n" % s)
	f.close()

def write_file(fi, s):
	fi.write("%s" % s)

def writeln_file(fi, s):
	fi.write("%s\n" % s)


def new_file(filepath):
	f = open(filepath, 'w')
	f.close()

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
		
	#print( "nombre %s %s   resultat %s" % (entier,mantisse,new_str) )
	return new_str
		
		

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



def write_faces( filename, mesh ):
	f = open(filename, 'a+')
	
	nbFaces = len(mesh.tessfaces)
	print( 'Nombre de face "%d"' % nbFaces )
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
	# for each face
	for i in range(nbFaces):
		face = mesh.tessfaces[i]
		'''
		meshUvLoop = mesh.uv_layers.active
		print( 'Indice  "%d"' % i )
		print( 'Nb UV "%d"' % len(meshUvLoop.data) )
		'''

		uv = []
		
		meshUvLoop = mesh.uv_layers.active
		if meshUvLoop != None:
			print( '\tNb points  "%d"' %  len(mesh.tessfaces[i].vertices) )
			print( '\tIndice  "%d"' % i )
			print( '\tNb UV "%d"' % len(meshUvLoop.data) )
			for idx in mesh.tessfaces[i].vertices:
				print( '\t\t UV "%s"' % str(meshUvLoop.data[idx].uv) )
				print( '\tIndice  "%d"' % j )
				uv.append( meshUvLoop.data[j].uv[0] )
				uv.append( meshUvLoop.data[j].uv[1] )
				j = j + 1
				#print( str(uv) )
		else:
			uv =[]
			for j in range(8):
				uv += [0.0]
				

		if len(mesh.materials) != 0:
			no = mesh.tessfaces[i].material_index
			matName = mesh.materials[no].name
			no = list_material.index(matName)
			#print( "Face no %d material %s no %d" % (i,matName,no) )
	



		nbVertices = len(face.vertices)
		# face header
		writeln_file( f, "SURF 0x10" )
		writeln_file( f, "mat %d" % no)
		writeln_file( f, "refs "+str(nbVertices) )
		# write two first vertex
		writeln_file( f, "%d %s %s" % ( face.vertices[0], significatif("%0.12f"%uv[0]), significatif("%0.12f"%uv[1]) ) )
		writeln_file( f, "%d %s %s" % ( face.vertices[1], significatif("%0.12f"%uv[2]), significatif("%0.12f"%uv[3]) ) )
		# if triangle
		if nbVertices >= 3:
			writeln_file( f, "%d %s %s" % ( face.vertices[2], significatif("%0.12f"%uv[4]), significatif("%0.12f"%uv[5]) ) )
		# if quad
		if nbVertices == 4:
			writeln_file( f, "%d %s %s" % ( face.vertices[3], significatif("%0.12f"%uv[6]), significatif("%0.12f"%uv[7]) ) )
	
	#writeln_file( f, "kids 0" )
	f.close()




def print_matrix( matrix, name ):
	print( 'Matrix "%s"'  % name )
	for i in range(4):
		#print( 'Ligne no %d' % i )
		l = matrix[i]
		print( "\t%f\t%f\t%f\t%f" % (l[0],l[1],l[2],l[3]) )
		#print( "matrix %f %f %f %f" % (l[0],l[1],l[2],l[3]) )



def extrait_translation_matrix( matrix ):
	t = matrix[3]
	ret = mathutils.Vector( (t[0],t[1],t[2]) )
	return ret

def write_vertice( filename, obj, mesh ):
	f = open(filename, 'a+')

	scale = obj.scale
	location = obj.location
	euler = obj.rotation_euler

	delta_scale = obj.delta_scale
	delta_location = obj.delta_location
	delta_euler = obj.delta_rotation_euler

	euler_string = "x=%0.6f y=%0.6f z=%0.6f" % (euler[0],euler[1],euler[2])
	scale_string = "x=%0.6f y=%0.6f z=%0.6f" % (scale[0],scale[1],scale[2])
	location_string = "x=%0.6f y=%0.6f z=%0.6f" % (location[0],location[1],location[2])

	delta_location_string = "x=%0.6f y=%0.6f z=%0.6f" % (delta_location[0],delta_location[1],delta_location[2])
	delta_scale_string = "x=%0.6f y=%0.6f z=%0.6f" % (delta_scale[0],delta_scale[1],delta_scale[2])
	delta_euler_string = "x=%0.6f y=%0.6f z=%0.6f" % (delta_euler[0],delta_euler[1],delta_euler[2])

	nbVertices = len(mesh.vertices)
	
	l = obj.matrix_basis[0]


	print( "*** Objet %s" % obj.name )
	print( "Contraints %d" % len(obj.constraints) )

	#print_matrix( obj.matrix_basis, 'matrix_basis' )
	#print_matrix( obj.matrix_local, 'matrix_local' )
	#print_matrix( obj.matrix_world, 'matrix_world' )


	'''
	b = True
	delta = mathutils.Vector( (0.0,0.0,0.0) )
	Obj = obj
	while(b):
		if Obj.parent != None:
			Obj = Obj.parent
			delta -=  mathutils.Vector( Obj.location )
		else:
			b = False
	'''
	delta =  extrait_translation_matrix(obj.matrix_world) - extrait_translation_matrix(obj.matrix_basis)
	delta =  extrait_translation_matrix(obj.matrix_world) - extrait_translation_matrix(obj.matrix_basis)
	parent = extrait_translation_matrix(obj.matrix_local) - extrait_translation_matrix(obj.matrix_basis)
	#parent = mathutils.Vector( (0.0,0.0,0.0) )

	'''
	print( "matrix %f %f %f %f" % ( obj.matrix_basis[0], obj.matrix_basis[1], obj.matrix_basis[2], obj.matrix_basis[3] )  )
	print( "matrix %f %f %f %f" % ( matrix_basis[4], matrix_basis[5], matrix_basis[6], matrix_basis[7] )  )
	print( "matrix %f %f %f %f" % ( matrix_basis[8], matrix_basis[9], matrix_basis[10], matrix_basis[11] )  )
	print( "matrix %f %f %f %f" % ( matrix_basis[12], matrix_basis[13], matrix_basis[14], matrix_basis[15] )  )
	print( "Delta location %s" % delta_location_string )
	print( "Delta scale %s" % delta_scale_string )
	print( "Delta euler %s" % delta_euler_string )
	'''
	print( "Location %s" % location_string )
	'''
	print( "Scale %s" % scale_string )
	print( "Euler %s" % euler_string )
	'''
	
	writeln_file( f, "numvert " + str(nbVertices) )
	
	vec3_locat	= mathutils.Vector(location)
	vec3_scale	= mathutils.Vector(scale)
	euler_euler	= mathutils.Euler(euler)
	mat_euler	= euler_euler.to_matrix()
	# for each vertex
	for v in mesh.vertices:
		vec3_vert = mathutils.Vector(v.co)
		vec3_resu = mathutils.Vector()

		vec3_vert.x *= vec3_scale.x
		vec3_vert.y *= vec3_scale.y
		vec3_vert.z *= vec3_scale.z

		v	= mathutils.Vector(vec3_vert)
		v_loc = mathutils.Vector( (obj.matrix_local[0][3],-obj.matrix_local[1][3],obj.matrix_local[2][3]) )
		v_wor = mathutils.Vector( (obj.matrix_world[0][3],-obj.matrix_world[1][3],obj.matrix_world[2][3]) )
		v_bas = mathutils.Vector( (obj.matrix_basis[0][3],-obj.matrix_basis[1][3],obj.matrix_basis[2][3]) )
		
		#vec3_vert -= - v_wor + v_bas + v_bas
		#v -= - v_wor + v_bas + v_bas

		vec3_vert = mat_euler * v

		vec3_vert.x -= - v_wor.x + v_bas.x
		#vec3_vert = obj.matrix_world * v


		vec3_resu = vec3_vert
		
		#vec3_resu = obj.matrix_local * vec3_vert
		#vec3_resu = vec3_vert + delta + extrait_translation_matrix(obj.matrix_local)
		#vec3_resu = vec3_vert + delta
		#vec3_resu = vec3_vert + extrait_translation_matrix(obj.matrix_local) - extrait_translation_matrix(obj.matrix_basis)

		str_x = significatif("%0.6f" % vec3_resu.x)
		str_y = significatif("%0.6f" % vec3_resu.z)
		str_z = significatif("%0.6f" % -vec3_resu.y)
		# write vertex into ac file
		writeln_file( f, str_x +' '+ str_y +' '+ str_z )		
		
	f.close()





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
		
	

def write_header_mesh( filename, obj, mesh ):
	f = open(filename, 'a+')

	try:
		#material = mesh.materials[0]
		tex_name = mesh.uv_textures[0].data[0].image.filepath
		#tex_name = mesh.uv_textures[0].data[0].image.name
		print( 'Chemin texture "%s"' % mesh.uv_textures[0].data[0].image.filepath)
		print( 'Texture "%s"' % mesh.uv_textures[0].data[0].image.name)
		#writeln_file( f, "Texture name : %s" % tex_name )
	except:
		tex_name = ""
		#print( "Impossible read image name nb mesh.materials = %d  nb uv_texture[0].data  = %d" % (len(mesh.materials),len(mesh.uv_textures[0].data)) )
		pass
	'''
	if TEX_PATH==False:
		tex_name = without_path(tex_name)
	else:
		tex_name = tex_name[2:]
		print(tex_name)
	'''
	
	#mesh location
	vec3_locat	= mathutils.Vector(obj.location) + parent
		
	writeln_file( f, "OBJECT poly" )
	writeln_file( f, 'name "' + obj.name + '"' )
	str_x = significatif("%0.6f" % vec3_locat.x)
	str_y = significatif("%0.6f" % vec3_locat.z)
	str_z = significatif("%0.6f" % -vec3_locat.y)
	writeln_file( f, "loc %s %s %s" % (str_x, str_y, str_z) )
	writeln_file( f, 'data %d'%len(obj.name) )
	writeln_file( f, obj.name )
	if tex_name != "":
		#relative_name_tex = bpy.path.relpath( tex_name, start=path_name).split('//')[1]
		relative_name_tex = bpy.path.relpath( tex_name ).split('//')[1]
		print( 'Chemin relatif "%s" ' % relative_name_tex )
		writeln_file( f, 'texture "%s"' % relative_name_tex )
		
	writeln_file( f, 'texrep 1 1' )
	cr = extrait_crease(obj,mesh)
	if cr != -1.0:
		writeln_file( f, 'crease %0.6f' % extrait_crease(obj,mesh) )

 
	f.close()



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
				#print( str(name) + " Ambient = " + amb)
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
				write_file( f, " trans %s" % significatif("%0.6f" % (1.0-material.alpha)) )
	
				writeln_file( f, "" )
	f.close()




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
				
	print( '"%s"  %d childs' % (name_parent, nb) )
	return nb







def recurs_son( filename, context, list_objects, obj ):
	print( "Ecriture de %s" % obj.name )


	if obj.type == 'MESH':
		mesh = obj.to_mesh( context.scene, APPLY_MODIFIERS, 'PREVIEW' )
		write_header_mesh( filename, obj, mesh )
		write_vertice( filename, obj, mesh )
		write_faces( filename, mesh )
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
	#print( "%d enfants" % nb )
	
	if nb != 0:
		for obj_ in list_objects:
			if test_son( list_objects, obj_, obj.name ):
				recurs_son( filename, context, list_objects, obj_ )
	#print ( " fin enfant de %s" % obj.name )
	

def write_ac_file( context, filename, object_list, select_only, tex_path, apply_modifiers ):
	global	SELECT_ONLY, TEX_PATH, APPLY_MODIFIERS
	
	SELECT_ONLY		= select_only
	TEX_PATH		= tex_path
	APPLY_MODIFIERS = apply_modifiers

	extract_path( filename )
	new_file( filename )
	writeln_some_data( filename, "AC3Db" )
	
	'''
	list_objects = []
	if SELECT_ONLY:
		for obj in context.selected_objects:
			if obj.type != 'MESH':
				continue
			list_objects.append( obj )
	else:
		list_objects = context.scene.objects
	'''	
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
	
	for obj in list_objects_sort:
		print( "Object : %s" % obj.name )
		if test_son(list_objects, obj, 'world' ):
			recurs_son( filename, context, list_objects, obj )
	
	return

