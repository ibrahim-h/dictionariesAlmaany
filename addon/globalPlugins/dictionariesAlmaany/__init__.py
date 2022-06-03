# -*- coding: utf-8 -*-
# Copyright (C) 2020 Ibrahim Hamadeh, released under GPLv2.0
# See the file COPYING for more details.
# This addon is aimed to get meaning of words using almaany.com website dictionaries.
# The default gesture of this addon is: nvda+windows+d.

import gui, wx
import api
import textInfos
import config
import globalPluginHandler
import globalVars
from gui import guiHelper
from scriptHandler import script
from .myDialog import MyDialog
from .myDialog import getListOfDictionaryNames, getUrlOfDictionary
from logHandler import log

import addonHandler
addonHandler.initTranslation()

#the function that specifies if a certain text is selected or not
#and if it is, returns text selected
def isSelectedText():
	obj=api.getFocusObject()
	treeInterceptor=obj.treeInterceptor
	if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
		obj=treeInterceptor
	try:
		info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
	#except (RuntimeError, NotImplementedError):
	except:
		info=None
	if not info or info.isCollapsed:
		return False
	else:
		return info.text

#default configuration 
configspec={
	"defaultDictionary": "integer(default=0)",
	"windowType": "integer(default=0)",
	"closeDialogAfterRequiringTranslation": "boolean(default= False)"
}
config.conf.spec["dictionariesAlmaany"]= configspec

# Ensure one instance is running.
INSTANCE= None

def disableInSecureMode(decoratedCls):
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decoratedCls

@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Translators: Category in input gestures dialog.
	scriptCategory= _('Dictionaries Almaany')

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)

		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(DictionariesAlmaany)

	def terminate(self):
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(DictionariesAlmaany)

	def showDictionariesAlmaanyDialog(self):
		global INSTANCE
		if not INSTANCE:
			d= MyDialog(gui.mainFrame)
#			log.info('after creating object')
			d.postInit()
			d.Raise()
			d.Show()
			INSTANCE= d
		else:
			INSTANCE.Raise()

	@script(
		# Translators: Message displayed in input help mode.
		description= _("Get the meaning of selected word by Dictionaries Almaany, and if no selection, Opens Dictionaries Almaany dialog to enter a word and get it's meaning ."),
		gesture= "kb:nvda+windows+d"
	)
	def script_dictionariesAlmaany(self, gesture):
		text= isSelectedText()
		if text and not text.isspace():
			text= text.strip()
			# We need to get the url of default dictionary.
			#indexOfDefault= config.conf["dictionariesAlmaany"]["defaultDictionary"]
			url= getUrlOfDictionary(default= True)
			MyDialog.getMeaning(text, url)
			return
		# Open Dictionaries Almaany dialog
		self.showDictionariesAlmaanyDialog()

#make  SettingsPanel  class
class DictionariesAlmaany(gui.SettingsPanel):
	# Translators: title of the dialog
	title= _("Dictionaries Almaany")

	def makeSettings(self, sizer):
		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=sizer)

		self.availableDictionariesComboBox= settingsSizerHelper.addLabeledControl(
		# Translators: label of cumbo box to choose default dictionary.
		_("Choose default dictionary:"), 
		wx.Choice, choices= getListOfDictionaryNames()
		)
		self.availableDictionariesComboBox.SetSelection(config.conf["dictionariesAlmaany"]["defaultDictionary"])

		windowTypes= [
		# Translators: Type of windows to display translation result.
		_("Default full browser"), 
		# Translators: Type of windows to display translation result.
		_("Browser window only"), 
		# Translators: Type of windows to display translation result.
		_("NVDA browseable message box(choose it after testing)")
		]
		self.resultWindowComboBox= settingsSizerHelper.addLabeledControl(
		# Translators: label of cumbo box to choose type of window to display result.
		_("Choose type of window To Display Result:"), 
		wx.Choice, choices= windowTypes)
		self.resultWindowComboBox.SetSelection(config.conf["dictionariesAlmaany"]["windowType"])

		# Translators: label of the check box 
		self.closeDialogCheckBox=wx.CheckBox(self,label=_("Close Dictionaries almaany Dialog after requesting translation"))
		self.closeDialogCheckBox.SetValue(config.conf["dictionariesAlmaany"]["closeDialogAfterRequiringTranslation"])
		settingsSizerHelper.addItem(self.closeDialogCheckBox)

	def onSave(self):
		config.conf["dictionariesAlmaany"]["defaultDictionary"]= self.availableDictionariesComboBox.GetSelection()
		config.conf["dictionariesAlmaany"]["windowType"]= self.resultWindowComboBox.GetSelection()
		config.conf["dictionariesAlmaany"]["closeDialogAfterRequiringTranslation"]= self.closeDialogCheckBox.IsChecked() 
