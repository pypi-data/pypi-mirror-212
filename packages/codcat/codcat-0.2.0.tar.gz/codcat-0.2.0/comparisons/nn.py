import os
from functools import partial

import pandas as pd
import sklearn
from simpletransformers.classification import ClassificationModel
from sklearn.base import (
    BaseEstimator,
    ClassifierMixin,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

train_args = {
    "max_seq_length": 200,
    "num_train_epochs": 2,
    "train_batch_size": 32,
    "eval_batch_size": 32,
    "gradient_accumulation_steps": 1,
    "learning_rate": 5e-5,
    "save_steps": 50000,
    "wandb_project": "codcat",
    "evaluate_during_training": True,
    "evaluate_during_training_steps": 1000,
    "reprocess_input_data": True,
    "save_model_every_epoch": False,
    "overwrite_output_dir": True,
    "no_cache": True,
    "use_early_stopping": True,
    "early_stopping_patience": 3,
    "manual_seed": 4,
    "use_multiprocessing": False,
    "use_multiprocessing_for_evaluation": False,
    # 'special_tokens_list': special_tokens,
}

os.environ["TOKENIZERS_PARALLELISM"] = "true"


class SimpleTransformersWrapper(BaseEstimator, ClassifierMixin):
    def __init__(self, model_type, model_name):
        self.model_type = model_type
        self.model_name = model_name
        self.train_args = train_args.copy()
        self.train_args["wandb_kwargs"] = {"name": f"{model_type}-{model_name}"}
        self.train_args["output_dir"] = f"{model_type}-{model_name}-outputs"

        self._model = None
        self._label_encoder = None

    def fit(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.05, random_state=42
        )
        train_df = pd.DataFrame({"text": X_train, "labels": y_train})
        eval_df = pd.DataFrame({"text": X_test, "labels": y_test})
        self._label_encoder = LabelEncoder()
        train_df["labels"] = self._label_encoder.fit_transform(
            train_df["labels"]
        )
        eval_df["labels"] = self._label_encoder.transform(eval_df["labels"])
        self._model = ClassificationModel(
            self.model_type,
            self.model_name,
            num_labels=len(set(train_df["labels"])),
            args=self.train_args,
        )
        self._model.train_model(
            train_df,
            eval_df=eval_df,
            acc=partial(sklearn.metrics.f1_score, average="macro"),
        )

    def predict(self, X):
        return self._label_encoder.inverse_transform(
            self._model.predict(X.values.tolist())[0]
        )
