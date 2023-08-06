from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.recommendation_type import RecommendationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_item_dto import BaseItemDto


T = TypeVar("T", bound="RecommendationDto")


@attr.s(auto_attribs=True)
class RecommendationDto:
    """
    Attributes:
        items (Union[Unset, List['BaseItemDto']]):
        recommendation_type (Union[Unset, RecommendationType]):
        baseline_item_name (Union[Unset, str]):
        category_id (Union[Unset, int]):
    """

    items: Union[Unset, List["BaseItemDto"]] = UNSET
    recommendation_type: Union[Unset, RecommendationType] = UNSET
    baseline_item_name: Union[Unset, str] = UNSET
    category_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()

                items.append(items_item)

        recommendation_type: Union[Unset, str] = UNSET
        if not isinstance(self.recommendation_type, Unset):
            recommendation_type = self.recommendation_type.value

        baseline_item_name = self.baseline_item_name
        category_id = self.category_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if items is not UNSET:
            field_dict["Items"] = items
        if recommendation_type is not UNSET:
            field_dict["RecommendationType"] = recommendation_type
        if baseline_item_name is not UNSET:
            field_dict["BaselineItemName"] = baseline_item_name
        if category_id is not UNSET:
            field_dict["CategoryId"] = category_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.base_item_dto import BaseItemDto

        d = src_dict.copy()
        items = []
        _items = d.pop("Items", UNSET)
        for items_item_data in _items or []:
            items_item = BaseItemDto.from_dict(items_item_data)

            items.append(items_item)

        _recommendation_type = d.pop("RecommendationType", UNSET)
        recommendation_type: Union[Unset, RecommendationType]
        if isinstance(_recommendation_type, Unset):
            recommendation_type = UNSET
        else:
            recommendation_type = RecommendationType(_recommendation_type)

        baseline_item_name = d.pop("BaselineItemName", UNSET)

        category_id = d.pop("CategoryId", UNSET)

        recommendation_dto = cls(
            items=items,
            recommendation_type=recommendation_type,
            baseline_item_name=baseline_item_name,
            category_id=category_id,
        )

        recommendation_dto.additional_properties = d
        return recommendation_dto

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
