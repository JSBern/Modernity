#  
#  Copyright (C) 2010 Cardapio Team (tvst@hotmail.com)
# 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# this function should be the first thing loaded
def fatal_error(title, errortext):
	"""
	This shows an error message, which does not depend on any
	external modules.
	"""

	print("Fatal error: [%s], Code: [%s]" % (title, errortext))

try:
	import os
	import logging
	import commands

except Exception, exception:
	fatal_error('Loading libraries in Misc ', exception)
	import sys
	sys.exit(1)


# note - this is duplicated in cardapio_helper.py
def which(filename):
	"""
	Searches the folders in the OS's PATH variable, looking for a file called
	"filename". If found, returns the full path. Otherwise, returns None.
	"""

	for path in os.environ["PATH"].split(os.pathsep):
		if os.access(os.path.join(path, filename), os.X_OK):
			return "%s/%s" % (path, filename)
	return None


def get_output(shell_command):
	"""
	Returns the output (from stdout) of a shell command. If an error occurs,
	returns False.
	"""

	try: 
		return commands.getoutput(shell_command)
		#return subprocess.check_output(shell_command, shell = True) # use this line with Python 2.7
	except Exception, exception: 
		logging.info('Exception when executing' + shell_command)
		logging.info(exception)
		return False


import gc
#
# When debugging leaks:
#from guppy import hpy
#h = hpy()
#
def get_memory_usage():
	gc.collect()
	#print h.heap()
	#print h.setref()
	return get_output("ps -A -o rss -o cmd | awk '/cardapio / && !/awk/ {print $1}'")


def return_true(*dummy): return True
def return_false(*dummy): return False


