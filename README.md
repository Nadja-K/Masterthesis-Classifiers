## Directory structure

classifiers
├── annoy_data
|   └── ...
|
├── bert
|   └── ...
|
├── classifiers
|   └── ...
|
├── configs
|   └── bert_train_config.ini
|   └── config.ini
|   └── remote_config.ini
|   └── logging_config.ini
|
├── eval
|   └── ...
|
├── examples
|   └── ...
|
├── heuristics
|   └── ...
|
├── index
|   └── ...
|
├── logs
|   └── ...
|
├── utils
|   └── ...
|
├── main.py
├── main_train.py
├── ngram_probs.py
├── README.md
└── requirements.txt


## Setup
Install dependencies:
```sh 
pip install -r requirements.txt
```

Install sent2vec:
```sh 
pip install git+https://github.com/epfml/sent2vec.git
```

Install CharSplit:
Follow the instructions [below](###CharSplit) to install the module.
Add the trained ```ngram_prob.py``` model from the original git repo to the classifier [directory structure](##Directory structure)
 
Download the nltk punkt sentence tokenizer: 
```
import nltk
nltk.download('punkt')
```

### CharSplit
In order to install CharSplit as a module with ```pip install .```, first clone the 
[repository](https://github.com/dtuggener/CharSplit) and add the [setup.py file](####setup.py) 
as seen in the following folder structure:
```
CharSplit/
    LICENSE
    README.md
    setup.py
    CharSplit
        __init__.py
        char_split_train.py
        char_split.py
```

#### setup.py  
``` 
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CharSplit",
    version="0.1",
    author="dtuggener",
    author_email="",
    description="An ngram-based compound splitter for German",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dtuggener/CharSplit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GPL-3.0",
        "Operating System :: Linux",
    ],
)
```
