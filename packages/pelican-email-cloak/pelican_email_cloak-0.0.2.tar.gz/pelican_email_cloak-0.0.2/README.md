# E-mail Cloak: A Plugin for Pelican

[![PyPI Version](https://img.shields.io/pypi/v/pelican-email-cloak)](https://pypi.org/project/pelican-email-cloak/)
![License](https://img.shields.io/pypi/l/pelican-email-cloak?color=blue)

E-mail cloaking plugin for Pelican

## Installation

This plugin can be installed via:

    python -m pip install pelican-email-cloak

## Usage

To use this plugin, add the following to your `pelicanconf.py`:

```python
PLUGINS = [
    # ...
    'email_cloak',
    # ...
]
```

and place the plugin at `pelican/plugins/email_cloak` in your plugins folder.

E-mails in articles and pages will be cloaked.

## License

This project is licensed under the MIT license.
