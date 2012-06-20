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
# Contributors: René Nègre
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#
#							Pasre .ac file in object ac_manager.MESH
#
#
#----------------------------------------------------------------------------------------------------------------------------------


import os
import bpy
import mathutils
import time
from math import radians
from bpy_extras.io_utils import unpack_list, unpack_face_list
from .ac_manager import MESH
from .ac_manager import MATERIAL
from .ac_manager import material_list
from .ac_manager import path_name

#path_name = ""
#material_list = []
SMOOTH_ALL = False
EDGE_SPLIT = False
SPLIT_ANGLE = 30.0
CONTEXT = None

DEBUG = False
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
	debug_info( "read_face()  nb = %d " % nb )

	f = []
	uv = []
	
	#if nb > len(local_mesh.uv):
	#	local_mesh.uv = [] * nb
	#debug_info( "Longeur uv %d " % len(local_mesh.uv) )
	
	
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
		local_mesh.uv.append( (uv[0],uv[1],uv[2],uv[3]) )
	# for triangles
	if nb == 3:
		new_face = [ (f[0], f[1], f[2]) ]
		new_edge = [ (f[0],f[1]) , (f[1],f[2]) , (f[2],f[0]) ]
		local_mesh.add_faces( new_face )
		local_mesh.add_edges( new_edge )
		local_mesh.uv.append( (uv[0],uv[1],uv[2]) )
	#for edge only    ignore
	'''
	if nb == 2:
		new_face = [ (f[0], f[1]) ]
		new_edge = [ (f[0], f[1]) ]
		local_mesh.add_faces( new_face )
		local_mesh.add_edges( new_edge )
		local_mesh.uv.append( (uv[0],uv[1]) )
	'''
	#for other more than 4 vetex per faces.  Split in triangles
	if nb > 4:
		#print( "refs = %d" % nb )
		for i in range(nb-2):
			new_face = [ (f[0], f[1+i], f[2+i]) ]
			new_edge = [ (f[0],f[1+i]) , (f[1+i],f[2+i]) , (f[2+i],f[0]) ]
			local_mesh.add_faces( new_face )
			local_mesh.add_edges( new_edge )
		
		for i in range(nb-2):
			local_mesh.uv.append( (uv[0],uv[i+1],uv[i+2]) )
	debug_info( "Longeur uv %d " % len(local_mesh.uv) )
#----------------------------------------------------------------------------------------------------------------------------------
		
def read_texture( fi, line, local_mesh):
	mot = line.split()
	local_mesh.tex_name = mot[1].split('"')[1]
	local_mesh.tex_name_bl = local_mesh.create_texture()
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
		local_mesh.create_empty()
	elif local_mesh.mesh_name != 'WORLD':
		print( 'Import du mesh : %s' % local_mesh.mesh_name )
		local_mesh.create_mesh()
	
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
	#global path_name, material_list

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
	#global path_name, material_list
	global SMOOTH_ALL, EDGE_SPLIT, SPLIT_ANGLE
	global CONTEXT

	version = bpy.app.version
	if version[1] < 63:
		print( "Erreur : Scrpit pour blender >= 2.63" )
		return
		
	
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
	local_mesh.filename = filename
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


