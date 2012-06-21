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


from mathutils import Vector
from mathutils import Euler


from .ac_manager import AC_FILE

#----------------------------------------------------------------------------------------------------------------------------------

xml_files = []
xml_current = None


#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS XML_OPTION
#----------------------------------------------------------------------------------------------------------------------------------
#	Option for xml parser file
#----------------------------------------------------------------------------------------------------------------------------------

class XML_OPTION:
	def __init__(self):
		self.include		= False

#----------------------------------------------------------------------------------------------------------------------------------
#							CLASS XML_FILE
#----------------------------------------------------------------------------------------------------------------------------------
#	name		= "plane.xml"								string	xml file name
#	ac_name		= [ fuse.ac" , "wings.ac" , ...]			List of string
#	ac_file		= [ AC_FILE(), AC_FILE() , ... ]			List of ac_file object
#	offset		= ( 0.0 , 0.0 , 0.0 )						mathutils.Vector		
#	eulerXYZ	= ( 0.0 , 0.0 , 0.0 )						mathutils.Euler (for pich-deb,roll-deg, etc)
#	file_offset = "include.xml"								strings    where xml define offset (parent file name)
#----------------------------------------------------------------------------------------------------------------------------------

class XML_FILE:
	def __init__(self):
		self.name			= ""
		self.ac_names		= []
		self.ac_files		= []
		self.offset			= Vector( (0.0, 0.0, 0.0) )
		self.eulerXYZ		= Euler( (0.0, 0.0, 0.0) )
		self.file_offset	= ""

		
	def add_ac_file( self, ac_file = None ):
		if ac_file:
			self.ac_files.append( ac_file )
			self.ac_names.append( ac_file.name )
#----------------------------------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------------------------------

def add_xml_file( xml_file=None ):
	if xml_file:
		xml_files.append( xml_file )
#----------------------------------------------------------------------------------------------------------------------------------

def set_current_xml( xml_file=None ):
	global xml_current
	
	xml_current = xml_file
#----------------------------------------------------------------------------------------------------------------------------------

def get_current_xml():
	global xml_current
	
	return  xml_current
#----------------------------------------------------------------------------------------------------------------------------------

def is_defined( filename ):
	global xml_files
	
	for xml_file in xml_files:
		if xml_file.name == filename:
			return True
	return False
#----------------------------------------------------------------------------------------------------------------------------------

def isnot_defined( filename ):
	return not is_defined( filename )
#----------------------------------------------------------------------------------------------------------------------------------

def get_xml_file( filename ):
	global xml_files
	
	for xml_file in xml_files:
		if xml_file.name == filename:
			return xml_file
	return None
#----------------------------------------------------------------------------------------------------------------------------------
	
