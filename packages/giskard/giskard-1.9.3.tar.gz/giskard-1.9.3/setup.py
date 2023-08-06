# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['giskard',
 'giskard.client',
 'giskard.ml_worker',
 'giskard.ml_worker.bridge',
 'giskard.ml_worker.core',
 'giskard.ml_worker.exceptions',
 'giskard.ml_worker.server',
 'giskard.ml_worker.testing',
 'giskard.ml_worker.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'cloudpickle>=2.1.0,<3.0.0',
 'eli5>=0.13.0,<0.14.0',
 'grpcio-status>=1.46.3,<=1.51.1',
 'grpcio>=1.46.3,<=1.51.1',
 'importlib_metadata>=4.11.4,<5.0.0',
 'ipython>=7.0.0,<8.0.0',
 'lockfile>=0.12.2,<0.13.0',
 'mixpanel>=4.10.0,<5.0.0',
 'numpy>=1.21.6,<1.22.0',
 'pandas>=1.3.5,<2.0.0',
 'protobuf>=3.9.2,<4.0.0',
 'psutil>=5.9.2,<6.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-daemon>=2.3.1,<3.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.28.1,<3.0.0',
 'scikit-learn>=1.0.0,<1.1.0',
 'scipy>=1.7.2,<1.8',
 'setuptools>=65.4.1,<68.0.0',
 'shap>=0.41.0,<0.42.0',
 'tenacity>=8.1.0,<9.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'zstandard==0.20.0']

entry_points = \
{'console_scripts': ['giskard = giskard.cli:cli']}

