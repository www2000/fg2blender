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




 
familles = ['APU','anti_ice','armament','autoflight','electric' , 'engine','flight','fuel','gear', 'consumable']
 
 
 
#Tuples ('Property',min,max,time)
#               min max :       'x' : valeur variable
#               time :          True/False : cinématique ou non
 
 
APUs = [                 ('/controls/APU/off-start-run',0,1,False),
                                ('/controls/APU/fire-switch',0,'x',False)						]
 
anti_ices = [    ('/controls/anti-ice/wing-heat',0,1,False),
                                ('/controls/anti-ice/pitot-heat',0,1,False),
                                ('/controls/anti-ice/wiper',0,'x',False),
                                ('/controls/anti-ice/window-heat',0,1,False),
                                ('/controls/anti-ice/engine[%d]/carb-heat',0,1,False),
                                ('/controls/anti-ice/engine[%d]/inlet-heat',0,1,False)			]
 
armaments = [    ('/controls/armament/master-arm',0,1,False),
                                ('/controls/armament/station-select',0,1,False),
                                ('/controls/armament/release-all',0,1,False),
                                ('/controls/armament/station[%d]/stick-size',0,1,False),
                                ('/controls/armament/station[%d]/release-stick',0,1,False),
                                ('/controls/armament/station[%d]/release-all',0,1,False),
                                ('/controls/armament/station[%d]/jettison-all',0,1,False)		]
 
autoflights = [  ('/controls/autoflight/autopilot[%d]/engage',0,1,False),
                                ('/controls/autoflight/autothrottle-arm',0,1,False),
                                ('/controls/autoflight/autothrottle-engage',0,1,False),
                                ('/controls/autoflight/heading-select',0,360,False),
                                ('/controls/autoflight/altitude-select',0,'x',False),
                                ('/controls/autoflight/bank-angle-select',0,'x',False),
                                ('/controls/autoflight/vertical-speed-select',0,'x',False),
                                ('/controls/autoflight/speed-select',0,'x',False),
                                ('/controls/autoflight/mach-select',0,'x',False),
                                ('/controls/autoflight/vertical-mode',0,'x',False),
                                ('/controls/autoflight/lateral-mode',0,1,False)					]
                               
electrics = [    ('/controls/electric/battery-switch',0,1,False),
                                ('/controls/electric/external-power',0,1,False),
                                ('/controls/electric/APU-generator',0,1,False),
                                ('/controls/electric/engine[%d]/generator',0,1,False),
                                ('/controls/electric/engine[%d]/bus-tie',0,1,False)				]
 
                               
#engines comportement des variables à affiner
engines = [             ('/controls/engines/throttle_idle',0,1,False),
                                ('/controls/engines/engine[%d]/throttle',0,1,False),
                                ('/controls/engines/engine[%d]/starter',0,1,False),
                                ('/controls/engines/engine[%d]/fuel-pump',0,1,False),
                                ('/controls/engines/engine[%d]/fire-switch',0,1,False),
                                ('/controls/engines/engine[%d]/fire-bottle-discharge',0,1,False),
                                ('/controls/engines/engine[%d]/cutoff',0,1,False),
                                ('/controls/engines/engine[%d]/mixture',0,1,False),
                                ('/controls/engines/engine[%d]/propeller-pitch',0,1,False),
                                ('/controls/engines/engine[%d]/magnetos',0,3,False),
                                ('/controls/engines/engine[%d]/boost',0,1,False),
                                ('/controls/engines/engine[%d]/WEP',0,1,False),
                                ('/controls/engines/engine[%d]/cowl-flaps-norm',0,1,False),
                                ('/controls/engines/engine[%d]/feather',0,1,False),
                                ('/controls/engines/engine[%d]/ignition',0,3,False),
                                ('/controls/engines/engine[%d]/augmentation',0,1,False),
                                ('/controls/engines/engine[%d]/afterburner',0,1,False),
                                ('/controls/engines/engine[%d]/reverser',0,1,False),
                                ('/controls/engines/engine[%d]/water-injection',0,1,False),
                                ('/controls/engines/engine[%d]/condition',0,1,False)			]
 
