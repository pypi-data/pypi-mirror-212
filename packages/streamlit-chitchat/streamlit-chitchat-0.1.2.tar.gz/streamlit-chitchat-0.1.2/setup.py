# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit-chitchat',
 'streamlit-chitchat.streamlit_chitchat',
 'streamlit-chitchat.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'streamlit-chitchat',
    'version': '0.1.2',
    'description': '',
    'long_description': '<br>\n\n  \n\n<img  src="https://user-images.githubusercontent.com/7164864/217935870-c0bc60a3-6fc0-4047-b011-7b4c59488c91.png"  alt="Streamlit logo"  style="margin-top:50px"></img>\n\n  \n\n# streamlit-chitchat\n\n  \n\n**make chat messages easier to style in streamlit**\n\n  \n\nstreamlit-chitchat lets you style messages from the user and responses from a bot differently. you can also update an existing message, so that streamed tokens render as they are received. \n\n\n  \n\n## Installation\n\n  \n\nOpen a terminal and run:\n\n  \n\n```bash\n\n$  pip  install  streamlit-chitchat\n\n```\n\n## example use\n  \n\nin your streamlit app, insert:\n\n  \n\n```bash\n\nfrom streamlit-chitchat.chitchat import message\nmessage(\'hello, how are you?\', is_user=True)\nbot=message()\nfor w in \'excellent! have any plans for tonight?\'.split(\' \'):\n\tbot.write(w+\' \')\n```\n\n\n',
    'author': 'k4144',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
