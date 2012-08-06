'''
====================================================================================================================



				EXPORT


====================================================================================================================
'''
import os
import bpy
import mathutils

from math import radians
from math import degrees


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


	
def write_file(fi, s):
	fi.write("%s" % s)

def writeln_file(fi, s):
	fi.write("%s\n" % s)


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
		
		
'''
	mesh.edges
    Edge in a Mesh datablock
    is_loose
        Loose edge
        Type :	boolean, default False
    select
        Type :	boolean, default False
   
'''

def write_edges( f, mesh ):
	
	nbEdges = len(mesh.edges)
	
	writeln_file( f, "numsurf " + str(nbEdges) )
	
	mesh_materials = mesh.materials
	no = 0 # by default, put 'default white'                                                                                                                                                                         
	if len(mesh_materials) > 0:                                                                                                                                                                                         
			if mesh_materials[0] is not None:                                                                                                                                                         
					if mesh_materials[0].name!="DefaultWhite":
					
						no = list_material.index(mesh_materials[0].name)+1 #+1 because we have 'default white'    


	for i in range(nbEdges):
		edge = mesh.edges[i]
	
		nbVertices = len(edge.vertices)

		writeln_file( f, "SURF 0x02" )
		writeln_file( f, "mat %d" % no )
		writeln_file( f, "refs "+str(nbVertices) )
		
		for ed in edge.vertices:
			writeln_file( f, "%d 0 0" % ed )
		


def write_faces( f, mesh ):
	
	nbFaces = len(mesh.polygons)
	
	if nbFaces == 0 :
		write_edges( f, mesh )
		return
		
	#count face of mesh
	writeln_file( f, "numsurf " + str(nbFaces) )
	
	totUvNr=0	
	uvnr=0
	# for each face
	for i in range(nbFaces):
		face = mesh.polygons[i]
		nbVertices = len(face.vertices)
		uvnr=nbVertices*2
		
		try :
			uv_tex = mesh.uv_layers.active.data[:]
			uv = []
			for j in range(nbVertices):
				uv.append(uv_tex[totUvNr+j].uv[0])
				uv.append(uv_tex[totUvNr+j].uv[1])
		
		except:
			uv =[]
			for j in range(uvnr):
				uv += [0.0]

		totUvNr = totUvNr+ nbVertices	
		
		'''
		Surf section	SURF %d

		The start of a surface. The parameter specifies the surface type and flags. T
		he first 4 bits (flags & 0xF) is the type (0 = polygon, 1 = closedline, 2 = line). 
		The next four bits (flags >> 4) specify the shading and backface. 
		bit1 = shaded surface bit2 = twosided.
		'''
		flaglow  = 0 # polygon
		flaghigh = 0
		
		if face.use_smooth:
			flaghigh = flaghigh+ 1
			
		if mesh.show_double_sided:
			flaghigh = flaghigh+ 2
			
		surfstr = "SURF 0x%d%d" % (flaghigh, flaglow)
		# face header
		writeln_file( f, surfstr)
		
		# calculating material number:
		mesh_materials = mesh.materials
		matno = 0 # by default, put 'default white'                                                                                                                                                                         
		if len(mesh_materials) > 0:                                                                                                                                                                                         
				if mesh_materials[face.material_index] is not None:                                                                                                                                                         
						if mesh_materials[face.material_index].name!="DefaultWhite":
						
							matno = list_material.index(mesh_materials[face.material_index].name)+1 #+1 because we have 'default white'    
		
		
		# found material used by face
		
		writeln_file( f, "mat %d" % matno)
		writeln_file( f, "refs "+str(nbVertices) )
	
		iVxy = 0
		for iVert in range(nbVertices):
			writeln_file( f, "%d %s %s" % ( face.vertices[iVert], significatif("%0.12f"%uv[iVxy]), significatif("%0.12f"%uv[iVxy+1]) ) )
			iVxy=iVxy+2


def print_matrix( matrix ):
	l = matrix[3]
	#for l in matrix:
	print( "matrix %f %f %f %f" % (l[0],l[1],l[2],l[3]) )



def extrait_translation_matrix( matrix ):
	t = matrix[3]
	ret = mathutils.Vector( (t[0],t[1],t[2]) )
	return ret

def write_vertice( f, obj, mesh ):
	
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

	delta =  extrait_translation_matrix(obj.matrix_world) - extrait_translation_matrix(obj.matrix_basis)
	delta =  extrait_translation_matrix(obj.matrix_world) - extrait_translation_matrix(obj.matrix_basis)
	parent = extrait_translation_matrix(obj.matrix_local) - extrait_translation_matrix(obj.matrix_basis)
	
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
		vec3_vert = mat_euler * v
		
		vec3_resu = vec3_vert + extrait_translation_matrix(obj.matrix_local) - extrait_translation_matrix(obj.matrix_basis)

		str_x = significatif("%0.6f" % vec3_resu.x)
		str_y = significatif("%0.6f" % vec3_resu.z)
		str_z = significatif("%0.6f" % -vec3_resu.y)
		# write vertex into ac file
		writeln_file( f, str_x +' '+ str_y +' '+ str_z )		
		


def extrait_crease( obj, mesh ):
	pi = 3.141592653589793238462643383279502884197
	if len(obj.modifiers)!=0:
		for mod in obj.modifiers:
			if ((mod.type=='EDGE_SPLIT') and (mod.use_edge_angle==True) ):
				return (mod.split_angle/pi)*180.0
	if mesh.use_auto_smooth:	
		if mesh.auto_smooth_angle!=0.0:
			return (mesh.auto_smooth_angle/pi)*180.0
	else:
		#return -1.0
		return 179.0
	
	return 30.0
		
	

