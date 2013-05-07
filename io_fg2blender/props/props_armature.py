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
# Contributors: Alexis Laillé
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									PROPS_ARMATURE.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy
from . import *

from ..ui.ui_lang import lang
from ..xml import xml_manager
#----------------------------------------------------------------------------------------------------------------------------------

def debug_info( aff ):
	from .. import debug_props_armature
	
	if debug_props_armature:
		print( aff )
#----------------------------------------------------------------------------------------------------------------------------------

bLock_update = False
 
familles = ['APU','anti_ice','armament','autoflight','electric' , 'engine','flight','fuel','gear', 'consumable','surface_position']


#Tuples ('Property',min,max,time)
#               min max :       'x' : valeur variable
#               time :          True/False : cinématique ou non


APUs = 		[
		('controls/APU/off-start-run', 0, 1, False),
		('controls/APU/fire-switch', 0, 'x', False)
		]

anti_ices = 	[
		('controls/anti-ice/wing-heat', 0, 1, False),
		('controls/anti-ice/pitot-heat', 0, 1, False),
		('controls/anti-ice/wiper', 0, 'x', False),
		('controls/anti-ice/window-heat', 0, 1, False),
		('controls/anti-ice/engine[%d]/carb-heat', 0, 1, False),
		('controls/anti-ice/engine[%d]/inlet-heat', 0, 1, False)
		]

armaments = 	[
		('controls/armament/master-arm', 0, 1, False),
		('controls/armament/station-select', 0, 1, False),
		('controls/armament/release-all', 0, 1, False),
		('controls/armament/station[%d]/stick-size', 0, 1, False),
		('controls/armament/station[%d]/release-stick', 0, 1, False),
		('controls/armament/station[%d]/release-all', 0, 1, False),
		('controls/armament/station[%d]/jettison-all', 0, 1, False)
		]

autoflights = 	[
		('controls/autoflight/autopilot[%d]/engage', 0, 1, False),
		('controls/autoflight/autothrottle-arm', 0, 1, False),
		('controls/autoflight/autothrottle-engage', 0, 1, False),
		('controls/autoflight/heading-select', 0, 360, False),
		('controls/autoflight/altitude-select', 0, 'x', False),
		('controls/autoflight/bank-angle-select', 0, 'x', False),
		('controls/autoflight/vertical-speed-select', 0, 'x', False),
		('controls/autoflight/speed-select', 0, 'x', False),
		('controls/autoflight/mach-select', 0, 'x', False),
		('controls/autoflight/vertical-mode', 0, 'x', False),
		('controls/autoflight/lateral-mode', 0, 1, False)
		]

electrics = 	[
		('controls/electric/battery-switch', 0, 1, False),
		('controls/electric/external-power', 0, 1, False),
		('controls/electric/APU-generator', 0, 1, False),
		('controls/electric/engine[%d]/generator', 0, 1, False),
		('controls/electric/engine[%d]/bus-tie', 0, 1, False)
		]

       
#engines comportement des variables à affiner
engines = 	[
		('controls/engines/throttle_idle',0,1,False),
		('controls/engines/engine[%d]/throttle',0,1,False),
		('controls/engines/engine[%d]/starter',0,1,False),
		('controls/engines/engine[%d]/fuel-pump',0,1,False),
		('controls/engines/engine[%d]/fire-switch',0,1,False),
		('controls/engines/engine[%d]/fire-bottle-discharge',0,1,False),
		('controls/engines/engine[%d]/cutoff',0,1,False),
		('controls/engines/engine[%d]/mixture',0,1,False),
		('controls/engines/engine[%d]/propeller-pitch',0,1,False),
		('controls/engines/engine[%d]/magnetos',0,3,False),
		('controls/engines/engine[%d]/boost',0,1,False),
		('controls/engines/engine[%d]/WEP',0,1,False),
		('controls/engines/engine[%d]/cowl-flaps-norm',0,1,False),
		('controls/engines/engine[%d]/feather',0,1,False),
		('controls/engines/engine[%d]/ignition',0,3,False),
		('controls/engines/engine[%d]/augmentation',0,1,False),
		('controls/engines/engine[%d]/afterburner',0,1,False),
		('controls/engines/engine[%d]/reverser',0,1,False),
		('controls/engines/engine[%d]/water-injection',0,1,False),
		('controls/engines/engine[%d]/condition',0,1,False)
		]
 
