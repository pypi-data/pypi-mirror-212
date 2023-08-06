"""This module provides a functions and classes to tokenize source code"""
import logging
from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import List

from nltk import NLTKWordTokenizer
from pygments.lexers import guess_lexer

__all__ = [
    "Tokenizer",
    "NLTKWordTokenizer",
    "PygmentsTokenizer",
    "NLTKTokenizer",
]


log = logging.getLogger(__name__)


class Tokenizer(metaclass=ABCMeta):
    @abstractmethod
    def tokenize(self, text, label) -> List[str]:
        raise NotImplementedError


class NLTKTokenizer(Tokenizer):
    def tokenize(self, text, label) -> List[str]:
        return NLTKWordTokenizer().tokenize(text)


class PygmentsTokenizer(Tokenizer):
    """Pygments tokenizer"""

    TO_IGNORE = frozenset({"Comment", "Literal"})

    def tokenize(self, text, label) -> List[str]:
        lexer_subclass = guess_lexer(text)
        tokens = list(
            filter(
                lambda x: str(x[0]).split(".")[1] not in self.TO_IGNORE,
                lexer_subclass.get_tokens(text),
            )
        )
        return [tok for _, tok in tokens]
