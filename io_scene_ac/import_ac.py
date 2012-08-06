


'''
====================================================================================================================


				IMPORT

def read_ac(filename):

'MATERIAL '		: read_material


====================================================================================================================
'''
import os
import bpy
import mathutils
from math import radians
from math import degrees

from bpy_extras.image_utils import load_image

path_name = ""
path_file_name = ""

material_list = []


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



class MESH:
	def __init__(self):
		self.vertices		= []
		self.edges			= []
		self.faces			= []
		self.face_smooth	= []
		self.face_mat		= []
		
		self.mat_slot		= []
		
		self.uv				= []
		self.tex_name		= ""
		self.tex_name_clean	= ""
		self.mesh_name		= ""
		self.location		= mathutils.Vector( (0.0, 0.0, 0.0) )
		
		self.loc_group		= []
		self.group			= False
		self.parent			= []
		self.parent_name	= []
		self.mat			= -1
		self.double_sided 	= False
		
		self.crease_auto		= False
		self.crease_angle 	= 0.0
		
		self.texrepx	= 1.0
		self.texrepy	= 1.0
	
		
	def reset(self):
		self.vertices		= []
		self.edges			= []
		self.faces			= []
		self.face_smooth	= []
		self.face_mat		= []
		
		self.mat_slot		= []

		self.uv				= []
		self.tex_name		= ""
		self.tex_name_clean	= ""
		self.mesh_name		= ""
		self.location		= mathutils.Vector( (0.0, 0.0, 0.0) )
		self.group			= False
		self.mat			= -1
		self.double_sided 	= False
		
		self.crease_auto	= False
		self.crease_angle 	= 0.0
		
		self.texrepx	= 1.0
		self.texrepy	= 1.0
		
	
	def add_vertices(self, vert):
		self.vertices +=  [vert]
		
	def add_edges(self, ed):
		self.edges +=  ed
	
	def add_faces(self, fa):
		self.faces +=  fa
		
	def add_face_smooth(self, fs):
		self.face_smooth +=  fs
	
	
	
	def add_face_mat(self, fm):
		self.face_mat +=  fm
		
	def add_mat_slot(self, ms):
		self.mat_slot +=  ms
		
	
	
	def set_name( self, new_name ):
		self.mesh_name = new_name

	def set_tex_name( self, new_name ):
		self.tex_name = new_name


		
def extract_path(name_path):
	global path_name
	global path_file_name
	
	path_file_name=name_path
	
	name = ""
	rep = name_path.split('/')
	
	for i in range(len(rep)-1):
		name += rep[i] + '/'

	path_name = name
	print(path_name)




def without_path(name_path):
	name = ""
	for c in reversed(name_path):
		if c != '/':
			name = c + name
		else:
			break
	return name


def cleaner_name(name_path):
	name = without_path( name_path )
	name = name[:21]
	return name



def edge_split( context ):
	
	bFound = False
	bpy.ops.object.select_all(action='DESELECT')
	list_objects = context.scene.objects
	for obj in list_objects:
		if obj.type == 'MESH':
			obj_name = obj.name
			bpy.ops.object.select_name(name=obj_name)
			if (obj.data.use_auto_smooth == True):
				split_angle = obj.data.auto_smooth_angle
				if ((degrees(split_angle) > 29.999999) and (degrees(split_angle) < 80.000001 ) ):
					for mod in obj.modifiers:
						if mod.type=='EDGE_SPLIT':
							bFound = True
							break
					
					if bFound == False:
						bpy.ops.object.modifier_add( type='EDGE_SPLIT')   
						for mod in obj.modifiers:
							if mod.type=='EDGE_SPLIT':
								mod.split_angle = split_angle

		

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




def create_empty( local_mesh):
	
	obj_name = local_mesh.mesh_name
	print( "creation objet empty %s" % obj_name )
	obj_new = bpy.data.objects.new(obj_name, None)
	v = local_mesh.location
	obj_new.location = (v.x, v.y, v.z )
	sc = bpy.context.scene
	o = sc.objects.link(obj_new)



