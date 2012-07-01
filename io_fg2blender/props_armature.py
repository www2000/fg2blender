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
# Contributors: Alexis
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									PROPS_ARMATURE.PY
#
#----------------------------------------------------------------------------------------------------------------------------------







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






import bpy
from . import *



#----------------------------------------------------------------------------------------------------------------------------------

def dynamic_items( self, context ):
	obj = context.active_object

	if obj.data.fg.familly == 'controls':
		items = [ (fc,fc.split('/')[-1],fc.split('/')[-1]) for fc in flight_controls ]
	elif obj.data.fg.familly == 'engines':
	    items = [ (en,en.split('/')[-1],en.split('/')[-1]) for en in engines ]
	elif obj.data.fg.familly == 'fuel':
	    items =	[ (fu,fu.split('/')[-1],fu.split('/')[-1]) for fu in fuels ]
	elif obj.data.fg.familly == 'gear':
	    items = [ (ge,ge.split('/')[-1],ge.split('/')[-1]) for ge in gears ]
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
	familly = bpy.props.EnumProperty(	attr='familly',
				                        name='Familly',
				                        description="familly animation",
				                        default='custom',
				                        items = [ ('custom','custom','custom') ]
				                        	+	[ (famille,famille,famille) for famille in familles ]    )

	familly_value = bpy.props.EnumProperty(	attr='familly_value',
											name='Value',
											description="property flight_control",
											items = dynamic_items
									)


	property_value = bpy.props.StringProperty(	attr = 'value', name = 'value')

	factor = bpy.props.FloatProperty(	attr = 'factor', name = 'Factor')

	xml_file = bpy.props.StringProperty(	attr = 'xml_file', name = 'xml File')

	xml_present = bpy.props.EnumProperty(	attr='xml_present',
										    name='xml Present',
										    description="familly animation",
										    items = dynamic_items_xml_file )

	type_anim = bpy.props.IntProperty(	attr = 'type_anim', name = 'Type')
#----------------------------------------------------------------------------------------------------------------------------------

def RNA_armature():
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="familly",
														type=FG_PROP_armature,
														name="Familly",
														description="Property familly")

	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="familly_value",
														type=FG_PROP_armature,
														name="Familly value",
														description="Familly value")
                                             
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="property_value",
														type=FG_PROP_armature,
														name="Property",
														description="Property value")

	bpy.types.Armature.fg =  bpy.props.PointerProperty(	attr="factor",
														type=FG_PROP_armature,
														name="Factor",
														description="Property value")
	
	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr="xml_file",
														type=FG_PROP_armature,
														name="xml file",
														description="Property value")

	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='xml_present',
														type=FG_PROP_armature,
													    name='xml file present',
													    description="familly" )

	bpy.types.Armature.fg = bpy.props.PointerProperty(	attr='type_anim',
														type=FG_PROP_armature,
													    name='type_anim',
													    description="familly" )
#----------------------------------------------------------------------------------------------------------------------------------

class FG_PROP_object(bpy.types.PropertyGroup):
	ac_file = bpy.props.StringProperty(	attr = 'ac_file', name = 'ac File')
#----------------------------------------------------------------------------------------------------------------------------------

def RNA_object():
	bpy.types.Object.fg = bpy.props.PointerProperty(	attr="ac_file",
														type=FG_PROP_object,
														name="ac_file",
														description="File .ac")










def removeProjectRNA():
	# complex classes, depending on basic classes
	bpy.utils.unregister_class( FG_PROP_armature )
	bpy.utils.unregister_class( FG_PROP_object )
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------
    
    
def register():
	bpy.utils.register_class( FG_PROP_armature )
	bpy.utils.register_class( FG_PROP_object )
	RNA_armature()
	RNA_object()

def unregister():
	removeProjectRNA()

