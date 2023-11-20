"""
This approach is inspired by https://github.com/IHosseini083/Shortify/blob/main/shortify/app/models/__init__.py
"""
import sys
from typing import Sequence, Type, TypeVar

from beanie import Document

# All database models must be imported here to be able to
# initialize them on startup.
from .student import Student

DocType = TypeVar("DocType", bound=Document)


def gather_documents() -> Sequence[Type[DocType]]:
    """Returns a list of all MongoDB document models defined in `models` module."""
    from inspect import getmembers, isclass

    return [doc for _, doc in getmembers(sys.modules[__name__], isclass) if issubclass(doc, Document) and doc.__name__ != "Document"]
