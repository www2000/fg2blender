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
#									AC_MANAGER.PY
#
#----------------------------------------------------------------------------------------------------------------------------------


import os
import bpy
import mathutils
import time

from math import radians
from math import degrees

from bpy_extras.io_utils import unpack_list, unpack_face_list

from mathutils import Vector
from mathutils import Euler

material_list = []

current_ac_file = None
xml_extra_position = None
xml_extra_rotation = None


CONTEXT = None

DEBUG = True
#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS AC_OPTION
#----------------------------------------------------------------------------------------------------------------------------------
#	Parser option
#----------------------------------------------------------------------------------------------------------------------------------

class AC_OPTION:
	def __init__(self):
		self.active_layer	= True
		self.layer_beg		= 1
		self.layer_end		= 20

#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS AC_FILE
#----------------------------------------------------------------------------------------------------------------------------------
#	name			= "fuse.ac"						String  file name
#	meshs			= [ "fuse",  "cockpit" , ...]	list of String       Mesh name
#	dic_name_meshs	= {}							Dictionnary : to convert ac name in blender name	
#
#	Use by xml parser for create 'clone'
#			see  clone_ac()
#----------------------------------------------------------------------------------------------------------------------------------

class AC_FILE:
	def __init__(self):
		self.name				= ""
		self.meshs				= []
		self.dic_name_meshs		= {}	
	#----------------------------------------------------------------------------------------------------------------------------------

	def create_group_ac( self ):
		group_name = os.path.basename( self.name )
		
		for obj in bpy.data.objects:
			obj.select = False
		if not group_name in bpy.data.groups:
			bpy.data.groups.new( group_name )
			print( 'Create group : "%s"' % group_name )
		for mesh_name in self.meshs:
			obj = bpy.data.objects[mesh_name]
			obj.select = True
			bpy.context.scene.objects.active = obj
			bpy.ops.object.group_link( group = group_name)
			obj.select = False
			bpy.context.scene.objects.active = None