flights = [              ('/controls/flight/aileron',-1,1,False),
                                ('/controls/flight/aileron-trim',-1,1,False),
                                ('/controls/flight/elevator',-1,1,False),
                                ('/controls/flight/elevator-trim',-1,1,False),
                                ('/controls/flight/rudder',-1,1,False),
                                ('/controls/flight/rudder-trim',-1,1,False),
                                ('/controls/flight/flaps',0,1,False),
                                ('/controls/flight/slats',0,1,False),
                                ('/controls/flight/BLC',0,1,False),
                                ('/controls/flight/spoilers',0,1,False),
                                ('/controls/flight/speedbrake',0,1,False),
                                ('/controls/flight/wing-sweep',0,1,False),
                                ('/controls/flight/wing-fold',0,1,False),
                                ('/controls/flight/drag-chute',0,1,False)						]
 
fuels = [                ('/controls/fuel/dump-valve',0,1,False),
                                ('/controls/fuel/tank[%d]/fuel_selector',0,1,False),
                                ('/controls/fuel/tank[%d]/to_engine',0,'x',False),
                                ('/controls/fuel/tank[%d]/to_tank',0,'x',False),
                                ('/controls/fuel/tank[%d]/boost-pump[%d]',0,1,False)			]
 
consumables = [ ('/consumables/fuel/tank[%d]/level-lbs',0,'x',False),
                                ('/consumables/fuel/tank[%d]/level-gal_us',0,'x',False),
                                ('/consumables/fuel/tank[%d]/capacity-gal_us',0,'x',False),
                                ('/consumables/fuel/tank[%d]/density-ppg',0,'x',False),
                                ('/consumables/fuel/total-fuel-lbs',0,'x',False),
                                ('/consumables/fuel/total-gal_us',0,'x',False)                  ]
                               
gears = [                ('/controls/gear/brake-left',0,1,False),
                                ('/controls/gear/brake-right',0,1,False),
                                ('/controls/gear/brake-parking',0,1,False),
                                ('/controls/gear/steering',0,'x',False),
                                ('/controls/gear/gear-down',0,1,True),
                                ('/controls/gear/antiskid',0,1,False),
                                ('/controls/gear/tailhook',0,1,False),
                                ('/controls/gear/tailwheel-lock',0,1,False),
                                ('/controls/gear/wheel[%d]/alternate-extension',0,1,False),
                                ('/gear/gear[%d]/caster-angle-deg',0,1,False),
                                ('/gear/gear[%d]/compression-m',0,1,False),
                                ('/gear/gear[%d]/compression-norm',0,1,False),
                                ('/gear/gear[%d]/ground-friction-factor',0,1,False),
                                ('/gear/gear[%d]/ground-is-solid',0,1,False),
                                ('/gear/gear[%d]/has-brake',0,1,False),
                                ('/gear/gear[%d]/position-norm',0,1,True),
                                ('/gear/gear[%d]/rollspeed-ms',0,'x',False),
                                ('/gear/gear[%d]/rollspeed-ms',0,1,False)						]
 
 

