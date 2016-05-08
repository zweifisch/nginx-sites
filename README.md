# nginx-sites

cli utility for managing nginx vhost configs

install using pip
```sh
pip install nginx-sites
```

## usage

```sh
ngx ls
ngx enable <name>
ngx disable <name>
ngx new <name> [--path=<path>] [--template=<template>] [(--port=<port>)...]
ngx rm <name>
ngx open <name>
ngx cp <source> <target>
ngx --version
```

examples

```
ngx new nodejs.test --template=node --port=3003 --port=3004
ngx new phpfpm.test --template=php --port=9000
service nginx reload
```

## adding new vhost templates

Copy the directory `/usr/local/lib/python2.7/dist-packages/nginx_sites/templates` to `~/.nginx-sites-templates`

Edit the configuration file `~/.nginx-sites.json` and set it according to the settings below:

```json
{
    "templates_path": "/home/username/.nginx-sites-templates",
    "sites_available": "/etc/nginx/sites-available",
    "nginx_bin": "/usr/sbin/nginx",
    "sites_enabled": "/etc/nginx/sites-enabled"
}
```

Create your templates in `~/.nginx-sites-templates`

After setting up your new template, it is available for use with the command:

```sh
ngx new myapp.dev --template=mytemplate
ngx reload
```