#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS MATERIAL
#----------------------------------------------------------------------------------------------------------------------------------
#	AC3D material
#	info material inside the ac file
#----------------------------------------------------------------------------------------------------------------------------------
# Note...
#---------
#	material_list = [ (,,,,) , (,,,,) , ..... ]       list of tuple
#
#	tuple	[0]	material_bl			: blender material
#			[1]	material_no			: number inside ac file
#			[2]	material_tex		: texture name   (blender name)
#			[3]	material_ac_mat		: MATERIAL object
#			[4]	material_use		: boolean    False if not assign to a mesh
#
# Use by script to assign material to a mesh
# in ac format a material can have multiple textures
# example :
# object poly "cube"    -> material 0 -> texture "picture0.png"
# object poly "sphere"  -> material 0 -> texture "an_other.png"
# This is impossible in blender
#
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
#							CLASS MESH
#----------------------------------------------------------------------------------------------------------------------------------
#  vertices = [  (0.0,0.0,0.0) , (1.0,1.0,1.0) , ... ]									coord (x,y,z)
#  edges    = [  (0,1) , (1,2) , (5,4) ,  ... ]											don't use   (point indice)
#  faces    = [  (1,2,3) , (2,3,4,5) , ... ]											point indice  
#  uv		= [	 ((0,0),(0,0),(0,0))  , ((0,0),(0,0),(0,0),(0,0)) ,  .... ]				coord uv  !?! len(faces) = len(uv)
#
# Member fonctions:
# -----------------
# create_empty()				:	create a empty object for ac group
# create_uv()					:	create uv mapping  call by create_mesh()
# assign_material()				:	assign material to a object. call by create_mesh()
# create_mesh()					:	create a blender object. call by parser when find 'kids' keyword
# create_texture()				:	create a blender texture. call by parser when find 'texture' keyword
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
		self.filename		= ""
		self.bDDS			= False
		self.texrep			= (1.0,1.0)
		self.texoff			= (0.0,0.0)

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
		self.bDDS			= False
		self.texrep			= (1.0,1.0)
		self.texoff			= (0.0,0.0)
		#self.filename		= ""

		
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

	def create_empty( self ):
	
		obj_name = self.mesh_name
		debug_info( "create empty objet %s" % obj_name )
		obj_new = bpy.data.objects.new(obj_name, None)
		self.mesh_name_bl = obj_new.name
		v = self.location
		obj_new.location = (v.x, v.y, v.z )

		if self.parent_name[-1]!='WORLD':
			obj_new.parent = bpy.data.objects[self.parent_name[-1]]

		current_ac_file.meshs.append( obj_new.name )
		current_ac_file.dic_name_meshs[obj_name] = obj_new.name

		sc = bpy.context.scene
		o = sc.objects.link(obj_new)
		#o = sc.objects.link(obj_new)
	#----------------------------------------------------------------------------------------------------------------------------------

	def create_uv( self, mesh ):
		global material_list

		if self.uv!=[]:
			mesh.uv_textures.new()
			uvtex = mesh.uv_layers.active
			j=0
			if self.img_name_bl != "":
				try:
					img = bpy.data.images[self.img_name_bl]
				except:
					img = None
					print( '     Erreur recherche img "%s"'%self.img_name_bl )
			else:
				img = None

			idx = 0
			debug_info( "Nb uv_textures : %d " % len(mesh.uv_textures[-1].data) )
			debug_info( "Nb faces       : %d " % len(self.faces) )
			debug_info( "Nb points      : %d " % len(self.vertices) )
			debug_info( "Nb uvtext		: %d " % len(uvtex.data) )
		
			#optimisation foreach_set don't work
			#uvtex.data.add(len(self.uv))
			#uvtex.data.foreach_set( "uv", unpack_face_list(self.uv) )
			#for i in range(len(self.faces)):
			#	print( str(self.uv[i]) )
			#	for j in range(len(self.uv[i])):
			#		debug_info( "uv[%d]  %0.4f,%0.4f" % (i,self.uv[i][j][0],self.uv[i][j][1]) )
				
			for i in range(len(self.faces)):
				nb = len(self.faces[i])
				debug_info( "Face no        : %d " % i )
				debug_info( "Nb points      : %d " % nb )
				debug_info( "Nb uv : %d  nb self.uv : %d      idx : %d" % (len(uvtex.data), len(self.uv[i]), idx ) )
				debug_info( "uvtext = %s" % str( uvtex.data )    )
				#for uvloop in uvtex.data:
				#	print( str(uvloop.uv) )
				# triangle or  quad or edge
				if nb >= 2:
					j = self.faces[i][0]
					#debug_info( "indice j  : %d" % (j) )
					k = self.faces[i][1]
					#uvtex.data[idx+0].uv = self.uv[j]
					#uvtex.data[idx+1].uv = self.uv[k]
					uvtex.data[idx+0].uv = self.uv[i][0]
					uvtex.data[idx+1].uv = self.uv[i][1]
				# triangle or  quad
				if nb >= 3:
					l = self.faces[i][2]
					#uvtex.data[idx+2].uv = self.uv[l]
					uvtex.data[idx+2].uv = self.uv[i][2]
				#quad
				if nb == 4:
					m = self.faces[i][3]
					#uvtex.data[idx+3].uv = self.uv[m]
					uvtex.data[idx+3].uv = self.uv[i][3]
		
				mesh.uv_textures[-1].data[i].image = img
				idx = idx + nb
	#----------------------------------------------------------------------------------------------------------------------------------

	def assign_material( self, obj_new ):
		global material_list

		if self.uv!=[]:
			texture = None
			for texture in bpy.data.textures:
				if texture.name == tronc_name(self.tex_name_bl):
					break
			mesh = obj_new.data	

			no = self.mat_no
			#debug_info( obj_new.name )
			#debug_info( self.tex_name_bl )
			#debug_info( "%d %s %s" % (no, material_list[no][0].name, material_list[no][2]) )
			if texture:
				debug_info( 'Texture trouve : "%s"' % (texture.name) )

			debug_info( 'recherche material no %d text "%s"'% ( no, self.tex_name_bl) )
			idx =0
			for material_bl, material_no, material_tex, material_ac_mat, material_use in material_list:
				debug_info( '\t%d-%s %d "%s" %s' % ( idx, material_bl.name, material_no, material_tex, str(material_use)) )
				idx += 1



			if find_material_not_use( self.mat_no, tronc_name(self.tex_name_bl) ) != -1:
				ml = material_list[no]
				bl_mat = ml[0]
				ac_mat = ml[3]
				mesh.materials.append(bl_mat)
				if self.tex_name_bl !="":
					bl_mat.use_transparency = True
					bl_mat.alpha			= 0.0
					texture_slot = bl_mat.texture_slots.add()
					texture_slot.texture = texture
					texture_slot.texture_coords='UV'
					#ac_mat = ml[3]
					texture_slot.use_map_alpha = True

				if ac_mat.trans != 0.0:
					obj_new.show_transparent = True
				else:
					obj_new.show_transparent = False
					
				material_list[no] = ( ml[0],ml[1],self.tex_name_bl, ml[3], True )
				#material_list[self.mat_no][4] = True
				debug_info( "Assign not use de material   %d %s %s" % (no, ml[0].name, ml[2]) )

			elif find_material_use( self.mat_no, tronc_name(self.tex_name_bl) ) != -1:
				no = get_number_material_use( self.mat_no, tronc_name(self.tex_name_bl) )
				ml = material_list[no]
				bl_mat = ml[0]
				ac_mat = ml[3]
				mesh.materials.append(bl_mat)
					
				debug_info( "Assignation de material    %d %s %s" % (no, ml[0].name, ml[2]) )

				if ac_mat.trans != 0.0:
					obj_new.show_transparent = True
				else:
					obj_new.show_transparent = False

			elif find_material_use_with_diff( self.mat_no, tronc_name(self.tex_name_bl) ) != -1:
				ml = material_list[no]
				ac_mat = ml[3]
				bl_mat = bpy.data.materials.new(ac_mat.name_ac)

				#debug_info( '    Create material %s with texture "%s"' % (bl_mat.name,self.tex_name_bl) )
				ac_mat.name_bl			= bl_mat.name

				bl_mat.diffuse_color	= ac_mat.rgb
				bl_mat.ambient			= ac_mat.amb.x
				bl_mat.emit				= ac_mat.emis.x
				bl_mat.emit				= 0.2
				bl_mat.specular_color	= ac_mat.spec
				bl_mat.specular_hardness= ac_mat.shi
				#bl_mat.use_transparency = True
				#bl_mat.alpha			= 0.0
				if ac_mat.trans != 0.0:
					bl_mat.use_transparency = True
					bl_mat.alpha			= 1.0-ac_mat.trans
					obj_new.show_transparent = True
				else:
					obj_new.show_transparent = False

				if self.tex_name != "":
					bl_mat.use_transparency = True
					bl_mat.alpha			= 0.0
					texture_slot = bl_mat.texture_slots.add()
					texture_slot.texture = texture
					texture_slot.texture_coords='UV'
					#if ac_mat.trans == 0.0:
					texture_slot.use_map_alpha = True
					
				nb = len( material_list )
				material_list.append( ( bl_mat ,ml[1],self.tex_name_bl, ml[3], True )  )
				mesh.materials.append(bl_mat)
				
				debug_info( "Creation de material   %d-%s %d %s" % (nb, ml[0].name, ml[1], ml[2]) )
			else:
				print( "*****Cas non résolu******" );

	#----------------------------------------------------------------------------------------------------------------------------------

	def edge_split( self, obj  ):
		debug_info( "Edge split all % 0.2f" % self.crease )
		modifier = obj.modifiers.new( "", 'EDGE_SPLIT' )
		if self.crease != -1.0:
			modifier.split_angle = radians( self.crease )
	#----------------------------------------------------------------------------------------------------------------------------------

	def create_mesh( self ):
		global material_list
		global current_ac_file
		global xml_extra_position
		global xml_extra_rotation
		
		if not self.parent_name:
			return
		
		debug_info( "ac_manager::MESH.create_mesh() %s" % self.mesh_name )
		obj_name = self.mesh_name
		context = CONTEXT
	
		mesh = bpy.data.meshes.new(obj_name+".mesh")

		if self.crease != -1.0:
			mesh.use_auto_smooth = True
			mesh.auto_smooth_angle = radians(self.crease)


		mesh.vertices.add(len(self.vertices))
		mesh.tessfaces.add(len(self.faces))

		mesh.vertices.foreach_set("co", unpack_list(self.vertices))
		mesh.tessfaces.foreach_set("vertices_raw", unpack_face_list(self.faces))
		mesh.tessfaces.foreach_set("use_smooth", [(True)]*len(self.faces) )

		mesh.update()

		sc = bpy.context.scene
		obj_new = bpy.data.objects.new(obj_name,mesh)
		current_ac_file.meshs.append( obj_new.name )
		current_ac_file.dic_name_meshs[obj_name] = obj_new.name

		obj_new.data.fg.name_ac = obj_name
		obj_new.location = self.location
		
		compute_extra_transforme( obj_new, xml_extra_position, xml_extra_rotation )
			
		self.mesh_name_bl = obj_new.name
	
		o = sc.objects.link(obj_new)
	
		if self.parent_name[-1]!='WORLD':
			str_print = "create_mesh() %s   parent = %s" % (self.mesh_name_bl,self.parent_name[-1])
			obj_new.parent = bpy.data.objects[self.parent_name[-1]]
		else:
			str_print = "create_mesh() %s" % (self.mesh_name_bl)

		str_print += ' mat no = %d  texture="%s" image="%s"' % (self.mat_no, self.tex_name_bl, self.img_name_bl)
		debug_info(str_print)

		self.create_uv( mesh )
		self.assign_material( obj_new )

		#mesh.update(calc_edges=True)
		mesh.validate()
		mesh.update(calc_edges=True)

		obj_new.data.fg.ac_file = "" + self.filename
		self.edge_split( obj_new )
	#----------------------------------------------------------------------------------------------------------------------------------

	def create_texture( self ):
	
		img_name = os.path.basename(self.tex_name)
		#21 name 21 char max
		img_name_clean = tronc_name( img_name )

		# null ???
		if img_name == "":
			return
		
		name_path = os.path.dirname(self.filename)
		name_path = os.path.normpath(name_path + os.sep + self.tex_name)
	
		filenamepath = img_name
	
		debug_info( "create_texture()  name_path : %s" % (name_path) )
	
		for tex in bpy.data.textures:
			if tex.type=='IMAGE':
				img = tex.image
				if img.filepath == name_path:
					self.img_name_bl = img.name
					self.tex_name_bl = tex.name
					return img.name
	
		try:
			img = bpy.data.images.load( name_path )
		except:
			print( '*** erreur **** %s introuvale' % (name_path) )
			img = bpy.data.images.new(name='void', width=1024, height=1024, alpha=True, float_buffer=True)
			return ""
	
		self.img_name_bl = img.name
		tex = bpy.data.textures.new( img_name_clean, 'IMAGE')
		tex.image = img
		tex.use_alpha = True
		self.set_tex_name( img_name_clean )
		self.tex_name_bl = tex.name
		self.img_name_bl = img.name
		debug_info( '    Creation de la texture "%s" img="%s"'%(self.tex_name_bl,self.img_name_bl) )
		return tex.name