def create_mesh( local_mesh ):
	obj_name = local_mesh.mesh_name
	
	newmesh = bpy.data.meshes.new(obj_name+".mesh")
	newmesh.from_pydata(local_mesh.vertices, local_mesh.edges, local_mesh.faces)

	newmesh.calc_normals()
	
	newmesh.show_double_sided = local_mesh.double_sided
	
	newmesh.use_auto_smooth = False
	if local_mesh.crease_auto == True:
		newmesh.use_auto_smooth = True
		newmesh.auto_smooth_angle = local_mesh.crease_angle 	
		
	
	y=0	
	for facesm in newmesh.polygons:
		if local_mesh.face_smooth[y]>0:
			facesm.use_smooth = True
		else:
			facesm.use_smooth = False
		y= y+1
	
		
	obj_show_transparent = False

	newmesh.update()

	'''
	=========================
	uv mapping
	=========================
	'''
	sc = bpy.context.scene
	obj_new = bpy.data.objects.new(obj_name,newmesh)
	v = local_mesh.location
	obj_new.location = (v.x, v.y, v.z )
	
	o = sc.objects.link(obj_new)
	
	str_print = ""
	
	if local_mesh.parent_name[-1]!='WORLD':
		str_print += "create_mesh() %s   parent = %s" % (local_mesh.mesh_name,local_mesh.parent_name[-1])
		obj_new.parent = bpy.data.objects[local_mesh.parent_name[-1]]
	else:
		str_print += "create_mesh() %s" % (local_mesh.mesh_name)

	str_print += ' mat no = %d  texture ="%s"' % (local_mesh.mat, local_mesh.tex_name)
	print(str_print)


	
	if local_mesh.uv!=[]:
		#Loading UV tex coords
		uvtex1 = newmesh.uv_textures.new()#create uvset
		if uvtex1:
				
			uvtex = newmesh.uv_layers.active.data[:]
			j=0
			for i in range(len(local_mesh.faces)):
				nb = len(local_mesh.faces[i])

				if nb > 2:
					for z in range(nb):
						uvtex[j+z].uv = local_mesh.uv[j+z]
				
				j += nb
				
				found = False
				
				if local_mesh.tex_name != "":
				
					imgname = local_mesh.tex_name
					imgpath = os.path.dirname(path_file_name)  +"/" +imgname
					img = bpy.data.images.load( imgpath )
					
					uvtex1.data[i].image = img
				
					found = True

	
	newmesh.validate()
	newmesh.update()
	
	'''
	=========================
	 assign material
	=========================
	'''

	#start - face mat	
	#put materials in material slots
	for mtsl in local_mesh.mat_slot:
		no = mtsl
		ml = material_list[no]
		bl_mat = ml[0]
		newmesh.materials.append(bl_mat)

		if bl_mat.alpha < 1.0:
			obj_show_transparent = True
		
	
	#material_index  (in material slots)
    #Type :	int in [0, 32767], default 0
	#assign face material index
	y=0	
	for facemi in newmesh.polygons:
		facemi.material_index = local_mesh.face_mat[y]
		y= y+1
		
	#end - face mat	
	
	# Update mesh with new data
	newmesh.update(calc_edges=True)
	
	newmesh.validate()
	newmesh.update()
	
	#last because mesh must update first
	obj_new.show_transparent = obj_show_transparent


def create_texture( local_mesh ):
	pass

def create_material( local_mesh ):
	pass
	

def read_vertice( f, line, local_mesh ):
	#global vertices

	vertices = []
	nb = int(line.split()[1])

	for i in range(nb):
		line = f.readline()
		reel = line.split()
		v = local_mesh.location
		vec3 = mathutils.Vector( (float(reel[0]), -float(reel[2]), float(reel[1]) ) )
		
		local_mesh.add_vertices( vec3 )
	
	
	
