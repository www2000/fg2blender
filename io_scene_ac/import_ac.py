'''
====================================================================================================================


				IMPORT


====================================================================================================================
'''

import os
import bpy
import mathutils
import time
from math import radians
from bpy_extras.io_utils import unpack_list, unpack_face_list




path_name = ""
material_list = []
SMOOTH_ALL = False
EDGE_SPLIT = False
SPLIT_ANGLE = 30.0
CONTEXT = None

DEBUG = False

#----------------------------------------------------------------------------------------------------------------------------------
class MATERIAL:
	def __init__(self):
		self.rgb			= mathutils.Vector( (0.0, 0.0, 0.0) )
		self.amb			= mathutils.Vector( (0.0, 0.0, 0.0) )
		self.emis			= mathutils.Vector( (0.0, 0.0, 0.0) )
		self.spec			= mathutils.Vector( (0.0, 0.0, 0.0) )
		self.shi			= 0
		self.trans			= 0
		self.name_ac		= ""
		self.name_bl		= ""
#----------------------------------------------------------------------------------------------------------------------------------

class MESH:
	def __init__(self):
		self.vertices		= []
		self.edges			= []
		self.faces			= []
		self.uv				= []
		self.tex_name		= ""
		self.tex_name_bl	= ""
		self.img_name_bl	= ""
		self.tex_name_clean	= ""
		self.mesh_name		= ""
		self.mesh_name_bl	= ""
		self.location		= mathutils.Vector( (0.0, 0.0, 0.0) )
		self.loc_group		= []
		self.group			= False
		self.parent			= []
		self.parent_name	= []
		self.mat_no			= -1
		self.crease			= -1.0
		
	def reset(self):
		del self.vertices
		del self.edges
		del self.faces
		del self.uv

		self.vertices		= []
		self.edges			= []
		self.faces			= []
		self.uv				= []
		self.tex_name_bl	= ""
		self.img_name_bl	= ""
		self.tex_name		= ""
		self.tex_name_clean	= ""
		self.mesh_name		= ""
		self.mesh_name_bl	= ""
		self.location		= mathutils.Vector( (0.0, 0.0, 0.0) )
		self.group			= False
		self.mat_no			= -1
		self.crease			= -1.0

		
	def add_vertices(self, vert):
		self.vertices +=  [vert]
		
	def add_edges(self, ed):
		self.edges +=  ed
		
	def add_faces(self, fa):
		self.faces +=  fa
		
	def set_name( self, new_name ):
		self.mesh_name = new_name

	def set_tex_name( self, new_name ):
		self.tex_name = new_name
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
	#print( "extract_path() : %s " % path_name )
#----------------------------------------------------------------------------------------------------------------------------------

def without_path(name_path):
	"""
	name = ""
	for c in reversed(name_path):
		if c != '/':
			name = c + name
		else:
			break
	"""	
	n = name_path.split('/')
	if ( len(n) == 1 ):
		n = name_path.split('\\')
		
	nn = ""
	
	for s in n:
		nn = os.path.join( nn, s )


	name = os.path.normpath(nn)

	return name
#----------------------------------------------------------------------------------------------------------------------------------

def cleaner_name(name_path):
	name = without_path( name_path )
	return name
#----------------------------------------------------------------------------------------------------------------------------------

def tronc_name(name_path):
	name = name_path[:21]
	return name
#----------------------------------------------------------------------------------------------------------------------------------

def debug_info( aff):
	global DEBUG
	if DEBUG:
		print( aff )
#----------------------------------------------------------------------------------------------------------------------------------

def edge_split( context, split_angle ):
	bpy.ops.object.select_all(action='DESELECT')
	list_objects = context.scene.objects
	
	print( "--------------" )
	print( "Edge split all" )
	print( "--------------" )
	for obj in list_objects:
		if obj.type == 'MESH':
			obj_name = obj.name
			print( "Edge-split %s" % obj.name )
			try:
				bpy.ops.object.select_name(name=obj_name)
				bpy.ops.object.shade_smooth()
				try:
					bpy.ops.object.modifier_add( type='EDGE_SPLIT')	
				except:
					print( "Erreur modifier_add Edge-split" )
					
				try:
					for mod in obj.modifiers:
						if mod.type=='EDGE_SPLIT':
							mod.split_angle = radians(split_angle)
				except:
					print( "Erreur Edge-split angle" )
				
			except:
				print( "Erreur Edge-split" )
