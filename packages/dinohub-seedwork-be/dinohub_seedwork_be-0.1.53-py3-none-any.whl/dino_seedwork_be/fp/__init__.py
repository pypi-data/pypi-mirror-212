from typing import Callable, Iterable, List, Tuple, TypeVar

from returns.interfaces.applicative import ApplicativeN
from returns.interfaces.failable import FailableN
from returns.iterables import Fold
from returns.maybe import Maybe, Some
from returns.primitives.hkt import KindN
from returns.result import Result, Success

from dino_seedwork_be.domain.exceptions import DomainException

from .domain_safe import domain_safe
from .list import to_list

InnerValue = TypeVar("InnerValue")
ResultValue = TypeVar("ResultValue")

_FirstType = TypeVar("_FirstType")
_SecondType = TypeVar("_SecondType")
_ThirdType = TypeVar("_ThirdType")
_UpdatedType = TypeVar("_UpdatedType")

_ApplicativeKind = TypeVar("_ApplicativeKind", bound=ApplicativeN)
_FailableKind = TypeVar("_FailableKind", bound=FailableN)


def handle_on_maybe(
    handler: Callable[[InnerValue], Result[None, DomainException]]
) -> Callable[[Maybe[InnerValue]], Result[None, DomainException]]:
    def _handler(inner_value: Maybe[InnerValue]):
        match inner_value:
            case Some(v):
                return handler(v)
            case _:
                return Success(None)

    return _handler


def collect(
    iterable: Iterable[
        KindN[_ApplicativeKind, _FirstType, _SecondType, _ThirdType],
    ],
    acc: KindN[
        _ApplicativeKind,
        "Tuple[_FirstType, ...]",
        _SecondType,
        _ThirdType,
    ],
) -> KindN[_ApplicativeKind, "Tuple[_FirstType, ...]", _SecondType, _ThirdType,]:
    return Fold.collect(iterable, acc)


def collect_all(
    iterable: Iterable[
        KindN[_ApplicativeKind, _FirstType, _SecondType, _ThirdType],
    ],
    acc: KindN[
        _ApplicativeKind,
        "Tuple[_FirstType, ...]",
        _SecondType,
        _ThirdType,
    ],
) -> KindN[_ApplicativeKind, "Tuple[_FirstType, ...]", _SecondType, _ThirdType,]:
    return Fold.collect_all(iterable, acc)


__all__ = ["to_list", "domain_safe", "handle_on_maybe", "collect", "collect_all"]