def read_face( fi, local_mesh):
	#global faces, edges
	face_smooth =0
	
	line = fi.readline()

	while line.find('refs')==-1:
		if line.find('mat ')!=-1:
			local_mesh.mat = int(line.split()[1])
		
		#---------
		elif line.find('SURF ')!=-1:
			
			flags = line.split()[1][2:]
			if len(flags) > 1:
				flaghigh = int(flags[0])
				flaglow = int(flags[1])
			else:
				flaghigh = 0
				flaglow = int(flags[0])

			
			if flaghigh == 3:
				face_smooth = 1
				local_mesh.double_sided  =True
			elif flaghigh == 2:
				local_mesh.double_sided  = True
			elif flaghigh == 1:
				face_smooth =1
				
			
		#----------
		line = fi.readline()

	#refs	
	nb = int(line.split()[1])
		
	f = []
	fng = []
	for i in range(nb):
		line = fi.readline()
		idx = line.split()
		f.append( int(idx[0]) )
		if nb != 2:
			local_mesh.uv.append( [ float(idx[1]), float(idx[2]) ]  )
		
		
	#start - face mat ----------
	
	face_mat=0
	mtcnt=0
	mtsl=0
	mat_found=False
	for mtsl in local_mesh.mat_slot:
		if mtsl==local_mesh.mat:
			mat_found=True
			break
		mtcnt=mtcnt+1	
	
	if (mat_found==False):
		new_mat_slot = [ local_mesh.mat ]
		local_mesh.add_mat_slot( new_mat_slot )
		
	face_mat=mtcnt
	new_face_mat = [ face_mat ]
	local_mesh.add_face_mat( new_face_mat )
	
	#end - face mat	------------
		

	new_face =[]
	new_f =[]
	new_edge =[]
		
	if nb == 2:
		new_edgefc = [ (f[0], f[1]) ]
		local_mesh.add_edges( new_edgefc )
	
	elif nb > 2:	
		
		for i in range(nb):
				new_f.append( f[i] ) 
		new_face.append( new_f)
		local_mesh.add_faces( new_face )
			
		for i in range(nb-1):
			new_edge.append( (f[i],f[i+1]) )
		new_edge.append( (f[nb-1], f[0]) )
		local_mesh.add_edges( new_edge )
		
		new_face_smooth = [ face_smooth ]
		local_mesh.add_face_smooth( new_face_smooth )
		
		
		
def read_texture( fi, line, local_mesh):
	#global faces, edges
	mot = line.split()
	local_mesh.tex_name = mot[1].split('"')[1]
	create_texture(local_mesh)
	create_material( local_mesh )
		

def read_texrep( fi, line, local_mesh):

	mot = line.split()
	local_mesh.texrepx = float(line.split()[1])
	local_mesh.texrepy = float(line.split()[2])

	'''
	NOT IMPLEMMENTED
	
	try:
		mesh.materials[0].texture_slots[0].texture.repeat_x = self.texrepx 
		mesh.materials[0].texture_slots[0].texture.repeat_y = self.texrepy 
	except:
		tex_name = ""
	'''	
		

def read_surface( f, line, local_mesh ):
	mot = line.split()
	nb = int(mot[1])
	for i in range(nb):
		#print( str(i) )
		read_face( f, local_mesh )
	
		
def read_location( f, line, local_mesh ):
	mot = line.split()

	local_mesh.location.x =  float(mot[1])
	local_mesh.location.y = -float(mot[3])
	local_mesh.location.z =  float(mot[2])
	

def read_kids( f, line, local_mesh ):

	if local_mesh.group:
		create_empty(local_mesh)
	elif local_mesh.mesh_name != 'WORLD':
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
		local_mesh.parent_name.append( local_mesh.mesh_name )
		local_mesh.loc_group.append( local_mesh.location )

		

def read_name( f, line, local_mesh ):
	#local_mesh.reset()
	mot = line.split()

	mesh_name = mot[1].split('"')[1]
	local_mesh.set_name( mesh_name[:21] )



