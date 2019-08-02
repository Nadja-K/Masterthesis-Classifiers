## Directory structure
```sh
Classifiers
├── annoy_data                  # Tmp dir for annoy indices
├── bert                        # BERT related source files
├── classifiers                 # Source files for the classifiers
├── configs                     # Config files for running the classification or finetuning BERT
├── eval                        # Evaluation class
├── examples                    # Output examples for all classifiers
├── logs                        # Tmp dir for output logs
├── utils                       # Tools and utilities, including the annoy index class and heuristics
├── main.py                     
├── main_train.py               
├── ngram_probs.py              # Trained CharSplit model
├── README.md                   
└── requirements.txt
```

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
nltk.download('stopwords')
```

Download a German spacy model:
``` 
python -m spacy download de_core_news_sm
```

### CharSplit Setup
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

## Classification
In order to classify a query mention (or mention-sentence pair):
``` 
python demo.py --classifier=bert --mention Baum --sentence In der Informatik ist ein Baum eine Datenstruktur und ein abstrakter Datentyp.
```
All relevant options can be configured in the config file.
Choose one of the three classifiers: bert, rule, hybrid (the token-level classifier is not supported in the demo).