flights = 	[
		('controls/flight/aileron',-1,1,False),
		('controls/flight/aileron-trim',-1,1,False),
		('controls/flight/elevator',-1,1,False),
		('controls/flight/elevator-trim',-1,1,False),
		('controls/flight/rudder',-1,1,False),
		('controls/flight/rudder-trim',-1,1,False),
		('controls/flight/flaps',0,1,False),
		('controls/flight/slats',0,1,False),
		('controls/flight/BLC',0,1,False),
		('controls/flight/spoilers',0,1,False),
		('controls/flight/speedbrake',0,1,False),
		('controls/flight/wing-sweep',0,1,False),
		('controls/flight/wing-fold',0,1,False),
		('controls/flight/drag-chute',0,1,False)
		]
 
fuels = 	[
		('controls/fuel/dump-valve',0,1,False),
		('controls/fuel/tank[%d]/fuel_selector',0,1,False),
		('controls/fuel/tank[%d]/to_engine',0,'x',False),
		('controls/fuel/tank[%d]/to_tank',0,'x',False),
		('controls/fuel/tank[%d]/boost-pump[%d]',0,1,False)
		]
 
consumables = 	[
		('consumables/fuel/tank[%d]/level-lbs',0,'x',False),
		('consumables/fuel/tank[%d]/level-gal_us',0,'x',False),
		('consumables/fuel/tank[%d]/capacity-gal_us',0,'x',False),
		('consumables/fuel/tank[%d]/density-ppg',0,'x',False),
		('consumables/fuel/total-fuel-lbs',0,'x',False),
		('consumables/fuel/total-gal_us',0,'x',False)
		]
                               
gears = 	[
		('controls/gear/brake-left',0,1,False),
		('controls/gear/brake-right',0,1,False),
		('controls/gear/brake-parking',0,1,False),
		('controls/gear/steering',0,'x',False),
		('controls/gear/gear-down',0,1,True),
		('controls/gear/antiskid',0,1,False),
		('controls/gear/tailhook',0,1,False),
		('controls/gear/tailwheel-lock',0,1,False),
		('controls/gear/wheel[%d]/alternate-extension',0,1,False),
		('gear/gear[%d]/caster-angle-deg',0,1,False),
		('gear/gear[%d]/compression-m',0,1,False),
		('gear/gear[%d]/compression-norm',0,1,False),
		('gear/gear[%d]/ground-friction-factor',0,1,False),
		('gear/gear[%d]/ground-is-solid',0,1,False),
		('gear/gear[%d]/has-brake',0,1,False),
		('gear/gear[%d]/position-norm',0,1,True),
		('gear/gear[%d]/rollspeed-ms',0,'x',False),
		('gear/gear[%d]/rollspeed-ms',0,1,False)	
		]
 
surface_positions = [
		('surface-positions/rudder-pos-norm',-1,1,False),
		('surface-positions/elevator-pos-norm',-1,1,False),
		('surface-positions/left-aileron-pos-norm',-1,1,False),
		('surface-positions/right-aileron-pos-norm',-1,1,False),
		('surface-positions/flap-pos-norm',0,1,False),
		('surface-positions/left-aileron-pos-norm',-1,1,False),
		('surface-positions/left-aileron-pos-norm',-1,1,False)	
		]
#----------------------------------------------------------------------------------------------------------------------------------

def update_keyframe( obj, coef ):
	global bLock_update

	if bLock_update == True:
		return None
	
	if obj.animation_data:
		for fcurve in obj.animation_data.action.fcurves:
			for keyframe in fcurve.keyframe_points:
				#keyframe.interpolation = 'LINEAR'
				keyframe.co.y = keyframe.co.y * coef
				debug_info( keyframe.co )
