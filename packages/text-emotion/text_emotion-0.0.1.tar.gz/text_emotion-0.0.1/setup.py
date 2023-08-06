# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['emotion']

package_data = \
{'': ['*']}

install_requires = \
['easynmt>=2.0.2,<3.0.0',
 'fasttext>=0.9.2,<0.10.0',
 'requests>=2.31.0,<3.0.0',
 'torch>=2.0.1,<3.0.0',
 'transformers>=4.29.2,<5.0.0']

setup_kwargs = {
    'name': 'text-emotion',
    'version': '0.0.1',
    'description': 'Multilingual Emotion Classification',
    'long_description': '# Emotion\n\n# Introduction\n\n### Supported Languages\n\n# Installation\n\nYou can install emotion using:\n\n    $ pip install emotion\n\n# Usage\n\n```python\nfrom emotion import Detector\n\ndetector = Detector()\n\nprint(detector.detect("Hello, I am so happy!", emotion_language="fr"))\n```',
    'author': 'ma2za',
    'author_email': 'mazzapaolo2019@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ma2za/emotion',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
