## Changes for 2.4 .

*	Make possible to change the default dictionary, through the setting panel of the addon.  
*	Drop support for python2, and remove urllib2 package from the addon.  
This means, changing minimum tested version to 2019.3.  
*	Solve a problem showd up recently, when the addon not able to get accurate meaning or results.  
The problem solved, by removing old user agent, and use instead user_agent module.
