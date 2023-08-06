"""Module that contains dataset tools"""

import logging
import pathlib

import pandas as pd

from codcat.utils.types import PathLike

__all__ = ["load_labeled_data"]


log = logging.getLogger(__name__)


def load_labeled_data(path: PathLike) -> pd.DataFrame:
    """
    Load labeled data from a folder with gists.

    Parameters
    ----------
    path
        Path to the folder with gists.

    Returns
    -------
        DataFrame with columns: ['language', 'code'].
    """

    path = pathlib.Path(path)
    data = []

    for lang_folder in path.iterdir():
        for file in lang_folder.iterdir():
            text = file.read_text()
            if len(text.strip()) == 0:
                continue
            data.append({"language": lang_folder.name, "code": text})

    return pd.DataFrame(data)