#----------------------------------------------------------------------------------------------------------------------------------

def smooth_all( context ):
	bpy.ops.object.select_all(action='DESELECT')
	list_objects = context.scene.objects

	print( "----------" )
	print( "Smooth_all" )
	print( "----------" )
	
	for obj in list_objects:
		if obj.type == 'MESH':
			obj_name = obj.name	
			print( "Smooth %s" % obj.name )
			bpy.ops.object.select_name(name=obj_name)
			bpy.ops.object.shade_smooth()
#----------------------------------------------------------------------------------------------------------------------------------

def create_empty( local_mesh):
	
	obj_name = local_mesh.mesh_name
	debug_info( "create empty objet %s" % obj_name )
	obj_new = bpy.data.objects.new(obj_name, None)
	local_mesh.mesh_name_bl = obj_new.name
	v = local_mesh.location
	obj_new.location = (v.x, v.y, v.z )

	if local_mesh.parent_name[-1]!='WORLD':
		obj_new.parent = bpy.data.objects[local_mesh.parent_name[-1]]

	sc = bpy.context.scene
	o = sc.objects.link(obj_new)
#----------------------------------------------------------------------------------------------------------------------------------

def create_uv( local_mesh, mesh ):
	global path_name, material_list
	global SMOOTH_ALL, EDGE_SPLIT, SPLIT_ANGLE

	version = bpy.app.version

	if local_mesh.uv!=[]:
		if version[1] > 62:
			mesh.uv_textures.new()
			uvtex = mesh.uv_layers.active
		#Loading UV tex coords
		#uvtex = mesh.uv_textures.new()#create uvset
		j=0
		if local_mesh.img_name_bl != "":
			try:
				img = bpy.data.images[local_mesh.img_name_bl]
			except:
				img = None
				print( '     Erreur recherche img "%s"'%local_mesh.img_name_bl )
		else:
			img = None

		if version[1] > 62:
			idx = 0
			debug_info( "Nb uv_textures : %d " % len(mesh.uv_textures[-1].data) )
			debug_info( "Nb faces       : %d " % len(local_mesh.faces) )
			debug_info( "Nb points      : %d " % len(local_mesh.vertices) )
			for i in range(len(local_mesh.faces)):
				nb = len(local_mesh.faces[i])
				debug_info( "Face no        : %d " % i )
				debug_info( "Nb points      : %d " % nb )
				debug_info( "Nb uv : %d  nb local_mesh.uv : %d      idx : %d" % (len(uvtex.data), len(local_mesh.uv), idx ) )
				# triangle or  quad or edge
				if nb >= 2:
					j = local_mesh.faces[i][0]
					debug_info( "indice j  : %d" % (j) )
					k = local_mesh.faces[i][1]
					#uvtex.data[idx+0].uv = local_mesh.uv[idx+0]
					#uvtex.data[idx+1].uv = local_mesh.uv[idx+1]
					uvtex.data[idx+0].uv = local_mesh.uv[j]
					uvtex.data[idx+1].uv = local_mesh.uv[k]
				# triangle or  quad
				if nb >= 3:
					l = local_mesh.faces[i][2]
					#uvtex.data[idx+2].uv = local_mesh.uv[idx+2]
					uvtex.data[idx+2].uv = local_mesh.uv[l]
				#quad
				if nb == 4:
					m = local_mesh.faces[i][3]
					#uvtex.data[idx+3].uv = local_mesh.uv[idx+3]
					uvtex.data[idx+3].uv = local_mesh.uv[m]
			
				mesh.uv_textures[-1].data[i].image = img
				idx = idx + nb
#----------------------------------------------------------------------------------------------------------------------------------