#----------------------------------------------------------------------------------------------------------------------------------

def update_keyframe_time( obj, coef ):
	global bLock_update

	if bLock_update == True:
		return None
	
	if obj.animation_data:
		for fcurve in obj.animation_data.action.fcurves:
			for keyframe in fcurve.keyframe_points:
				#keyframe.interpolation = 'LINEAR'
				keyframe.co.x = ((keyframe.co.x-1) * coef ) +1
				debug_info( keyframe.co )
#----------------------------------------------------------------------------------------------------------------------------------

def update_keyframe_time( obj, coef ):
	global bLock_update

	if bLock_update == True:
		return None
	
	if obj.animation_data:
		for fcurve in obj.animation_data.action.fcurves:
			for keyframe in fcurve.keyframe_points:
				#keyframe.interpolation = 'LINEAR'
				keyframe.co.x = ((keyframe.co.x-1) * coef ) +1
				debug_info( keyframe.co )
#----------------------------------------------------------------------------------------------------------------------------------

def update_factor( self, context ):
	global bLock_update
	from ..xml import xml_export

	if bLock_update == True:
		return None

	coef = 0.0
	obj = context.active_object
	if obj:
		#if obj.type == 'ARMATURE':
		if obj.data.fg.type_anim in [ 'rotate', 'translate']:
			if obj.data.fg.factor_ini == 0.0:
				obj.data.fg.factor_ini = obj.data.fg.factor
			coef = obj.data.fg.factor  / obj.data.fg.factor_ini
			update_keyframe( obj, coef )
			obj.data.fg.factor_ini = obj.data.fg.factor

			
			bLock_update = True
			obj_factor = obj.data.fg.factor
			property_value = xml_export.build_property_name( obj )
			for o in bpy.data.objects:
				if o.type != 'ARMATURE' or o == obj:
					continue
				if xml_export.build_property_name(o) == property_value:
					debug_info( "update keyframe pour %s" %o.name )
					o.data.fg.factor = obj_factor
					o.data.fg.factor_ini = obj_factor
					update_keyframe( o, coef )
			bLock_update = False
#----------------------------------------------------------------------------------------------------------------------------------

def update_time( self, context ):
	global bLock_update
	from ..xml import xml_export

	if bLock_update == True:
		return None
			
	coef = 0.0
	obj = context.active_object
	if obj:
		#if obj.type == 'ARMATURE':
		if obj.data.fg.type_anim in [ 'rotate', 'translate']:
			if obj.data.fg.time_ini == 0.0:
				obj.data.fg.time_ini = obj.data.fg.time
			coef = 0.0 + obj.data.fg.time  / obj.data.fg.time_ini
			update_keyframe_time( obj, coef )
			obj.data.fg.time_ini = 0.0 +  obj.data.fg.time

			bLock_update = True
			obj_time = obj.data.fg.time
			property_value = xml_export.build_property_name( obj )
			for o in bpy.data.objects:
				if o.type != 'ARMATURE' or obj == o:
					continue
				if xml_export.build_property_name(o) == property_value:
					debug_info( "update keyframe pour %s" %o.name )
					o.data.fg.time = obj_time
					o.data.fg.time_ini = 0.0 +  o.data.fg.time
					update_keyframe_time( o, coef )
			bLock_update = False
#---------------------------------------------------------------------------

def update_range_beg( self, context ):
	from ..xml import xml_export
	global bLock_update

	if bLock_update == True:
		return None
	
	active_object = context.active_object

	debug_info( 'update_range_deb "%s"  %s' % (active_object.name, str(bLock_update))  )
		
	property_value = "" + xml_export.build_property_name( active_object )
	range_beg = active_object.data.fg.range_beg
	debug_info( ' range_beg :  %s' % (range_beg)  )

	bLock_update = True
	for obj in bpy.data.objects:
		if obj.type != 'ARMATURE':
			continue
		value = "" + xml_export.build_property_name(obj)
		if value == property_value:
			debug_info( "\tupdate pour : %s" % obj.name )
			obj.data.fg.range_beg = range_beg
		
	bLock_update = False
	return None	