setup_kwargs = {
    'name': 'giskard',
    'version': '1.9.3',
    'description': 'The testing framework dedicated to ML models, from tabular to LLMs',
    'long_description': '<p align="center">\n  <img alt="giskardlogo" src="https://github.com/Giskard-AI/giskard/blob/9f9f9994ab5deb503ed9c64e672982432a493cca/readme/giskard_logo.png?raw=true">\n</p>\n<h1 align="center" weight=\'300\' >The testing framework dedicated to ML models, from tabular to LLMs</h1>\n<h3 align="center" weight=\'300\' >Scan AI models to detect risks of biases, performance issues and errors. In 4 lines of code. </h3>\n<p align="center">\n   <a href="https://github.com/Giskard-AI/giskard/releases">\n      <img alt="GitHub release" src="https://img.shields.io/github/v/release/Giskard-AI/giskard">\n  </a>\n <a href="https://github.com/Giskard-AI/giskard/blob/main/LICENSE">\n     <img alt="GitHub" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg">\n </a>\n  <a href="https://github.com/Giskard-AI/giskard/actions/workflows/build.yml">\n    <img alt="build" src="https://github.com/Giskard-AI/giskard/actions/workflows/build.yml/badge.svg?branch=main"/>\n </a>\n  <a href="https://gisk.ar/discord">\n    <img alt="Giskard on Discord" src="https://img.shields.io/discord/939190303397666868?label=Discord"/>\n  </a>\n  <a rel="me" href="https://fosstodon.org/@Giskard"></a>\n</p>\n<h3 align="center">\n   <a href="https://docs.giskard.ai/en/latest/getting-started/quickstart.html"><b>Documentation</b></a> &bull;\n   <a href="https://www.giskard.ai/knowledge-categories/blog/?utm_source=github&utm_medium=github&utm_campaign=github_readme&utm_id=readmeblog"><b>Blog</b></a> &bull;  \n  <a href="https://www.giskard.ai/?utm_source=github&utm_medium=github&utm_campaign=github_readme&utm_id=readmeblog"><b>Website</b></a> &bull;\n  <a href="https://gisk.ar/discord"><b>Discord Community</b></a> &bull;\n  <a href="https://www.giskard.ai/about?utm_source=github&utm_medium=github&utm_campaign=github_readme&utm_id=readmeblog#advisors"><b>Advisors</b></a>\n </h3>\n<br />\n\n## Table of contents\n1. [What is Giskard?](#what-is-giskard)\n2. [Getting started](#getting-started)\n  * [Installation](#installation)\n  * [Scan your model to detect vulnerabilities](#scan-your-model-to-detect-vulnerabilities)\n  * [Automatically generate a test suite](#automatically-generate-a-test-suite-based-on-the-scan-results)\n  * [Upload your test suite to the Giskard server](#upload-your-test-suite-to-the-giskard-server)\n3. [How to contribute](#how-to-contribute)\n4. [Like what we\'re doing?](#like-what-were-doing)\n\n\n<div id="what-is-giskard">\n\n## What is Giskard?\n\n**Giskard is an open-source testing framework dedicated to ML models, from tabular models to LLMs.**\n\nTesting Machine Learning applications can be tedious. Since ML models depend on data, testing scenarios depend on the domain specificities and are often infinite. \n\n<p align="center">\n<strong>Where to start testing? Which tests to implement? What issues to cover? How to implement the tests?</strong>\n</p>\n\n<p align="center">\n  <img src="https://giskard.readthedocs.io/en/latest/_images/hey.png" alt="hey" width="20%">\n</p>\n\nAt Giskard, we believe that Machine Learning needs its own testing framework. Created by ML engineers for ML engineers, Giskard enables you to:\n\n- **Scan your model to find dozens of vulnerabilities**: The Giskard scan automatically detects vulnerability issues such as performance bias, data leakage, unrobustness, spurious correlation, overconfidence, underconfidence, unethical issue, etc.\n\n<p align="center">\n  <img src="https://github.com/Giskard-AI/giskard/blob/9f9f9994ab5deb503ed9c64e672982432a493cca/readme/scan_example.png?raw=true" alt="Scan Example" width="700px">\n</p>\n\n- **Instantaneously generate domain-specific tests**: Giskard automatically generates relevant tests based on the vulnerabilities detected by the scan. You can easily customize the tests depending on your use case by defining domain-specific data slicers and transformers as fixtures of your test suites.\n\n<p align="center">\n  <img src="https://github.com/Giskard-AI/giskard/blob/9f9f9994ab5deb503ed9c64e672982432a493cca/readme/test_suite_example.png?raw=true" alt="Scan Example" width="700px">\n</p>\n\n- **Leverage the Quality Assurance best practices of the open-source community**: The Giskard catalog enables you to easily contribute and load data slicing & transformation functions such as AI-based detectors (toxicity, hate, etc.), generators (typos, paraphraser, etc.), or evaluators. Inspired by the Hugging Face philosophy, the aim of Giskard is to become the open-source hub of ML Quality Assurance.\n\n<p align="center">\n  <img src="https://github.com/Giskard-AI/giskard/blob/9f9f9994ab5deb503ed9c64e672982432a493cca/readme/catalog_example.png?raw=true" alt="Scan Example" width="700px">\n</p>\n\nAnd of course, Giskard works with any model, any environment and integrates seamlessly with your favorite tools ⤵️ <br/>\n<p align="center">\n  <img width=\'600\' src="https://github.com/Giskard-AI/giskard/blob/9f9f9994ab5deb503ed9c64e672982432a493cca/readme/tools.png?raw=true">\n</p>\n<br/>\n</div>\n\n<div id="getting-started">\n\n## Getting started\n\n<div id="installation">\n\n### Installation\n```sh\npip install "giskard[server]==2.0.0b2"\n\ngiskard server start\n```\n\nThat\'s it. Access at http://localhost:19000\n</div>\n<div id="scan-your-model-to-detect-vulnerabilities">\n\n### Scan your model to detect vulnerabilities\n\nAfter having wrapped your [model](https://docs.giskard.ai/en/latest/guides/wrap_model/index.html) & [dataset](https://docs.giskard.ai/en/latest/guides/wrap_dataset/index.html), you can scan your model for vulnerabilities using:\n\n```python\nimport giskard\n\nmodel, df = giskard.demo.titanic()\n\nmodel = giskard.Model(model=model, model_type="classification")\ndataset = giskard.Dataset(\n    df=df,\n    target="Survived",\n    cat_columns=["Pclass", "Sex", "SibSp", "Parch", "Embarked"],\n)\n\nscan_results = giskard.scan(model, dataset)\n```\n\nOnce the scan completes, you can display the results directly in your notebook:\n\n```python\ndisplay(scan_results)  # in your notebook\n```\n</div>\n\n<div id="automatically-generate-a-test-suite-based-on-the-scan-results">\n\n### Automatically generate a test suite based on the scan results\n\nIf the scan found potential issues in your model, you can automatically generate a test suite.\n\nGenerating a test suite from your scan results will enable you to:\n- Turn the issues you found into actionable tests that you can directly integrate in your CI/CD pipeline\n- Diagnose your vulnerabilities and debug the issues you found in the scan\n\n```python\ntest_suite = scan_results.generate_test_suite("My first test suite")\n\n# You can run the test suite locally to verify that it reproduces the issues\ntest_suite.run()\n```\n</div>\n<div id="upload-your-test-suite-to-the-giskard-server">\n\n### Upload your test suite to the Giskard server\n\nYou can then upload the test suite to the local Giskard server. This will enable you to:\n- Compare the quality of different models to decide which one to promote\n- Debug your tests to diagnose the identified issues\n- Create more domain-specific tests relevant to your use case\n- Share results, and collaborate with your team to integrate business feedback\n\nFirst, install the Giskard server by following [this documentation](https://docs.giskard.ai/en/latest/guides/installation_app/index.html)\n\n```python\n# Create a Giskard client after having installed the Giskard server (see documentation)\ntoken = "API_TOKEN"  # Find it in Settings in the Giskard server\nclient = GiskardClient(\n    url="http://localhost:19000", token=token  # URL of your Giskard instance\n)\n\nmy_project = client.create_project("my_project", "PROJECT_NAME", "DESCRIPTION")\n\n# Upload to the current project\ntest_suite.upload(client, "my_project")\n\n```\n    \nFor more information on uploading to your local Giskard server, go to the [Upload an object to the Giskard server](https://docs.giskard.ai/en/latest/guides/upload/index.html) page.\n</div>\n</div>\n\n<div id="how-to-contribute">\n\n## How to contribute\nWe welcome contributions from the Machine Learning community!\n\nRead this [guide](https://github.com/Giskard-AI/giskard/blob/main/CONTRIBUTING.md) to get started.\n</div>\n<br />\n<div id="like-what-were-doing">\n\n## Like what we\'re doing?\n\n🌟 [Leave us a star](https://github.com/Giskard-AI/giskard), it helps the project to get discovered by others and keeps us motivated to build awesome open-source tools! 🌟\n\n❤️ You can also [sponsor us](https://github.com/sponsors/Giskard-AI) on GitHub. With a monthly sponsor subscription, you can get a sponsor badge and get your bug reports prioritized. We also offer one-time sponsoring if you want us to get involved in a consulting project, run a workshop, or give a talk at your company.\n</div>\n',
    'author': 'Giskard AI',
    'author_email': 'hello@giskard.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.5,<3.11',
}


setup(**setup_kwargs)
