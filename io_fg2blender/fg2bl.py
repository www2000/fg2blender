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

class PATH:
	def __init__(self):
		self.DEBUG = True
		self.dir_name_plane = ""
		self.bSaveBlend = False
	
	def debug_info(self, aff):
		if self.DEBUG:
			print(aff)

	def print_filename(self, filename ):
		self.debug_info( filename )
	
	'''
	def rel_from( self, filepath="", frompath="" ):
		self.test_blender_filename()
		
		if bSaveBlend:
			pathname = os.path.dirname( filepath )
			filename = os.path.basename( filepath )
			rel_path = os.path.relpath( pathname, frompath )
			rel_path_normalized = os.path.normpath( rel_path )
			return rel_path_normalized + os.sep + filename

		return rel_path_normalize + os.sep + filename
	'''		
	def get_blender_filename( self ):
		return bpy.data.filepath
		
	def test_blender_filename( self ):
		print( "Name blend : %s"  % bpy.data.filepath )
		if bpy.data.filepath == "":
			self.bSaveBlend = False
		else:
			self.bSaveBlend = True
		
path = PATH()

