"""This module provides CLI interface."""
import json
from pathlib import Path

import click
import pandas as pd
from lightgbm import LGBMClassifier
from nltk import (
    NLTKWordTokenizer,
    TweetTokenizer,
)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from codcat.models.estimator import SklearnEstimator

NAME2TOK = {"nltk": NLTKWordTokenizer(), "tweet": TweetTokenizer()}


def validate_input_dataframe(ctx, param, value):
    try:
        df = pd.read_csv(value)
    except pd.errors.ParserError:
        raise click.BadParameter("Input dataset must be in `csv` format.")

    if "code" not in df.columns or "language" not in df.columns:
        raise click.BadParameter(
            "Input dataframe must have `code` and `language` columns."
        )

    return df


def validate_tokenizer(ctx, param, value):
    value = value.lower()
    if value not in NAME2TOK:
        raise click.BadParameter(
            f"`{value}` is not one of {', '.join(NAME2TOK.keys())}."
        )
    return NAME2TOK[value]


@click.group()
def cli():
    pass


@click.command()
@click.argument(
    "dataset",
    type=click.Path(exists=True, path_type=Path),
    callback=validate_input_dataframe,
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Output to preprocessed data",
    default=Path.cwd().joinpath("preprocessed"),
)
@click.option(
    "--tokenizer",
    "-t",
    "tokenizer",
    callback=validate_tokenizer,
    help="Tokenizer name",
    default="nltk",
)
def preprocess(dataset, output, tokenizer):
    dataset["code"] = dataset["code"].apply(
        lambda x: " ".join(tokenizer.tokenize(x))
    )
    dataset.to_csv(output, index=None)


@click.command()
@click.argument(
    "dataset",
    type=click.Path(exists=True, path_type=Path),
    callback=validate_input_dataframe,
)
@click.option("--test-size", type=float, default=0.33)
@click.option("--random-state", type=int, default=42)
@click.option(
    "--output-train",
    type=click.Path(path_type=Path),
    help="Output to train data",
    default=Path.cwd().joinpath("train.csv"),
)
@click.option(
    "--output-test",
    type=click.Path(path_type=Path),
    help="Output to test data",
    default=Path.cwd().joinpath("train.csv"),
)
def split(dataset, test_size, random_state, output_train, output_test):
    train, test = train_test_split(
        dataset, test_size=test_size, random_state=random_state
    )
    train.to_csv(output_train)
    test.to_csv(output_test)


@click.command()
@click.argument(
    "train-dataset",
    type=click.Path(exists=True, path_type=Path),
    callback=validate_input_dataframe,
)
@click.option(
    "--lowercase",
    is_flag=True,
    show_default=True,
    default=True,
    help="Use lowercase to text",
)
@click.option("--token-pattern", type=str, default=r"\S+")
@click.option("--random-state", type=int, default=42)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Output to trained model",
    default=Path.cwd().joinpath("model.onnx"),
)
def train(train_dataset, lowercase, token_pattern, random_state, output):
    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=lowercase, token_pattern=token_pattern
                ),
            ),
            ("lgbm", LGBMClassifier(random_state=random_state)),
        ]
    )
    pipeline.fit(train_dataset["code"], train_dataset["language"])
    estimator = SklearnEstimator.from_sklearn(pipeline)
    estimator.save(output)


@click.command()
@click.argument(
    "test-dataset",
    type=click.Path(exists=True, path_type=Path),
    callback=validate_input_dataframe,
)
@click.option(
    "--model-path",
    type=click.Path(exists=True, path_type=Path),
    help="ONNX dump of model",
)
@click.option(
    "--report-output",
    type=click.Path(path_type=Path),
    help="Report to output",
)
def evaluate(test_dataset, model_path, report_output):
    estimator = SklearnEstimator.load(model_path)
    preds = estimator.predict(test_dataset["code"])
    report = classification_report(
        test_dataset["language"], preds, digits=3, output_dict=True
    )

    Path(report_output.parent).mkdir(parents=True, exist_ok=True)

    with open(report_output, "w") as f:
        f.write(json.dumps(report, indent=4))


cli.add_command(preprocess)
cli.add_command(split)
cli.add_command(train)
cli.add_command(evaluate)


if __name__ == "__main__":
    cli()
