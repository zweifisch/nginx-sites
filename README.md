# nginx-sites

cli utility for managing nginx vhost configs

install using pip
```sh
pip install nginx-sites
```

## usage

```sh
nginx-sites ls
nginx-sites enable <name>
nginx-sites disable <name>
nginx-sites new <name> [--path=<path>] [--template=<template>] [(--port=<port>)...]
nginx-sites rm <name>
nginx-sites open <name>
nginx-sites cp <source> <target>
nginx-sites --version
```

examples

```
nginx-sites new nodejs.test --template=node --port=3003 --port=3004
nginx-sites new phpfpm.test --template=php --port=9000
service nginx reload
```

## adding new vhost templates

Copy the directory `/usr/local/lib/python2.7/dist-packages/nginx_sites/templates` to `~/.nginx-sites-templates` 

Create your templates in `~/.nginx-sites-templates`

After setting up your new template, it is available for use with the command:

```sh
nginx-sites new myapp.dev --template=mytemplate
service nginx reload
```