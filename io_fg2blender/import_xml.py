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

