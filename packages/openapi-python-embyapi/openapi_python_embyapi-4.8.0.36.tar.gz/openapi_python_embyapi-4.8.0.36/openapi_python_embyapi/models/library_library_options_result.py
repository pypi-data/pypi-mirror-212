from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.library_library_option_info import LibraryLibraryOptionInfo
    from ..models.library_library_type_options import LibraryLibraryTypeOptions


T = TypeVar("T", bound="LibraryLibraryOptionsResult")


@attr.s(auto_attribs=True)
class LibraryLibraryOptionsResult:
    """
    Attributes:
        metadata_savers (Union[Unset, List['LibraryLibraryOptionInfo']]):
        metadata_readers (Union[Unset, List['LibraryLibraryOptionInfo']]):
        subtitle_fetchers (Union[Unset, List['LibraryLibraryOptionInfo']]):
        lyrics_fetchers (Union[Unset, List['LibraryLibraryOptionInfo']]):
        type_options (Union[Unset, List['LibraryLibraryTypeOptions']]):
    """

    metadata_savers: Union[Unset, List["LibraryLibraryOptionInfo"]] = UNSET
    metadata_readers: Union[Unset, List["LibraryLibraryOptionInfo"]] = UNSET
    subtitle_fetchers: Union[Unset, List["LibraryLibraryOptionInfo"]] = UNSET
    lyrics_fetchers: Union[Unset, List["LibraryLibraryOptionInfo"]] = UNSET
    type_options: Union[Unset, List["LibraryLibraryTypeOptions"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        metadata_savers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metadata_savers, Unset):
            metadata_savers = []
            for metadata_savers_item_data in self.metadata_savers:
                metadata_savers_item = metadata_savers_item_data.to_dict()

                metadata_savers.append(metadata_savers_item)

        metadata_readers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.metadata_readers, Unset):
            metadata_readers = []
            for metadata_readers_item_data in self.metadata_readers:
                metadata_readers_item = metadata_readers_item_data.to_dict()

                metadata_readers.append(metadata_readers_item)

        subtitle_fetchers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.subtitle_fetchers, Unset):
            subtitle_fetchers = []
            for subtitle_fetchers_item_data in self.subtitle_fetchers:
                subtitle_fetchers_item = subtitle_fetchers_item_data.to_dict()

                subtitle_fetchers.append(subtitle_fetchers_item)

        lyrics_fetchers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.lyrics_fetchers, Unset):
            lyrics_fetchers = []
            for lyrics_fetchers_item_data in self.lyrics_fetchers:
                lyrics_fetchers_item = lyrics_fetchers_item_data.to_dict()

                lyrics_fetchers.append(lyrics_fetchers_item)

        type_options: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.type_options, Unset):
            type_options = []
            for type_options_item_data in self.type_options:
                type_options_item = type_options_item_data.to_dict()

                type_options.append(type_options_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metadata_savers is not UNSET:
            field_dict["MetadataSavers"] = metadata_savers
        if metadata_readers is not UNSET:
            field_dict["MetadataReaders"] = metadata_readers
        if subtitle_fetchers is not UNSET:
            field_dict["SubtitleFetchers"] = subtitle_fetchers
        if lyrics_fetchers is not UNSET:
            field_dict["LyricsFetchers"] = lyrics_fetchers
        if type_options is not UNSET:
            field_dict["TypeOptions"] = type_options

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.library_library_option_info import LibraryLibraryOptionInfo
        from ..models.library_library_type_options import LibraryLibraryTypeOptions

        d = src_dict.copy()
        metadata_savers = []
        _metadata_savers = d.pop("MetadataSavers", UNSET)
        for metadata_savers_item_data in _metadata_savers or []:
            metadata_savers_item = LibraryLibraryOptionInfo.from_dict(metadata_savers_item_data)

            metadata_savers.append(metadata_savers_item)

        metadata_readers = []
        _metadata_readers = d.pop("MetadataReaders", UNSET)
        for metadata_readers_item_data in _metadata_readers or []:
            metadata_readers_item = LibraryLibraryOptionInfo.from_dict(metadata_readers_item_data)

            metadata_readers.append(metadata_readers_item)

        subtitle_fetchers = []
        _subtitle_fetchers = d.pop("SubtitleFetchers", UNSET)
        for subtitle_fetchers_item_data in _subtitle_fetchers or []:
            subtitle_fetchers_item = LibraryLibraryOptionInfo.from_dict(subtitle_fetchers_item_data)

            subtitle_fetchers.append(subtitle_fetchers_item)

        lyrics_fetchers = []
        _lyrics_fetchers = d.pop("LyricsFetchers", UNSET)
        for lyrics_fetchers_item_data in _lyrics_fetchers or []:
            lyrics_fetchers_item = LibraryLibraryOptionInfo.from_dict(lyrics_fetchers_item_data)

            lyrics_fetchers.append(lyrics_fetchers_item)

        type_options = []
        _type_options = d.pop("TypeOptions", UNSET)
        for type_options_item_data in _type_options or []:
            type_options_item = LibraryLibraryTypeOptions.from_dict(type_options_item_data)

            type_options.append(type_options_item)

        library_library_options_result = cls(
            metadata_savers=metadata_savers,
            metadata_readers=metadata_readers,
            subtitle_fetchers=subtitle_fetchers,
            lyrics_fetchers=lyrics_fetchers,
            type_options=type_options,
        )

        library_library_options_result.additional_properties = d
        return library_library_options_result

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