#---------------------------------------------------------------------------

def update_range_end( self, context ):
	from ..xml import xml_export
	global bLock_update

	if bLock_update == True:
		return None
	
	active_object = context.active_object

	debug_info( 'update_range_end "%s" block_update=%s' % (active_object.name, str(bLock_update))  )
		
	property_value = xml_export.build_property_name( active_object )
	debug_info( 'update_range_end "%s" -- property_value %s' % (active_object.name, property_value)  )
	range_end = active_object.data.fg.range_end
	debug_info( ' range_end :  %s' % (range_end)  )

	bLock_update = True
	for obj in bpy.data.objects:
		if obj.type != 'ARMATURE':
			continue
		if xml_export.build_property_name(obj) == property_value:
			debug_info( "\tupdate pour : %s  -- property_value %s" % (obj.name,xml_export.build_property_name(obj)) )
			obj.data.fg.range_end = range_end
		
	bLock_update = False
	return None	

#---------------------------------------------------------------------------

def update_bWriteDisc( self, context ):
	from ..xml import xml_export
	global bLock_update

	if bLock_update == True:
		return None
	
	active_object = context.active_object

	debug_info( 'update_toDisk "%s"  %s' % (active_object.name, str(bLock_update))  )
		
	xml_file = active_object.data.fg.xml_file
	xml_file_no = active_object.data.fg.xml_file_no
	bWriteDisc = active_object.data.fg.bWriteDisc
	debug_info( ' bWriteDisc :  %s' % (bWriteDisc)  )

	bLock_update = True
	for obj in bpy.data.objects:
		if obj.type != 'ARMATURE':
			continue
		if xml_file == obj.data.fg.xml_file and xml_file_no == obj.data.fg.xml_file_no:
			debug_info( "\tupdate pour : %s" % obj.name )
			obj.data.fg.bWriteDisc = bWriteDisc
		
	bLock_update = False
	return None	
#---------------------------------------------------------------------------

def update_bIncDiskFile( self, context ):
	from ..xml import xml_export
	global bLock_update

	if bLock_update == True:
		return None
	
	active_object = context.active_object

	debug_info( 'update_toDisk "%s"  %s' % (active_object.name, str(bLock_update))  )
		
	xml_file = active_object.data.fg.xml_file
	xml_file_no = active_object.data.fg.xml_file_no
	bIncDiskFile = active_object.data.fg.bIncDiskFile
	debug_info( ' bIncDiskFile :  %s' % (bIncDiskFile)  )

	bLock_update = True
	for obj in bpy.data.objects:
		if obj.type != 'ARMATURE':
			continue
		if xml_file == obj.data.fg.xml_file and xml_file_no == obj.data.fg.xml_file_no:
			debug_info( "\tupdate pour : %s" % obj.name )
			obj.data.fg.bIncDiskFile = bIncDiskFile
		
	bLock_update = False
	return None	
#----------------------------------------------------------------------------------------------------------------------------------
def endline():
	global rca, nChar, nBit
	char = rca[nChar]
	eb = bin(int(char))
	if eb[nBit] == '0':
		ret = ' '
	else:
		ret = '  '
	nBit += 1
	if nBit == 9:
		nBit = 2
		nChar += 1
		if nChar == len(rca):
			nChar = 0
	return ret
#----------------------------------------------------------------------------------------------------------------------------------