def write_header_mesh( f, obj, mesh ):
	
	tex_name = ""
	texrepx = 1
	texrepy = 1
	
	try:
		#material = mesh.materials[0]
		if mesh.materials[0].texture_slots[0].texture.type =='IMAGE':
			tex_name = mesh.materials[0].texture_slots[0].texture.image.filepath
			
			texrepx = mesh.materials[0].texture_slots[0].texture.repeat_x
			texrepy = mesh.materials[0].texture_slots[0].texture.repeat_y
	except:
		tex_name = ""
		
	try:
		#material = mesh.materials[0]
		tex_name = mesh.tessface_uv_textures[0].data[0].image.filepath
		
	except:
		tex_name = ""
			
	if TEX_PATH==False:
		tex_name = without_path(tex_name)
	else:
		tex_name = tex_name[2:]
		print(tex_name)
	
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
		relative_name_tex = tex_name
		#print( relative_name_tex )
		writeln_file( f, 'texture "%s"' % relative_name_tex )
		writeln_file( f, 'texrep %0.6f %0.6f' % (texrepx,  texrepy) )
		
	cr = extrait_crease(obj,mesh)
	if cr != -1.0:
		writeln_file( f, 'crease %0.6f' % extrait_crease(obj,mesh) )



def write_material( f, sel_obj ):
	global list_material

	list_material = []
	
	writeln_file( f, 'MATERIAL "DefaultWhite" rgb 1 1 1  amb 1 1 1  emis 0 0 0  spec 0.5 0.5 0.5  shi 64  trans 0' )
	
	for obj in sel_obj:
		if obj.type != 'MESH':
			continue
		
		
		if len(obj.data.materials)==0:
			continue
			
		for material in obj.data.materials:
			
			if (( material !=None)  and  (material.name !='DefaultWhite') ):
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
					#write_file( f, " shi %d" % material.specular_hardness )
				
					# shininess
					#write_file( f, " shi %d" % material.specular_hardness )
					write_file( f, " shi %d" % int( material.specular_intensity * 128 ) )
					#shininess of materials is taken from the shader specularity value in Blender, 
					#old mapped from [0.0, 2.0] to [0, 128]
					#noting above 1.0 so mapped from [0.0, 1.0] to [0, 128]
					
					# transparent
					write_file( f, " trans %s" % significatif("%0.6f" % (1.0-material.alpha)) )
		
					writeln_file( f, "" )


def test_son( list_objects, obj,name_parent ):
	if obj.parent!=None:
		if obj.parent.name == name_parent:
			return True
	elif name_parent == 'world':
		return True

	return False


def count_son( list_objects, name_parent ):
	nb = 0
	for obj in list_objects:
			if obj.parent!=None:
				if obj.parent.name == name_parent:
					nb += 1
			elif name_parent == 'world':
				nb += 1
	return nb


def recurs_son( f, context, list_objects, obj ):
	print( "Ecriture de %s" % obj.name )


	if obj.type == 'MESH':
		mesh = obj.to_mesh( context.scene, APPLY_MODIFIERS, 'PREVIEW' )
		write_header_mesh( f, obj, mesh )
		write_vertice( f, obj, mesh )
		write_faces( f, mesh )
	elif obj.type == 'EMPTY':
		f.write("OBJECT group\n" )
		f.write('name "' + obj.name + '"\n' )
		vec3_locat   = mathutils.Vector(obj.location)
		str_x = significatif("%0.6f" % vec3_locat.x)
		str_y = significatif("%0.6f" % vec3_locat.z)
		str_z = significatif("%0.6f" % -vec3_locat.y)
		f.write("loc %s %s %s\n" % (str_x, str_y, str_z) )


	nb = count_son(list_objects, obj.name)
	f.write("kids %d\n" % nb )
	#print( "%d enfants" % nb )
	
	if nb != 0:
		for obj_ in list_objects:
			if test_son( list_objects, obj_, obj.name ):
				recurs_son( f, context, list_objects, obj_ )
	#print ( " fin enfant de %s" % obj.name )

		
# writes an ac file 
def write_ac_file( context, filename, select_only, apply_modifiers ):
	global	SELECT_ONLY, TEX_PATH, APPLY_MODIFIERS
	
	SELECT_ONLY		= select_only
	TEX_PATH			= False
	APPLY_MODIFIERS 	= apply_modifiers

	
	extract_path( filename )
	
	f = open(filename, 'w')
	f.write("%s\n" %  "AC3Db" )
	
	if SELECT_ONLY:
		list_objects = context.selected_objects
	else:
		list_objects = context.scene.objects
	
	# create dictionnary for mesh order
	dic_obj_meshs = {}
	for obj in list_objects:
		if obj.type == 'MESH' or obj.type == 'EMPTY':
			dic_obj_meshs[obj.name] = obj
			
	list_objects_sort = []
	for name in sorted(dic_obj_meshs.keys()):
		list_objects_sort.append( dic_obj_meshs[name] )
	
	
	# write materials   
	write_material( f, list_objects )
	# Header
	# object world
	f.write("%s\n" % "OBJECT world" )
	string_to_write = "kids %d" % count_son(list_objects, 'world' ) 
	f.write("%s\n" % string_to_write )

	for obj in list_objects_sort:
		if test_son(list_objects, obj, 'world' ):
			recurs_son( f, context, list_objects, obj )

	f.close()
	
	return