def assign_material( local_mesh, obj_new ):
	global path_name, material_list
	global SMOOTH_ALL, EDGE_SPLIT, SPLIT_ANGLE

	if local_mesh.uv!=[]:
		texture = None
		for texture in bpy.data.textures:
			if texture.name == local_mesh.tex_name_bl:
				break
		
		mesh = obj_new.data	

		no = local_mesh.mat_no
		if ( len(material_list) != 0 ):
			ml = material_list[no]
			bl_mat = ml[0]
		
			if ml[2]!="":
				bOK = True
				for ml in material_list:
					if ml[2] == local_mesh.tex_name_bl and ml[1] == no:
						bl_mat = ml[0]
						mesh.materials.append(bl_mat)
						if bl_mat.use_transparency:
							obj_new.show_transparent = True
						#print( "    assign material %s avec la texture %s" % (bl_mat.name, local_mesh.tex_name_bl) )
						bOK = False
						break
			
				if bOK:
					debug_info( "   Pas la meme texture %s %s" % (ml[2],local_mesh.tex_name_bl) )
						
					for ml in material_list:
						if ml[1] == no:
							ac_mat = ml[3]
							# First use of material ??
							if len(bl_mat.texture_slots) != 0:
								bl_mat = bpy.data.materials.new(ac_mat.name_ac)

							debug_info( '    Create material %s with texture "%s"' % (bl_mat.name,local_mesh.tex_name_bl) )
							ac_mat.name_bl			= bl_mat.name
	
							bl_mat.diffuse_color	= ac_mat.rgb
							bl_mat.ambient			= ac_mat.amb.x
							bl_mat.emit				= ac_mat.emis.x
							bl_mat.emit				= 0.2
							bl_mat.specular_color	= ac_mat.spec
							bl_mat.specular_hardness= ac_mat.shi
							bl_mat.alpha			= 1.0-ac_mat.trans
							bl_mat.use_transparency = False
							if bl_mat.alpha != 1.0:
								bl_mat.use_transparency = True
								obj_new.show_transparent = True

							if local_mesh.tex_name != "":
								texture_slot = bl_mat.texture_slots.add()
								texture_slot.texture = texture
								texture_slot.texture_coords='UV'

							material_list.append( (bl_mat, no, local_mesh.tex_name_bl, ac_mat))
							mesh.materials.append(bl_mat)
							break
						
				
			else:
				if local_mesh.tex_name_bl !="":
					texture_slot = bl_mat.texture_slots.add()
					texture_slot.texture = texture
					texture_slot.texture_coords='UV'
					material_list[no] = ( ml[0],ml[1],local_mesh.tex_name_bl, ml[3] )
					debug_info( "    material %s with new texture = %s" % (ml[0].name,local_mesh.tex_name_bl) )
				else:
					debug_info( '    material %s without texture' % (ml[0].name) )
				mesh.materials.append(bl_mat)
#----------------------------------------------------------------------------------------------------------------------------------

def create_mesh( local_mesh ):
	global path_name, material_list
	global SMOOTH_ALL, EDGE_SPLIT, SPLIT_ANGLE, CONTEXT

	obj_name = local_mesh.mesh_name
	context = CONTEXT
	
	mesh = bpy.data.meshes.new(obj_name+".mesh")
	#mesh.from_pydata(local_mesh.vertices, local_mesh.edges, local_mesh.faces)
	#mesh.from_pydata(local_mesh.vertices, [], local_mesh.faces)

	if local_mesh.crease != -1.0:
		mesh.use_auto_smooth = True
		mesh.auto_smooth_angle = radians(local_mesh.crease)


	version = bpy.app.version

	if version[1] == 63:
		mesh.vertices.add(len(local_mesh.vertices))
		mesh.tessfaces.add(len(local_mesh.faces))

		mesh.vertices.foreach_set("co", unpack_list(local_mesh.vertices))
		mesh.tessfaces.foreach_set("vertices_raw", unpack_face_list(local_mesh.faces))
		mesh.tessfaces.foreach_set("use_smooth", [(True)]*len(local_mesh.faces) )
	else:
		print( "Erreur script pour blender 2.63" )

	mesh.update()

	sc = bpy.context.scene
	obj_new = bpy.data.objects.new(obj_name,mesh)
	#v = local_mesh.location
	#obj_new.location = (v.x, v.y, v.z )
	obj_new.location = local_mesh.location
	local_mesh.mesh_name_bl = obj_new.name
	
	o = sc.objects.link(obj_new)
	
	if local_mesh.parent_name[-1]!='WORLD':
		str_print = "create_mesh() %s   parent = %s" % (local_mesh.mesh_name_bl,local_mesh.parent_name[-1])
		obj_new.parent = bpy.data.objects[local_mesh.parent_name[-1]]
	else:
		str_print = "create_mesh() %s" % (local_mesh.mesh_name_bl)

	str_print += ' mat no = %d  texture="%s" image="%s"' % (local_mesh.mat_no, local_mesh.tex_name_bl, local_mesh.img_name_bl)
	debug_info(str_print)

	create_uv( local_mesh, mesh )
	assign_material( local_mesh, obj_new )

	#mesh.update(calc_edges=True)
	mesh.validate()
	mesh.update(calc_edges=True)
