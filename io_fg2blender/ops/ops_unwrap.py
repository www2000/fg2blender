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
#									OPS_UNWRAP.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy

from . import *

from mathutils import Vector
from mathutils import Matrix

from math import radians
from math import degrees
from math import acos


from bpy.props import FloatProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import CollectionProperty

#----------------------------------------------------------------------------------------------------------------------------------
def debug_info( aff ):
	from .. import debug_unwrap
	
	if debug_unwrap:
		print( aff )

#----------------------------------------------------------------------------------------------------------------------------------

class FG_OT_unwrap_4_faces(bpy.types.Operator):
	'''C'est un exemple d'operateur blender '''
	bl_idname = "view3d.unwrap_4_faces"					# sera appelé par bpy.ops.view3d.exemple()
	bl_label = "Exemple d'operateur"
	bl_options = {'REGISTER', 'UNDO'}

	axis = bpy.props.StringProperty()

	#---------------------------------------------------------------------------
	@classmethod
	def poll(cls, context):
		if not context.active_object:
			return False
		return context.active_object.type in( 'MESH')

	#---------------------------------------------------------------------------

	def invoke(self, context, event):
		#---------------------------------------------------------------------------

		def compute_uv_up( indices, vertices, uvtex, idx, mat, bbmin, bbmax, dim, coef,  _max, decal ):
			#return 0.0
			dim = m * dim
			b = m * bbmin
			#decal = 0
			j = 0
			for i in indices:
				v = vertices[i].co
				w = m * v
				debug_info( '(%0.2f,%0.2f,%0.2f) (%0.2f,%0.2f)' % (w.x,w.y,w.z ,  (w.x-b.x) , (w.y-b.y) ) )
				u = (w.x-b.x)/coef
				v = (w.y-b.y)/coef
				if v >decal:
					decal = v
				uvtex.data[idx+j].uv = ( u, 0.0 + v + _max )
				j = j + 1
			return decal
		#---------------------------------------------------------------------------

		def compute_uv_down( indices, vertices, uvtex, idx, mat, bbmin, bbmax, dim, coef,  _max, decal  ):
			#return 0.0
			dim = m * dim
			bi = m * bbmin
			ba = m * bbmax
			j = 0
			for i in indices:
				v = vertices[i].co
				w = m * v
				u = (w.x-bi.x)/coef
				v = (-w.y+ba.y)/coef
				if  v>decal:
					decal = v
				
				uvtex.data[idx+j].uv = ( u, 0.0 + v + _max )
				j = j + 1
			return decal
		#---------------------------------------------------------------------------
		
		def compute_uv_left( indices, vertices, uvtex, idx, mat, bbmin, bbmax, dim, coef,  _max, decal  ):
			#return 0.0
			dim = m * dim
			b = m * bbmin
			j = 0
			for i in indices:
				v = vertices[i].co
				w = m * v
				u = (w.x-b.x)/coef
				v = (w.z-b.z)/coef
				if v >decal:
					decal = v
				#v = (-w.z+b.z)/coef
				
				uvtex.data[idx+j].uv = ( u, 0.0 + v + _max )
				j = j + 1
			return decal
		#---------------------------------------------------------------------------

		def compute_uv_right( indices, vertices, uvtex, idx, mat, bbmin, bbmax, dim, coef,  _max, decal  ):
			#return 0.0
			dim = m * dim
			bm = m * bbmin
			bM = m * bbmax
			j = 0
			for i in indices:
				v = vertices[i].co
				w = m * v
				u = (w.x-bm.x)/coef
				v = (-w.z+bM.z)/coef
				if v >decal:
					decal = v
				
				uvtex.data[idx+j].uv = ( u, 0.0 + v + _max )
				j = j + 1
			return decal
	#---------------------------------------------------------------------------

		_max = 0

		obj = context.active_object
		up		= Vector( (0.0,0.0,1.0) )
		front	= Vector( (0.0,1.0,0.0) )
		mw = obj.matrix_world
		if self.axis == 'X':
			mat_rot = Matrix.Rotation(radians(0.0), 4, 'Z')
		elif self.axis == 'Y':
			mat_rot = Matrix.Rotation(radians(-90.0), 4, 'Y')
		elif self.axis == 'Z':
			mat_rot = Matrix.Rotation(radians(90.0), 4, 'Z')
		
		m = mw * mat_rot
		m3 = m.to_3x3()
		#m = mw * mat_rot

		mesh = obj.data
		uvtex = mesh.uv_layers.active
		debug_info( 'uv_textures.active "%s"' % (mesh.uv_textures.active) )
		if uvtex != None:
			debug_info( 'uv_textures.active.active "%s"' % str(mesh.uv_textures.active.active) )
			debug_info( 'uv_textures.active.active_clone "%s"' % str(mesh.uv_textures.active.active_clone) )
			debug_info( 'uv_textures.active.active_render "%s"' % str(mesh.uv_textures.active.active_render) )
		if uvtex == None:
			uv = mesh.uv_textures.new()
			debug_info( 'Creation uv text Name "%s"' % uv.name )
			uvtex = mesh.uv_layers.active

		debug_info( ' uvtext = "%s"' % str(uvtex) )
		debug_info( ' nb = %s' % len(uvtex.data) )
		n_uvtex = mesh.uv_layers.active_index
		debug_info( 'Name "%s"' % mesh.uv_textures[n_uvtex].name )

		bbb = obj.bound_box
		for i in range(8):
			v = Vector( (bbb[i][0],bbb[i][1],bbb[i][2]) )
			w = m * v
			debug_info( 'BB (%0.2f,%0.2f,%0.2f)' % (w.x,w.y,w.z) )

		bbmin = Vector( (bbb[0][0],bbb[0][1],bbb[0][2]) )
		bbmax = Vector( (bbb[6][0],bbb[6][1],bbb[6][2]) )
		#w = Vector( (bb[6][0],bb[6][1],bb[6][2]) )
		#bb = m * b
		dim = obj.dimensions

		debug_info( str(context.selected_objects) )
		if len(context.selected_objects) == 2:
			for bbox in context.selected_objects:
				if bbox != obj:
					break
			debug_info( bbox.name )
			dim = bbox.dimensions


		idx = 0

		coef = dim.x
		if dim.y > coef:
			coef = dim.y
		if dim.z > coef:
			coef = dim.z

		if self.axis == 'X':
			coef = dim.x
		elif self.axis == 'Y':
			coef = dim.y
		elif self.axis == 'Z':
			coef = dim.z
		
		
		#coef = coef

		debug_info( 'Coef %0.2f' %  coef )


		idx = 0
		decal = 0		
		for polygon in obj.data.polygons:
			if not polygon.select:
				idx = idx + len(polygon.vertices)
				continue
			n = Vector( (0.0,0.0,0.0) ) + polygon.normal
			v = m3 * n
			v.x = 0.0
			v.normalize()
			angle =  degrees( up.angle(v, 999) )
			if angle == 999:
				idx = idx + len(polygon.vertices)
				continue
			
			if angle < 45 or angle > 360-45:
				idx = idx + len(polygon.vertices)
				continue
			elif angle < 225 and angle > 135:
				idx = idx + len(polygon.vertices)
				continue
			else:
				#angle = degrees( front.angle(v) )
				n = Vector( (0.0,0.0,0.0) ) + polygon.normal
				v = m3 * n
				angle =  degrees( front.angle(v, 999) )
				debug_info( "Normal x=%0.2f y=%0.2f z=%0.2f" % (v.x,v.y,v.z) )
				debug_info( "     dot=%0.2f" % angle )
				if angle == 999:
					idx = idx + len(polygon.vertices)
					continue
				if angle<90:# and angle < 180:
					idx = idx + len(polygon.vertices)
					continue
				else:
					decal = compute_uv_left( polygon.vertices, mesh.vertices, uvtex, idx, m, bbmin, bbmax, dim, coef,  _max, decal )
					debug_info( "dot=%0.2f" % angle )
			idx = idx + len(polygon.vertices)

		debug_info( 'Decal Left %0.2f' % decal )


		_max = _max + decal + 0.03
		idx = 0
		decal = 0		
		for polygon in obj.data.polygons:
			if not polygon.select:
				idx = idx + len(polygon.vertices)
				continue
			n = Vector( (0.0,0.0,0.0) ) + polygon.normal
			v = m3 * n
			v.x = 0.0
			v.normalize()
			#v.normalize()
			#v = n
			angle =  degrees( up.angle(v, 999) )
			if angle == 999:
				idx = idx + len(polygon.vertices)
				continue
				
			
			#uv = Vector( (0.0,0.0) )
			if (360-45)<angle or angle < 45:# or angle >= 360-45:
				debug_info( "------------------------------------" )
				decal = compute_uv_up( polygon.vertices, mesh.vertices, uvtex, idx, m, bbmin, bbmax, dim, coef,  _max, decal )
				debug_info( 'Up decal %0.2f' % decal )
			idx = idx + len(polygon.vertices)


		debug_info( 'Decal Up %0.2f' % decal )

		_max = _max + decal + 0.03
		idx = 0
		decal = 0		
		for polygon in obj.data.polygons:
			if not polygon.select:
				idx = idx + len(polygon.vertices)
				continue
			n = Vector( (0.0,0.0,0.0) ) + polygon.normal
			v = m3 * n
			v.x = 0.0
			v.normalize()
			angle =  degrees( up.angle(v, 999) )
			if angle == 999:
				idx = idx + len(polygon.vertices)
				continue
			
			#uv = Vector( (0.0,0.0) )
			if angle < 45 or angle > 360-45:
				idx = idx + len(polygon.vertices)
				continue
			elif 135 < angle and angle < 225 :
				idx = idx + len(polygon.vertices)
				continue
			else:
				#angle = degrees( front.angle(v) )
				n = Vector( (0.0,0.0,0.0) ) + polygon.normal
				v = m3 * n
				angle =  degrees( front.angle(v, 999) )
				if angle == 999:
					idx = idx + len(polygon.vertices)
					continue
				#if 0 <angle and angle < 180:
				if angle < 90:
					decal = compute_uv_right( polygon.vertices, mesh.vertices, uvtex, idx, m, bbmin, bbmax, dim, coef,  _max, decal )
					debug_info( "dot=%0.2f" % angle )
					debug_info( 'Right' )
			idx = idx + len(polygon.vertices)
		
		debug_info( 'Decal Right %0.2f' % decal )

				
		_max = _max + decal + 0.03
		idx = 0
		decal = 0		
		for polygon in obj.data.polygons:
			if not polygon.select:
				idx = idx + len(polygon.vertices)
				continue
			n = Vector( (0.0,0.0,0.0) ) + polygon.normal
			v = m3 * n
			v.x = 0.0
			v.normalize()
			angle =  degrees( up.angle(v, 999) )
			if angle == 999:
				idx = idx + len(polygon.vertices)
				continue
			
			if angle < 45 or angle > 360-45:
				idx = idx + len(polygon.vertices)
				continue
			elif 135 < angle and angle < 225 :
				debug_info( "------------------------------------" )
				debug_info( "Normal x=%0.2f y=%0.2f z=%0.2f" % (v.x,v.y,v.z) )
				debug_info( "dot=%0.2f" % angle )
				decal = compute_uv_down( polygon.vertices, mesh.vertices, uvtex, idx, m, bbmin, bbmax, dim, coef,  _max, decal )
				debug_info( 'Down decal %0.2f' % decal )
			idx = idx + len(polygon.vertices)

		debug_info( 'Decal Down %0.2f' % decal )
		
		#bpy.data.objects['Cube'].data.polygons[1].normal
		return {'FINISHED'}
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class( FG_OT_unwrap_4_faces )

def unregister():
	bpy.utils.unregister_class( FG_OT_unwrap_4_faces )

