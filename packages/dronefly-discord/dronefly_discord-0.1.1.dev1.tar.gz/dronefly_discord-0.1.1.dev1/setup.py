# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discord']

package_data = \
{'': ['*']}

install_requires = \
['dronefly-core>=0.3.6.dev0,<0.4.0',
 'inflect>=5.3.0,<6.0.0',
 'pyinaturalist>=0.19.0.dev2,<0.20']

setup_kwargs = {
    'name': 'dronefly-discord',
    'version': '0.1.1.dev1',
    'description': 'Dronefly Discord library',
    'long_description': "# Dronefly Discord\n\nThis library will support writing Discord cogs based on\n[dronefly-core](https://github.com/dronefly-garden/dronefly-core). It is\nderived from the Discord-specific code extracted from the original\n[Dronefly](https://dronefly.readthedocs.io) bot codebase. We aim to keep\nthe library general enough to work with any bot based on\n[discord.py](https://discordpy.readthedocs.io), as well as on bots using\nthe [Red-DiscordBot](https://docs.discord.red) framework.\n\n# Related packages\n\n## Dronefly core\n\nThe [dronefly-core](https://github.com/dronefly-garden/dronefly-core)\npackage is an incomplete rewrite of [Dronefly](https://dronefly.readthedocs.io/)\nDiscord bot's core components.\n\n## Dronefly Discord bot\n\nDronefly Discord bot brings [iNaturalist](https://www.inaturalist.org) taxa,\nobservations, and other data from the site into conversations on the\n[Discord](https://discord.com) chat platform.\n",
    'author': 'Ben Armstrong',
    'author_email': 'synrg@debian.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