'''

familles = ['controls','engines','fuel','gear']

controls = [	'/controls/flight/aileron',
				'/controls/flight/aileron-trim',
				'/controls/flight/elevator',
				'/controls/flight/elevator-trim',
				'/controls/flight/rudder',
				'/controls/flight/rudder-trim',
				'/controls/flight/flaps',
				'/controls/flight/slats',
				'/controls/flight/BLC',
				'/controls/flight/spoilers',
				'/controls/flight/speedbrake',
				'/controls/flight/wing-sweep',
				'/controls/flight/wing-fold',
				'/controls/flight/drag-chute'		]
         
engines = [		'/controls/engines/throttle_idle',
				'/controls/engines/engine[%d]/throttle',
				'/controls/engines/engine[%d]/starter',
				'/controls/engines/engine[%d]/fuel-pump',
				'/controls/engines/engine[%d]/fire-switch',
				'/controls/engines/engine[%d]/fire-bottle-discharge',
				'/controls/engines/engine[%d]/cutoff',
				'/controls/engines/engine[%d]/mixture',
				'/controls/engines/engine[%d]/propeller-pitch',
				'/controls/engines/engine[%d]/magnetos',
				'/controls/engines/engine[%d]/boost',
				'/controls/engines/engine[%d]/WEP',
				'/controls/engines/engine[%d]/cowl-flaps-norm',
				'/controls/engines/engine[%d]/feather',
				'/controls/engines/engine[%d]/ignition',
				'/controls/engines/engine[%d]/augmentation',
				'/controls/engines/engine[%d]/afterburner',
				'/controls/engines/engine[%d]/reverser',
				'/controls/engines/engine[%d]/water-injection',
				'/controls/engines/engine[%d]/condition'		]

flight_controls = [		'/controls/flight/aileron',
						'/controls/flight/aileron-trim',
						'/controls/flight/elevator',
						'/controls/flight/elevator-trim',
						'/controls/flight/rudder',
						'/controls/flight/rudder-trim',
						'/controls/flight/flaps',
						'/controls/flight/slats',
						'/controls/flight/BLC',
						'/controls/flight/spoilers',
						'/controls/flight/speedbrake',
						'/controls/flight/wing-sweep',
						'/controls/flight/wing-fold',
						'/controls/flight/drag-chute'	]

fuels = [	'/controls/fuel/dump-valve',
			'/controls/fuel/tank[%d]/fuel_selector',
			'/controls/fuel/tank[%d]/to_engine',
			'/controls/fuel/tank[%d]/to_tank',
			'/controls/fuel/tank[%d]/boost-pump[%d]',
			'/consumables/fuel/tank[%d]/level-lbs',
			'/consumables/fuel/tank[%d]/level-gal_us',
			'/consumables/fuel/tank[%d]/capacity-gal_us',
			'/consumables/fuel/tank[%d]/density-ppg',
			'/consumables/fuel/total-fuel-lbs',
			'/consumables/fuel/total-gal_us'	]
            
gears = [	'/controls/gear/brake-left',
			'/controls/gear/brake-right',
			'/controls/gear/brake-parking',
			'/controls/gear/steering',
			'/controls/gear/gear-down',
			'/controls/gear/antiskid',
			'/controls/gear/tailhook',
			'/controls/gear/tailwheel-lock',
			'/controls/gear/wheel[%d]/alternate-extension'		]


'''



import bpy
from . import *


#----------------------------------------------------------------------------------------------------------------------------------

def update_keyframe( obj, coef ):
	#from mathutils import Euler
	
	if obj.animation_data:
		for fcurve in obj.animation_data.action.fcurves:
			for keyframe in fcurve.keyframe_points:
				#keyframe.interpolation = 'LINEAR'
				keyframe.co.y = keyframe.co.y * coef
				#print( keyframe.co )
#----------------------------------------------------------------------------------------------------------------------------------

def update_keyframe_time( obj, coef ):
	#from mathutils import Euler
	
	if obj.animation_data:
		for fcurve in obj.animation_data.action.fcurves:
			for keyframe in fcurve.keyframe_points:
				#keyframe.interpolation = 'LINEAR'
				keyframe.co.x = ((keyframe.co.x-1) * coef ) +1
				#print( keyframe.co )
#----------------------------------------------------------------------------------------------------------------------------------

