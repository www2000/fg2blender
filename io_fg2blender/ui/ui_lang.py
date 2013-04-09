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

lang_en['MEN006'] = 'Increase speed animation'
lang_fr['MEN006'] = 'Augmente la vitesse d\'animation'

lang_en['MEN007'] = 'Decrease speed animation'
lang_fr['MEN007'] = 'Diminue la vitesse d\'animation'

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

lang_en['MEN043'] = 'Convert to rotate'
lang_fr['MEN043'] = 'Convertir en rotation'

lang_en['MEN044'] = 'Convert to translate'
lang_fr['MEN044'] = 'Convertir en translation'

lang_en['MEN045'] = 'Convert to spin'
lang_fr['MEN045'] = 'Convertir en spin'

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

lang_en['MEN053'] = 'Freeze selected armature'
lang_fr['MEN053'] = 'Geler armature'

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

lang_en['UI001'] = 'Save AC3D file'
lang_fr['UI001'] = 'Sauvegarde le fichier AC3D'

lang_en['UI002'] = 'Save XML file'
lang_fr['UI002'] = 'Sauvegarde le fichier XML'

lang_en['UI003'] = 'Show objects related to selected object'
lang_fr['UI003'] = 'Afficher les objets liés à l\'objet séléctionné'

lang_en['UI004'] = 'Show all objects'
lang_fr['UI004'] = 'Afficher tous les objets'

lang_en['UI005'] = 'AC3D File'
lang_fr['UI005'] = 'Fichier AC3D'

lang_en['UI006'] = 'JSBSim File'
lang_fr['UI006'] = 'Fichier JSBSim'

lang_en['UI007'] = 'Camera File'
lang_fr['UI007'] = 'Fichier caméra'

lang_en['UI008'] = 'Property'
lang_fr['UI008'] = 'Propriété'

lang_en['UI009'] = 'Property:'
lang_fr['UI009'] = 'Propriété:'

lang_en['UI010'] = 'XML File'
lang_fr['UI010'] = 'Fichier XML'

lang_en['UI011'] = 'Show objects related to selected animation'
lang_fr['UI011'] = 'Afficher tous les objets liés à l\'animation séléctionné'

lang_en['UI012'] = 'Parent(s):'
lang_fr['UI012'] = 'Parent(s):'

lang_en['UI013'] = 'Child object(s):'
lang_fr['UI013'] = 'Objet(s) enfant:'

lang_en['UI014'] = 'Filename'
lang_fr['UI014'] = 'Fichier'

lang_en['UI015'] = 'Mesh Name'
lang_fr['UI015'] = 'Nom d\'objet'

lang_en['UI016'] = 'Attribute'
lang_fr['UI016'] = 'Attribue'

lang_en['UI017'] = 'Family'
lang_fr['UI017'] = 'Famille'

lang_en['UI018'] = 'Value'
lang_fr['UI018'] = 'Valeur'

lang_en['UI019'] = 'Index'
lang_fr['UI019'] = 'Index'

lang_en['UI020'] = 'Factor'
lang_fr['UI020'] = 'Facteur'

lang_en['UI021'] = 'Type'
lang_fr['UI021'] = 'Type'

lang_en['UI022'] = 'Min'
lang_fr['UI022'] = 'Min'

lang_en['UI023'] = 'Max'
lang_fr['UI023'] = 'Max'

lang_en['UI024'] = 'Duration'
lang_fr['UI024'] = 'Durée'

lang_en['UI025'] = 'Include disk file'
lang_fr['UI025'] = 'Inclure le fichier du disque'

lang_en['UI026'] = 'To disk'
lang_fr['UI026'] = 'Vers le disque'

lang_en['UI027'] = '??'
lang_fr['UI027'] = '??'

lang_en['UI028'] = '??'
lang_fr['UI028'] = '??'

lang_en['UI029'] = '??'
lang_fr['UI029'] = '??'

lang_en['UI030'] = '??'
lang_fr['UI030'] = '??'

#----------------------------------------------------------------------------------------------------------------------------------

lang_en['DOC001'] = 'Assign AC3D filename from active object to selected object(s)'
lang_fr['DOC001'] = 'Assigne le nom du fichier AC3D de l\'objet actif a(ux) objet(s) séléctionné(s)'

lang_en['DOC002'] = 'Select AC3D file destination'
lang_fr['DOC002'] = 'Sélection du fichier AC3D de destination'

