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

lang = {}
lang_en = {}
lang_fr = {}

lang_en['ERR001'] = "It's a syntax error"
lang_fr['ERR001'] = "C'est une erreur de syntaxe"

lang_en['ERR002'] = 'Unknow file'
lang_fr['ERR002'] = 'Fichier inconnu'

lang_en['ERR003'] = 'Armature information is missing'
lang_fr['ERR003'] = "Informations manquantes pour l'armature"

lang_en['ERR004'] = 'Keyframes are already saved'
lang_fr['ERR004'] = 'Les keyframes sont déjà sauvegardés'

lang_en['ERR005'] = 'Armatures are already freezed'
lang_fr['ERR005'] = 'Les armatures sont déjà gelés'

lang_en['ERR006'] = "Can't found keyframes"
lang_fr['ERR006'] = 'Aucune keyframes trouvés'

#----------------------------------------------------------------------------------------------------------------------------------
lang_en['MENTIT'] = 'Flightgear Tools Menu'
lang_fr['MENTIT'] = 'Flightgear boîte à outils'

#----------------------------------------------------------------------------------------------------------------------------------
lang_en['MEN000'] = 'Insert Keyframe Rotate'
lang_fr['MEN000'] = 'Insérer une keyframe de rotation'

lang_en['MEN001'] = 'Insert Keyframe Translate'
lang_fr['MEN001'] = 'Insérer une keyframe de translation'

lang_en['MEN002'] = 'Import (.xml)'
lang_fr['MEN002'] = 'Importer (.xml)'

lang_en['MEN003'] = 'Create animations'
lang_fr['MEN003'] = 'Créer les animations'

lang_en['MEN004'] = 'Apply edge-split'
lang_fr['MEN004'] = 'Exécute edge-split'

lang_en['MEN005'] = 'Select objects by property'
lang_fr['MEN005'] = 'Séléctionne objets par propriété'

lang_en['MEN006'] = 'Time x2'
lang_fr['MEN006'] = 'Accélération par 2'

lang_en['MEN007'] = 'Time x0.5'
lang_fr['MEN007'] = 'Décéleration par 2'

lang_en['MEN008'] = 'Assign object name'
lang_fr['MEN008'] = 'Initialise le nom ac3d'

lang_en['MEN009'] = 'Copy AC3D filename'
lang_fr['MEN009'] = 'Recopie le nom de fichier AC3D'

lang_en['MEN010'] = 'Armatures'
lang_fr['MEN010'] = 'Armatures'

lang_en['MEN011'] = 'Unwrap'
lang_fr['MEN011'] = 'Dépliage UV'

#----------------------------------------------------------------------------------------------------------------------------------
lang_en['MEN020'] = 'Along X'
lang_fr['MEN020'] = 'Le long de X'

lang_en['MEN021'] = 'Along Y'
lang_fr['MEN021'] = 'Le long de Y'

lang_en['MEN022'] = 'Along Z' 
lang_fr['MEN022'] = 'Le long de Z'

#----------------------------------------------------------------------------------------------------------------------------------
lang_en['MEN040'] = 'Create rotate' 
lang_fr['MEN040'] = 'Créer rotation'

lang_en['MEN041'] = 'Create translate' 
lang_fr['MEN041'] = 'Créer translation'

lang_en['MEN042'] = 'Create spin' 
lang_fr['MEN042'] = 'Créer spin'

lang_en['MEN043'] = 'Transform to rotate'
lang_fr['MEN043'] = 'Type rotation'

lang_en['MEN044'] = 'Transform to translate'
lang_fr['MEN044'] = 'Type translation'

lang_en['MEN045'] = 'Transform to spin'
lang_fr['MEN045'] = 'Type spin'

lang_en['MEN046'] = 'Select related armatures'
lang_fr['MEN046'] = "Séléction relié à l'armature"

lang_en['MEN047'] = 'Select armature(s) by property'
lang_fr['MEN047'] = 'Séléctionne l(es) armature(s) par propriété'

lang_en['MEN048'] = 'Select object(s) by armature(s)'
lang_fr['MEN048'] = "Séléctionne le(s) objet(s) par armature(s)"

lang_en['MEN049'] = 'Copy xml file (active->selects)'
lang_fr['MEN049'] = 'Copie xml file (active->selects)'

lang_en['MEN050'] = 'Copy property (active->selects)'
lang_fr['MEN050'] = 'Copie propriété (active->selects)'

lang_en['MEN051'] = 'Reset Rotate'
lang_fr['MEN051'] = 'Reset'

lang_en['MEN052'] = 'Init Rotate'
lang_fr['MEN052'] = 'Initialise'

lang_en['MEN053'] = 'Freeze selected armatures'
lang_fr['MEN053'] = 'Geler armatures'

lang_en['MEN054'] = 'Save Keyframe and Reset'
lang_fr['MEN054'] = 'Sauver keyframe et reset'

lang_en['MEN055'] = 'Unfreeze'
lang_fr['MEN055'] = 'Dégeler'

lang_en['MEN056'] = 'Save Parent and Reset'
lang_fr['MEN056'] = 'Sauve parenté et reset'

lang_en['MEN057'] = 'Restore Parent '
lang_fr['MEN057'] = 'Restaurer parenté'

lang_en['MEN058'] = 'Select by file'
lang_fr['MEN058'] = 'Séléction par fichier'

#----------------------------------------------------------------------------------------------------------------------------------
lang_en['MEN070'] = 'Along X'
lang_fr['MEN070'] = 'Axe X'

lang_en['MEN071'] = 'Along Y'
lang_fr['MEN071'] = 'Axe Y'

lang_en['MEN072'] = 'Along Z'
lang_fr['MEN072'] = 'Axe Z'

lang_en['MEN073'] = 'Along -X'
lang_fr['MEN073'] = 'Axe -X'

lang_en['MEN074'] = 'Along -Y'
lang_fr['MEN074'] = 'Axe -Y'

lang_en['MEN075'] = 'Along -Z'
lang_fr['MEN075'] = 'Axe -Z'

lang_en['MEN076'] = 'Along  XY'
lang_fr['MEN076'] = 'Axe XY'

lang_en['MEN077'] = 'Along XZ'
lang_fr['MEN077'] = 'Axe XZ'

lang_en['MEN078'] = 'Along YZ'
lang_fr['MEN078'] = 'Axe YZ'

lang_en['MEN079'] = 'Along XYZ '
lang_fr['MEN079'] = 'Axe XYZ'

#----------------------------------------------------------------------------------------------------------------------------------
lang_en['DOC001'] = 'Assign AC3D filename from active object to selected object(s)'
lang_fr['DOC001'] = 'Assigne le nom du fichier AC3D de l\'objet actif a(ux) objet(s) séléctionné(s)'



user_lang = bpy.context.user_preferences.system.language

if user_lang == 'DEFAULT':
	lang = lang_en
elif user_lang == 'en_EN':
	lang = lang_en
elif user_lang == 'fr_FR':
	lang = lang_fr
else:
	lang = lang_en

