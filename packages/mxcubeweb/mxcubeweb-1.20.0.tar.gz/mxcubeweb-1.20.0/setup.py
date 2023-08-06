# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['mxcube3',
 'mxcube3.core',
 'mxcube3.core.adapter',
 'mxcube3.core.components',
 'mxcube3.core.components.user',
 'mxcube3.core.models',
 'mxcube3.core.util',
 'mxcube3.routes',
 'mxcube3.video']

package_data = \
{'': ['*'], 'mxcube3': ['templates/*']}

install_requires = \
['Flask-Security-Too>=5.0.2,<6.0.0',
 'Flask-SocketIO>=5.3.2,<6.0.0',
 'Flask>=2.2.2,<3.0.0',
 'PyDispatcher>=2.0.6,<3.0.0',
 'bcrypt>=4.0.1,<5.0.0',
 'devtools>=0.10.0,<0.11.0',
 'flask-sqlalchemy>=3.0.2,<4.0.0',
 'gevent-websocket>=0.10.1,<0.11.0',
 'jsonschema>=4.17.1,<5.0.0',
 'mock>=4.0.3,<5.0.0',
 'mxcube_video_streamer==1.0.0',
 'mxcubecore==1.6.0',
 'pydantic>=1.10.2,<2.0.0',
 'pytz>=2022.6,<2023.0',
 'redis>=4.3.5,<5.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'scandir>=1.10.0,<2.0.0',
 'spectree>=1.0.2,<2.0.0',
 'tzlocal>=4.2,<5.0']

entry_points = \
{'console_scripts': ['mxcubeweb-server = mxcube3:main']}

setup_kwargs = {
    'name': 'mxcubeweb',
    'version': '1.20.0',
    'description': 'MXCuBE Web user interface',
    'long_description': '[![Build Status](https://travis-ci.org/mxcube/mxcube3.svg?branch=master)](https://travis-ci.org/mxcube/mxcube3)\n[![codecov](https://codecov.io/gh/mxcube/mxcube3/branch/master/graph/badge.svg)](https://codecov.io/gh/mxcube/mxcube3)\n\n<p align="center"><img src="http://mxcube.github.io/mxcube/img/mxcube_logo20.png" width="125"/></p>\n\n# MXCuBE-Web\nMXCuBE-Web is the latest generation of the data acquisition software MXCuBE (Macromolecular Xtallography Customized Beamline Environment). The project started in 2005 at [ESRF](http://www.esrf.eu), and has since then been adopted by other institutes in Europe. In 2010, a collaboration agreement has been signed for the development of MXCuBE with the following partners:\n\n* ESRF\n* [Soleil](http://www.synchrotron-soleil.fr/)\n* [MAX IV](https://www.maxiv.lu.se/)\n* [HZB](http://www.helmholtz-berlin.de/)\n* [EMBL](http://www.embl.org/)\n* [Global Phasing Ltd.](http://www.globalphasing.com/)\n* [ALBA](https://www.cells.es/en)\n* [DESY](https://www.desy.de)\n* [LNLS](https://www.lnls.cnpem.br/)\n* [Elettra](https://www.elettra.trieste.it/)\n* [NSRRC](https://www.nsrrc.org.tw/english/index.aspx)\n\nMXCuBE-Web is developed as a web application and runs in any recent browser. The application is further built using standard web technologies and does not require any third party plugins to be installed in order to function. \n\n Data collection           | Sample grid\n:-------------------------:|:-------------------------:\n![datacollection-view](https://user-images.githubusercontent.com/4331447/42496925-d983bf3e-8427-11e8-890e-898dda649101.png)|![samplegrid-view](https://user-images.githubusercontent.com/4331447/42496937-e8547b34-8427-11e8-9447-645e6d7f1dc5.png)\n\nThe underlaying beamline control layer is implemented using the library [**mxcubecore**](https://github.com/mxcube/mxcubecore) previously known as [HardwareRepository](https://github.com/mxcube/HardwareRepository). The **mxcubecore** module is compatable with both MXCuBE-Web and the [MXCuBE-Qt application](https://github.com/mxcube/mxcubeqt). The earlier versions of MXCuBE-Web (upto 3.2.x) uses [HardwareRepository](https://github.com/mxcube/HardwareRepository) while versions after 4.x uses [**mxcubecore**](https://github.com/mxcube/mxcubecore).\n\nLatest information about the MXCuBE project can be found on the\n[project webpage](http://mxcube.github.io/mxcube/).\n\n### Technologies in use\n\nThe backend is built on a Python-flask micro-framework, a library called SocketIO is further used to provide a bi-directional communication channel between backend and client. The backend exposes a REST API to the client.\n\nThe client is implemented in ECMAScript6 and HTML5. React, Boostrap and FabricJS are the main libraries used for the UI development\n\n### Installation and testing\nFollow the instructions [here](https://github.com/mxcube/mxcube3/wiki)\n\n## Information for developers\n- [Contributing guidelines](https://github.com/mxcube/mxcube3/blob/master/CONTRIBUTING.md)\n\n## Information for users\n\n- [User Manual MXCuBE3](https://www.esrf.fr/mxcube3)\n- [Feature overview](https://github.com/mxcube/mxcubeqt/blob/master/docs/source/feature_overview.rst)\n- If you cite MXCuBE, please use the references:\n\n```\nOscarsson, M. et al. 2019. “MXCuBE2: The Dawn of MXCuBE Collaboration.” Journal of Synchrotron Radiation 26 (Pt 2): 393–405.\n\nGabadinho, J. et al. (2010). MxCuBE: a synchrotron beamline control environment customized for macromolecular crystallography experiments. J. Synchrotron Rad. 17, 700-707\n```\n\n',
    'author': 'The MXCuBE collaboration',
    'author_email': 'mxcube@esrf.fr',
    'maintainer': 'MXCuBE collaboration',
    'maintainer_email': 'mxcube@esrf.fr',
    'url': 'http://github.com/mxcube/mxcubeweb',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