lang_en['DOC003'] = 'Assign object name to Mesh Name for selected objects'
lang_fr['DOC003'] = 'Assigne les noms d\'objets dans Nom d\'objet pour le(s) objet(s) séléctionné(s)'

lang_en['DOC004'] = 'Save AC3D file (create it automatically if doesn\'t exist)'
lang_fr['DOC004'] = 'Sauvegarde le fichier AC3D (créer automatiquement si inexistant)'

lang_en['DOC005'] = 'Assign XML filename from active armature to selected armature(s)'
lang_fr['DOC005'] = 'Assigne le nom du fichier XML de l\'armature active pour le(s) armature(s) séléctionné(s)'

lang_en['DOC006'] = 'Select XML file destination'
lang_fr['DOC006'] = 'Sélection du fichier XML de destination'

lang_en['DOC007'] = 'Select JSBSim (XML) file destination'
lang_fr['DOC007'] = 'Sélection du fichier JSBSim (XML) de destination'

lang_en['DOC008'] = 'Save XML file (create it automatically if doesn\'t exist)'
lang_fr['DOC008'] = 'Sauvegarde le fichier XML (créer automatiquement si inexistant)'

lang_en['DOC009'] = 'Unwrap selected object for 4 faces'
lang_fr['DOC009'] = 'Dépliage de l\'objet séléctionné en 4 faces'

lang_en['DOC010'] = 'Apply edge split to selected object(s)'
lang_fr['DOC010'] = 'Applique un edge split a(ux) objet(s) séléctionné(s)'

lang_en['DOC011'] = 'Increase speed animation x2'
lang_fr['DOC011'] = 'Augmente la vitesse d\'animation x2'

lang_en['DOC012'] = 'Decrease speed animation x2'
lang_fr['DOC012'] = 'Diminue la vitesse d\'animation x2'

lang_en['DOC013'] = 'Create armature type "translate" on selected axis'
lang_fr['DOC013'] = 'Crée une armature de type "translate" pour l\'axe donné'

lang_en['DOC014'] = 'Create armature type "rotate" on selected axis'
lang_fr['DOC014'] = 'Crée une armature de type "rotate" pour l\'axe donné'

lang_en['DOC015'] = 'Create armature type "spin" on selected axis'
lang_fr['DOC015'] = 'Crée une armature de type "spin" pour l\'axe donné'

lang_en['DOC016'] = 'Compute XML animations loaded from the XML import, press Alt+a to run animations'
lang_fr['DOC016'] = 'Calcul les animations XML chargées depuis l\'import XML, pressez Alt+a pour démarrer les animations'

lang_en['DOC017'] = '?????????'
lang_fr['DOC017'] = '?????????'

lang_en['DOC018'] = '?????????'
lang_fr['DOC018'] = '?????????'

lang_en['DOC019'] = 'Convert selected armature(s) as armature type "rotate"'
lang_fr['DOC019'] = 'Converti la(es) armature(s) séléctionné(s) en armature de type "rotate"'

lang_en['DOC020'] = 'Convert selected armature(s) as armature type "translate"'
lang_fr['DOC020'] = 'Converti la(es) armature(s) séléctionné(s) en armature de type "translate"'

lang_en['DOC021'] = 'Convert selected armature(s) as armature type "spin"'
lang_fr['DOC021'] = 'Converti la(es) armature(s) séléctionné(s) en armature de type "spin"'

lang_en['DOC022'] = 'Freeze selected armature(s)'
lang_fr['DOC022'] = 'Geler la(es) armature(s) sélectionné(s)'

lang_en['DOC023'] = 'Unfreeze selected armature(s)'
lang_fr['DOC023'] = 'Dégeler la(es) armature(s) séléctionné(s)'

lang_en['DOC024'] = 'Select objects and armatures by file'
lang_fr['DOC024'] = 'Séléctionne les objets et armatures d\'un fichier'

lang_en['DOC025'] = '?????????'
lang_fr['DOC025'] = '?????????'

lang_en['DOC026'] = '?????????'
lang_fr['DOC026'] = '?????????'

lang_en['DOC027'] = '?????????'
lang_fr['DOC027'] = '?????????'

lang_en['DOC028'] = 'Assign FG property from active armature to selected armature(s)'
lang_fr['DOC028'] = 'Assigne la propriété FG de l\'armature active a(ux) armature(s) séléctionné(s)'

