# Brython-dev

Brython-dev is a Python library for developers in brython.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install brython-dev
```

## Usage

For runserver

'''bash
py -m brython_dev run
'''

## Configuration

The configuration is in the filename `brython.yml`

* *name*: String. The name of the proyect
* *app*: String, Default: `app.py`. The python main filename
* *template*: String, Default: `app.html`. The html main template
* *stylesheets*: List. A list whith extras stylesheets
* *extensions*: Dict. A dict whith enable brython extensions
  * *brython*: Boolean, Default: `True`. Enable the brython library
  * *brython_stdlib*: Boolean, Default: `False`. Enable the brython stdlib library
* *scripts*: List. A list whith extras scripts
* *brython_options*: Dict. A dict whith brython options

## License
[MIT](https://choosealicense.com/licenses/mit/)