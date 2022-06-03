# Dictionaries Almaany #

*	Author: Ibrahim Hamadeh
*	Contributors: Abdel
*	NVDA compatibility: 2019.3 and later
*	Download [version 2.5][1]  

This addon helps you get the meaning of single words through the almaany.com website.  
[almaany.com](https://www.almaany.com/en/dict/ar-en/).

notice: All dictionaries used are bilingual, meaning that for instance, the arabic english dictionary translates from arabic to english and from english to arabic also. 

***

## Usage

*	Press nvda+windows+d, if no selection, dictionaries almaany dialog will be displayed  
if when pressing this command, you were standing on a selected word, you will access the meaning of word in the default dictionary directly.  
*	otherwise when no selection, a dialog opens, enter in the edit field the word you want, tab an choose the dictionary you want and press enter on it.  
if you want to get the meaning in the default Arabic to English, English to Arabic dictionary, you can always press enter on the edit field and after that the meaning of the word will be displayed in a separate browseable window.  
*	You can of cource change the default dictionary of the addon, from the setting panel of the addon, through preferences menu.  

## Options in setting panel ##

*	You can any time adjust these options, going to addon's setting panel, through:  
NVDA menu/preferences/Settings/dictionaries almaany  
*	First, you got a combo box, and from there you can fchoose the default dictionary of the addon.  
This means, when selecting a word and pressing the gesture of the addon, will let you access directly it's meaning in this dictionary.  
After that, you can choose the type of window used to display the meaning.  
	1.	the default and first choice, is your ordinary default browser  
choosing this, the result will be displayed in your default ordinary full browser.  
	2.	the  second choice, is a browser like window as in firefox or google chrome, it is a browser window without file menus or address brar.  
please remember you can close this window only, with control+w or alt+f4.  
	3.	the third, is the native NVDA message box, used it only after testing and if it suits you, for in our experience it smetimes make NVDA freezes.  
*	After that you got a check box, to choose whether to close Dictionaries Almaany dialog after requesting the meaning of word or not.  
 
## Changes for 2.5 .

*	Make the addon compatible with NVDA 2022.1.
*	Removing pieces of unWanted text from the page, that was added recently, by using regular expression, and replacing it with an empty string.

## Changes for 2.4 .

*	Make possible to change the default dictionary, through the setting panel of the addon.  
*	Drop support for python2, and remove urllib2 package from the addon.  
This means, changing minimum tested version to 2019.3.  
*	Solve a problem showd up recently, when the addon not able to get accurate meaning or results.  
The problem solved, by removing old user agent, and use instead user_agent module.

## Changes for 2.3 .

*	Add the option to choose the default full browser to display result in setting dialog.  
*	Add five new dictionaries to list of available dictionaries, mainly Arabic German and Arabic Russian dictionaries.  

## Changes for 2.1 .

*	Make setting dialog for the addon  
*	Give the user the choice to get the result in browser window in kiosk mode, like chrome or firefox, full screen without menus or address bar.  
*	Give the user the option to close Dictionaries Almaany dialog after requesting translation.  

## Changes for 2.0 .

*	Added compatibility with versions of NVDA using Python 3.

## Changes for 1.1 ##

fixing some bugs, getting the addon to return to work after it has stopped working from the server  

*	using urllib2 to make a request object  
*	add user-agent to the request headers.  

## Changes for 1.0 ##

*	Initial version.

### Contributions ###

*	Thanks to Abdel contribution for porting the addon to python3, and using last nvda addon template.  

[1]: https://github.com/ibrahim-h/dictionariesAlmaany/releases/download/2.5/DictionariesAlmaany-2.5.nvda-addon