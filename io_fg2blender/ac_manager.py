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
#							IMPORT
#
#
#----------------------------------------------------------------------------------------------------------------------------------


import os
import bpy
import mathutils
import time
from math import radians
from bpy_extras.io_utils import unpack_list, unpack_face_list


material_list = []

current_ac_file = None
xml_extra_position = None


SMOOTH_ALL = False
EDGE_SPLIT = False
SPLIT_ANGLE = 30.0
CONTEXT = None

DEBUG = True
#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS AC_OPTION
#----------------------------------------------------------------------------------------------------------------------------------
#	Option for ac mesh
#----------------------------------------------------------------------------------------------------------------------------------

class AC_OPTION:
	def __init__(self):
		self.smooth_all		= True
		self.edge_split		= True
		self.split_angle	= 60.0

#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS AC_OPTION
#----------------------------------------------------------------------------------------------------------------------------------
#	name		= "fuse.ac"						String  file name
#	meshs		= [ "fuse",  "cockpit" , ...]	list of String       Mesh name
#----------------------------------------------------------------------------------------------------------------------------------

class AC_FILE:
	def __init__(self):
		self.name			= ""
		self.meshs			= []
	#----------------------------------------------------------------------------------------------------------------------------------

	def create_group_ac( self ):
		return
		for obj in bpy.data.objects:
			obj.select = False
		group_name = os.path.basename( self.name )
		bpy.data.groups.new( group_name )
		for mesh_name in self.meshs:
			obj = bpy.data.objects[mesh_name]
			obj.select = True
			bpy.context.scene.objects.active = obj
			bpy.ops.object.group_link( group = group_name)
			obj.select = False
#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS MATERIAL
#----------------------------------------------------------------------------------------------------------------------------------
#	AC3D material
# material_list = [ MATERIAL() , MATERIAL() ,  ... ]
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

		sc = bpy.context.scene
		o = sc.objects.link(obj_new)
	#----------------------------------------------------------------------------------------------------------------------------------

	def create_uv( self, mesh ):
		global material_list
		global SMOOTH_ALL, EDGE_SPLIT, SPLIT_ANGLE

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
		
			#optimisation foreach_set don't work
			#uvtex.data.add(len(self.uv))
			#uvtex.data.foreach_set( "uv", unpack_face_list(self.uv) )
			for i in range(len(self.faces)):
				nb = len(self.faces[i])
				#debug_info( "Face no        : %d " % i )
				#debug_info( "Nb points      : %d " % nb )
				#debug_info( "Nb uv : %d  nb self.uv : %d      idx : %d" % (len(uvtex.data), len(self.uv), idx ) )
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
		global SMOOTH_ALL, EDGE_SPLIT, SPLIT_ANGLE

		if self.uv!=[]:
			texture = None
			for texture in bpy.data.textures:
				if texture.name == self.tex_name_bl:
					break
		
			mesh = obj_new.data	

			no = self.mat_no
			if ( len(material_list) != 0 ):
				ml = material_list[no]
				bl_mat = ml[0]
		
				if ml[2]!="":
					bOK = True
					for ml in material_list:
						if ml[2] == self.tex_name_bl and ml[1] == no:
							bl_mat = ml[0]
							mesh.materials.append(bl_mat)
							if bl_mat.use_transparency:
								obj_new.show_transparent = True
							#print( "    assign material %s avec la texture %s" % (bl_mat.name, self.tex_name_bl) )
							bOK = False
							break
			
					if bOK:
						debug_info( "   Pas la meme texture %s %s" % (ml[2],self.tex_name_bl) )
						
						for ml in material_list:
							if ml[1] == no:
								ac_mat = ml[3]
								# First use of material ??
								if len(bl_mat.texture_slots) != 0:
									bl_mat = bpy.data.materials.new(ac_mat.name_ac)

								debug_info( '    Create material %s with texture "%s"' % (bl_mat.name,self.tex_name_bl) )
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

								if self.tex_name != "":
									texture_slot = bl_mat.texture_slots.add()
									texture_slot.texture = texture
									texture_slot.texture_coords='UV'

								material_list.append( (bl_mat, no, self.tex_name_bl, ac_mat))
								mesh.materials.append(bl_mat)
								break
						
				
				else:
					if self.tex_name_bl !="":
						texture_slot = bl_mat.texture_slots.add()
						texture_slot.texture = texture
						texture_slot.texture_coords='UV'
						material_list[no] = ( ml[0],ml[1],self.tex_name_bl, ml[3] )
						debug_info( "    material %s with new texture = %s" % (ml[0].name,self.tex_name_bl) )
					else:
						debug_info( '    material %s without texture' % (ml[0].name) )
					mesh.materials.append(bl_mat)
	#----------------------------------------------------------------------------------------------------------------------------------

	def create_mesh( self ):
		global material_list
		global SMOOTH_ALL, EDGE_SPLIT, SPLIT_ANGLE, CONTEXT
		global current_ac_file
		
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
		#current_ac_file.meshs.append( self.mesh_name )
		current_ac_file.meshs.append( obj_new.name )

		obj_new.location = self.location
		if xml_extra_position:
			obj_new.delta_location = xml_extra_position.offset
			
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
	#----------------------------------------------------------------------------------------------------------------------------------

	def create_texture( self ):
	
		img_name = os.path.basename(self.tex_name)
		#21 name 21 char max
		img_name_clean = tronc_name( img_name )

		#print( "create_texture()  img_name : %s" % img_name )
		#print( "create_texture()  img_name_clean : %s" % img_name_clean )
	
		# null ???
		if img_name == "":
			return
		
		name_path = os.path.dirname(self.filename)
		name_path = os.path.normpath(name_path + os.sep + self.tex_name)
	
		filenamepath = img_name
	
		#debug_info( "create_texture()  name_path : %s" % bpy.path.basename(name_path) )
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
		self.set_tex_name( img_name_clean )
		self.tex_name_bl = tex.name
		self.img_name_bl = img.name
		debug_info( '    Creation de la texture "%s" img="%s"'%(self.tex_name_bl,self.img_name_bl) )
		return tex.name
#----------------------------------------------------------------------------------------------------------------------------------
#
#					FIN  object MESH
#
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

def get_ac_file():
	global current_ac_file
	return current_ac_file
#----------------------------------------------------------------------------------------------------------------------------------

def set_ac_file( new_ac_file ):
	global current_ac_file
	current_ac_file = new_ac_file