#----------------------------------------------------------------------------------------------------------------------------------

def create_texture( local_mesh ):
	global path_name
	
	img_name = cleaner_name(local_mesh.tex_name)
	img_name_clean = tronc_name( os.path.basename(img_name) )

	#print( "create_texture()  img_name : %s" % img_name )
	#print( "create_texture()  img_name_clean : %s" % img_name_clean )
	
	# null ???
	if img_name == "":
		return
		
	name_path = os.path.join( path_name, img_name )
	name_path = os.path.normpath(name_path)
	
	filenamepath = img_name
	
	debug_info( "create_texture()  name_path : %s" % bpy.path.basename(name_path) )
	
	for tex in bpy.data.textures:
		if tex.type=='IMAGE':
			img = tex.image
			if img.filepath == name_path:
				local_mesh.img_name_bl = img.name
				local_mesh.tex_name_bl = tex.name
				return img.name
	
	try:
		img = bpy.data.images.load( name_path )
	except:
		print( '*** erreur **** %s introuvale' % (name_path) )
		img = bpy.data.images.new(name='void', width=1024, height=1024, alpha=True, float_buffer=True)
		return ""
	
	local_mesh.img_name_bl = img.name
	tex = bpy.data.textures.new( img_name_clean, 'IMAGE')
	tex.image = img
	local_mesh.set_tex_name( img_name_clean )
	local_mesh.tex_name_bl = tex.name
	local_mesh.img_name_bl = img.name
	debug_info( '    Creation de la texture "%s" img="%s"'%(local_mesh.tex_name_bl,local_mesh.img_name_bl) )
	return tex.name
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#					-------------------------------------
#						Parse fonctions
#					-------------------------------------
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def read_vertice( f, line, local_mesh ):
	nb = int(line.split()[1])
	#print( line )

	for i in range(nb):
		#pour les lignes vides
		nb = 1
		while nb == 1:
			line = f.readline()
			nb = len(line)
		#print( " ligne no %d : %s" % (i,line) )
		reel = line.split()
		#v = local_mesh.location
		vec3 = mathutils.Vector( (float(reel[0]), -float(reel[2]), float(reel[1]) ) )

		local_mesh.add_vertices( vec3 )
		#print( "No de vertex %d " % i )
#----------------------------------------------------------------------------------------------------------------------------------
	
