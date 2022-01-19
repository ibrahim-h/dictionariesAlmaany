# -*- coding: utf-8 -*-
#this module is aimed to get a specific piece in almaany.com page
#that contains the meaning of a specific word

import urllib
import re
import os, sys
import threading
from logHandler import log

currentPath= os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentPath)
from user_agent import generate_user_agent
del sys.path[-1]

import addonHandler
addonHandler.initTranslation()

regex1= '(<h1 class="section">[\s\S]+<h1 class="section">[\s\S]+?)<h[23456]'
regex2= '(<h1 class="section">[\s\S]+?)<h[23456]'
regex3= '(<h1>[\s\S]+?<h2>[\s\S]+?</h2>[\s\S]+?)<h[23456]'

class MyThread(threading.Thread):
	def __init__(self, text, base_url):
		# text is the word or phrase to be translated.
		threading.Thread.__init__(self)
		self.text= text
		self.base_url= base_url
		self.meaning= ""
		self.daemon=True
		self.error= False

	def run(self):
		text= self.text
		url= self.base_url + urllib.parse.quote(text)
		#log.info(f"url: {url}")
		request= urllib.request.Request(url)
		request.add_header('User-Agent', generate_user_agent())
		try:
			handle = urllib.request.urlopen(request)
			html= handle.read().decode(handle.headers.get_content_charset())
			handle.close()
			#log.info(html)
		except Exception as e:
			log.info('', exc_info= True)
			self.error= str(e)
		else:
			try:
				content= re.findall(regex1, html)
				if not content:
					content= re.findall(regex2, html)
					if not content:
						content= re.findall(regex3, html)
				content= content[0]
			except Exception as e:
				log.info('', exc_info= True)
				self.error= str(e)
			else:
				page= content +"<p> <a href=%s>"%(url) +"Look for the meaning on the web site</a></p>"
				self.meaning= page
