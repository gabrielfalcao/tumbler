# tumbler `0.0.11`

Flask workflow


## 1. install

```bash
pip install tumbler
```

## 2. create your controllers

```python
# foo.py

from tumbler import tumbler, json_response

route = tumbler.module(__name__)

@route.get('/')
def index():
    return json_response({'ok': True}, 200)


@route.get('/api/foo')
def api():
    return json_response({'foo': ['bar']}, 200)

```

## 3. run

```bash
tumbler run foo.py
tumbler run foo.py --port=3000
tumbler run foo.py --host=0.0.11.0 --port=8080
```


## 4. unit and functional tests

```bash
tumbler unit
tumbler functional
```

## 5. deploy

```python

# wsgi.py

import foo
from tumbler.core import Web

application = Web(
    static_folder='/srv/static',
    static_url_path='/assets',
    templates_folder='/srv/templates',
)
```

```bash
uwsgi --http-socket 127.0.0.0.11080 --chdir /home/foobar/myproject/ --wsgi-file wsgi.py --master --processes 4 --threads 2 --stats 127.0.0.11:9191
```