def read_object( f, line, local_mesh ):
	
	local_mesh.reset()
	mot = line.split()
	local_mesh.group = False
	if mot[1] == 'group':
		local_mesh.group = True
		
	if mot[1] == 'world':
		local_mesh.mesh_name = 'WORLD'
		
def read_material( f, line, local_mesh ):
	m = line.split()
	ac_mat = MATERIAL()		

	ac_mat.rgb				= mathutils.Vector( (float(m[3]),float(m[4]),float(m[5]) ) )
	ac_mat.amb				= mathutils.Vector( (float(m[7]),float(m[8]),float(m[9]) ) )
	ac_mat.emis				= mathutils.Vector( (float(m[11]),float(m[12]),float(m[13]) ) )
	ac_mat.spec				= mathutils.Vector( (float(m[15]),float(m[16]),float(m[17]) ) )
	ac_mat.shi				= int(m[19])
	#ac_mat.shi				= float(m[19])
	
	ac_mat.trans			= float(m[21])
	ac_mat.name_ac			= m[1].split('"')[1]

	bl_mat = bpy.data.materials.new(ac_mat.name_ac)
	ac_mat.name_bl			= bl_mat.name
	
	bl_mat.diffuse_color	= ac_mat.rgb
	bl_mat.ambient			= ac_mat.amb.x
	bl_mat.emit				= ac_mat.emis.x
	bl_mat.specular_color	= ac_mat.spec
	
	#bl_mat.specular_hardness= ac_mat.shi
	bl_mat.specular_intensity= float (  ac_mat.shi ) /128
	#bl_mat.specular_intensity=  (  ac_mat.shi ) /128
		
	bl_mat.alpha			= 1.0-ac_mat.trans
	bl_mat.use_transparency = False
	if bl_mat.alpha != 1.0:
		bl_mat.use_transparency = True
		bl_mat.transparency_method = 'Z_TRANSPARENCY'
	    
	
	no = len(material_list)
	material_list.append( (bl_mat, no, "", ac_mat))
	
	#bpy.data.materials.append(bl_mat)
	
	


def read_crease( f, line, local_mesh ):
	
	mot = line.split()
	read_crease_angle =  float(mot[1])
	
	if ((read_crease_angle > 29.999999) and (read_crease_angle < 80.000001 ) ):
		local_mesh.crease_auto	= True
		
		#pi = 3.141592653589793238462643383279502884197
		
		#deg=(rad/pi)*180.0 -> rad =(deg*pi)/180
		#local_mesh.crease_angle 	=  (read_crease_angle*pi)/180
		
		local_mesh.crease_angle 	=  radians(read_crease_angle)
				
			
	
TOKEN = 	{	
			'numvert ' 		: read_vertice,
			'numsurf '		: read_surface,
			'name '			: read_name,
			'loc '			: read_location,
			'crease'			: read_crease,
			'texture "'		: read_texture,
			'texrep'			: read_texrep,
			'kids ' 			: read_kids,
			'OBJECT '			: read_object,
			'MATERIAL '		: read_material
			
		}

#			'OBJECT group'	: read_name,




def display_texture():
	for screen in bpy.data.screens:
		for area in screen.areas:
			for space in area.spaces:
				if space.type == 'VIEW_3D':
					space.show_textured_solid = True



#def read_ac( context, filename, select_only, tex_path, apply_modifiers ):
#import_ac.read_ac( self.filepath , context, self.edge_split)
def read_ac(filename, context, bEdgeSplit):  
	extract_path( filename )
	f = open(filename,'r')
	line = f.readline()
	
	local_mesh = MESH()
	
	while line!="":
		for token, fct in TOKEN.items():
			if line.find(token)!=-1:
				fct(f, line, local_mesh)
		line = f.readline()
	
	f.close()
	
	#TODO: apply this only to created meshes
	if bEdgeSplit == True:
		edge_split( context )
	
	scene = context.scene
	scene.update()
	 
	print( "Parent restant %d" % len(local_mesh.parent) )
	#display_texture()