def read_face( fi, local_mesh):
	line = fi.readline()

	while line.find('refs')==-1:
		if line.find('mat ')!=-1:
			local_mesh.mat_no = int(line.split()[1])
		line = fi.readline()

	nb = int(line.split()[1])

	f = []
	uv = []
	
	if len(local_mesh.vertices) != len(local_mesh.uv):
		local_mesh.uv = [ (0.0,0.0) ] * len(local_mesh.vertices)
	
	
	for i in range(nb):
		#pour les lignes vides
		cnb = 1
		while cnb == 1:
			line = fi.readline()
			cnb = len(line)

		idx = line.split()
		f.append( int(idx[0]) )
		#if nb != 2:
		#	if nb<5:
		#		local_mesh.uv.append( [ float(idx[1]), float(idx[2]) ]  )
		uv.append( [ float(idx[1]), float(idx[2]) ]  )

	# for quads	
	if nb == 4:
		new_face = [ (f[0], f[1], f[2], f[3]) ]
		new_edge = [ (f[0],f[1]) , (f[1],f[2]) , (f[2],f[3]) , (f[3],f[0])  ]
		local_mesh.add_faces( new_face )
		local_mesh.add_edges( new_edge )
		local_mesh.uv[ f[0] ] = uv[0]
		local_mesh.uv[ f[1] ] = uv[1]
		local_mesh.uv[ f[2] ] = uv[2]
		local_mesh.uv[ f[3] ] = uv[3]
		#local_mesh.uv.append( uv[0] )
		#local_mesh.uv.append( uv[1] )
		#local_mesh.uv.append( uv[2] )
		#local_mesh.uv.append( uv[3] )
	# for triangles
	if nb == 3:
		new_face = [ (f[0], f[1], f[2]) ]
		new_edge = [ (f[0],f[1]) , (f[1],f[2]) , (f[2],f[0]) ]
		local_mesh.add_faces( new_face )
		local_mesh.add_edges( new_edge )
		local_mesh.uv[ f[0] ] = uv[0]
		local_mesh.uv[ f[1] ] = uv[1]
		local_mesh.uv[ f[2] ] = uv[2]
		#local_mesh.uv.append( uv[0] )
		#local_mesh.uv.append( uv[1] )
		#local_mesh.uv.append( uv[2] )
	#for edge only
	if nb == 2:
		new_edge = [ (f[0], f[1]) ]
		local_mesh.add_edges( new_edge )
		local_mesh.uv[ f[0] ] = uv[0]
		local_mesh.uv[ f[1] ] = uv[1]
		#local_mesh.uv.append( uv[0] )
		#local_mesh.uv.append( uv[1] )

	#for other more than 4 vetex per faces.  Split in triangles
	if nb > 4:
		#print( "refs = %d" % nb )
		for i in range(nb-2):
			new_face = [ (f[0], f[1+i], f[2+i]) ]
			new_edge = [ (f[0],f[1+i]) , (f[1+i],f[2+i]) , (f[2+i],f[0]) ]
			local_mesh.add_faces( new_face )
			local_mesh.add_edges( new_edge )
		
		for i in range(nb-2):
			local_mesh.uv[ f[0] ] = uv[0]
			local_mesh.uv[ f[i+1] ] = uv[i+1]
			local_mesh.uv[ f[i+2] ] = uv[i+2]
			#local_mesh.uv.append( uv[0] )
			#local_mesh.uv.append( uv[i+1] )
			#local_mesh.uv.append( uv[i+2] )
#----------------------------------------------------------------------------------------------------------------------------------
		
def read_texture( fi, line, local_mesh):
	mot = line.split()
	local_mesh.tex_name = mot[1].split('"')[1]
	local_mesh.tex_name_bl = create_texture(local_mesh)
#----------------------------------------------------------------------------------------------------------------------------------

def read_surface( f, line, local_mesh ):
	mot = line.split()
	nb = int(mot[1])
	for i in range(nb):
		read_face( f, local_mesh )
#----------------------------------------------------------------------------------------------------------------------------------
		
def read_location( f, line, local_mesh ):
	mot = line.split()

	local_mesh.location.x =  float(mot[1])
	local_mesh.location.y = -float(mot[3])
	local_mesh.location.z =  float(mot[2])
#----------------------------------------------------------------------------------------------------------------------------------

def read_kids( f, line, local_mesh ):

	if local_mesh.group:
		create_empty(local_mesh)
	elif local_mesh.mesh_name != 'WORLD':
		print( 'Creation du mesh : %s' % local_mesh.mesh_name )
		create_mesh( local_mesh )
	
	if len(local_mesh.parent) != 0:
		local_mesh.parent[-1] -= 1
		if local_mesh.parent[-1] == 0:
			local_mesh.loc_group.pop()
			local_mesh.parent_name.pop()
			local_mesh.parent.pop()

	mot = line.split()
	nbSon = int(mot[1])


	if nbSon != 0:
		local_mesh.parent.append( nbSon )
		local_mesh.parent_name.append( local_mesh.mesh_name_bl )
		local_mesh.loc_group.append( local_mesh.location )
#----------------------------------------------------------------------------------------------------------------------------------

def read_name( f, line, local_mesh ):
	mot = line.split()

	mesh_name = mot[1].split('"')[1]
	local_mesh.set_name( mesh_name[:21] )
#----------------------------------------------------------------------------------------------------------------------------------

