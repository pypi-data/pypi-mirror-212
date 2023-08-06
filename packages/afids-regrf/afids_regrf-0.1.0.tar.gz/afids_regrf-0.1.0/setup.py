# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['afids_regrf',
 'afids_regrf.modelling.workflow.scripts',
 'afids_regrf.modelling.workflow.scripts.commonsmk',
 'afids_regrf.registration.workflow',
 'afids_regrf.registration.workflow.scripts',
 'afids_regrf.registration.workflow.scripts.commonsmk',
 'afids_regrf.resources']

package_data = \
{'': ['*'],
 'afids_regrf': ['modelling/config/*',
                 'modelling/resources/*',
                 'modelling/workflow/*',
                 'modelling/workflow/envs/*',
                 'modelling/workflow/rules/*',
                 'registration/config/*',
                 'registration/resources/*'],
 'afids_regrf.registration.workflow': ['envs/*', 'rules/*']}

install_requires = \
['importlib-resources>=5.12.0,<6.0.0',
 'joblib>=1.2.0,<2.0.0',
 'nibabel>=5.0.1,<6.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scikit-learn>=1.2.1,<2.0.0']

entry_points = \
{'console_scripts': ['afids_regrf_apply = afids_regrf.apply:main',
                     'afids_regrf_train = afids_regrf.train:main']}

setup_kwargs = {
    'name': 'afids-regrf',
    'version': '0.1.0',
    'description': '',
    'long_description': '# afids-regRF\n \n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.8.1,<4',
}


setup(**setup_kwargs)
