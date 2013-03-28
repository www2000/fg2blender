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
# Script copyright (C) Clément de l'Hamaide
# Contributors: 
#

#----------------------------------------------------------------------------------------------------------------------------------
#
#									UI_LANG.PY
#
#----------------------------------------------------------------------------------------------------------------------------------
import bpy

user_lang = bpy.context.user_preferences.system.language

lang = {}
lang_en = {}
lang_fr = {}

lang_en['ERR001'] = "It's a syntax error"
lang_fr['ERR001'] = "C'est une erreur de syntaxe"

lang_en['ERR002'] = "Unknow file"
lang_fr['ERR002'] = "Fichier inconnu"

lang_en['ERR003'] = "Armature information is missing !"
lang_fr['ERR003'] = "Informations manquantes pour l'armature"

lang_en['ERR004'] = "Keyframes are already saved !"
lang_fr['ERR004'] = "Les keyframes sont déjà sauvegardés"

lang_en['ERR005'] = "Armatures are already freezed !"
lang_fr['ERR005'] = "Les armatures sont déjà gelés"

lang_en['insert_keyframe_rotate'] = "Insert Keyframe Rotate"
lang_fr['insert_keyframe_rotate'] = "Insérer une keyframe Rotate"

lang_en['insert_keyframe_translate'] = "Insert Keyframe Translate"
lang_fr['insert_keyframe_translate'] = "Insérer une keyframe Translate"

lang_en['import_(.xml)'] = "Import (.xml)"
lang_fr['import_(.xml)'] = "Importer (.xml)"

lang_en['create_animations'] = "Create animations"
lang_fr['create_animations'] = "Créer les animations"



if user_lang == 'DEFAULT':
	lang = lang_en
elif user_lang == 'en_EN':
	lang = lang_en
elif user_lang == 'fr_FR':
	lang = lang_fr
else:
	lang = lang_en

