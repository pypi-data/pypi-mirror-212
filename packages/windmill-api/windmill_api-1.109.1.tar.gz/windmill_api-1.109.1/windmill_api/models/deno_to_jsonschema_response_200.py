from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.deno_to_jsonschema_response_200_args_item import DenoToJsonschemaResponse200ArgsItem
from ..models.deno_to_jsonschema_response_200_type import DenoToJsonschemaResponse200Type
from ..types import UNSET, Unset

T = TypeVar("T", bound="DenoToJsonschemaResponse200")


@attr.s(auto_attribs=True)
class DenoToJsonschemaResponse200:
    """
    Attributes:
        type (DenoToJsonschemaResponse200Type):
        error (str):
        star_args (bool):
        args (List[DenoToJsonschemaResponse200ArgsItem]):
        star_kwargs (Union[Unset, bool]):
    """

    type: DenoToJsonschemaResponse200Type
    error: str
    star_args: bool
    args: List[DenoToJsonschemaResponse200ArgsItem]
    star_kwargs: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        error = self.error
        star_args = self.star_args
        args = []
        for args_item_data in self.args:
            args_item = args_item_data.to_dict()

            args.append(args_item)

        star_kwargs = self.star_kwargs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "error": error,
                "star_args": star_args,
                "args": args,
            }
        )
        if star_kwargs is not UNSET:
            field_dict["star_kwargs"] = star_kwargs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = DenoToJsonschemaResponse200Type(d.pop("type"))

        error = d.pop("error")

        star_args = d.pop("star_args")

        args = []
        _args = d.pop("args")
        for args_item_data in _args:
            args_item = DenoToJsonschemaResponse200ArgsItem.from_dict(args_item_data)

            args.append(args_item)

        star_kwargs = d.pop("star_kwargs", UNSET)

        deno_to_jsonschema_response_200 = cls(
            type=type,
            error=error,
            star_args=star_args,
            args=args,
            star_kwargs=star_kwargs,
        )

        deno_to_jsonschema_response_200.additional_properties = d
        return deno_to_jsonschema_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
