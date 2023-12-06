# -*- coding: UTF-8 -*-
# Update add-ons module based on the work of several add-on authors
# Copyright (C) 2023 updated by Ibrahim Hamadeh <ibra.hamadeh@hotmail.com>
# This file is covered by the GNU General Public License.

# import the necessary modules.
import wx
import os
import globalVars
import addonHandler
import threading
from threading import Thread
import urllib.request
from urllib.request import urlopen
import json
import config
import gui
import shutil
import tones
import time
from logHandler import log
from typing import Optional

# For translation
addonHandler.initTranslation()

def getMyAddon():
	return addonHandler.getCodeAddon()

def downloadInChunkAndBeep(url: str, destPath: Optional[str]) -> None:
	# tempPath is the path of downloaded file.
	global tempPath
	if not destPath:
		import tempfile
		fileHandler, tempPath = tempfile.mkstemp(prefix="nvda_addonUpdate-", suffix=".nvda-addon")
	else:
		tempPath = destPath
	#log.info(f"temp path is {tempPath}")
	# #2352: Some security scanners such as Eset NOD32 HTTP Scanner
	# cause huge read delays while downloading.
	# Therefore, set a higher timeout.
	try:
		remote = urlopen(url, timeout=120)
	except Exception:
		log.debug("Could not access download URL")
		raise RuntimeError("Could not access download URL")
	if remote.code != 200:
		remote.close()
		raise RuntimeError("Download failed with code %d" % remote.code)
	size: int = int(remote.headers["content-length"])
	#log.info(f"remote size is {size} bytes")
	with open(tempPath, "wb") as local:
		read: int = 0
		chunk: int = 8192
		beepCounter= 0
		while True:
			if beepCounter%3== 0:
			# Every 3 cycles it beeps once.
				tones.beep(200, 200)
			time.sleep(0.2)
			if size - read < chunk:
				chunk = size - read
			block = remote.read(chunk)
			if not block:
				break
			read += len(block)
			local.write(block)
			beepCounter+=1
		remote.close()
		if read < size:
			raise RuntimeError("Content too short")
	# we have to close the file by fileHandler, in order to be able to remove it later.
	os.close(fileHandler)
	#log.info("download complete")

myAddon = getMyAddon()
urlRepos = "https://api.github.com/repos/ibrahim-h/"+myAddon.manifest["name"]+"/releases"
urlName = ""
addonDownloadedName = ""
# path of downloaded file.
tempPath= ""
# directory is when we choose explicity a path of downloaded file.
# but I have prefered the temporary path in temp folder.
directory = ""

class Initialize(Thread):
	# Creating the constructor of the newly created GlobalPlugin class.
	def __init__(self):
		# Call of the constructor of the parent class.
		super(Initialize, self).__init__()
		self.daemon = True
		wx.CallAfter(AddonFlow.upgradeVerify)

class AddonFlow(Thread):
	def __init__(self):
		super(AddonFlow, self).__init__()
		self.daemon = True

	def upgradeVerify():
		global downloadUrl, addonDownloadedName
		if globalVars.appArgs.secure or config.isAppX or globalVars.appArgs.launcher:
			AddonFlow.doNothing()
		request = urllib.request.Request(urlRepos)
		content = urllib.request.urlopen(request).read()
		githubApi = json.loads(content.decode('utf-8'))
		newVersion= githubApi[0]["tag_name"].strip('v')
		currVersion= myAddon.manifest["version"]
		#log.info(f'newVersion: {newVersion} and currVersion: {currVersion}')
		# Compare versions as tuple of ints.
		if tuple(int(s) for s in newVersion.split('.'))> tuple(int(s) for s in currVersion.split('.')):
			downloadUrl = githubApi[0]['assets'][0]['browser_download_url']
			addonDownloadedName = str(downloadUrl.split("/")[-1:]).replace("[", "").replace("\'", "").replace("]", "")

			# Translators: Message dialog box to ask user if wants to update.
			if gui.messageBox(_("It is available a new version {} of this add-on.\n Do you want to update?".format(newVersion)),
			_("{}-Update".format(myAddon.manifest["summary"])),
			style=wx.ICON_QUESTION|wx.YES_NO) == wx.YES:
				download = Thread(target = AddonFlow.downloadAddon)
				download.setDaemon(True)
				try:
					download.start()
					#log.info("download started ...")
				except:
					log.info('error in downloading the addon', excc_info= True)
			else:
				AddonFlow.doNothing()

	def downloadAddon():
		global directory, bundle
		directory = os.path.join(globalVars.appArgs.configPath, "updates")
		if not os.path.exists(directory):
			os.mkdir(directory)
		file = os.path.join(directory, addonDownloadedName)
		req = urllib.request.Request(downloadUrl, headers={'User-Agent': 'Mozilla/5.0'})
		#downloadInChunkAndBeep(req, file)
		# we made destPath= "", to have file dowloaded in temp folder.
		downloadInChunkAndBeep(req, "")
		# tempPath is the path of downloaded file.
		bundle = addonHandler.AddonBundle(tempPath)
		if bundle.manifest["name"] == myAddon.manifest['name']:
			AddonFlow.checkCompatibility()
		AddonFlow.doNothing()

	def checkCompatibility():
		if addonHandler.addonVersionCheck.isAddonCompatible(bundle):
			#log.info("addon is compatible")
			# It is compatible, so install
			AddonFlow.install()
		# It is not compatible, so do not install and inform user
		else:
			# Translators: Message dialog box to inform user that the add-on is not compatible
			gui.messageBox(_("This new version of this add-on is not compatible with your version of NVDA.\n The update process will be terminated."), myAddon.manifest["summary"], style=wx.ICON_WARNING)
			AddonFlow.doNothing()

	def install():
		#log.info('installing the addon ...')
		# To remove the old version
		if not myAddon.isPendingRemove:
			myAddon.requestRemove()
		# to install the new version
		try:
			gui.ExecAndPump(addonHandler.installAddonBundle, bundle)
		except Exception:
			log.error(f"Error installing  addon bundle from {bundle._path}", exc_info=True)
		# to delete the downloads folder
		if directory:
			shutil.rmtree(directory, ignore_errors=True)
		if tempPath:
			os.unlink(tempPath)
		# to restart NVDA
		gui.addonGui.promptUserForRestart()

	def doNothing():
		pass
