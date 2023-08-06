from __future__ import annotations

__all__ = ["create_compose"]

from collections.abc import Callable, Sequence

from gravitorch.utils import setup_object
from torchvision.transforms import Compose


def create_compose(transforms: Sequence[Callable | dict]) -> Compose:
    r"""Instantiates a ``torchvision.transforms.Compose`` from its configuration.

    Args:
        transforms (sequence of ``Transform`` objects): Specifies the
            sequence of transforms (or their configuration) to compose.

    Returns:
        ``torchvision.transforms.Compose``: The instantiated
            composition of transforms

    Raises:
        RuntimeError if ``torchvision`` is not installed.

    Example usage:

    .. code-block:: pycon

        >>> from gtvision.transforms import create_compose
        >>> from torchvision.transforms import PILToTensor
        >>> create_compose(
        ...     [
        ...         {"_target_": "torchvision.transforms.CenterCrop", "size": 10},
        ...         PILToTensor(),
        ...     ]
        ... )
    """
    return Compose([setup_object(transform) for transform in transforms])
