# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['surprisal']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.23.1,<2.0.0',
 'openai>=0.23.0,<0.24.0',
 'pandas>=1.4.3,<2.0.0',
 'plotext>=5.0.2,<6.0.0',
 'torch>=1.12.0,<2.0.0',
 'transformers>=4.20.1,<5.0.0']

setup_kwargs = {
    'name': 'surprisal',
    'version': '0.1.3',
    'description': 'A package to conveniently compute surprisals for text sequences and subsequences',
    'long_description': '# surprisal\nCompute surprisal from language models!\n\n`surprisal` supports most Causal Language Models (`GPT2`- and `GPTneo`-like models) from Huggingface or local checkpoint, \nas well as `GPT3` models from OpenAI using their API!\n\nMasked Language Models (`BERT`-like models) are in the pipeline and will be supported at a future time. \n\n## Usage\n\nThe snippet below computes per-token surprisals for a list of sentences\n```python\nfrom surprisal import AutoHuggingFaceModel\n\nsentences = [\n    "The cat is on the mat",\n    "The cat is on the hat",\n    "The cat is on the pizza",\n    "The pizza is on the mat",\n    "I told you that the cat is on the mat",\n    "I told you the cat is on the mat",\n]\n\nm = AutoHuggingFaceModel.from_pretrained(\'gpt2\')\nm.to(\'cuda\') # optionally move your model to GPU!\n\nfor result in m.surprise(sentences):\n    print(result)\n```\nand produces output of this sort:\n```\n       The       Ġcat        Ġis        Ġon       Ġthe       Ġmat  \n     3.276      9.222      2.463      4.145      0.961      7.237  \n       The       Ġcat        Ġis        Ġon       Ġthe       Ġhat  \n     3.276      9.222      2.463      4.145      0.961      9.955  \n       The       Ġcat        Ġis        Ġon       Ġthe     Ġpizza  \n     3.276      9.222      2.463      4.145      0.961      8.212  \n       The     Ġpizza        Ġis        Ġon       Ġthe       Ġmat  \n     3.276     10.860      3.212      4.910      0.985      8.379  \n         I      Ġtold       Ġyou      Ġthat       Ġthe       Ġcat        Ġis        Ġon       Ġthe       Ġmat \n     3.998      6.856      0.619      2.443      2.711      7.955      2.596      4.804      1.139      6.946 \n         I      Ġtold       Ġyou       Ġthe       Ġcat        Ġis        Ġon       Ġthe       Ġmat  \n     3.998      6.856      0.619      4.115      7.612      3.031      4.817      1.233      7.033 \n```\n\n### extracting surprisal over a substring\n\nA surprisal object can be aggregated over a subset of tokens that best match a span of words or characters. \nWord boundaries are inherited from the model\'s standard tokenizer, and may not be consistent across models,\nso using character spans when slicing is the default and recommended option.\nSurprisals are in log space, and therefore added over tokens during aggregation.  For example:\n```python\n>>> [s] = m.surprise("The cat is on the mat")\n>>> s[3:6, "word"] \n12.343366384506226\nĠon Ġthe Ġmat\n>>> s[3:6, "char"]\n9.222099304199219\nĠcat\n>>> s[3:6]\n9.222099304199219\nĠcat\n```\n\n### GPT-3 using OpenAI API\n\nIn order to use a GPT-3 model from OpenAI\'s API, you will need to obtain your organization ID and user-specific API key using your account.\nThen, use the `OpenAIModel` in the same way as a Huggingface model.\n\n```python\n\nimport surprisal\nm = surprisal.OpenAIModel(model_id=\'text-davinci-002\',\n                          openai_api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", \n                          openai_org="org-xxxxxxxxxxxxxxxxxxxxxxxx")\n```\n\nThese values can also be passed using environment variables, `OPENAI_API_KEY` and `OPENAI_ORG` before calling a script.\n\nYou can also call `Surprisal.lineplot()` to visualize the surprisals:\n\n```python\nfrom matplotlib import pyplot as plt\n\nf, a = None, None\nfor result in m.surprise(sentences):\n    f, a = result.lineplot(f, a)\n\nplt.show()\n```\n\n![](https://i.imgur.com/HusVOUq.png)\n\n\n`surprisal` also has a minimal CLI:\n```python\npython -m surprisal -m distilgpt2 "I went to the train station today."\n      I      Ġwent        Ġto       Ġthe     Ġtrain   Ġstation     Ġtoday          . \n  4.984      5.729      0.812      1.723      7.317      0.497      4.600      2.528 \n\npython -m surprisal -m distilgpt2 "I went to the space station today."\n      I      Ġwent        Ġto       Ġthe     Ġspace   Ġstation     Ġtoday          . \n  4.984      5.729      0.812      1.723      8.425      0.707      5.182      2.574\n```\n\n\n## Installing\n`pip install surprisal`\n\n\n## Acknowledgments\n\nInspired from the now-inactive [`lm-scorer`](https://github.com/simonepri/lm-scorer); thanks to\nfolks from [CPLlab](http://cpl.mit.edu) and [EvLab](https://evlab.mit.edu) for comments and help.\n\n\n## License \n[MIT License](./LICENSE).\n(C) 2022-23, contributors.\n',
    'author': 'aalok-sathe',
    'author_email': 'asathe@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aalok-sathe/surprisal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
