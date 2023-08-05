# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['koschei_messages']

package_data = \
{'': ['*']}

install_requires = \
['coverage[toml]>=7.2.7,<8.0.0',
 'fedora-messaging>=3.3.0,<4.0.0',
 'reuse>=1.1.2,<2.0.0']

entry_points = \
{'fedora.messages': ['koschei.collection.state.change = '
                     'koschei_messages.collection:CollectionStateChange',
                     'koschei.package.state.change = '
                     'koschei_messages.package:PackageStateChange']}

setup_kwargs = {
    'name': 'koschei-messages',
    'version': '1.0.0',
    'description': 'A schema package for messages sent by Koschei',
    'long_description': '<!--\nSPDX-FileCopyrightText: 2023 Contributors to the Fedora Project\n\nSPDX-License-Identifier: GPL-2.0-or-later\n-->\n\n# Koschei messages\n\nA schema package for [Koschei](http://github.com/fedora-infra/koschei).\n\nSee the [detailed documentation](https://fedora-messaging.readthedocs.io/en/stable/messages.html) on packaging your schemas.\n',
    'author': 'Fedora Infrastructure Team',
    'author_email': 'infrastructure@lists.fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedora-infra/koschei-messages',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
