"""nginx sites

Usage:
  nginx-sites ls
  nginx-sites enable <name>
  nginx-sites disable <name>
  nginx-sites new <name> [--path=<path>] [--template=<template>] [(--port=<port>)...]
  nginx-sites rm <name>
  nginx-sites open <name>
  nginx-sites cp <source> <target>
  nginx-sites --version

Options:
  -h --help     Show this screen.
  --version     Show version.

Examples:
	nginx-sites new nodejs.test --template=node --port=3003 --port=3004
	nginx-sites new phpfpm.test --template=php --port=9000
"""

import os
from subprocess import call
import pkg_resources
import shutil
from docopt import docopt
from blessings import Terminal
from pystache import render

dist = pkg_resources.get_distribution('nginx-sites')


config = {
	'sites_enabled': '/etc/nginx/sites-enabled/',
	'sites_available': '/etc/nginx/sites-available/',
	'templates_path': os.path.join(dist.location, 'nginxSites', 'templates')
}


class NginxSites:
	def __init__(self, config):
		self.config = config
		self.term = Terminal()

	def enabled_conf(self, name=None):
		if name is None:
			return self.config['sites_enabled']
		return self.config['sites_enabled'] + name

	def available_conf(self, name=None):
		if name is None:
			return self.config['sites_available']
		return self.config['sites_available'] + name

	def new(self, server_name, root, template, port):
		if port is not None:
			port = [{'port':p} for p in port]
		with open(self.available_conf(server_name), 'w') as fp:
			template_path = os.path.join(self.config['templates_path'], template + '.conf')
			with open(template_path, 'r') as tmpl:
				fp.write(render(tmpl.read(), locals()))
				self.enable(server_name)

	def rm(self, name):
		self.disable(name)
		if os.path.exists(self.available_conf(name)):
			os.remove(self.available_conf(name))

	def ls(self):
		walker = os.walk(self.enabled_conf())
		_, _, enabled_sites = next(walker)
		walker = os.walk(self.available_conf())
		_, _, available_sites = next(walker)
		print("\n".join([self.term.green(site) for site in enabled_sites if site in available_sites]))
		print("\n".join([self.term.yellow(site) for site in available_sites if site not in enabled_sites]))
		print("\n".join([self.term.red(site) for site in enabled_sites if site not in available_sites]))

	def enable(self, name):
		if os.path.exists(self.enabled_conf(name)):
			os.remove(self.enabled_conf(name))
		os.symlink(self.available_conf(name), self.enabled_conf(name))

	def disable(self, name):
		if os.path.exists(self.enabled_conf(name)):
			os.remove(self.enabled_conf(name))

	def cp(self, source, target):
		if os.path.exists(self.available_conf(source)):
			shutil.copy2(self.available_conf(source), self.available_conf(target))
			self.open(target)
		else:
			print("%s not exists" % self.available_conf(source))

	def open(self, name):
		editor = os.environ.get('EDITOR', 'vi')
		call([editor, self.available_conf(name)])


def main():
	args = docopt(__doc__, version='nginx-sites 0.0.5')
	nginxSites = NginxSites(config)
	if args['ls']:
		nginxSites.ls()
	elif args['enable']:
		nginxSites.enable(args['<name>'])
	elif args['disable']:
		nginxSites.disable(args['<name>'])
	elif args['new']:
		root = os.getcwd() if args['--path'] is None else args['--path']
		template = 'php' if args['--template'] is None else args['--template']
		nginxSites.new(args['<name>'], root, template, args['--port'])
	elif args['rm']:
		nginxSites.rm(args['<name>'])
	elif args['cp']:
		nginxSites.cp(args['<source>'], args['<target>'])
	elif args['open']:
		nginxSites.open(args['<name>'])


if __name__ == '__main__':
	main()
