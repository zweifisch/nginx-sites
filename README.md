# nginx-sites

cli utility for managing nginx vhost configs

install using pip
```sh
pip install nginx-sites
```

## usage

```sh
nginx-sites add <name> <python|php>
nginx-sites add new-app-test python

nginx-sites ls

nginx-sites copy new-app-test new-app

nginx-sites remove new-app-test

nginx-sites edit new-app
```

## more tmplates

customized template file can be added to `~/.nginx-sites-tmpls/`,
once added, can be used as
```sh
nginx-sites add <name> <tmpl-name>
```

## config

`~/.nginx-sites`

```yaml
root: var/www/
confdir: /etc/nginx/conf/sites/
tmpls: ~/.nginx-sites-tmps/
```