#----------------------------------------------------------------------------------------------------------------------------------
#
#					END  MESH CLASS
#
#----------------------------------------------------------------------------------------------------------------------------------

def find_material_use_with_diff( mat_no, tex_name ):
	for material_bl, material_no, material_tex, material_ac_mat, material_use in material_list:
		if material_use:
			if material_no==mat_no and material_tex!=tex_name:
				return material_no
	return -1
#----------------------------------------------------------------------------------------------------------------------------------

def find_material_use( mat_no, tex_name ):
	for material_bl, material_no, material_tex, material_ac_mat, material_use in material_list:
		if material_use:
			if material_no==mat_no and material_tex==tex_name:
				return material_no
	return -1
#----------------------------------------------------------------------------------------------------------------------------------

def get_number_material_use( mat_no, tex_name ):
	i = 0
	for material_bl, material_no, material_tex, material_ac_mat, material_use in material_list:
		if material_use:
			if material_no==mat_no and material_tex==tex_name:
				return i
		i += 1
	return i
#----------------------------------------------------------------------------------------------------------------------------------

def find_material_not_use( mat_no, tex_name ):
	for material_bl, material_no, material_tex, material_ac_mat, material_use in material_list:
		#print( 'recherche material no %d text "%s"   dans %s %d "%s" %s' % ( mat_no, tex_name, material_bl.name, material_no, material_tex, str(material_use)) )
		if not material_use:
			if material_no==mat_no:
				return material_no
	return -1
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