def update_factor( self, context ):
	obj = context.active_object
	if obj:
		#if obj.type == 'ARMATURE':
		if obj.data.fg.type_anim in [ 1,2]:
			if obj.data.fg.factor_ini == 0.0:
				obj.data.fg.factor_ini = obj.data.fg.factor
			coef = obj.data.fg.factor  / obj.data.fg.factor_ini
			update_keyframe( obj, coef )
			obj.data.fg.factor_ini = obj.data.fg.factor
#----------------------------------------------------------------------------------------------------------------------------------

def update_time( self, context ):
	obj = context.active_object
	if obj:
		#if obj.type == 'ARMATURE':
		if obj.data.fg.type_anim in [ 1,2]:
			coef = 0.0
			if obj.data.fg.time_ini == 0.0:
				obj.data.fg.time_ini = obj.data.fg.time
			coef = 0.0 + obj.data.fg.time  / obj.data.fg.time_ini
			update_keyframe_time( obj, coef )
			obj.data.fg.time_ini = 0.0 +  obj.data.fg.time
#----------------------------------------------------------------------------------------------------------------------------------

def dynamic_items( self, context ):
	obj = context.active_object

	#familles = ['APU','anti_ice','armament','autoflight','electric' , 'engine','flight','fuel','gear']

	if obj.data.fg.familly == 'APU':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for (fc, _min, _max, b )in APUs ]
	elif obj.data.fg.familly == 'anti_ice':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for fc, _min, _max, b in anti_ices ]
	elif obj.data.fg.familly == 'armament':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for fc, _min, _max, b in armaments ]
	elif obj.data.fg.familly == 'autoflight':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for fc, _min, _max, b in autoflights ]
	elif obj.data.fg.familly == 'electric':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for fc, _min, _max, b in electrics ]
	elif obj.data.fg.familly == 'controls':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for fc, _min, _max, b in flight_controls ]
	elif obj.data.fg.familly == 'engine':
	    items = [ (en,en.split('/')[-1],en.split('/')[-1]) for en, _min, _max, b in engines ]
	elif obj.data.fg.familly == 'flight':
	    items =	[ (fu,fu.split('/')[-1],fu.split('/')[-1]) for fu, _min, _max, b in flights ]
	elif obj.data.fg.familly == 'fuel':
	    items =	[ (fu,fu.split('/')[-1],fu.split('/')[-1]) for fu, _min, _max, b in fuels ]
	elif obj.data.fg.familly == 'gear':
	    items = [ (ge,ge.split('/')[-1],ge.split('/')[-1]) for ge, _min, _max, b in gears ]
	elif obj.data.fg.familly == 'consumable':
	    items = [ (ge,ge.split('/')[-1],ge.split('/')[-1]) for ge, _min, _max, b in consumables ]
	else:
		items = [  ('error','error','error') ]
	return items
#----------------------------------------------------------------------------------------------------------------------------------

def dynamic_items_xml_file( self, context ):
	#items = [ (xf.name,xf.name.split('/')[-1],xf.name.split('/')[-1]) for xf,no in xml_manager.xml_files ]
	items = [ ("","","") ] + [ (xf.name,xf.name,xf.name) for xf,no in xml_manager.xml_files ]
	return items
#----------------------------------------------------------------------------------------------------------------------------------