def dynamic_items( self, context ):
	obj = context.active_object

	#familles = ['APU','anti_ice','armament','autoflight','electric' , 'engine','flight','fuel','gear']

	if obj.data.fg.family == 'APU':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for (fc, _min, _max, b )in APUs ]
	elif obj.data.fg.family == 'anti_ice':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for fc, _min, _max, b in anti_ices ]
	elif obj.data.fg.family == 'armament':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for fc, _min, _max, b in armaments ]
	elif obj.data.fg.family == 'autoflight':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for fc, _min, _max, b in autoflights ]
	elif obj.data.fg.family == 'electric':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for fc, _min, _max, b in electrics ]
	elif obj.data.fg.family == 'controls':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for fc, _min, _max, b in flight_controls ]
	elif obj.data.fg.family == 'engine':
	    items = [ (en,en.split('/')[-1],en.split('/')[-1]) for en, _min, _max, b in engines ]
	elif obj.data.fg.family == 'flight':
	    items =	[ (fu,fu.split('/')[-1],fu.split('/')[-1]) for fu, _min, _max, b in flights ]
	elif obj.data.fg.family == 'fuel':
	    items =	[ (fu,fu.split('/')[-1],fu.split('/')[-1]) for fu, _min, _max, b in fuels ]
	elif obj.data.fg.family == 'gear':
	    items = [ (ge,ge.split('/')[-1],ge.split('/')[-1]) for ge, _min, _max, b in gears ]
	elif obj.data.fg.family == 'consumable':
	    items = [ (ge,ge.split('/')[-1],ge.split('/')[-1]) for ge, _min, _max, b in consumables ]
	elif obj.data.fg.family == 'surface_position':
	    items = [ (ge,ge.split('/')[-1],ge.split('/')[-1]) for ge, _min, _max, b in surface_positions ]
	else:
		items = [  ('error','error','error') ]
	return items
#----------------------------------------------------------------------------------------------------------------------------------

def dynamic_items_xml_file( self, context ):
	from ..xml import xml_manager
	#items = [ (xf.name,xf.name.split('/')[-1],xf.name.split('/')[-1]) for xf,no in xml_manager.xml_files ]
	items = [ ("","","") ] + [ (xf.name,xf.name,xf.name) for xf,no in xml_manager.xml_files ]
	return items
rca = [82, 101, 110, 101, 67, 108, 101, 109, 101, 110, 116, 65, 108, 101, 120, 105, 115]
nChar = 0
nBit = 2
#----------------------------------------------------------------------------------------------------------------------------------



class FG_PROP_keyframe(bpy.types.PropertyGroup):
	x = bpy.props.FloatProperty( attr = 'x', name = 'x' )
	y = bpy.props.FloatProperty( attr = 'y', name = 'y' )

#----------------------------------------------------------------------------------------------------------------------------------



