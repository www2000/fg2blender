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
import bpy
import os

#--------------------------------------------------------------------------------------------------------------------------------
def debug_info(aff):
	from . import debug_fg2bl

	if debug_fg2bl:
		print(aff)


#--------------------------------------------------------------------------------------------------------------------------------
class PATH:
	#--------------------------------------------------------------------------------------------------------------------------------
	def __init__(self):
		self.dir_name_plane = ""
		self.bSaveBlend = False
	

	#--------------------------------------------------------------------------------------------------------------------------------
	def print_filename(self, filename ):
		debug_info( filename )
	
	#--------------------------------------------------------------------------------------------------------------------------------
	def rel_from( self, filepath="", frompath="" ):
		self.test_blender_filename()

		debug_info( "------------------------------" )
		debug_info( "args : filepath=%s frompath=%s" % (filepath, frompath) )
		
		from_pathname = ""
		if self.bSaveBlend and frompath[:2] == '//':
				fromp = os.path.dirname(bpy.data.tilepath) + os.sep +  frompath[2:]
				from_pathname = os.path.dirname( fromp )
		else:
			from_pathname = os.path.dirname( frompath )
		
		debug_info( "from_pathname : %s" % from_pathname )

		pathname = ""
		filename = ""
		if self.bSaveBlend and filepath[:2] == '//':
				filep = os.path.dirname(bpy.data.filepath) + os.sep +  filepath[2:]
				pathname = os.path.dirname( filep )
				filename = os.path.basename( filep )
		else:
			pathname = os.path.dirname( filepath )
			filename = os.path.basename( filepath )

		debug_info( "pathname : %s" % pathname )
		debug_info( "filename : %s" % filename )

		rel_path = os.path.relpath( pathname, from_pathname )
		rel_path_normalized = os.path.normpath( rel_path )

		return rel_path_normalized + os.sep + filename

	#--------------------------------------------------------------------------------------------------------------------------------
	def abs_from_with_aircraft( self, filepath="", frompath="" ):
		self.test_blender_filename()

		from_pathname = os.path.dirname( frompath )
		i = from_pathname.find( 'Aircraft' )
		from_pathname = frompath[:i]
		filename = from_pathname + os.sep + filepath
		
		return filename
	#--------------------------------------------------------------------------------------------------------------------------------
	def abs_from( self, filepath="", frompath="" ):
		self.test_blender_filename()

		if filepath.find( 'Aircraft' ) != -1:
			return self.abs_from_with_aircraft( filepath, frompath )
			
		from_pathname = os.path.dirname( frompath )
		from_basename = os.path.basename( frompath )
		
		#if not self.bSaveBlend:
		pathname = os.path.dirname( filepath )
		basename = os.path.basename( filepath )
		debug_info( "from_pathname    : %s" % from_pathname )
		debug_info( "from_basename    : %s" % from_basename )
		debug_info( "     pathname    : %s" % pathname )
		debug_info( "     basename    : %s" % basename )

		filename = filepath			
		pos = from_pathname.find(pathname)
		if pos != -1:
			filename = from_pathname[:pos] + os.sep + pathname + basename
		return filename
		#else:
		#	debug_info( "TODO")
		#	
		#return filename

	#--------------------------------------------------------------------------------------------------------------------------------
	def get_blender_filename( self ):
		return bpy.data.filepath
		
	#--------------------------------------------------------------------------------------------------------------------------------
	def test_blender_filename( self ):
		#debug_info( "Name blend : %s"  % bpy.data.filepath )
		#print( "Name blend : %s"  % bpy.data.filepath )
		if bpy.data.filepath == "":
			self.bSaveBlend = False
		else:
			self.bSaveBlend = True

	#--------------------------------------------------------------------------------------------------------------------------------
	def compute_path_abs( self, filepath ):
		self.test_blender_filename()
		
		if filepath == "" or filepath == None:
			return ""
		
		if self.bSaveBlend:
			if filepath[:2] == "//":
				filepath = os.path.dirname(bpy.data.filepath) + os.sep + os.path.basename(filepaht[2:])

			return filepath
		else:
			return filepath

	#--------------------------------------------------------------------------------------------------------------------------------
	def compute_path( self, filepath ):
		self.test_blender_filename()
		debug_info( "Name blend : %s"  % bpy.data.filepath )
		
		if filepath == "" or filepath == None:
			return ""
		
		
		if self.bSaveBlend:
			filepath = self.compute_path_abs( filepath )
			return bpy.path.relpath( filepath )
		else:
			return filepath

	#--------------------------------------------------------------------------------------------------------------------------------
	def change_all_to_relatif( self ):
		#----------------------------------------------------------------------------------------------------------------------------
		def change_to_relatif( filepath ):
			debug_info( 'change_to_relatif( "%s" )' % (filepath) )
			if filepath == "":
				return ""
			pathfile = bpy.path.relpath( filepath )
			#print ( bpy.ops.wm.save_as_mainfile.filepath )
			#pathfile = "//" + os.path.normpath( pathfile[2:])
			return pathfile
			
		#----------------------------------------------------------------------------------------------------------------------------
		def change_mesh( obj ):
			if obj:
				pathfile = change_to_relatif( obj.data.fg.ac_file )
				debug_info( "%s : %s" % (obj.name, pathfile) )
				if pathfile != obj.data.fg.ac_file:
					obj.data.fg.ac_file = pathfile
		#----------------------------------------------------------------------------------------------------------------------------
		def change_armature( obj ):
			if obj:
				pathfile = change_to_relatif( obj.data.fg.xml_file )
				debug_info( "%s : %s" % (obj.name, pathfile) )
				if pathfile != obj.data.fg.xml_file:
					obj.data.fg.xml_file = pathfile
		#----------------------------------------------------------------------------------------------------------------------------
		def change_camera( obj ):
			if obj:
				pathfile = change_to_relatif( obj.data.fg.xml_file )
				debug_info( "%s : %s" % (obj.name, pathfile) )
				if pathfile != obj.data.fg.xml_file:
					obj.data.fg.xml_file = pathfile
		#----------------------------------------------------------------------------------------------------------------------------
		def change_empty( obj ):
			if obj:
				if hasattr( obj, "fg" ):
					pathfile = change_to_relatif( obj.fg.jsb_xml_file )
					debug_info( "%s : %s" % (obj.name, pathfile) )
					if pathfile != obj.fg.jsb_xml_file:
						obj.fg.jsb_xml_file = pathfile
		#----------------------------------------------------------------------------------------------------------------------------
		
		self.test_blender_filename()
		
		for obj in bpy.data.objects:
			if obj.type == 'MESH':
				change_mesh( obj )
			if obj.type == 'ARMATURE':
				change_armature( obj )
			if obj.type == 'CAMERA':
				change_camera( obj )
			if obj.type == 'EMPTY':
				change_empty( obj )
		
	#--------------------------------------------------------------------------------------------------------------------------------
	def change_all_to_abs_previous( self ):
		#----------------------------------------------------------------------------------------------------------------------------
		def change_to_abs( filepath ):
			global previous_blendfile
		
			if filepath == "":
				return ""
	
			pathfile = ""
			if filepath[:2] == "//":
				pathfile = os.path.dirname(previous_blendfile) + os.sep + filepath[2:]
			else:
				pathfile = filepath
			return pathfile
			
		#----------------------------------------------------------------------------------------------------------------------------
		def change_mesh( obj ):
			if obj:
				pathfile = change_to_abs( obj.data.fg.ac_file )
				debug_info( "%s : %s" % (obj.name, pathfile) )
				if path != obj.data.fg.ac_file:
					obj.data.fg.ac_file = pathfile
		#----------------------------------------------------------------------------------------------------------------------------
		def change_armature( obj ):
			if obj:
				pathfile = change_to_abs( obj.data.fg.xml_file )
				debug_info( "%s : %s" % (obj.name, pathfile) )
				if pathfile != obj.data.fg.xml_file:
					obj.data.fg.xml_file = pathfile
		#----------------------------------------------------------------------------------------------------------------------------
		def change_camera( obj ):
			if obj:
				pathfile = change_to_abs( obj.data.fg.xml_file )
				debug_info( "%s : %s" % (obj.name, pathfile) )
				if pathfile != obj.data.fg.xml_file:
					obj.data.fg.xml_file = pathfile
		#----------------------------------------------------------------------------------------------------------------------------
		def change_empty( obj ):
			print( "change_empty " + obj.name + " " + obj.fg.jsb_xml_file )
			#return
			if obj:
				pathfile = change_to_abs( obj.fg.jsb_xml_file )
				debug_info( "%s : %s" % (obj.name, pathfile) )
				if pathfile != obj.fg.jsb_xml_file:
					obj.fg.jsb_xml_file = pathfile
		#----------------------------------------------------------------------------------------------------------------------------
		
		self.test_blender_filename()
		
		for obj in bpy.data.objects:
			if obj.type == 'MESH':
				change_mesh( obj )
			if obj.type == 'ARMATURE':
				change_armature( obj )
			if obj.type == 'CAMERA':
				change_camera( obj )
			if obj.type == 'EMPTY':
				change_empty( obj )
		
#------------------------------------------------------------------------------------------------------------------------------------
path = PATH()


		
#----------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------
from bpy.app.handlers import persistent
bBlockSave = True
previous_blendfile = ""

@persistent
def cb_save_pre( dummy ):
	global path
	global previous_blendfile
	
	if bpy.data.filepath != "":
		previous_blendfile = "" + bpy.data.filepath




@persistent
def cb_save_post( dummy ):
	global path
	global bBlockSave
	global previous_blendfile

	if not bBlockSave:
		return

	if previous_blendfile != "":
		path.change_all_to_abs_previous()
		
	path.change_all_to_relatif()

	bBlockSave = False
	bpy.ops.wm.save_as_mainfile()
	bBlockSave = True


bpy.app.handlers.save_pre.append( cb_save_pre )
bpy.app.handlers.save_post.append( cb_save_post )
#----------------------------------------------------------------------------------------------------------------------------------


