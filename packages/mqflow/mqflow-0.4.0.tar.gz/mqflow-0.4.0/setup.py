# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mqflow',
 'mqflow.broker',
 'mqflow.consumer',
 'mqflow.exceptions',
 'mqflow.pipeline',
 'mqflow.producer',
 'mqflow.utils']

package_data = \
{'': ['*']}

install_requires = \
['pyassorted>=0.7.0,<0.8.0',
 'pytz',
 'rich',
 'typing-extensions',
 'urllib3==1.26.16']

setup_kwargs = {
    'name': 'mqflow',
    'version': '0.4.0',
    'description': 'Simple python message queue framework is ready to serve.',
    'long_description': '# mqflow #\n\n[![dockhardman](https://circleci.com/gh/dockhardman/mqflow.svg?style=shield)](https://app.circleci.com/pipelines/github/dockhardman/mqflow)\n\nmqflow is a simple Python message queue framework, providing an easy-to-use and efficient method to handle tasks asynchronously.\n\nGithub: https://github.com/dockhardman/mqflow\n\n## Installation ##\n\n```bash\npip install mqflow\n```\n\n## Features ##\n\n- Easy-to-use: mqflow provides a Pythonic API that is both simple and effective for managing message queues.\n- Flexibility: It supports different types of message queues such as FIFO, priority, and circular queues.\n- Thread-Safe: mqflow uses Python\'s built-in queue library to ensure that your application is thread-safe.\n- Customizable: mqflow allows you to customize your producer and consumer functions, providing great flexibility to fit your needs.\n\n## Usage ##\n\nHere is an example of a simple message queue pipeline in memory:\n\n```python\nfrom mqflow.broker import QueueBroker\nfrom mqflow.producer import Producer\nfrom mqflow.consumer import Consumer\nfrom mqflow.pipeline import SequentialMessageQueue\n\n\ndef work(item, queue: "QueueBroker", *args, **kwargs):\n    print(f"[{item}] -> [{queue}] -> [{\'\'.join(args)}]")\n\n\ntask_num = 3\nmq = SequentialMessageQueue(\n    producers=[Producer(target=lambda: "Task sent", max_count=task_num)],\n    consumers=[Consumer(target=work, args=("Task received",), max_count=task_num)],\n    broker=QueueBroker(),\n)\nmq.run()\n# [Task sent] -> [QueueBroker(name=QueueBroker, maxsize=0)] -> [Task received]\n# [Task sent] -> [QueueBroker(name=QueueBroker, maxsize=0)] -> [Task received]\n# [Task sent] -> [QueueBroker(name=QueueBroker, maxsize=0)] -> [Task received]\n```\n\nThis creates a SequentialMessageQueue with a single producer that generates "Task sent" messages, and a single consumer that prints these messages with some additional information. The max_count parameter specifies the number of tasks the producer/consumer will handle before stopping. The broker manages the communication between producers and consumers.\n',
    'author': 'Allen Chou',
    'author_email': 'f1470891079@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.11.0',
}


setup(**setup_kwargs)
