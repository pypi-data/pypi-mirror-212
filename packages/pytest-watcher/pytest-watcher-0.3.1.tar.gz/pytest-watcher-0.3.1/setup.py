# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_watcher']

package_data = \
{'': ['*']}

install_requires = \
['watchdog>=2.0.0']

entry_points = \
{'console_scripts': ['ptw = pytest_watcher:run',
                     'pytest-watcher = pytest_watcher:run']}

setup_kwargs = {
    'name': 'pytest-watcher',
    'version': '0.3.1',
    'description': 'Automatically rerun your tests on file modifications',
    'long_description': '# A simple watcher for pytest\n\n[![PyPI](https://img.shields.io/pypi/v/pytest-watcher)](https://pypi.org/project/pytest-watcher/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-watcher)](https://pypi.org/project/pytest-watcher/)\n[![GitHub](https://img.shields.io/github/license/olzhasar/pytest-watcher)](https://github.com/olzhasar/pytest-watcher/blob/master/LICENSE)\n\n## Overview\n\n**pytest-watcher** is a tool to automatically rerun tests (using `pytest` by default) whenever your code changes.\n\nWorks on Unix (Linux, MacOS, BSD) and Windows.\n\n## Table of Contents\n\n- [Motivation](#motivation)\n- [File Events](#file-events)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Using a different test runner](#using-a-different-test-runner)\n- [Watching different patterns](#watching-different-patterns)\n- [Delay](#delay)\n- [Compatibility](#compatibility)\n- [License](#license)\n\n## Motivation\n\n### Why not general tools (e.g. `watchmedo`, `entr`)?\n\n- Easy to use and remember\n- Works for most python projects out of the box\n- Minimum dependencies (`watchdog` is the only one)\n- Handles post-processing properly (see [delay](#delay))\n\n### What about pytest-watch?\n\n[pytest-watch](https://github.com/joeyespo/pytest-watch) has been around for a long time and used to address exactly this problem. Unfortunately, pytest-watch is no longer maintained and does not work for many users. To provide a substitute, I developed this tool.\n\n## File events\n\nBy default `pytest-watcher` looks for the following events:\n\n- New `*.py` file created\n- Existing `*.py` file modified\n- Existing `*.py` file deleted\n- A `*.py` file moved either from or to the watched path\n\nYou can specify alternative file patterns to watch. See [Watching different patterns](#watching-different-patterns)\n\n## Installation\n\n```sh\npip install pytest-watcher\n```\n\n## Usage\n\nSpecify the path that you want to monitor:\n\n```sh\nptw .\n```\n\nor\n\n```sh\nptw /home/repos/project\n```\n\nAny arguments after `<path>` will be passed to the test runner (which is `pytest` by default). For example:\n\n```sh\nptw . -x --lf --nf\n```\n\nwill call `pytest` with the following arguments:\n\n```sh\npytest -x --lf --nf\n```\n\n## Using a different test runner\n\nYou can specify an alternative test runner using the `--runner` flag:\n\n```sh\nptw . --runner tox\n```\n\n## Watching different patterns\n\nYou can use the `--patterns` flag to specify file patterns that you want to monitor. It accepts a list of Unix-style patterns separated by a comma. The default value is "\\*.py".\n\nExample:\n\n```sh\nptw . --patterns \'*.py,pyproject.toml\'\n```\n\nYou can also **ignore** certain patterns using the `--ignore-patterns` flag:\n\n```sh\nptw . --ignore-patterns \'settings.py,db.py\'\n```\n\n## Delay\n\n`pytest-watcher` uses a short delay (0.2 seconds by default) before triggering the actual test run. The main motivation for this is post-processors that can run after you save the file (e.g., `black` plugin in your IDE). This ensures that tests will be run with the latest version of your code.\n\nYou can control the actual delay value with the `--delay` flag:\n\n`ptw . --delay 0.2`\n\nTo disable the delay altogether, you can provide zero as a value:\n\n`ptw . --delay 0`\n\n## Compatibility\n\nThe code is tested for Python versions 3.7+\n\n## License\n\nThis project is licensed under the [MIT License](LICENSE).\n',
    'author': 'Olzhas Arystanov',
    'author_email': 'o.arystanov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/olzhasar/pytest-watcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
