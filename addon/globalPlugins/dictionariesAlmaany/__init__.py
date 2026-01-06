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
import core
from gui import guiHelper
from scriptHandler import script
from gui.message import isModalMessageBoxActive
from .myDialog import MyDialog, setOnCloseCallback
from .myDialog import getListOfDictionaryNames, getUrlOfDictionary
from .update import Initialize
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
	except (RuntimeError, NotImplementedError):
		info=None
	if not info or info.isCollapsed:
		return False
	else:
		return info.text

#default configuration 
configspec={
	"defaultDictionary": "integer(default=0)",
	# 0=NVDA message box (recommended), 1=Default browser, 2=Browser window only
	"windowType": "integer(default=0)",
	"closeDialogAfterRequiringTranslation": "boolean(default= False)",
	"autoUpdate": "boolean(default= True)"
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
		# To allow check for update after NVDA started.
		core.postNvdaStartup.register(self.checkForUpdate)

	def checkForUpdate(self):
		if not config.conf["dictionariesAlmaany"]["autoUpdate"]:
			# Auto update is False
			return
		# Do not check for update in these conditions.
		if globalVars.appArgs.secure or globalVars.appArgs.launcher or isModalMessageBoxActive():
			return
		# starting the update process
		def checkWithDelay():
			_beginChecking = Initialize()
			_beginChecking.start()
		wx.CallLater(9000, checkWithDelay)

	def terminate(self):
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(DictionariesAlmaany)
		core.postNvdaStartup.unregister(self.checkForUpdate)
		global INSTANCE
		if INSTANCE:
			try:
				INSTANCE.Destroy()
			except Exception:
				pass
			INSTANCE = None

	def _onDialogClose(self):
		"""Callback when dialog is closed."""
		global INSTANCE
		INSTANCE = None

	def showDictionariesAlmaanyDialog(self):
		global INSTANCE
		if not INSTANCE:
			setOnCloseCallback(self._onDialogClose)
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
class DictionariesAlmaany(gui.settingsDialogs.SettingsPanel):
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
		_("NVDA browseable message (Recommended)"), 
		# Translators: Type of windows to display translation result.
		_("Default full browser"), 
		# Translators: Type of windows to display translation result.
		_("Browser window only")
		]
		self.resultWindowComboBox= settingsSizerHelper.addLabeledControl(
		# Translators: label of cumbo box to choose type of window to display result.
		_("Choose type of window To Display Result:"), 
		wx.Choice, choices= windowTypes)
		self.resultWindowComboBox.SetSelection(config.conf["dictionariesAlmaany"]["windowType"])

		# Translators: label of the check box 
		self.closeDialogCheckBox=wx.CheckBox(self,label=_("Close Dictionaries almaany Dialog after requesting translation"))
		settingsSizerHelper.addItem(self.closeDialogCheckBox)
		self.closeDialogCheckBox.SetValue(config.conf["dictionariesAlmaany"]["closeDialogAfterRequiringTranslation"])

		# Translators: label of the check box 
		self.updateCheckBox=wx.CheckBox(self,label=_("Check for update on startup"))
		settingsSizerHelper.addItem(self.updateCheckBox)
		self.updateCheckBox.SetValue(config.conf["dictionariesAlmaany"]["autoUpdate"])

	def onSave(self):
		config.conf["dictionariesAlmaany"]["defaultDictionary"]= self.availableDictionariesComboBox.GetSelection()
		config.conf["dictionariesAlmaany"]["windowType"]= self.resultWindowComboBox.GetSelection()
		config.conf["dictionariesAlmaany"]["closeDialogAfterRequiringTranslation"]= self.closeDialogCheckBox.IsChecked() 
		config.conf["dictionariesAlmaany"]["autoUpdate"]= self.updateCheckBox.IsChecked() 
