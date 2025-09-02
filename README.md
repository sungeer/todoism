# demo_wsgi

*A backend scaffold depends on the Werkzeug WSGI toolkit.*

## Installation

clone:
```
$ git clone https://github.com/sungeer/demo_wsgi.git
$ cd demo_wsgi
```
create & activate virtual env then install dependency:

with venv + pip:
```
$ python -m venv venv
$ source venv/bin/activate  # use `venv\Scripts\activate` on Windows
$ pip install -r requirements.txt
```

run:
```
$ waitress --host=127.0.0.1 --port=7788 app:app
* Running on http://127.0.0.1:7788/
```

## License

This project is licensed under the GPL-3.0 License (see the
[LICENSE](LICENSE) file for details).
