import os

import numpy as np
import pytest
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from codcat.models.estimator import SklearnEstimator


def test_sklearn_estimator():
    corpus = [
        "def foo(bar): return bar",
        "#include <stdio.h>",
        """data Name = Mononym String
          | FirstLastName String String
          | FullName String String String""",
    ]
    labels = ["python", "c", "haskell"]
    pipeline = Pipeline(
        [
            ("vectorizer", CountVectorizer()),
            ("classifier", LogisticRegression()),
        ]
    )
    pipeline.fit(corpus, labels)

    model = SklearnEstimator.from_sklearn(pipeline)
    model.save("test_model.onnx")
    model2 = SklearnEstimator.load("test_model.onnx")

    assert isinstance(model2.predict(["def foo(bar): return bar"]), np.ndarray)
    assert isinstance(model2.predict_proba(["def foo(bar): return bar"]), list)

    os.remove("test_model.onnx")


def test_sklearn_estimator_not_fitted():
    pipeline = Pipeline(
        [
            ("vectorizer", CountVectorizer()),
            ("classifier", LogisticRegression()),
        ]
    )
    with pytest.raises(ValueError):
        SklearnEstimator.from_sklearn(pipeline)
