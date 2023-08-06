# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kpops',
 'kpops.cli',
 'kpops.component_handlers',
 'kpops.component_handlers.helm_wrapper',
 'kpops.component_handlers.kafka_connect',
 'kpops.component_handlers.schema_handler',
 'kpops.component_handlers.topic',
 'kpops.component_handlers.utils',
 'kpops.components',
 'kpops.components.base_components',
 'kpops.components.base_components.models',
 'kpops.components.streams_bootstrap',
 'kpops.components.streams_bootstrap.producer',
 'kpops.components.streams_bootstrap.streams',
 'kpops.pipeline_generator',
 'kpops.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'cachetools>=5.2.0,<6.0.0',
 'dictdiffer>=0.9.0,<0.10.0',
 'pydantic[dotenv]>=1.10.8,<2.0.0',
 'pyhumps>=3.7.3,<4.0.0',
 'python-schema-registry-client>=2.4.1,<3.0.0',
 'requests>=2.28.0,<3.0.0',
 'rich>=12.4.4,<13.0.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['kpops = kpops.cli.main:app']}

setup_kwargs = {
    'name': 'kpops',
    'version': '1.1.5',
    'description': 'KPOps is a tool to deploy Kafka pipelines to Kubernetes',
    'long_description': '# KPOps\n\n[![Build status](https://github.com/bakdata/kpops/actions/workflows/ci.yaml/badge.svg)](https://github.com/bakdata/kpops/actions/workflows/ci.yaml)\n[![pypi](https://img.shields.io/pypi/v/kpops.svg)](https://pypi.org/project/kpops)\n[![versions](https://img.shields.io/pypi/pyversions/kpops.svg)](https://github.com/bakdata/kpops)\n[![license](https://img.shields.io/github/license/bakdata/kpops.svg)](https://github.com/bakdata/kpops/blob/main/LICENSE)\n\n## Key features\n\n- **Deploy Kafka apps to Kubernetes**: KPOps allows to deploy consecutive Kafka Streams applications and producers using an easy-to-read and -write pipeline definition.\n- **Manage Kafka Connectors**: KPOps connects with your Kafka Connect cluster and deploys, validates, and deletes your connectors.\n- **Configure multiple pipelines and steps**: KPOps has various abstractions that simplify configuring multiple pipelines and steps within pipelines by sharing common configuration between different components, such as producers or streaming applications.\n- **Handle your topics and schemas**: KPOps not only creates and deletes your topics but also registers and deletes your schemas.\n- **Clean termination of Kafka components**: KPOps removes your pipeline components (i.e., Kafka Streams applications) from the Kubernetes cluster _and_ cleans up the component-related states (i.e., removing/resetting offset of Kafka consumer groups).\n- **Preview your pipeline changes**: With the KPOps dry-run, you can ensure your pipeline definition is set up correctly. This helps to minimize downtime and prevent potential errors or issues that could impact your production environment.\n\n## Documentation\n\nFor detailed usage and installation instructions, check out\nthe [documentation](https://bakdata.github.io/kpops/latest/user/what-is-kpops/).\n\n## Install KPOps\n\nKPOps comes as a [PyPI package](https://pypi.org/project/kpops/). \nYou can install it with [pip](https://github.com/pypa/pip):\n\n```shell\npip install kpops\n```\n\n## Contributing\n\nWe are happy if you want to contribute to this project.\nIf you find any bugs or have suggestions for improvements, please open an issue.\nWe are also happy to accept your PRs.\nJust open an issue beforehand and let us know what you want to do and why.\n\n## License\n\nKPOps is licensed under the [MIT License](https://github.com/bakdata/kpops/blob/main/LICENSE).\n',
    'author': 'bakdata',
    'author_email': 'opensource@bakdata.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bakdata/kpops',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
