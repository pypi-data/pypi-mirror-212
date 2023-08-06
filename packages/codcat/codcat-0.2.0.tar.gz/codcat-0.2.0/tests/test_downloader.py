import hashlib
import os
import pathlib
from pathlib import Path

import pytest
import yaml
from hypothesis import (
    given,
    strategies as st,
)

# noinspection PyProtectedMember
from codcat.downloader import (
    _download,
    hashsum,
    load,
)
from codcat.models.estimator import Estimator


@given(text=st.text())
def test_hashsum(text):
    # create temporary file
    file = Path(__file__).parent.joinpath("resources", "test_file.txt")
    with open(file, "w") as f:
        f.write(text)
    # calculate hashsum of file using hashlib
    expected_hash = hashlib.md5(text.encode()).hexdigest()
    # calculate hashsum of file using hashsum function from models_loading_api module
    actual_hash = hashsum(file)
    assert actual_hash == expected_hash
    os.remove(file)


def test_download():
    with open(
        pathlib.Path(__file__).parent.joinpath("resources/test-manifest.yaml")
    ) as f:
        manifest = yaml.safe_load(f)
    _download("__test_tfidf-rf", manifest)
    with pytest.raises(KeyError):
        _download("unknown-model", manifest)


def test_load():
    manifest_path = pathlib.Path(__file__).parent.joinpath(
        "resources/test-manifest.yaml"
    )
    estimator = load("__test_tfidf-rf", manifest_path)
    assert isinstance(estimator, Estimator)
    predictions = estimator.predict(
        ["int * a = malloc(sizeof(int) * 10);", "def foo(bar): return bar"]
    )
    probabilities = estimator.predict_proba(
        ["int * a = malloc(sizeof(int) * 10);", "def foo(bar): return bar"]
    )
    assert predictions.shape == (2,)
    assert isinstance(probabilities, list)
    assert isinstance(probabilities[0], dict)