def get_ac_file():
	global current_ac_file
	return current_ac_file
#----------------------------------------------------------------------------------------------------------------------------------

def set_ac_file( new_ac_file ):
	global current_ac_file
	current_ac_file = new_ac_file
#----------------------------------------------------------------------------------------------------------------------------------

def compute_extra_transforme( obj, translate, rotate ):
	if translate:
		obj.delta_location = Vector( (0.0,0.0,0.0) ) + translate

	if rotate:
		e = rotate
		eleur  = Euler( (e.x, e.y, e.z) )

		mat4 = eleur.to_matrix().to_4x4()
		w = Vector( (0.0,0.0,0.0) ) + obj.location
		pos = mat4 * w
		tr = Vector( (0.0,0.0,0.0) ) + pos - w
		w = Vector( (0.0,0.0,0.0) ) + obj.delta_location

		obj.delta_location			= Vector( (0.0,0.0,0.0) ) + w  + tr
		obj.delta_rotation_euler	= Euler( (rotate.x, rotate.y, rotate.z) )
#----------------------------------------------------------------------------------------------------------------------------------

def find_key( name, dic ):
	for key, value in dic.items():
		if value == name:
			return key
	return ""
#----------------------------------------------------------------------------------------------------------------------------------

def clone_ac( ac_file, xml_extra_position ):
	time_deb = time.time()
	print( "\tac_manager:clone_ac() %s" % ac_file.name.partition( 'Aircraft'+os.sep )[2] )

	new_ac_file = AC_FILE()
	new_ac_file.name = ac_file.name
	set_ac_file( new_ac_file )

	sc = bpy.context.scene

	for obj_name in ac_file.meshs:
		obj = bpy.data.objects[obj_name]
		location = obj.location
		#print( "CLONE object %s" % obj_name )
		if obj.type == 'EMPTY':
			obj_new = bpy.data.objects.new(obj_name, None)
		else:
			mesh = obj.data
			obj_new = bpy.data.objects.new(obj_name,mesh)

		obj_new.location = Vector( (0.0,0.0,0.0) )	+ obj.location		#self.location
		if xml_extra_position:
			offset = Vector( (0.0,0.0,0.0) ) + xml_extra_position.offset
			euler  = Vector( (0.0,0.0,0.0) ) + xml_extra_position.eulerXYZ
			obj_new.delta_location = offset
			obj_new.delta_rotation_euler = Euler( (euler.x, euler.y, euler.z) )
			compute_extra_transforme( obj_new, offset, euler )
			debug_info( "\tExtra offset  %0.2f, %0.2f, %0.2f" % ( offset.x, offset.y, offset.z ) )
			debug_info( "\tExtra rotate  %0.2f, %0.2f, %0.2f" % ( euler.x, euler.y, euler.z ) )
	
		o = sc.objects.link(obj_new)

		if obj_new.type != 'EMPTY':
			mesh.validate()
			mesh.update(calc_edges=True)

			obj_new.data.fg.ac_file = "" + ac_file.name
			
		obj_name_ac = find_key( obj_name, ac_file.dic_name_meshs )
		current_ac_file.meshs.append( obj_new.name )
		current_ac_file.dic_name_meshs[obj_name_ac] = obj_new.name
		if obj_new.type == 'MESH':
			obj_new.data.fg.name_ac = obj_name_ac

	time_end = time.time()
	print( "\tClone %s in %0.2f sec" % (os.path.basename(ac_file.name),(time_end-time_deb) ) )
	return




