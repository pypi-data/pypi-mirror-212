from dataclasses import field
from dataclasses import make_dataclass
from typing import List

from dict_tools.typing import Computed


def str_alias(hub, param: "alias=p"):
    return param


def multiple_str_alias(hub, param: "alias=p, alias=prm"):
    return param


def tuple_alias(hub, param: (str, "alias=p")):
    return param


def multiple_tuple_alias(hub, param: (str, "alias=p", "alias=prm")):
    return param


def tuple_alias_dataclass(
    hub,
    param: (
        List[
            make_dataclass(
                "Tag",
                [
                    ("Key", str, field(default=None)),
                    ("Value", str, field(default=None)),
                ],
            )
        ],
        "alias=p",
        "alias=prm",
    ),
):
    return param


def computed(hub, param: Computed[str] = None):
    return param


def computed_nest(
    hub,
    param: Computed[
        List[
            make_dataclass(
                "Tag",
                [
                    ("Key", str, field(default=None)),
                    ("Value", str, field(default=None)),
                ],
            )
        ]
    ],
):
    return param


def computed_alias(hub, param: (Computed[str], "alias=p")):
    return param
