# Requirements
* [Python SymSpell](https://github.com/mammothb/symspellpy) (based on [SymSpell](https://github.com/wolfgarbe/SymSpell))
* [Compound splitter](https://github.com/dtuggener/CharSplit)
    * Add [setup.py](#setup.py) to install CharSplit with ```pip install .```
    * Copy the trained ngrams_probs.py model to your directory
* nltk 

## SymSpell
Install symspellpy with ```pip install -U symspellpy```.

## CharSplit
In order to install CharSplit as a module with ```pip install .```, add the [setup.py file](#setup.py) 
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

## NLTK
Download the punkt sentence tokenizer with: 
```
import nltk
nltk.download('punkt')
```