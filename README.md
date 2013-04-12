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

