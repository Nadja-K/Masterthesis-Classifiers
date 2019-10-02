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
├── demo.py                     
├── ngram_probs.py              # Trained CharSplit model
├── README.md                   
└── requirements.txt
```

## Setup
Python version: 3.7

Install dependencies:
```sh 
pip install -r requirements.txt
```

Install Sent2Vec:
```sh 
pip install git+https://github.com/epfml/sent2vec.git
```

Install CharSplit:
Follow the instructions [below](###CharSplit) to install the module.
Add the trained ```ngram_prob.py``` model from the original Sent2Vec git repo to the classifier [directory structure](##Directory structure).
 
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

Download a pre-trained BERT model from [here](https://github.com/google-research/bert).
This should include three files which should be added to the folder hierarchy as follows:
```
../bert/models/vocab.txt
../bert/models/bert_config.json
../bert/models/bert_model.ckpt
``` 

Finally, make sure the paths in the provided config file are set correctly. 
Otherwise please update the config file accordingly.

Note: A dataset database needs to be added to the folder hierarchy as follows:
``` 
../data/databases/dataset_name.db
```
Please ensure a dataset is provided in the folder specified in the config file. 
Otherwise the config file needs to be updated. 
To generate your own dataset please refer to the ```Data``` generation code, which is provided separately.

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

## Demo
In order to classify a query mention (or mention-sentence pair) run the following code:
``` 
python demo.py --classifier hybrid --mention Zielmarkierung --sentence Unter Zielmarkierung versteht man Verfahren zur Markierung meist militärischer Ziele.
```
Choose one of the four classifiers: bert, rule, hybrid, token.
For the token-level and BERT classifier, an additional parameter can be specified: ```--num_results```.
The rule-based and hybrid classifier do NOT support this parameter. 
The rule-based classifier will always return all entities that share the lowest distance.
The hybrid classifier on the other hand always returns exactly one entity.
Finally, it should be noted that it is possible for the token-level and BERT classifier to return less than [num_results]
entities if an entity has been suggested multiple times. In this case, the entity is only returned once with the 
lowest distance value.
The remaining options can be configured in the config file.

Furthermore, it is possible to specify a single entity (that has to be known to the classifier based on the provided
 dataset) for which potential synonyms will be identified including a distance value (a lower distance value is better).
Example:
``` 
python demo.py --classifier hybrid --entity_synonyms Mythologie --entity_synonyms_distance_threshold 0.85
```
The entity_synonyms_distance_threshold is an optional parameter that filters out all results with a higher 
distance value.
