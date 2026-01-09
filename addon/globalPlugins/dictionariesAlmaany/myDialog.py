# -*- coding: utf-8 -*-
# Copyright (C) Ibrahim Hamadeh, released under GPLv2.0
# See the file COPYING for more details.
# This module is responsible for displaying dictionaries almaany dialog

import wx
import queueHandler
import config
import webbrowser
from .fetchtext import MyThread
from .getbrowsers import getBrowsers
from tones import beep
import time
import subprocess
import threading
import tempfile
import ui
import os

import addonHandler
addonHandler.initTranslation()

#browsers as dictionary with label as key, and executable path as value.
browsers= getBrowsers()

def appIsRunning(app):
	'''Checks if specific app is running or not.'''
	processes= subprocess.check_output('tasklist', shell=True).decode('mbcs')
	return app in processes

def openBrowserWindow(label, meaning, directive, default= False):
	html= """
	<!DOCTYPE html>
	<meta charset=utf-8>
	<title>{title}</title>
	<meta name=viewport content='initial-scale=1.0'>
	""".format(title= _('Dictionaries Almaany')) + meaning 
	temp= tempfile.NamedTemporaryFile(delete=False)
	path = temp.name + ".html"
	f = open(path, "w", encoding="utf-8")
	f.write(html)
	f.close()
	if default:
		webbrowser.open(path)
	else:
		subprocess.Popen(browsers[label] + directive + path)
	t=threading.Timer(30.0, os.remove, [f.name])
	t.start()

#dictionaries name and url
dictionaries_nameAndUrl= [
	(u'قاموس عربي إنجليزي, إنجليزي عربي', 'http://www.almaany.com/ar/dict/ar-en/'),
	(u'معجم عربي عربي', 'http://www.almaany.com/ar/dict/ar-ar/'),
	(u'قاموس عربي فرنسي, فرنسي عربي', 'http://www.almaany.com/ar/dict/ar-fr/'),
	(u'قاموس إنجليزي إنجليزي', 'https://www.almaany.com/en/dict/en-en/'),
	(u'قاموس عربي ⇔ إسباني', 'http://www.almaany.com/ar/dict/ar-es/'),
	(u'قاموس عربي ⇔ تركي', 'http://www.almaany.com/ar/dict/ar-tr/'),
	(u'قاموس عربي ⇐ فارسي', 'http://www.almaany.com/ar/dict/ar-fa/'),
	(u'قاموس عربي ⇔ ألماني', 'https://www.almaany.com/ar/dict/ar-de/'),
	(u'قاموس عربي ⇔ روسي', 'https://www.almaany.com/ar/dict/ar-ru/'),
	(u'قاموس عربي ⇔ برتغالي', 'https://www.almaany.com/ar/dict/ar-pt/'),
	(u'قاموس عربي ⇔ اندونيسي', 'https://www.almaany.com/ar/dict/ar-id/'),
	(u'قاموس عربي ⇐ اردو', 'https://www.almaany.com/ar/dict/ar-ur/'),
	(u'مَعاني الأسماء', 'https://www.almaany.com/ar/name/')
]

def getListOfDictionaryNames():
	return [name for name, url in dictionaries_nameAndUrl]

def getUrlOfDictionary(i=0, default= False):
	''' Getting the url of a specific dictionary from its index
	 i is the index of dictionary(selected in dialog).
	 if default= True, then we want the index of default dictionary.
	'''
	if default:
		# Index of default dictionary
		i= config.conf["dictionariesAlmaany"]["defaultDictionary"]
	# The url is the second item in the tuple.
	dict_url= dictionaries_nameAndUrl[i][1]
	return dict_url

