# Codcat

Natural Language Processing (NLP) is a rapidly growing field that aims to help machines understand and interpret human language. With the increasing use of code repositories like Github, there is a growing need to accurately categorize program code by programming language. This is particularly important in large repositories where multiple programming languages are used, as it allows developers to easily navigate and search for specific code snippets.

The goal of this NLP project is to develop a model that can automatically categorize program code by programming language. The model will be trained on a large dataset of code snippets from various programming languages, and will use NLP techniques to extract features and patterns from the code.

The project will involve several steps, including data collection, pre-processing, feature extraction, model selection and evaluation. The dataset for the project will be sourced from various public code repositories, including GitHub, GitLab, Stackoverflow. The collected data will then be pre-processed to remove irrelevant information and to standardize the format of the code snippets. This will involve techniques such as tokenization and stop-word removal.

Once the data is pre-processed, features will be extracted from the code snippets using NLP techniques. This will involve using methods such as Bag of Words (BoW), Term Frequency-Inverse Document Frequency (TF-IDF), and Embeddings to capture the semantics of the code. These features will then be used to train and evaluate several machine learning models, including Naive Bayes, RandomForest, CNN, RNN, Transformers.

The final model will be evaluated on a test set of code snippets to assess its accuracy and generalizability.

## Prerequisites

On your PC with local run you must have Python >= 3.9

## Installation
Install `codcat` with pip:

```bash
pip install codcat
```

or with your favorite package manager.

## Example

### Input

```python
from codcat.downloader import load
model = load('base-tiny')
print(model.predict(['def foo(bar): return bar', '#include <stdio.h>']))
```

### Output

```python
['python' 'c']
```

## Authors

- Templin Konstantin <1qnbhd@gmail.com>
