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
    'version': '0.1.1',
    'description': 'Send nice texts to your friends using LLMs',
    'long_description': '# compLLMents\n\n<!-- ![GitHub all releases](https://img.shields.io/github/downloads/botelhoa/compLLMents/total?style=plastic)\n![MIT License](https://img.shields.io/bower/l/compLLMents?style=plastic) -->\n\n## Description\n\nThis package enables you to send scheduled, uplifting, AI-generated text messages to your friends. \n\nIt works by first using an LLM to generate a batch of positive and complimentary messages in the language of your choice. Then, a multilingual sentiment classifier scores all the generated posts and selects the most positive to send either as an SMS or over WhatsApp. [Here](https://colab.research.google.com/drive/1gfTlCWNFgpHdvLR5g8o-OV_a30Pfps60?usp=sharing) is the accompanying Colab notebook.\n\n\nDISCLAIMER: If someone you know is suffering from mental health difficulties, please reach out person-to-person or encourage them to seek professional *human* help instead of from chatbots. [Here](https://www.nimh.nih.gov/health/find-help) is one good resource of many.\n\n\n## Table of Contents\n\n- [Installation](#installation)\n- [Usage](#usage)\n- [License](#license)\n\n## Installation\n\nFirst, ensure that [`poetry`](https://python-poetry.org/docs/#installation) is installed. \n\n```\npoetry install\npoe install-pytorch\n```\n\nTo download files to store locally and save time of future downloads, run:\n\n```\ndownload -m path/on/huggingface\n```\n\nTo send SMS messages, first create a free [Twilio](https://www.twilio.com/en-us) account and create a phone number (note: Twilio automatically prepends the message `Sent from your Twilio trial account` to free-tier accounts). Copy your credentials from the dashboard into the `TWILIO_CONFIG` dictionary in `config.py`. An example config will look like:\n\n```\n {\n    "account_sid": "a_string",\n    "auth_token": "a_token",\n    "from_": "+11234567890",\n}\n```\nTo send WhatsApp messages, you must log in from your computer.\n\n## Usage\n\nTexts are sent by running:\n\n```\nsend -r recipient-name -s sender-name -n +11234567890 -l language -b -t type\n```\n\n`send --help` explains the parameter options. Pass your OpenAI API key using `-o` to use their models.\n\nYou can send custom messages by chaning the text in the `TEMPLATE` object in `main.py`\n\nYou can set custom model configuration in the `INFERENCE_CONFIG` object in `conifg.py` including swapping out models, increasing the output length by chaning `max_new_tokens` or increasing the randomness in reponses by raising `temperature` or `top_p`. The default language generation model is `mosaicml/mpt-7b-instruct` which is the [best performing open-sourced LLM](https://gpt4all.io/index.html) at the time of creation. The default sentiment analysis model is `cardiffnlp/xlm-roberta-base-sentiment-multilingual` which supports 8 languagees: `arabic`, `english`, `french`, `german`, `hindi`, `italian`, `portuguese`, and, `spanish`. \n\n\nTo schedule texts to be sent at regular intervals, create a crontab similar to the example in `cron`.\n\n\n## Tests\n\nForethcoming...\n\n\n## License\n\nMIT License\n\nCopyright (c) [year] [fullname]\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n',
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
