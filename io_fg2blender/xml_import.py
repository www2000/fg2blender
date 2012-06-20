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

#====================================================================================================================#
#
#
#				IMPORT    .ac     FILE
#
#
#====================================================================================================================

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
#
#
#						==============
#
#						Main function
#
#						==============
#----------------------------------------------------------------------------------------------------------------------------------

def import_xml(filename, smooth_all, edge_split, split_angle, context):
	global path_name, material_list
	global SMOOTH_ALL, EDGE_SPLIT, SPLIT_ANGLE
	global CONTEXT
	
	from .read_xml import read_file_xml
	
	read_file_xml( filename )

