### haf plugin sql publish

    The plugin sql publish of haf, now only support mysql

[![Build Status](https://travis-ci.org/hautof/haf-plugin-sqlpublish.svg?branch=master)](https://travis-ci.org/hautof/haf-plugin-sqlpublish)

### How to get it?

> by pip tool

```shell
    tsbx-mw# pip install hafsqlpublish
```

> by src

```shell
    tsbx-mw# git clone https://github.com/hautof/haf-plugin-sqlpublish ./
    tsbx-mw# python setup.py install
```

### usage

> using as haf params

```bash
    python -m haf run --sql-publish=True --sql-publish-db=192.168.0.101:6606@root:test123@haf_publish
```

> using as haf config

```json
    "sql_publish": {
        "id": 1,
        "sql_name": "upload",
        "publish": true,
        "host": "192.168.1.2",
        "port": 3306,
        "username": "root",
        "password": "test123",
        "database": "haf_publish",
        "protocol": "mysql"
      }
```