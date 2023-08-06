import logging
from itertools import tee
from typing import Iterable
from unittest import mock

import code_tokenize as ctok
from code_ast.parsers import _exists_url
from git import Repo
from typing_extensions import NamedTuple

log = logging.getLogger("codcat")


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class SepToken(NamedTuple):
    text: str
    type: str = "sep"

    def __repr__(self):
        return self.text


def robust_tokenize(text, lang):
    tokens = ctok.tokenize(text, lang, syntax_error="ignore")

    buff = [tokens[0]]
    for prev_tok, cur_tok in pairwise(tokens):
        if not hasattr(prev_tok, "ast_node") or not hasattr(
            cur_tok, "ast_node"
        ):
            buff.append(cur_tok)
            continue
        buff.append(
            SepToken(
                text[prev_tok.ast_node.end_byte : cur_tok.ast_node.start_byte]
            )
        )
        buff.append(cur_tok)

    return buff


lang2repo = {
    "m68k": "https://github.com/grahambates/tree-sitter-m68k",
    "C": "https://github.com/tree-sitter/tree-sitter-c",
    "lua": "https://github.com/Azganoth/tree-sitter-lua",
    "markdown": "https://github.com/ikatyang/tree-sitter-markdown",
    "objc": "https://github.com/jiyee/tree-sitter-objc",
    "perl": "https://github.com/ganezdragon/tree-sitter-perl",
    "r": "https://github.com/r-lib/tree-sitter-r",
    "swift": "https://github.com/alex-pinkus/tree-sitter-swift",
    "sqlite": "https://github.com/dhcmrlchtdj/tree-sitter-sqlite",
    "c_sharp": "https://github.com/tree-sitter/tree-sitter-c-sharp",
}


def _clone_parse_def_from_github(lang, cache_path):
    # NOTE: This is a patch for code_tokenize, since version 0.2.0 does
    # not take into account the possibility of some repositories by other url addresses.
    log.warning("Using patched version [codcat]")
    repo_url = "https://github.com/tree-sitter/tree-sitter-%s" % lang
    repo_url = repo_url if lang not in lang2repo else lang2repo[lang]
    if not _exists_url(repo_url):
        raise ValueError(
            "There is no parsing def for language %s available." % lang
        )
    log.warning("Start cloning the parser definition from Github.")
    try:
        Repo.clone_from(repo_url, cache_path)
    except Exception:
        raise ValueError(
            "To autoload a parsing definition, git needs to be installed on the system!"
        )


_DEFAULT_IGNORE_TOKENS_LIST = frozenset(
    {
        "comment",
        "line_comment",
        # "string",
        # "newline",
        # "integer",
        # "float",
        # "number_literal",
        # "variable_name",
        # "indent",
        # "dedent",
    }
)

to_replace = {
    "indent": "\n\t",
    "dedent": "",
    "newline": "\n",
}


def preprocess(
    text: str, lang: str, to_ignore: Iterable = _DEFAULT_IGNORE_TOKENS_LIST
) -> str:
    if len(text.strip()) == 0:
        raise ValueError(
            f"The code string is empty. Cannot tokenize anything empty: {text}"
        )

    if not lang or lang == "vb.net":
        return text

    try:
        with mock.patch(
            "code_ast.parsers._clone_parse_def_from_github",
            _clone_parse_def_from_github,
        ):
            tokens = []

            for x in filter(
                lambda tok: tok.type not in to_ignore,
                robust_tokenize(text, lang),
            ):
                try:
                    if x.type in to_replace:
                        tokens.append(to_replace[x.type])
                        continue
                    tokens.append(x.text)
                except IndexError:
                    continue

            if not tokens:
                return text

            return "".join(tokens).strip()
    except ValueError:
        return text
