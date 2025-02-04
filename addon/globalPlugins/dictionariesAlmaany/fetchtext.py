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

regex1= '(<h1 class="section">[\s\S]+<h1[\s\S]*?>[\s\S]+?)<h[23456]'
regex2= '(<h1[\s\S]*?>[\s\S]+?<h2[\s\S]*?>[\s\S]+?</h2>[\s\S]+?)<h[23456]'
#regex2= '(<h1 class="section">[\s\S]+?)<h[23456]'
regex3= '(<div class="panel-heading"><h2>[\s\S]+?)<h[23456]'

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
			response = urllib.request.urlopen(request)
			# Some times the encoding of the page returns None, so in this case we use'utf-8' 
			encoding = response.headers.get_content_charset() or 'utf-8'
			html= response.read().decode(encoding)
			response.close()
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
				#removing unWanted text from the page.
				# regex of unWanted text in tables, third cell in the row.
				toBeRemoved1= r'<td>[\s\S]*?<div class="dropdown text-right">[\s\S]*?<span[\s\S]+?</span>[\s\S]*?<ol class="dropdown-menu">[\s\S]*?<li>[\s\S]+?</li>[\s\S]*?<li>[\s\S]+?</li>[\s\S]*?<li>[\s\S]+?</li>[\s\S]*?</ol>[\s\S]*?</div>[\s\S]*?</td>'
				#regex of unWanted text outside tables, in lists.
				toBeRemoved2= r'<div class="dropdown text-right"[\s\S]+?<span[\s\S]+?</span>[\s\S]*?<ol class="dropdown-menu">[\s\S]*?<li>[\s\S]+?</li>[\s\S]*?<li>[\s\S]+?</li>[\s\S]*?<li>[\s\S]+?</li>[\s\S]*?</ol>[\s\S]*?</div>'
				processedContent= re.sub(toBeRemoved1, "", content)
				finalContent= re.sub(toBeRemoved2, "", processedContent)
			except Exception as e:
				log.info('', exc_info= True)
				self.error= str(e)
			else:
				page= finalContent +"<p> <a href=%s>"%(url) +"Look for the meaning on the web site</a></p></body></html>"
				self.meaning= page