def read_crease( f, line, local_mesh ):
	mot = line.split()
	local_mesh.crease = float(mot[1])
	#print( "crease = %f" % local_mesh.crease )
#----------------------------------------------------------------------------------------------------------------------------------

def read_object( f, line, local_mesh ):
	local_mesh.reset()
	mot = line.split()
	local_mesh.group = False
	if mot[1] == 'group':
		local_mesh.group = True
		
	if mot[1] == 'world':
		local_mesh.mesh_name = 'WORLD'
		local_mesh.mesh_name_bl = 'WORLD'
#----------------------------------------------------------------------------------------------------------------------------------

def read_material( f, line, local_mesh ):
	global path_name, material_list

	m = line.split()
	ac_mat = MATERIAL()		

	ac_mat.rgb				= mathutils.Vector( (float(m[3]),float(m[4]),float(m[5]) ) )
	ac_mat.amb				= mathutils.Vector( (float(m[7]),float(m[8]),float(m[9]) ) )
	ac_mat.emis				= mathutils.Vector( (float(m[11]),float(m[12]),float(m[13]) ) )
	ac_mat.spec				= mathutils.Vector( (float(m[15]),float(m[16]),float(m[17]) ) )
	ac_mat.shi				= int(m[19])
	ac_mat.trans			= float(m[21])
	ac_mat.name_ac			= m[1].split('"')[1]

	bl_mat = bpy.data.materials.new(ac_mat.name_ac)
	ac_mat.name_bl			= bl_mat.name
	
	bl_mat.diffuse_color	= ac_mat.rgb
	bl_mat.ambient			= ac_mat.amb.x
	bl_mat.emit				= ac_mat.emis.x
	bl_mat.emit				= 0.2
	bl_mat.specular_color	= ac_mat.spec
	bl_mat.specular_hardness= ac_mat.shi
	bl_mat.alpha			= 1.0-ac_mat.trans
	bl_mat.use_transparency = False
	if bl_mat.alpha != 1.0:
		bl_mat.use_transparency = True
	
	no = len(material_list)
	material_list.append( (bl_mat, no, "", ac_mat))
#----------------------------------------------------------------------------------------------------------------------------------
	
TOKEN = {	'numvert ' 		: read_vertice,
			'numsurf '		: read_surface,
			'name '			: read_name,
			'loc '			: read_location,
			'texture "'		: read_texture,
			'kids ' 		: read_kids,
			'crease ' 		: read_crease,
			'OBJECT '		: read_object,
			'MATERIAL '		: read_material
		 }
#----------------------------------------------------------------------------------------------------------------------------------

def display_texture():
	for screen in bpy.data.screens:
		for area in screen.areas:
			for space in area.spaces:
				if space.type == 'VIEW_3D':
					space.show_textured_solid = True
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#						==============
#
#						Main function
#
#						==============
#----------------------------------------------------------------------------------------------------------------------------------

def read_ac(filename, smooth_all, edge_split, split_angle, context):
	global path_name, material_list
	global SMOOTH_ALL, EDGE_SPLIT, SPLIT_ANGLE
	global CONTEXT
	
	time_deb = time.time()
	CONTEXT		= context
	SMOOTH_ALL	= smooth_all
	EDGE_SPLIT	= edge_split
	SPLIT_ANGLE	= split_angle
	
	# init global variable
	path_name = ""
	material_list = []
	# extract pathname and open file
	extract_path( filename )
	f = open(filename,'r')
	line = f.readline()
	# init local_mesh for all fonctions (zero in read_object only)
	local_mesh = MESH()
	#--------------------------
	# main  loop
	# 
	# world key => function(f=file, line=line in the file, local_mesh= variable update by read_* function )
	# read_*() function prepare variable for create_mesh() funtion )
	# look TOKEN dict
	#--------------------------
	while line!="":
		#print("Ligne ----- %s" % line )
		for token, fct in TOKEN.items():
			if line.find(token)!=-1:
				fct(f, line, local_mesh)
		line = f.readline()
	
	# close file and byebye
	f.close()
	
	print( "Parent restant %d" % len(local_mesh.parent) )
	display_texture()
	time_end = time.time()
	print( "Import %s in %0.2f sec" % (without_path(filename),(time_end-time_deb) ) )


