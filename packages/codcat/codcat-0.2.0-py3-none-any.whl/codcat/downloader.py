"""Module that provides models loading api"""

import hashlib
import pathlib
import sys
from typing import (
    Dict,
    Optional,
)
from urllib.parse import urlencode

import requests
import yaml
from rich.progress import Progress

from codcat.models.estimator import (
    Estimator,
    SklearnEstimator,
)
from codcat.utils.types import PathLike

_DEFAULT_MANIFEST = pathlib.Path(__file__).parent.joinpath("manifest.yaml")


def hashsum(path):
    """
    Calculate md5 hash of a file

    Parameters
    ----------
    path : PathLike
        Path to the file

    Returns
    -------
    str
        md5 hash of the file
    """

    hash_inst = hashlib.md5()  # nosec
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(hash_inst.block_size * 128), b""):
            hash_inst.update(chunk)
    return hash_inst.hexdigest()


def _download(name: str, manifest: Dict) -> pathlib.Path:
    """
    Download model from Yandex.Disk if it is not already downloaded

    Parameters
    ----------
    name : str
        Model name

    Returns
    -------
    pathlib.Path
        Path to the downloaded model
    """

    model_info = manifest.get(name, None)

    if model_info is None:
        raise KeyError(f"Model `{name}` not found")

    ext = model_info["ext"]

    file_name = (
        pathlib.Path(__file__).parent.joinpath(f"{name}.{ext}").resolve()
    )

    base_url = "https://cloud-api.yandex.net/v1/disk/public/resources/"
    public_key = manifest[name].get("href", None)
    md5_link = base_url + "?" + urlencode(dict(public_key=public_key))
    md5_hash = requests.get(md5_link).json()["md5"]

    if file_name.exists() and hashsum(file_name) == md5_hash:
        return file_name

    if public_key is None:
        raise ValueError(f"Unknown model name: {name}")

    request_link = (
        base_url + "download?" + urlencode(dict(public_key=public_key))
    )

    with open(file_name, "wb") as f:
        href_response = requests.get(request_link)

        if href_response.status_code != 200:
            raise requests.exceptions.HTTPError(
                f"Failed to get download link for `{name}`"
            )

        file_href = href_response.json().get("href", None)

        if file_href is None:
            raise ValueError(f"Failed to get download link for `{name}`")

        response = requests.get(file_href, stream=True)
        total_length_header: Optional[str] = response.headers.get(
            "Content-Length"
        )

        if total_length_header is None:
            f.write(response.content)
        else:
            total_length = int(total_length_header)
            with Progress() as progress:
                task = progress.add_task(
                    f"[red]Downloading `{name}`...", total=total_length
                )
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    progress.update(task, advance=len(data))

    # verify md5 hash
    if hashsum(file_name) != md5_hash:
        raise ValueError(f"Downloaded file {file_name} has wrong md5 hash")

    # in jupyter notebook
    if "ipykernel" in sys.modules:
        from IPython.display import clear_output  # noqa

        clear_output(wait=False)

    return file_name


def load(name: str, manifest_path: PathLike = _DEFAULT_MANIFEST) -> Estimator:
    """
    Load model by name, download if it is not already downloaded

    Parameters
    ----------
    name : str
        Model name
    manifest_path:
        Manifest path

    Returns
    -------
    pathlib.Path
        Path to the downloaded model
    """

    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)
    path = _download(name, manifest)
    estimator_type = manifest[name]["type"]
    if estimator_type == "sklearn":
        return SklearnEstimator.load(path)
    raise ValueError(f"Unknown model type: `{estimator_type}`")


if __name__ == "__main__":
    model = load("base-tiny")
    texts = [
        "def foo(bar): return bar",
        '#include <iostream> using namespace std; int main() { cout << "Hello World"; return 0; }',
    ]
    print(model.predict_proba(texts))