class MyDialog(wx.Dialog):
	''' Dictionaries Almaany dialog, contains an edit field to enter a word, and a combo box to choose dictionary.
	It pops up only if no selection found.
	'''

	def __init__(self, parent):
		# Translators: Title of dialog.
		title= _("Dictionaries Almaany")
		super(MyDialog, self).__init__(parent, title = title, size = (300, 500))
		#self.word= word
		#list of available dictionaries
		#self.dictionaries= [name for name, url in dictionaries_nameAndUrl]

		panel = wx.Panel(self, -1)
		editTextLabel= wx.StaticText(panel, -1, _("Enter a word please"))
		editBoxSizer =  wx.BoxSizer(wx.HORIZONTAL)
		editBoxSizer.Add(editTextLabel, 0, wx.ALL, 5)
		self.editTextControl= wx.TextCtrl(panel)
		editBoxSizer.Add(self.editTextControl, 1, wx.ALL|wx.EXPAND, 5)

		cumboSizer= wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Label of cumbo box to choose a dictionary.
		cumboLabel= wx.StaticText(panel, -1, _("Choose Dictionary"))
		cumboSizer.Add(cumboLabel, 0, wx.ALL, 5)
		self.cumbo= wx.Choice(panel, -1, choices= getListOfDictionaryNames())
		cumboSizer.Add(self.cumbo, 1, wx.EXPAND|wx.ALL, 5)

		buttonSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: Label of OK button.
		self.ok= wx.Button(panel, -1, _('OK'))
		self.ok.SetDefault()
		self.ok.Bind(wx.EVT_BUTTON, self.onOk)
		buttonSizer.Add(self.ok, 0,wx.ALL, 10)
		# Translators: Label of Cancel button.
		self.cancel = wx.Button(panel, wx.ID_CANCEL, _('cancel'))
		self.cancel.Bind(wx.EVT_BUTTON, self.onCancel)
		buttonSizer.Add(self.cancel, 0, wx.EXPAND|wx.ALL, 10)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer.Add(editBoxSizer, 1, wx.EXPAND|wx.ALL, 10)
		mainSizer.Add(cumboSizer, 1, wx.EXPAND|wx.ALL,10)
		mainSizer.Add(buttonSizer, 0, wx.EXPAND|wx.ALL, 5)
		panel.SetSizer(mainSizer)

	def postInit(self):
		#if isSelectedText():
			#self.editTextControl.SetValue(isSelectedText())
		indexOfDefault= config.conf["dictionariesAlmaany"]["defaultDictionary"]
		self.cumbo.SetSelection(indexOfDefault)
		self.editTextControl.SetFocus()

	@staticmethod
	def getMeaning(text, base_url):
		t= MyThread(text, base_url)
		t.start()
		while not t.meaning and not t.error and t.is_alive():
			beep(500, 100)
			time.sleep(0.5)
		t.join()

		title= _('Dictionaries Almaany')
		# Window type options: 0=NVDA message, 1=Default browser, 2=Browser window only
		useNvdaMessageBox= config.conf["dictionariesAlmaany"]["windowType"]== 0
		useDefaultFullBrowser= config.conf["dictionariesAlmaany"]["windowType"]== 1
		useBrowserWindowOnly= config.conf["dictionariesAlmaany"]["windowType"]== 2
		
		if t.meaning and useNvdaMessageBox:
			queueHandler.queueFunction(queueHandler.eventQueue, ui.browseableMessage, t.meaning, title=title, isHtml=True)
			return
		elif t.meaning and useDefaultFullBrowser:
			openBrowserWindow('default', t.meaning, directive= '', default= True)
		elif t.meaning and useBrowserWindowOnly:
			if 'Firefox' in browsers and not appIsRunning('firefox.exe'):
				openBrowserWindow('Firefox', t.meaning, directive= ' --kiosk ')
			elif 'Google Chrome' in browsers and not appIsRunning('chrome.exe'):
				openBrowserWindow('Google Chrome', t.meaning, directive= ' -kiosk ')
			elif 'Internet Explorer' in browsers:
				openBrowserWindow('Internet Explorer', t.meaning, directive= ' -k -private ')
		elif t.error:
			if t.error== "HTTP Error 410: Gone":
				# Translators: Message displayed if error happened.
				msg= _("No meaning found")
			elif t.error== "<urlopen error [Errno 11001] getaddrinfo failed>":
				# Translators: Message displayed if error happened.
				msg= _("Most likely no internet connection")
			else:
				msg= t.error
			errorMessage= "{}( {})".format(_("Sorry, An Error Happened"), msg)
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, errorMessage)

	def onOk(self, e):
		# word or phrase to be translated.
		word= self.editTextControl.GetValue()
		# stripping white spaces.
		word= word.strip()
		if not word:
			# Return focus to edit control.
			self.editTextControl.SetFocus()
			return
		else:
			# Selecting the dictionary.
			i= self.cumbo.GetSelection()
			# The url is the second item in the tuple.
			dict_url= dictionaries_nameAndUrl[i][1]
			self.getMeaning(word, dict_url)
			closeDialogAfterRequiringTranslation= config.conf["dictionariesAlmaany"]["closeDialogAfterRequiringTranslation"]
			if closeDialogAfterRequiringTranslation:
				wx.CallLater(4000, self.Destroy)

	def onCancel (self, e):
		self.Destroy()
