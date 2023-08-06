from pathlib import Path

import joblib
import numpy as np
from nltk import TweetTokenizer
from pygments.lexers import (
    BashLexer,
    CLexer,
    CppLexer,
    CSharpLexer,
    CssLexer,
    HaskellLexer,
    JavaLexer,
    JavascriptLexer,
    LuaLexer,
    ObjectiveCLexer,
    PerlLexer,
    PhpLexer,
    PythonLexer,
    RubyLexer,
    ScalaLexer,
    SLexer,
    SqlLexer,
    SwiftLexer,
    VbNetLexer,
)
from sklearn.base import (
    BaseEstimator,
    OneToOneFeatureMixin,
    TransformerMixin,
)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

classes = {
    "lua": LuaLexer,
    "scala": ScalaLexer,
    "bash": BashLexer,
    "r": SLexer,
    "vb.net": VbNetLexer,
    "css": CssLexer,
    "javascript": JavascriptLexer,
    "objc": ObjectiveCLexer,
    "cpp": CppLexer,
    "php": PhpLexer,
    "swift": SwiftLexer,
    "ruby": RubyLexer,
    "java": JavaLexer,
    "c_sharp": CSharpLexer,
    "sqlite": SqlLexer,
    "haskell": HaskellLexer,
    "perl": PerlLexer,
    "python": PythonLexer,
    "c": CLexer,
}


def get_lexer(name):
    return classes[name]


class Prelude(OneToOneFeatureMixin, TransformerMixin, BaseEstimator):
    TO_IGNORE = frozenset(
        {
            "Token.Comment.Single",
            "Token.Comment.Multiline",
            # "Token.Name",
            # "Token.Literal.Number.Integer",
            # "Token.Literal.Number.Float",
            # "Token.Literal.String.Double",
            # "Token.Literal.String.Single"
        }
    )

    def __init__(self, pretrained=None):
        self.pretrained = False
        if pretrained:
            if isinstance(pretrained, (str, Path)):
                with open(pretrained, "rb") as f:
                    self.prelude_pipeline = joblib.load(f)
            else:
                self.prelude_pipeline = pretrained
            self.pretrained = True
        else:
            self.prelude_pipeline = Pipeline(
                [
                    (
                        "vectorizer",
                        TfidfVectorizer(tokenizer=TweetTokenizer().tokenize),
                    ),
                    ("preludeclf", MultinomialNB()),
                ]
            )

    def fit(self, X, y):
        if not self.pretrained:
            self.prelude_pipeline.fit(X, y)
        return self

    def transform(self, X):
        predictions = self.prelude_pipeline.predict(X)
        transformed = []
        for text, pred in zip(X, predictions):
            lex = get_lexer(pred)()
            tokens = list(
                filter(
                    lambda x: str(x[0]) not in self.TO_IGNORE,
                    lex.get_tokens(text),
                )
            )
            transformed.append("".join([tok for _, tok in tokens]).strip())
        return np.array(transformed)
