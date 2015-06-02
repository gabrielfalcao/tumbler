# tumbler `0.0.17`

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
tumbler run foo.py --host=0.0.17.0 --port=8080
```


## 4. unit and functional tests


simple steps:

**1** - On the root of your project folder create the folder: `tests/unit` and `tests/functional`:

```bash
mkdir -p tests/{unit,functional}
```

**2** - Create a `__init__.py` file inside of all the directories


```bash
touch tests/{unit,functional,}/__init__.py
```

**3** - To take advantage of "[sure's](http://falcao.it/sure)" syntax,
  import sure in the main __init__ file of each test folder.

```bash
printf 'import sure\nsure\n' > tests/unit/__init__.py
printf 'import sure\nsure\n' > tests/functional/__init__.py
```

**4** - Install test dependencies

```bash
tumbler dependencies  # will install local environment dependencies
```


**5** - Run your tests!

```bash
tumbler unit
tumbler functional
```

**6** - Browse the examples

1. [a functional test](https://github.com/gabrielfalcao/tumbler/blob/master/examples/tdd/tests/functional/test_users.py)
2. [a simple angularjs-based clock](https://github.com/gabrielfalcao/tumbler/tree/master/examples/nosql)

**7** - Learn more about testing flask

*Tumbler* is just a nice wrapper around Flask, giving you a test runner and a few other utilities.
It tries to help you with tedious tasks that you might need to perform in your flask apps while trying to keep your web stack as thin as possible.

With that in mind, writing *functional* tests for your controllers can be done like in the [flask official documentation](http://flask.pocoo.org/docs/0.10/testing/)


## 5. deploy

```python

# wsgi.py

import foo

# importing your routes is enough for tumbler to find them in memory
# and load up your web application

from tumbler.core import Web

application = Web(
    static_folder='/srv/static',
    static_url_path='/assets',
    templates_folder='/srv/templates',
    use_sqlalchemy=False  # or true if you're using a SQL db
)
```

```bash
uwsgi --http-socket 127.0.0.0.17080 --chdir /home/foobar/myproject/ --wsgi-file wsgi.py --master --processes 4 --threads 2 --stats 127.0.0.17:9191
```