lang_en['DOC029'] = 'Select all objects and armatures with same property than active object/armature'
lang_fr['DOC029'] = 'Séléctionne tous les objets et armatures utilisant la même propriété que l\'objet/armature actif'

lang_en['DOC030'] = 'Show all objects with the same property than active object/armature and hide other'
lang_fr['DOC030'] = 'Affiche tous les objets utilisant la même propriété que l\'objet/l\'armature active et cache les autres'

lang_en['DOC031'] = 'Show all objects/armatures'
lang_fr['DOC031'] = 'Affiche tous les objets/armatures'

lang_en['DOC032'] = 'Insert keyframe type "rotate" with linear interpolation'
lang_fr['DOC032'] = 'Insère une keyframe de type "rotate" avec une interpolation linéaire'

lang_en['DOC033'] = 'Insert keyframe type "translate" with linear interpolation'
lang_fr['DOC033'] = 'Insère une keyframe de type "translate" avec une interpolation linéaire'

lang_en['DOC034'] = 'Select all armatures with same FG property'
lang_fr['DOC034'] = 'Séléctionne toutes les armatures utilisant la propriété FG'

lang_en['DOC035'] = 'Select all objects related to selected armature(s)'
lang_fr['DOC035'] = 'Séléctionne tous les objets relié a(ux) armature(s) séléctionné(s)'

lang_en['DOC036'] = 'Path of the AC3D file (.ac)'
lang_fr['DOC036'] = 'Chemin du fichier AC3D (.ac)'

lang_en['DOC037'] = 'Mesh name in the AC3D file'
lang_fr['DOC037'] = 'Nom de l\'objet dans le fichier AC3D'

lang_en['DOC038'] = 'Path of the JSBSim file (.xml)'
lang_fr['DOC038'] = 'Chemin du fichier JSBSim (.xml)'

lang_en['DOC039'] = 'JSBSim attribute'
lang_fr['DOC039'] = 'Attribue JSBSim'

lang_en['DOC040'] = 'Path of the Camera file (.xml)'
lang_fr['DOC040'] = 'Chemin du fichier Camera (.xml)'

lang_en['DOC041'] = 'Name of view'
lang_fr['DOC041'] = 'Nom de la vue'

lang_en['DOC043'] = 'Property family'
lang_fr['DOC043'] = 'Famille de propriété'

lang_en['DOC044'] = 'Family value'
lang_fr['DOC044'] = 'Valeur de la famille'

lang_en['DOC045'] = 'Value used for XML file'
lang_fr['DOC045'] = 'Valeur utiliser pour le fichier XML'

lang_en['DOC046'] = 'Write file to disk'
lang_fr['DOC046'] = 'Écrit le fichier sur le disque'

lang_en['DOC047'] = 'Duration of animation'
lang_fr['DOC047'] = 'Durée de l\'animation'

lang_en['DOC048'] = 'Index X of the property "/engines/engine[\'X\']/throttle"'
lang_fr['DOC048'] = 'Indice X de la propriété "/engines/engine[\'X\']/throttle"'

lang_en['DOC049'] = 'Minimum value of the property'
lang_fr['DOC049'] = 'Valeur minimum de la propriété'

lang_en['DOC050'] = 'Maximum value of the property'
lang_fr['DOC050'] = 'Valeur maximum de la propriété'

lang_en['DOC051'] = 'Value of <factor> tags'
lang_fr['DOC051'] = 'Valeur de la balise <factor>'

lang_en['DOC052'] = '??'
lang_fr['DOC052'] = '??'

lang_en['DOC053'] = '??'
lang_fr['DOC053'] = '??'

lang_en['DOC054'] = '??'
lang_fr['DOC054'] = '??'

lang_en['DOC055'] = '??'
lang_fr['DOC055'] = '??'

lang_en['DOC056'] = '??'
lang_fr['DOC056'] = '??'

lang_en['DOC057'] = '??'
lang_fr['DOC057'] = '??'

#----------------------------------------------------------------------------------------------------------------------------------

user_lang = bpy.context.user_preferences.system.language

if user_lang == 'DEFAULT':
	lang = lang_en
elif user_lang == 'en_EN':
	lang = lang_en
elif user_lang == 'fr_FR':
	lang = lang_fr
else:
	lang = lang_en

