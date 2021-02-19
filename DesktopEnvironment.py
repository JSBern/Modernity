#
#  Cardapio is an alternative menu applet, launcher, and much more!
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

import os

class DesktopEnvironment:

	def __init__(self, cardapio):
		"""
		Initialize desktop-environment-related variables
		"""

		self.cardapio = cardapio

		try:
			self.environment = os.environ['DESKTOP_SESSION']

		except Exception, exception:
			self.environment = None 

		# We don't need to know all window managers, just a few problematic ones.
		wms = ['gnome-shell', 'cinnamon']

		for wm in wms:

			process = subprocess.Popen(
					['pgrep', wm],
					stdout=subprocess.PIPE, stderr=subprocess.PIPE)

			stdout, dummy = process.communicate()
			if stdout:
				self.environment = wm

		# initialize everything to Gnome defaults, then change them to other DEs as needed
		self.about_de            = 'gnome-about'
		self.about_distro        = 'yelp "ghelp:about-%s"' % cardapio.distro_name.lower() # NOTE: i'm assuming this is the pattern for all distros...
		self.menu_editor         = 'alacarte'
		self.file_open           = "xdg-open '%s'"
		self.connect_to_server   = which('nautilus-connect-server')
		self.lock_screen         = 'gnome-screensaver-command --lock'
		self.save_session        = 'gnome-session-quit --logout'
		self.shutdown            = 'gnome-session-quit --power-off'
		self.execute_in_terminal = None

		# Treat Gnome Flashback as Gnome3
		if self.environment.find('gnome-flashback') == 0:
			self.environent = 'gnome3'

		if   self.environment == 'kde'         : pass
		elif self.environment == 'xfce'        : pass
		elif self.environment == 'lxde'        : pass
		elif self.environment == 'lwde'        : pass
		elif self.environment == 'mate'        : self.init_mate()
		elif self.environment == 'gnome'       : pass
		elif self.environment == 'gnome-shell' : pass
		elif self.environment == 'cinnamon'    : pass

	def init_mate(self):
		"""
		Override some of the default variables for use in Mate
		"""

		# When libexo is installed (use in some xfce apps) it breaks xdg-open
		# for some reason. So we here substitute it with gnome-open.
		self.file_open           = "mate-open '%s'"
		self.menu_editor         = 'mozo'
		self.connect_to_server   = which('caja-connect-server')
		self.lock_screen         = 'mate-screensaver-command --lock'
		self.save_session        = 'mate-session-save --logout-dialog'
		self.shutdown            = 'mate-session-save --shutdown-dialog'
		self.about_de            = 'mate-about'

		try:
			from mate import execute_terminal_shell 
			self.execute_in_terminal = execute_terminal_shell

		except Exception, exception:
			logging.warn('Warning: you will not be able to execute scripts in the terminal')


	def register_session_close_handler(self, handler):
		"""
		Register the callback that saves all settings when the user's session is closed
		"""

		if self.environment == 'mate': self.register_gnome_session_close_handler(handler)


	def register_gnome_session_close_handler(self, handler):
		"""
		Same as register_session_close_handler(), but for Gnome
		"""

		try:
			if self.environment == 'mate':
				from mate import program_init as gnome_program_init
				from mate.ui import master_client as gnome_ui_master_client

		except Exception, exception:
			logging.warn('Warning: Cardapio will not be able to tell when the Gnome session is closed')
			return

		# The function below prints a warning to the screen, saying that
		# an assertion has failed. Apparently this is normal. Ignore it.
		gnome_program_init('', self.cardapio.version)
		client = gnome_ui_master_client()
		client.connect('save-yourself', lambda x: handler)