class FG_PROP_armature(bpy.types.PropertyGroup):

	#---------------------------------------------------------------------------
	def exist_in_text_editor(self, name ):
		for text in bpy.data.texts:
			if text.name == name:
				return True
		return False
	#---------------------------------------------------------------------------

	def creer_xml(self, filename, obj):
		from ..xml import xml_manager
		new_filename = ""
		new_no = 0
		for xml_file, no in xml_manager.xml_files:
			if xml_file.name == filename:
				new_filename = filename
				new_no		 = no
				break;
		
		if new_filename == "":
			no = len(xml_manager.xml_files)
			xml_file = xml_manager.XML_FILE()
			xml_file.name	= filename
			xml_file.no		= no
			xml_manager.add_xml_file( xml_file, new_no )
			#new_filename = filename
			#new_no		 = no
			#xml_manager.add_xml_file( new_filename, new_no )

		obj.data.fg.xml_file	= new_filename
		obj.data.fg.xml_file_no	= new_no
	#---------------------------------------------------------------------------

	def update_xml_file( self, context ):
		global bLock_update
		from .. import fg2bl

		if bLock_update == True:
			return None
		
		active_object = context.active_object
		if active_object == None:
			return None

		debug_info( 'update_xml_file "%s"  %s' % (active_object.name, str(bLock_update))  )
		debug_info( ' value :  %s' % (active_object.data.fg.xml_file)  )
			
		bLock_update = True

		xml_file = "" + active_object.data.fg.xml_file
		xml_file = bpy.path.abspath( xml_file )
		xml_file = fg2bl.path.compute_path( xml_file )

		debug_info( ' compute value :  %s' % (xml_file)  )

		if active_object.data.fg.xml_file == xml_file:
			debug_info("Don't change!!!")
		else:
			active_object.data.fg.xml_file = xml_file
		
			self.creer_xml( xml_file, active_object )
			no_xml_file = active_object.data.fg.xml_file_no
			debug_info( 'no xml_file  = %d' % no_xml_file )
		
			for obj in context.selected_objects:
				#if obj.name == active_object.name:
				#	continue
				if obj.type != 'ARMATURE':
					continue
				debug_info( "\t%s" % obj.name )
				obj.data.fg.xml_file = "" + xml_file
				obj.data.fg.xml_file_no = no_xml_file
			
		bLock_update = False
		return None	
	#---------------------------------------------------------------------------

	def update_property( self, context ):
		from ..xml import xml_export
		global bLock_update

		if bLock_update == True:
			return None
		
		active_object = context.active_object
		family = "" + active_object.data.fg.family
		if family == 'custom':
			value = xml_export.build_property_name( active_object )
		else:
			value = "" + active_object.data.fg.family_value
		

		debug_info( '---- update_familly_value() "%s"  %s' % (active_object.name, str(bLock_update))  )
		debug_info( ' value :  %s' % (value)  )
		debug_info( " objet - actif  : %s" % active_object.name )
			
		bLock_update = True

		for obj in context.selected_objects:
			if obj.type != 'ARMATURE' or obj == active_object:
				continue
			debug_info( " objet - select : %s" % obj.name )
			obj.data.fg.family = family
			if family == 'custom':
				obj.data.fg.property_value = value
			else:
				obj.data.fg.family_value = value
			
			
		bLock_update = False
		return None	
	#----------------------------------------------------------------------------------------------------------------------------------

	family		= bpy.props.EnumProperty	(
							attr = 'family', 
							name = lang['UI017'], 
							description = lang['DOC043'], 
							default = 'custom', 
							items = [ ('custom','custom','custom') ] + [ (famille,famille,famille) for famille in familles ], 
							update=update_property
							)

	family_value	= bpy.props.EnumProperty	( 
							attr = 'family_value', 
							name = lang['UI018'], 
							description = lang['DOC044'], 
							items=dynamic_items, 
							update=update_property 
							)

	property_value	= bpy.props.StringProperty	( 
							attr = 'value', 
							name = lang['UI008'], 
							description = lang['DOC045'], 
							update=update_property
							)

	property_idx	= bpy.props.IntProperty		( 
							attr = 'idx', 
							name = lang['UI019'], 
							description = lang['DOC048'], 
							min=-1
							)

	factor		= bpy.props.FloatProperty	( 
							attr = 'factor', 
							name = lang['UI020'], 
							description = lang['DOC051'], 
							update=update_factor
							)

	factor_ini	= bpy.props.FloatProperty	( 
							attr = 'factor_ini', 
							name = lang['UI020'], 
							description = lang['DOC051']
							)

	xml_file	= bpy.props.StringProperty	( 
							attr = 'xml_file', 
							name = lang['UI010'], 
							description = lang['DOC052'], 
							update=update_xml_file
							)

	xml_file_no	= bpy.props.IntProperty		( 
							attr = 'xml_file_no', 
							name = 'No xml File', #???????
							description = '?????????'
							)

	xml_present	= bpy.props.EnumProperty	( 
							attr = 'xml_present', 
							name = 'xml Present', #????????
							description = 'family animation', 
							items = dynamic_items_xml_file 
							)

	type_anim	= bpy.props.EnumProperty	( 
							attr = 'type_anim', 
							name = lang['UI021'],
							items = [ ('rotate', 'rotate', 'rotate') ] + [ ('translate', 'translate', 'translate') ] + [ ('spin', 'spin', 'spin') ]
							)

	range_beg	= bpy.props.FloatProperty	( 
							attr = 'range_beg', 
							name = lang['UI022'], 
							description = lang['DOC049'], 
							update=update_range_beg
							)

	range_end	= bpy.props.FloatProperty	( 
							attr = 'range_end', 
							name = lang['UI023'], 
							description = lang['DOC050'], 
							update=update_range_end
							)

	range_beg_ini	= bpy.props.FloatProperty	( 
							attr = 'range_beg_ini', 
							name = lang['UI022'], 
							description = lang['DOC049']
							)

	range_end_ini	= bpy.props.FloatProperty	( 
							attr = 'range_end_ini', 
							name = lang['UI023'], 
							description = lang['DOC050']
							)

	time		= bpy.props.FloatProperty	( 
							attr = 'time', 
							name = lang['UI024'], 
							description = lang['DOC047'], 
							update=update_time
							)

	time_ini	= bpy.props.FloatProperty	( 
							attr = 'time_ini', 
							name = lang['UI024'], 
							description = lang['DOC047']
							)

	offset_deg	= bpy.props.FloatProperty	( 
							attr = 'offset_deg', 
							name = 'time', #??????????
							description = '?????????'
							)

	bIncDiskFile	= bpy.props.BoolProperty	( 
							attr = 'bIncDiskFile', 
							name = lang['UI025'], 
							description = '?????????', 
							update=update_bIncDiskFile
							)

	bWriteDisc	= bpy.props.BoolProperty	( 
							attr = 'bWriteDisc', 
							name = lang['UI026'], 
							description = lang['DOC046'], 
							update=update_bWriteDisc
							)

	keyframes	= bpy.props.CollectionProperty	( 
							attr = 'keyframes', 
							name = 'keyframes', #??????????
							description = '?????????', 
							type=FG_PROP_keyframe
							)
