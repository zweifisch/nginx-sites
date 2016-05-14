"""nginx sites

Usage:
  ngx ls
  ngx enable <name>
  ngx disable <name>
  ngx new <name> [--root=<path>] [--template=<template>] [(--port=<port>)...]
  ngx rm <name>
  ngx open <name>
  ngx cp <source> <target>
  ngx reload
  ngx config [-e]
  ngx reconfig
  ngx templates
  ngx templates-show <name>
  ngx --version
  ngx -h

Options:
  -h --help              Show this screen.
  --version              Show version.
  --template=<template>  specify a template [default: static].
  --root=<path>          specify root default is pwd.

Examples:
    ngx new static.test --root /var/www/static
    ngx new nodejs.test --template=node --port=3003 --port=3004
    ngx new phpfpm.test --template=php --port=9000
"""

import os
import sys
import time
import tempfile
import readline
import json
from subprocess import call
from subprocess import check_output
import pkg_resources
import shutil
from docopt import docopt
from pystache import render

from .colorize import formatter

config_path = '~/.nginx-sites.json'


class NginxSites:
    def __init__(self, config):
        self.config = config

    def enabled_conf(self, name=None):
        if name is None:
            return self.config['sites_enabled']
        return os.path.join(self.config['sites_enabled'], name)

    def available_conf(self, name=None):
        if name is None:
            return self.config['sites_available']
        return os.path.join(self.config['sites_available'], name)

    def new(self, server_name, root, template, port):
        if port is not None:
            port = [{'port': p} for p in port]
        with open(self.available_conf(server_name), 'w') as fp:
            template_path = os.path.join(self.config['templates_path'],
                                         template + '.conf')
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
        print(formatter('green')('enabled sites:'))
        sys.stdout.writelines(['  %s\n' % site for site in enabled_sites
                               if site in available_sites])
        print(formatter('yellow')('available sites:'))
        sys.stdout.writelines(['  %s\n' % site for site in available_sites
                               if site not in enabled_sites])
        print(formatter('red')('active sites:'))
        sys.stdout.writelines(['  %s\n' % site for site in enabled_sites
                               if site not in available_sites])

    def enable(self, name):
        if os.path.exists(self.enabled_conf(name)):
            os.remove(self.enabled_conf(name))
        os.symlink(self.available_conf(name), self.enabled_conf(name))

    def disable(self, name):
        if os.path.exists(self.enabled_conf(name)):
            os.remove(self.enabled_conf(name))

    def cp(self, source, target):
        if os.path.exists(self.available_conf(source)):
            shutil.copy2(self.available_conf(source),
                         self.available_conf(target))
            self.open(target)
        else:
            print("%s not exists" % self.available_conf(source))

    def open(self, name):
        editor = os.environ.get('EDITOR', 'vi')
        call([editor, self.available_conf(name)])

    def reload(self):
        call(["sudo", self.config['nginx_bin'], '-s', 'reload'])

    def templates_list(self):
        walker = os.walk(self.config['templates_path'])
        _, _, templates = next(walker)
        sys.stdout.writelines(['%s\n' % t.replace(".conf", '')
                               for t in templates])

    def templates_show(self, name):
        template_path = os.path.join(self.config['templates_path'],
                                     name + '.conf')
        if os.path.exists(template_path):
            with open(template_path, 'r') as tmpl:
                sys.stdout.write(tmpl.read())
        else:
            print(formatter('red')("template %s not found in %s"
                                   % (name, template_path)))
            sys.exit(1)


def editconf(path):
    editor = os.environ.get('EDITOR', 'vi')
    f = tempfile.NamedTemporaryFile(delete=False)
    f.close()
    if(os.path.exists(path)):
        shutil.copyfile(path, f.name)
    ret = call([editor, f.name])
    if ret is 0:
        try:
            with open(f.name) as fp:
                json.load(fp)
            shutil.copyfile(f.name, path)
        except ValueError:
            print('not valid json')
        except:
            print('config failed!')


def load_config(path):
    if os.path.exists(path):
        try:
            with open(path) as fp:
                return json.load(fp)
        except ValueError:
            print('config file is not valid json')
            time.sleep(2)
            editconf(path)
            return load_config(path)
        except:
            print('failed to load config from %s' % path)


def dump_config(path, config):
    with open(path, 'w') as fp:
        json.dump(config, fp, indent=True)


def get_input(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return raw_input(prompt)
    finally:
        readline.set_startup_hook()


def config_interactively():
    ret = {}
    ret['sites_enabled'] = get_input('path to sites-enabled: ',
                                     '/etc/nginx/sites-enabled')
    ret['sites_available'] = get_input(
        'path to sites-available: ',
        ret['sites_enabled'].replace('enabled', 'available'))
    try:
        nginx_bin = check_output(['which', 'nginx']).strip()
    except:
        nginx_bin = ''
    ret['nginx_bin'] = get_input('path to nginx executable: ', nginx_bin)
    dist = pkg_resources.get_distribution('nginx_sites')
    ret['templates_path'] = os.path.join(dist.location,
                                         'nginx_sites', 'templates')
    return ret


def run():
    config_path_full = os.path.expanduser(config_path)
    config = load_config(config_path_full)

    if config is None:
        print('config file not loaded!')
        config = config_interactively()
        dump_config(config_path_full, config)

    args = docopt(__doc__, version='nginx-sites 0.1.6')
    sites = NginxSites(config)
    if args['ls']:
        sites.ls()
    elif args['enable']:
        sites.enable(args['<name>'])
    elif args['disable']:
        sites.disable(args['<name>'])
    elif args['new']:
        root = args['--root'] or os.getcwd()
        sites.new(args['<name>'], root, args['--template'], args['--port'])
    elif args['rm']:
        sites.rm(args['<name>'])
    elif args['cp']:
        sites.cp(args['<source>'], args['<target>'])
    elif args['open']:
        sites.open(args['<name>'])
    elif args['config']:
        if args['-e']:
            editconf(config_path_full)
        else:
            print(json.dumps(load_config(config_path_full), indent=2))
    elif args['reconfig']:
        config = config_interactively()
        dump_config(config_path_full, config)
    elif args['reload']:
        sites.reload()
    elif args['templates']:
        sites.templates_list()
    elif args['templates-show']:
        sites.templates_show(args['<name>'])


def main():
    try:
        run()
    except (IOError, OSError) as err:
        if err.errno is 13:
            os.execvp("sudo", ["sudo"] + sys.argv)
        else:
            print(err.strerror)
            sys.exit(1)


if __name__ == '__main__':
    main()
