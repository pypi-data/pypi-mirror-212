# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compllments', 'compllments.utils']

package_data = \
{'': ['*'], 'compllments': ['models/*']}

install_requires = \
['accelerate>=0.19.0,<0.20.0',
 'bitsandbytes>=0.39.0,<0.40.0',
 'click>=8.1.3,<9.0.0',
 'einops>=0.6.1,<0.7.0',
 'emoji>=2.4.0,<3.0.0',
 'langchain>=0.0.180,<0.0.181',
 'openai>=0.27.7,<0.28.0',
 'poethepoet>=0.20.0,<0.21.0',
 'pynput>=1.7.6,<2.0.0',
 'pywhatkit>=5.4,<6.0',
 'transformers>=4.29.2,<5.0.0',
 'twilio>=8.2.1,<9.0.0']

entry_points = \
{'console_scripts': ['download = compllments.main:download',
                     'send = compllments.main:cli']}

setup_kwargs = {
    'name': 'compllments',
    'version': '0.1.0',
    'description': 'Send nice texts to your friends using LLMs',
    'long_description': '# compLLMents>\n\n## Description\n\nThis package enables you to send scheduled, uplifting, AI-generated text messages to yourself and your friends. \n\nIt works by first using am LLM to generate a batch of positive and complimentary messages in the language of choice. Then, a multilingual sentiment classifier scores all the generated posts and selects the most positive to send either as an SMS or over WhatsApp.\n\n\nDISCLAIMER: If you or someone you know is suffering from mental health difficulties, please seek professional *human* help instead of from chatbots. \n[Here]() is one good resource of many.\n\n\nProvide a short description explaining the what, why, and how of your project. Use the following questions as a guide:\n\n- What was your motivation?\n- Why did you build this project? (Note: the answer is not "Because it was a homework assignment.")\n- What problem does it solve?\n- What did you learn?\n\n## Table of Contents (Optional)\n\nIf your README is long, add a table of contents to make it easy for users to find what they need.\n\n- [Installation](#installation)\n- [Usage](#usage)\n- [Credits](#credits)\n- [License](#license)\n\n## Installation\n\nFirst, ensure that [`poetry`](https://python-poetry.org/docs/#installation) is installed. \n\n```\npoetry install\npoe install-pytorch\n```\n\nTo download files to store locally and save time of future downloads, run:\n`download -m path/on/huggingface`\n\nTo send SMS messages, first create a free [Twilio](https://www.twilio.com/en-us) account (note: Twilio automatically prepends the message `blah` to free-tier accounts). Copy your credentials from the dashboard into the `TWILIO_CONFIG` dictionary in `config.py`. An example config will look like:\n```\n {\n    "account_sid": "a_string",\n    "auth_token": "a_token",\n}\n```\n\n## Usage\n\nProvide instructions and examples for use. Include screenshots as needed.\n\nTo add a screenshot, create an `assets/images` folder in your repository and upload your screenshot to it. Then, using the relative filepath, add it to your README using the following syntax:\n\n    ```md\n    ![alt text](assets/images/screenshot.png)\n    ```\n\nTexts are sent by running:\n```\nsend -r recipient-name -s sender-name -n +11234567890 -l language -b -t sms\n```\n\n`send --help` explains the parameter options.\n\nYou can send custom messages by chaning the text in the `TEMPLATE` object in `main.py`\n\nYou can set custom model configuration in the `INFERENCE_CONFIG` object in `conifg.py` including swapping out models, increasing the output length by chaning `max_new_tokens` or increasing the randomness in reponses by raising `temperature` or `top_p`.\n\n\nBelow are some example text generations\n```\n```\n\nAnd here are the sentiment scores for them\n```\n```\n\nTo schedule texts to be sent at regular intervals, \n- crontab setup\n\n\n\n## Tests\n\n\n## Credits\n\nList your collaborators, if any, with links to their GitHub profiles.\n\nIf you used any third-party assets that require attribution, list the creators with links to their primary web presence in this section.\n\nIf you followed tutorials, include links to those here as well.\n\n\n## License\n\nMIT License\n\nCopyright (c) [year] [fullname]\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\nRoadmap\n\n1.   Locally hosted\n2.   Ping API\n3.   Multilingual\n4.   SMS + WhatsApp support\n5.   Select nicest\n6.   cron job scheduling\n7.   publish to pypi\n\n',
    'author': 'Austin Botelho',
    'author_email': 'austinbotelho@nyu.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
