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
#									PROPS_ARMATURE.PY
#
#----------------------------------------------------------------------------------------------------------------------------------

import bpy
#----------------------------------------------------------------------------------------------------------------------------------

class fgAnimSettings(bpy.types.PropertyGroup):


   familly = bpy.props.EnumProperty(      attr='familly',
                                 name='familly',
                                 description="familly animation",
                                 default='none',
                                 items=[   ('none','none','none'),
                                       ('controls','controls','controls'),
                                       ('instrumentation','instrumentation','instrumentation'),
                                       ('flight_control','flight_control','flight_control'),
                                       ('engines','engines','engines'),
                                       ('fuel','fuel','fuel'),
                                       ('gear','gear','gear'),
                                       ('anti-ice','anti-ice','anti-ice'),
                                       ('electric','electric','electric'),
                                       ('pneumatic','pneumatic','pneumatic'),
                                       ('pressurization','pressurization','pressurization'),
                                       ('lights','lights','lights'),
                                       ('armament','armament','armament'),
                                       ('seat','seat','seat'),
                                       ('apu','apu','apu'),
                                       ('autoflight','autoflight','autoflight'),
                                       ('position','position','position'),
                                       ('orientation','orientation','orientation'),
                                       ('velocities','velocities','velocities'),
                                       ('acceleration','acceleration','acceleration')
                                       ]   )

   controls = bpy.props.EnumProperty(      attr='controls',
                                 name='controls',
                                 description="property control",
                                 default='aileron',
                                 items=[   
                                       ('aileron','aileron','aileron' ),
                                       ('aileron-trim','aileron-trim','aileron-trim' ),
                                       ('elevator','elevator','elevator' ),
                                       ('elevator-trim','elevator-trim','elevator-trim' )
                                    ]   )


   instrumentation = bpy.props.EnumProperty(      attr='instrumentation',
                                       name='instrumentation',
                                       description="property instrumentation",
                                       default='adf',
                                       items=[   
                                       ('adf','adf','adf' ),
                                       ('airspeed-indicator','airspeed-indicator','airspeed-indicator' ),
                                       ('altimeter','altimeter','altimeter' )
                                    ]   )
#----------------------------------------------------------------------------------------------------------------------------------

def addProjectRNA():
   # basic classes
   bpy.utils.register_class(fgAnimSettings)   

   bpy.types.Object.property = bpy.props.PointerProperty(   attr="familly",
                                             type=fgAnimSettings,
                                             name="familly",
                                             description="Property familly")
                                             
   bpy.types.Object.controls = bpy.props.PointerProperty(   attr="controls",
                                             type=fgAnimSettings,
                                             name="controls",
                                             description="Property controls")
                                             
   bpy.types.Object.instrumentation = bpy.props.PointerProperty(   attr="instrumentation",
                                             type=fgAnimSettings,
                                             name="instrumentation",
                                             description="Property instrumentation")
#----------------------------------------------------------------------------------------------------------------------------------

def removeProjectRNA():
    # complex classes, depending on basic classes
    bpy.utils.unregister_class(fgAnimSettings)
#----------------------------------------------------------------------------------------------------------------------------------
#
#
#
#				REGISTER
#
#
#----------------------------------------------------------------------------------------------------------------------------------
    
    
def register():
	addProjectRNA()

def unregister():
	removeProjectRNA()

