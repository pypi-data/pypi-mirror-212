"""Tests for persistent dataclasses functionality."""

import pytest

from dataclasses import dataclass, field
from typing import Optional

from anaml_client.utils.persistent import persistent


def test_persistent_classes():
    """Test persistent dataclass helpers."""

    @persistent
    @dataclass(frozen=True)
    class Foo:
        tag: str = field(init=False, repr=False, default="tag1")
        name: str
        id: Optional[int] = None

    @persistent
    @dataclass(frozen=True)
    class Bar(Foo):
        tag: str = field(init=False, repr=False, default="tag2")
        hello: bool = False

    foo1 = Foo(name="World")
    foo2 = foo1.copy(id=123)

    assert foo1 == Foo(name="World")
    assert foo2 == Foo(id=123, name="World")

    bar1 = Bar(name="What")
    bar2 = bar1.copy(id=456)
    bar3 = bar2.copy(hello=True)

    assert bar1 == Bar(name="What")
    assert bar2 == Bar(id=456, name="What")
    assert bar3 == Bar(id=456, name="What", hello=True)


def test_persistent_copy_method_argument_handling():
    """Test persistent dataclass helpers."""

    @persistent
    @dataclass(frozen=True)
    class Foo:
        tag: str = field(init=False, repr=False, default="tag1")
        name: str
        id: Optional[int] = None

    f1 = Foo(id=123, name="hello")

    with pytest.raises(TypeError):
        f1.copy(456)
