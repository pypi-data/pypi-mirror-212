r"""This module defines a image folder dataset."""

from __future__ import annotations

__all__ = ["ImageFolder"]

from collections.abc import Callable
from pathlib import Path
from typing import Any

from gravitorch import constants as ct
from gravitorch.utils import setup_object
from gravitorch.utils.path import sanitize_path
from torchvision.datasets import ImageFolder as ImageFolder_
from torchvision.datasets.folder import default_loader


class ImageFolder(ImageFolder_):
    r"""Implements a dataset that returns a dict instead of a tuple.

    This dataset extends the ``torchvision.datasets.ImageFolder`` class.

    Args:
        see ``torchvision.datasets.ImageFolder``
    """

    def __init__(
        self,
        root: Path | str,
        transform: Callable | dict | None = None,
        target_transform: Callable | dict | None = None,
        loader: Callable[[str], Any] = default_loader,
        is_valid_file: Callable[[str], bool] | None = None,
    ) -> None:
        super().__init__(
            root=sanitize_path(root).as_posix(),
            transform=setup_object(transform),
            target_transform=setup_object(target_transform),
            loader=loader,
            is_valid_file=is_valid_file,
        )

    def __getitem__(self, index: int) -> dict:
        r"""Get the image and the target of the index-th example.

        Args:
        ----
            index (int): Specifies the index of the example.

        Returns:
        -------
            dict: A dictionary with the image and the target of the
                ``index``-th example.
        """
        img, target = super().__getitem__(index)
        return {ct.INPUT: img, ct.TARGET: target}