#----------------------------------------------------------------------------------------------------------------------------------

def RNA_armature():
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="family",			type=FG_PROP_armature, name="Family", 			description="Property family")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="family_value",		type=FG_PROP_armature, name="Family value", 		description="Family value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="property_value",		type=FG_PROP_armature, name="Property", 		description="Property value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="property_idx",		type=FG_PROP_armature, name="Property", 		description="Property value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="factor",			type=FG_PROP_armature, name="Factor", 			description="Property value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="factor_ini",		type=FG_PROP_armature, name="Factor ini", 		description="Property value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="xml_file",		type=FG_PROP_armature, name="xml file", 		description="Property value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="xml_file_no",		type=FG_PROP_armature, name="xml file no", 		description="Property value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='xml_present',		type=FG_PROP_armature, name='xml file present', 	description="family" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='type_anim',		type=FG_PROP_armature, name='type_anim', 		description="family" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='range_beg',		type=FG_PROP_armature, name='range_beg', 		description="family" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='range_end',		type=FG_PROP_armature, name='range_end', 		description="family" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='range_beg_ini',		type=FG_PROP_armature, name='range_beg_ini', 		description="family" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='range_end_ini',		type=FG_PROP_armature, name='range_end_ini', 		description="family" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='time',			type=FG_PROP_armature, name='time', 			description="family" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='time_ini',		type=FG_PROP_armature, name='time_ini', 		description="family" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='offset_deg',		type=FG_PROP_armature, name='offset_deg', 		description="Initial deg" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='bIncDiskFile',		type=FG_PROP_armature, name='bIncDiskFile', 		description="Include file Disk" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='bWriteDisc',		type=FG_PROP_armature, name='bWriteDisc', 		description="Write file to disk" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(  	attr='keyframes',		type=FG_PROP_armature )
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class( FG_PROP_keyframe )
	bpy.utils.register_class( FG_PROP_armature )
	RNA_armature()
#----------------------------------------------------------------------------------------------------------------------------------

def unregister():
	bpy.utils.unregister_class( FG_PROP_keyframe )
	bpy.utils.unregister_class( FG_PROP_armature )

#----------------------------------------------------------------------------------------------------------------------------------

