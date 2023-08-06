"""
This module contains classes for loading, using, and exporting pretrained models.

The module defines an abstract base class `Estimator` that provides a common
interface for all text classification models. It also includes a concrete
implementation of the `Estimator` class, `SklearnEstimator`, which can load
trained scikit-learn models and make predictions on new data.
"""

import pathlib
from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import (
    Callable,
    List,
)

import numpy as np
import onnxruntime as rt
from lightgbm import LGBMClassifier
from nltk import TweetTokenizer
from onnxmltools.convert.lightgbm.operator_converters.LightGbm import (
    convert_lightgbm,
)
from skl2onnx import (
    to_onnx,
    update_registered_converter,
)
from skl2onnx.common.data_types import StringTensorType
from skl2onnx.common.shape_calculator import (
    calculate_linear_classifier_output_shapes,
)
from sklearn.utils.validation import check_is_fitted

from codcat.utils.types import PathLike

__all__ = [
    "Estimator",
    "SklearnEstimator",
]


_DEFAULT_TOKENIZER = TweetTokenizer().tokenize

update_registered_converter(
    LGBMClassifier,
    "LightGbmLGBMClassifier",
    calculate_linear_classifier_output_shapes,
    convert_lightgbm,
    options={"nocl": [True, False], "zipmap": [True, False, "columns"]},
)


# noinspection PyPep8Naming
class Estimator(metaclass=ABCMeta):
    """Abstract base class for Estimators."""

    @classmethod
    @abstractmethod
    def load(cls, path: PathLike) -> "Estimator":
        """
        Load model from .onnx file.

        Parameters
        ----------
        path : PathLike
            The path to the serialized model file.

        Returns
        -------
        Estimator
            The deserialized estimator object.
        """
        raise NotImplementedError

    @abstractmethod
    def predict(self, X):
        """
        Predict labels for X.

        Parameters
        ----------
        X : array-like of shape (n_samples, )
            The input samples.

        Returns
        -------
        array-like of shape (n_samples, )
            The predicted labels.
        """
        raise NotImplementedError

    @abstractmethod
    def predict_proba(self, X):
        """
        Predict probabilities for X.

        Parameters
        ----------
        X : array-like of shape (n_samples, )
            The input samples.

        Returns
        -------
        List of dicts
            The predicted probabilities.
        """
        raise NotImplementedError


# noinspection PyPep8Naming
# noinspection PyPep8Naming
class SklearnEstimator(Estimator):
    """
    A class for loading, saving, and making predictions using an ONNX-serialized Scikit-Learn model.

    Parameters
    ----------
    serialized_model : bytes
        A byte string representing the ONNX-serialized Scikit-Learn model.

    Attributes
    ----------
    _serialized_model : bytes
        A byte string representing the ONNX-serialized Scikit-Learn model.
    _session : onnxruntime.InferenceSession
        The ONNX runtime inference session for the serialized model.

    Methods
    -------
    load(path)
        Load a serialized model from a file.
    save(path)
        Save the serialized model to a file.
    from_sklearn(model)
        Convert a trained Scikit-Learn model to an ONNX-serialized model.
    predict(X, tokenizer=_DEFAULT_TOKENIZER)
        Make predictions on a set of inputs.
    predict_proba(X, tokenizer=_DEFAULT_TOKENIZER)
        Make probability predictions on a set of inputs.
    _transform(X, tokenizer)
        Apply the given tokenizer to a set of inputs and convert them to a numpy array.

    """

    def __init__(self, serialized_model):
        self._serialized_model = serialized_model
        self._session = rt.InferenceSession(serialized_model)

    @classmethod
    def load(cls, path: PathLike) -> "Estimator":
        """
        Load a SklearnEstimator object from a serialized model file.

        Parameters
        ----------
        path : PathLike
            The path to the serialized model file.

        Returns
        -------
        SklearnEstimator
            The deserialized SklearnEstimator object.
        """
        path = pathlib.Path(path)
        with open(path, "rb") as f:
            onnx_model = f.read()
        return cls(onnx_model)

    def save(self, path: PathLike):
        """
        Save the serialized model object to a file.

        Parameters
        ----------
        path : PathLike
            The path to the file where the serialized model object will be saved.
        """
        path = pathlib.Path(path)
        with open(path, "wb") as f:
            f.write(self._serialized_model)

    @classmethod
    def from_sklearn(cls, model) -> "SklearnEstimator":
        """
        Create a SklearnEstimator object from a Scikit-Learn model.

        Parameters
        ----------
        model : object
            The Scikit-Learn model object.

        Returns
        -------
        SklearnEstimator
            The SklearnEstimator object.
        """
        check_is_fitted(model)
        onnx_model = to_onnx(
            model, initial_types=[("text", StringTensorType([None, 1]))]
        )
        return cls(onnx_model.SerializeToString())

    # noinspection PyMethodMayBeStatic
    def _transform(self, X, tokenizer: Callable[[str], List[str]]):
        """
        Transform X into a numpy array.

        Parameters
        ----------
        X : array-like of shape (n_samples, )
            The input samples.
        tokenizer
            The tokenizer to use.

        Returns
        -------

        """
        return np.array([" ".join(tokenizer(text)) for text in X]).reshape(
            -1, 1
        )

    def predict(self, X, tokenizer=_DEFAULT_TOKENIZER):
        """
        Predict labels for X.

        Parameters
        ----------
        X : array-like of shape (n_samples,)
            Input data.
        tokenizer : callable, default=_DEFAULT_TOKENIZER
            The tokenizer function used to tokenize the input text.

        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            Predicted labels for X.
        """

        np_x = self._transform(X, tokenizer)
        test_data = {"text": np_x}
        return self._session.run(None, test_data)[0]

    def predict_proba(self, X, tokenizer=_DEFAULT_TOKENIZER):
        """
        Predict probabilities for X.

        Parameters
        ----------
        X : array-like of shape (n_samples,)
            Input data.
        tokenizer : callable, default=_DEFAULT_TOKENIZER
            The tokenizer function used to tokenize the input text.

        Returns
        -------
        proba : List[dict], shape (n_samples, n_classes)
            The class probabilities of the input samples.
        """

        np_x = self._transform(X, tokenizer)
        test_data = {"text": np_x}
        return self._session.run(None, test_data)[1]