class FG_PROP_armature(bpy.types.PropertyGroup):
	familly			= bpy.props.EnumProperty(	attr='familly', name='Familly', description="familly of properties", default='custom',
						                        items = [ ('custom','custom','custom') ]
						                        	+	[ (famille,famille,famille) for famille in familles ]    )

	familly_value	= bpy.props.EnumProperty(	attr = 'familly_value', name='Node', description="node of familly", items = dynamic_items )
	property_value	= bpy.props.StringProperty(	attr = 'value', name = 'Property')
	property_idx	= bpy.props.IntProperty(	attr = 'value', name = '%d ', min=0)
	factor			= bpy.props.FloatProperty(	attr = 'factor', name = 'Factor', update=update_factor)
	factor_ini		= bpy.props.FloatProperty(	attr = 'factor_ini', name = 'Factor ini')
	xml_file		= bpy.props.StringProperty(	attr = 'xml_file', name = 'xml File')
	xml_file_no		= bpy.props.IntProperty(	attr = 'xml_file_no', name = 'No xml File')
	xml_present		= bpy.props.EnumProperty(	attr = 'xml_present', name='xml Present', description="familly animation", items = dynamic_items_xml_file )
	type_anim		= bpy.props.IntProperty(	attr = 'type_anim', name = 'Type')
	range_beg		= bpy.props.FloatProperty(	attr = 'range_beg', name = 'min')
	range_end		= bpy.props.FloatProperty(	attr = 'range_end', name = 'max')
	range_beg_ini	= bpy.props.FloatProperty(	attr = 'range_beg_ini', name = 'min')
	range_end_ini	= bpy.props.FloatProperty(	attr = 'range_end_ini', name = 'max')
	time			= bpy.props.FloatProperty(	attr = 'time', name = 'time', update=update_time)
	time_ini		= bpy.props.FloatProperty(	attr = 'time_ini', name = 'time')
	offset_deg		= bpy.props.FloatProperty(	attr = 'offset_deg', name = 'time')
#----------------------------------------------------------------------------------------------------------------------------------

def RNA_armature():
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="familly",			type=FG_PROP_armature, name="Familly", description="Property familly")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="familly_value",	type=FG_PROP_armature, name="Familly value", description="Familly value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="property_value",	type=FG_PROP_armature, name="Property", description="Property value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="property_idx",	type=FG_PROP_armature, name="Property", description="Property value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="factor",			type=FG_PROP_armature, name="Factor", description="Property value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="factor_ini",		type=FG_PROP_armature, name="Factor ini", description="Property value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="xml_file",		type=FG_PROP_armature, name="xml file", description="Property value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="xml_file_no",		type=FG_PROP_armature, name="xml file no", description="Property value")
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='xml_present',		type=FG_PROP_armature, name='xml file present', description="familly" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='type_anim',		type=FG_PROP_armature, name='type_anim', description="familly" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='range_beg',		type=FG_PROP_armature, name='range_beg', description="familly" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='range_end',		type=FG_PROP_armature, name='range_end', description="familly" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='range_beg_ini',	type=FG_PROP_armature, name='range_beg_ini', description="familly" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='range_end_ini',	type=FG_PROP_armature, name='range_end_ini', description="familly" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='time',			type=FG_PROP_armature, name='time', description="familly" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='time_ini',		type=FG_PROP_armature, name='time_ini', description="familly" )
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='offset_deg',		type=FG_PROP_armature, name='offset_deg', description="Initial deg" )
#----------------------------------------------------------------------------------------------------------------------------------

class FG_PROP_mesh(bpy.types.PropertyGroup):
	ac_file = bpy.props.StringProperty(	attr = 'ac_file', name = 'ac File')
	name_ac = bpy.props.StringProperty(	attr = 'name_ac', name = 'ac name')
#----------------------------------------------------------------------------------------------------------------------------------

def RNA_mesh():
	bpy.types.Mesh.fg = bpy.props.PointerProperty(	attr="ac_file", type=FG_PROP_mesh, name="ac_file", description="File .ac")
	bpy.types.Mesh.fg = bpy.props.PointerProperty(	attr="name_ac", type=FG_PROP_mesh, name="name_ac", description="name in ac file")
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------

#def removeProjectRNA():
	# complex classes, depending on basic classes
#----------------------------------------------------------------------------------------------------------------------------------

def register():
	bpy.utils.register_class( FG_PROP_armature )
	bpy.utils.register_class( FG_PROP_mesh )
	RNA_armature()
	RNA_mesh()

def unregister():
	bpy.utils.unregister_class( FG_PROP_armature )
	bpy.utils.unregister_class( FG_PROP_mesh )
	#removeProjectRNA()
#----------------------------------------------------------------------------------------------------------------------------------

