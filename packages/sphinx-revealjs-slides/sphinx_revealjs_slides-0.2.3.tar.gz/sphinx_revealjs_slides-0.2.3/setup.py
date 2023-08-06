# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinx_revealjs', 'sphinx_revealjs.directives']

package_data = \
{'': ['*'],
 'sphinx_revealjs': ['themes/lib/reveal.js/dist/*',
                     'themes/lib/reveal.js/dist/theme/*',
                     'themes/lib/reveal.js/dist/theme/fonts/league-gothic/*',
                     'themes/lib/reveal.js/dist/theme/fonts/source-sans-pro/*',
                     'themes/lib/reveal.js/plugin/highlight/*',
                     'themes/lib/reveal.js/plugin/markdown/*',
                     'themes/lib/reveal.js/plugin/math/*',
                     'themes/lib/reveal.js/plugin/notes/*',
                     'themes/lib/reveal.js/plugin/search/*',
                     'themes/lib/reveal.js/plugin/zoom/*',
                     'themes/revealjs/*']}

install_requires = \
['sphinx>=6.1.3,<7.0.0']

setup_kwargs = {
    'name': 'sphinx-revealjs-slides',
    'version': '0.2.3',
    'description': '',
    'long_description': '# sphinx-revealjs',
    'author': 'Ashley Trinh',
    'author_email': 'ashley@hackbrightacademy.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
