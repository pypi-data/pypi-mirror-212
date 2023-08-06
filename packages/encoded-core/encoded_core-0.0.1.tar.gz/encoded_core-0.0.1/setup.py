# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['encoded_core', 'encoded_core.tests', 'encoded_core.types']

package_data = \
{'': ['*'], 'encoded_core': ['schemas/*']}

install_requires = \
['PyJWT>=2.6.0,<3.0.0',
 'SPARQLWrapper>=1.8.5,<2.0.0',
 'SQLAlchemy==1.4.41',
 'WSGIProxy2==0.4.2',
 'WebOb>=1.8.7,<2.0.0',
 'WebTest>=2.0.35,<3.0.0',
 'awscli>=1.25.36',
 'boto3>=1.24.36,<2.0.0',
 'botocore>=1.27.36,<2.0.0',
 'dcicsnovault>=8.0.1.0b3,<9.0.0.0',
 'dcicutils>=7.0.0,<8.0.0',
 'elasticsearch==7.13.4',
 'jsonschema_serialize_fork>=2.1.1,<3.0.0',
 'plaster-pastedeploy==0.6',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pyramid-multiauth>=0.9.0,<1',
 'pyramid-retry>=1.0,<2.0',
 'pyramid-tm>=2.4,<3.0',
 'pyramid==1.10.4',
 'pyramid_localroles>=0.1,<1',
 'pyramid_translogger>=0.1,<0.2',
 'requests>=2.23.0,<3.0.0',
 'structlog>=19.2.0,<20',
 'subprocess-middleware>=0.3.0,<0.4.0',
 'supervisor>=4.2.4,<5.0.0',
 'toml>=0.10.1,<1',
 'transaction>=3.0.0,<4.0.0',
 'translationstring==1.3',
 'uptime>=3.0.1,<4',
 'urllib3>=1.26.4,<2.0.0',
 'venusian>=1.2.0,<2.0.0',
 'waitress>=2.1.1,<3.0.0',
 'zope.deprecation>=4.4.0,<5.0.0',
 'zope.interface>=4.7.2,<5.0.0',
 'zope.sqlalchemy==1.6']

entry_points = \
{'console_scripts': ['add-image-tag = dcicutils.ecr_scripts:add_image_tag_main',
                     'show-global-env-bucket = '
                     'dcicutils.env_scripts:show_global_env_bucket_main',
                     'show-image-catalog = '
                     'dcicutils.ecr_scripts:show_image_catalog_main',
                     'show-image-manifest = '
                     'dcicutils.ecr_scripts:show_image_manifest_main',
                     'unrelease-most-recent-image = '
                     'dcicutils.ecr_scripts:unrelease_most_recent_image_main']}

setup_kwargs = {
    'name': 'encoded-core',
    'version': '0.0.1',
    'description': 'Core data models for Park Lab ENCODE based projects',
    'long_description': '============\nencoded-core\n============\n\n\nWelcome to ``encoded-core``!\n\nThis library contains common data models used across ENCODE style projects\nimplemented by the Park Lab.',
    'author': '4DN-DCIC Team',
    'author_email': 'support@4dnucleome.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/smaht-dac/encoded-core',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.10',
}


setup(**setup_kwargs)
