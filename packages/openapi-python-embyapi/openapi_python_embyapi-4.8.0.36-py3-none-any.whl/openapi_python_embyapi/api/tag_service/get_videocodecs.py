from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.query_result_user_library_tag_item import QueryResultUserLibraryTagItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    artist_type: Union[Unset, None, str] = UNSET,
    max_official_rating: Union[Unset, None, str] = UNSET,
    has_theme_song: Union[Unset, None, bool] = UNSET,
    has_theme_video: Union[Unset, None, bool] = UNSET,
    has_subtitles: Union[Unset, None, bool] = UNSET,
    has_special_feature: Union[Unset, None, bool] = UNSET,
    has_trailer: Union[Unset, None, bool] = UNSET,
    adjacent_to: Union[Unset, None, str] = UNSET,
    min_index_number: Union[Unset, None, int] = UNSET,
    min_players: Union[Unset, None, int] = UNSET,
    max_players: Union[Unset, None, int] = UNSET,
    parent_index_number: Union[Unset, None, int] = UNSET,
    has_parental_rating: Union[Unset, None, bool] = UNSET,
    is_hd: Union[Unset, None, bool] = UNSET,
    location_types: Union[Unset, None, str] = UNSET,
    exclude_location_types: Union[Unset, None, str] = UNSET,
    is_missing: Union[Unset, None, bool] = UNSET,
    is_unaired: Union[Unset, None, bool] = UNSET,
    min_community_rating: Union[Unset, None, float] = UNSET,
    min_critic_rating: Union[Unset, None, float] = UNSET,
    aired_during_season: Union[Unset, None, int] = UNSET,
    min_premiere_date: Union[Unset, None, str] = UNSET,
    min_date_last_saved: Union[Unset, None, str] = UNSET,
    min_date_last_saved_for_user: Union[Unset, None, str] = UNSET,
    max_premiere_date: Union[Unset, None, str] = UNSET,
    has_overview: Union[Unset, None, bool] = UNSET,
    has_imdb_id: Union[Unset, None, bool] = UNSET,
    has_tmdb_id: Union[Unset, None, bool] = UNSET,
    has_tvdb_id: Union[Unset, None, bool] = UNSET,
    exclude_item_ids: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    recursive: Union[Unset, None, bool] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    exclude_item_types: Union[Unset, None, str] = UNSET,
    include_item_types: Union[Unset, None, str] = UNSET,
    any_provider_id_equals: Union[Unset, None, str] = UNSET,
    filters: Union[Unset, None, str] = UNSET,
    is_favorite: Union[Unset, None, bool] = UNSET,
    is_movie: Union[Unset, None, bool] = UNSET,
    is_series: Union[Unset, None, bool] = UNSET,
    is_folder: Union[Unset, None, bool] = UNSET,
    is_news: Union[Unset, None, bool] = UNSET,
    is_kids: Union[Unset, None, bool] = UNSET,
    is_sports: Union[Unset, None, bool] = UNSET,
    project_to_media: Union[Unset, None, bool] = UNSET,
    media_types: Union[Unset, None, str] = UNSET,
    image_types: Union[Unset, None, str] = UNSET,
    sort_by: Union[Unset, None, str] = UNSET,
    is_played: Union[Unset, None, bool] = UNSET,
    genres: Union[Unset, None, str] = UNSET,
    official_ratings: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    years: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    person: Union[Unset, None, str] = UNSET,
    person_ids: Union[Unset, None, str] = UNSET,
    person_types: Union[Unset, None, str] = UNSET,
    studios: Union[Unset, None, str] = UNSET,
    studio_ids: Union[Unset, None, str] = UNSET,
    artists: Union[Unset, None, str] = UNSET,
    artist_ids: Union[Unset, None, str] = UNSET,
    albums: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    video_types: Union[Unset, None, str] = UNSET,
    containers: Union[Unset, None, str] = UNSET,
    audio_codecs: Union[Unset, None, str] = UNSET,
    audio_layouts: Union[Unset, None, str] = UNSET,
    video_codecs: Union[Unset, None, str] = UNSET,
    subtitle_codecs: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    min_official_rating: Union[Unset, None, str] = UNSET,
    is_locked: Union[Unset, None, bool] = UNSET,
    is_place_holder: Union[Unset, None, bool] = UNSET,
    has_official_rating: Union[Unset, None, bool] = UNSET,
    group_items_into_collections: Union[Unset, None, bool] = UNSET,
    is_3d: Union[Unset, None, bool] = UNSET,
    series_status: Union[Unset, None, str] = UNSET,
    name_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    artist_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    album_artist_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    name_starts_with: Union[Unset, None, str] = UNSET,
    name_less_than: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/VideoCodecs".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ArtistType"] = artist_type

    params["MaxOfficialRating"] = max_official_rating

    params["HasThemeSong"] = has_theme_song

    params["HasThemeVideo"] = has_theme_video

    params["HasSubtitles"] = has_subtitles

    params["HasSpecialFeature"] = has_special_feature

    params["HasTrailer"] = has_trailer

    params["AdjacentTo"] = adjacent_to

    params["MinIndexNumber"] = min_index_number

    params["MinPlayers"] = min_players

    params["MaxPlayers"] = max_players

    params["ParentIndexNumber"] = parent_index_number

    params["HasParentalRating"] = has_parental_rating

    params["IsHD"] = is_hd

    params["LocationTypes"] = location_types

    params["ExcludeLocationTypes"] = exclude_location_types

    params["IsMissing"] = is_missing

    params["IsUnaired"] = is_unaired

    params["MinCommunityRating"] = min_community_rating

    params["MinCriticRating"] = min_critic_rating

    params["AiredDuringSeason"] = aired_during_season

    params["MinPremiereDate"] = min_premiere_date

    params["MinDateLastSaved"] = min_date_last_saved

    params["MinDateLastSavedForUser"] = min_date_last_saved_for_user

    params["MaxPremiereDate"] = max_premiere_date

    params["HasOverview"] = has_overview

    params["HasImdbId"] = has_imdb_id

    params["HasTmdbId"] = has_tmdb_id

    params["HasTvdbId"] = has_tvdb_id

    params["ExcludeItemIds"] = exclude_item_ids

    params["StartIndex"] = start_index

    params["Limit"] = limit

    params["Recursive"] = recursive

    params["SearchTerm"] = search_term

    params["SortOrder"] = sort_order

    params["ParentId"] = parent_id

    params["Fields"] = fields

    params["ExcludeItemTypes"] = exclude_item_types

    params["IncludeItemTypes"] = include_item_types

    params["AnyProviderIdEquals"] = any_provider_id_equals

    params["Filters"] = filters

    params["IsFavorite"] = is_favorite

    params["IsMovie"] = is_movie

    params["IsSeries"] = is_series

    params["IsFolder"] = is_folder

    params["IsNews"] = is_news

    params["IsKids"] = is_kids

    params["IsSports"] = is_sports

    params["ProjectToMedia"] = project_to_media

    params["MediaTypes"] = media_types

    params["ImageTypes"] = image_types

    params["SortBy"] = sort_by

    params["IsPlayed"] = is_played

    params["Genres"] = genres

    params["OfficialRatings"] = official_ratings

    params["Tags"] = tags

    params["Years"] = years

    params["EnableImages"] = enable_images

    params["EnableUserData"] = enable_user_data

    params["ImageTypeLimit"] = image_type_limit

    params["EnableImageTypes"] = enable_image_types

    params["Person"] = person

    params["PersonIds"] = person_ids

    params["PersonTypes"] = person_types

    params["Studios"] = studios

    params["StudioIds"] = studio_ids

    params["Artists"] = artists

    params["ArtistIds"] = artist_ids

    params["Albums"] = albums

    params["Ids"] = ids

    params["VideoTypes"] = video_types

    params["Containers"] = containers

    params["AudioCodecs"] = audio_codecs

    params["AudioLayouts"] = audio_layouts

    params["VideoCodecs"] = video_codecs

    params["SubtitleCodecs"] = subtitle_codecs

    params["Path"] = path

    params["UserId"] = user_id

    params["MinOfficialRating"] = min_official_rating

    params["IsLocked"] = is_locked

    params["IsPlaceHolder"] = is_place_holder

    params["HasOfficialRating"] = has_official_rating

    params["GroupItemsIntoCollections"] = group_items_into_collections

    params["Is3D"] = is_3d

    params["SeriesStatus"] = series_status

    params["NameStartsWithOrGreater"] = name_starts_with_or_greater

    params["ArtistStartsWithOrGreater"] = artist_starts_with_or_greater

    params["AlbumArtistStartsWithOrGreater"] = album_artist_starts_with_or_greater

    params["NameStartsWith"] = name_starts_with

    params["NameLessThan"] = name_less_than

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, QueryResultUserLibraryTagItem]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = QueryResultUserLibraryTagItem.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = cast(Any, None)
        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, QueryResultUserLibraryTagItem]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    artist_type: Union[Unset, None, str] = UNSET,
    max_official_rating: Union[Unset, None, str] = UNSET,
    has_theme_song: Union[Unset, None, bool] = UNSET,
    has_theme_video: Union[Unset, None, bool] = UNSET,
    has_subtitles: Union[Unset, None, bool] = UNSET,
    has_special_feature: Union[Unset, None, bool] = UNSET,
    has_trailer: Union[Unset, None, bool] = UNSET,
    adjacent_to: Union[Unset, None, str] = UNSET,
    min_index_number: Union[Unset, None, int] = UNSET,
    min_players: Union[Unset, None, int] = UNSET,
    max_players: Union[Unset, None, int] = UNSET,
    parent_index_number: Union[Unset, None, int] = UNSET,
    has_parental_rating: Union[Unset, None, bool] = UNSET,
    is_hd: Union[Unset, None, bool] = UNSET,
    location_types: Union[Unset, None, str] = UNSET,
    exclude_location_types: Union[Unset, None, str] = UNSET,
    is_missing: Union[Unset, None, bool] = UNSET,
    is_unaired: Union[Unset, None, bool] = UNSET,
    min_community_rating: Union[Unset, None, float] = UNSET,
    min_critic_rating: Union[Unset, None, float] = UNSET,
    aired_during_season: Union[Unset, None, int] = UNSET,
    min_premiere_date: Union[Unset, None, str] = UNSET,
    min_date_last_saved: Union[Unset, None, str] = UNSET,
    min_date_last_saved_for_user: Union[Unset, None, str] = UNSET,
    max_premiere_date: Union[Unset, None, str] = UNSET,
    has_overview: Union[Unset, None, bool] = UNSET,
    has_imdb_id: Union[Unset, None, bool] = UNSET,
    has_tmdb_id: Union[Unset, None, bool] = UNSET,
    has_tvdb_id: Union[Unset, None, bool] = UNSET,
    exclude_item_ids: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    recursive: Union[Unset, None, bool] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    exclude_item_types: Union[Unset, None, str] = UNSET,
    include_item_types: Union[Unset, None, str] = UNSET,
    any_provider_id_equals: Union[Unset, None, str] = UNSET,
    filters: Union[Unset, None, str] = UNSET,
    is_favorite: Union[Unset, None, bool] = UNSET,
    is_movie: Union[Unset, None, bool] = UNSET,
    is_series: Union[Unset, None, bool] = UNSET,
    is_folder: Union[Unset, None, bool] = UNSET,
    is_news: Union[Unset, None, bool] = UNSET,
    is_kids: Union[Unset, None, bool] = UNSET,
    is_sports: Union[Unset, None, bool] = UNSET,
    project_to_media: Union[Unset, None, bool] = UNSET,
    media_types: Union[Unset, None, str] = UNSET,
    image_types: Union[Unset, None, str] = UNSET,
    sort_by: Union[Unset, None, str] = UNSET,
    is_played: Union[Unset, None, bool] = UNSET,
    genres: Union[Unset, None, str] = UNSET,
    official_ratings: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    years: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    person: Union[Unset, None, str] = UNSET,
    person_ids: Union[Unset, None, str] = UNSET,
    person_types: Union[Unset, None, str] = UNSET,
    studios: Union[Unset, None, str] = UNSET,
    studio_ids: Union[Unset, None, str] = UNSET,
    artists: Union[Unset, None, str] = UNSET,
    artist_ids: Union[Unset, None, str] = UNSET,
    albums: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    video_types: Union[Unset, None, str] = UNSET,
    containers: Union[Unset, None, str] = UNSET,
    audio_codecs: Union[Unset, None, str] = UNSET,
    audio_layouts: Union[Unset, None, str] = UNSET,
    video_codecs: Union[Unset, None, str] = UNSET,
    subtitle_codecs: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    min_official_rating: Union[Unset, None, str] = UNSET,
    is_locked: Union[Unset, None, bool] = UNSET,
    is_place_holder: Union[Unset, None, bool] = UNSET,
    has_official_rating: Union[Unset, None, bool] = UNSET,
    group_items_into_collections: Union[Unset, None, bool] = UNSET,
    is_3d: Union[Unset, None, bool] = UNSET,
    series_status: Union[Unset, None, str] = UNSET,
    name_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    artist_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    album_artist_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    name_starts_with: Union[Unset, None, str] = UNSET,
    name_less_than: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, QueryResultUserLibraryTagItem]]:
    """Gets items based on a query.

     Requires authentication as user

    Args:
        artist_type (Union[Unset, None, str]):
        max_official_rating (Union[Unset, None, str]):
        has_theme_song (Union[Unset, None, bool]):
        has_theme_video (Union[Unset, None, bool]):
        has_subtitles (Union[Unset, None, bool]):
        has_special_feature (Union[Unset, None, bool]):
        has_trailer (Union[Unset, None, bool]):
        adjacent_to (Union[Unset, None, str]):
        min_index_number (Union[Unset, None, int]):
        min_players (Union[Unset, None, int]):
        max_players (Union[Unset, None, int]):
        parent_index_number (Union[Unset, None, int]):
        has_parental_rating (Union[Unset, None, bool]):
        is_hd (Union[Unset, None, bool]):
        location_types (Union[Unset, None, str]):
        exclude_location_types (Union[Unset, None, str]):
        is_missing (Union[Unset, None, bool]):
        is_unaired (Union[Unset, None, bool]):
        min_community_rating (Union[Unset, None, float]):
        min_critic_rating (Union[Unset, None, float]):
        aired_during_season (Union[Unset, None, int]):
        min_premiere_date (Union[Unset, None, str]):
        min_date_last_saved (Union[Unset, None, str]):
        min_date_last_saved_for_user (Union[Unset, None, str]):
        max_premiere_date (Union[Unset, None, str]):
        has_overview (Union[Unset, None, bool]):
        has_imdb_id (Union[Unset, None, bool]):
        has_tmdb_id (Union[Unset, None, bool]):
        has_tvdb_id (Union[Unset, None, bool]):
        exclude_item_ids (Union[Unset, None, str]):
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        recursive (Union[Unset, None, bool]):
        search_term (Union[Unset, None, str]):
        sort_order (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        fields (Union[Unset, None, str]):
        exclude_item_types (Union[Unset, None, str]):
        include_item_types (Union[Unset, None, str]):
        any_provider_id_equals (Union[Unset, None, str]):
        filters (Union[Unset, None, str]):
        is_favorite (Union[Unset, None, bool]):
        is_movie (Union[Unset, None, bool]):
        is_series (Union[Unset, None, bool]):
        is_folder (Union[Unset, None, bool]):
        is_news (Union[Unset, None, bool]):
        is_kids (Union[Unset, None, bool]):
        is_sports (Union[Unset, None, bool]):
        project_to_media (Union[Unset, None, bool]):
        media_types (Union[Unset, None, str]):
        image_types (Union[Unset, None, str]):
        sort_by (Union[Unset, None, str]):
        is_played (Union[Unset, None, bool]):
        genres (Union[Unset, None, str]):
        official_ratings (Union[Unset, None, str]):
        tags (Union[Unset, None, str]):
        years (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        person (Union[Unset, None, str]):
        person_ids (Union[Unset, None, str]):
        person_types (Union[Unset, None, str]):
        studios (Union[Unset, None, str]):
        studio_ids (Union[Unset, None, str]):
        artists (Union[Unset, None, str]):
        artist_ids (Union[Unset, None, str]):
        albums (Union[Unset, None, str]):
        ids (Union[Unset, None, str]):
        video_types (Union[Unset, None, str]):
        containers (Union[Unset, None, str]):
        audio_codecs (Union[Unset, None, str]):
        audio_layouts (Union[Unset, None, str]):
        video_codecs (Union[Unset, None, str]):
        subtitle_codecs (Union[Unset, None, str]):
        path (Union[Unset, None, str]):
        user_id (Union[Unset, None, str]):
        min_official_rating (Union[Unset, None, str]):
        is_locked (Union[Unset, None, bool]):
        is_place_holder (Union[Unset, None, bool]):
        has_official_rating (Union[Unset, None, bool]):
        group_items_into_collections (Union[Unset, None, bool]):
        is_3d (Union[Unset, None, bool]):
        series_status (Union[Unset, None, str]):
        name_starts_with_or_greater (Union[Unset, None, str]):
        artist_starts_with_or_greater (Union[Unset, None, str]):
        album_artist_starts_with_or_greater (Union[Unset, None, str]):
        name_starts_with (Union[Unset, None, str]):
        name_less_than (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultUserLibraryTagItem]]
    """

    kwargs = _get_kwargs(
        client=client,
        artist_type=artist_type,
        max_official_rating=max_official_rating,
        has_theme_song=has_theme_song,
        has_theme_video=has_theme_video,
        has_subtitles=has_subtitles,
        has_special_feature=has_special_feature,
        has_trailer=has_trailer,
        adjacent_to=adjacent_to,
        min_index_number=min_index_number,
        min_players=min_players,
        max_players=max_players,
        parent_index_number=parent_index_number,
        has_parental_rating=has_parental_rating,
        is_hd=is_hd,
        location_types=location_types,
        exclude_location_types=exclude_location_types,
        is_missing=is_missing,
        is_unaired=is_unaired,
        min_community_rating=min_community_rating,
        min_critic_rating=min_critic_rating,
        aired_during_season=aired_during_season,
        min_premiere_date=min_premiere_date,
        min_date_last_saved=min_date_last_saved,
        min_date_last_saved_for_user=min_date_last_saved_for_user,
        max_premiere_date=max_premiere_date,
        has_overview=has_overview,
        has_imdb_id=has_imdb_id,
        has_tmdb_id=has_tmdb_id,
        has_tvdb_id=has_tvdb_id,
        exclude_item_ids=exclude_item_ids,
        start_index=start_index,
        limit=limit,
        recursive=recursive,
        search_term=search_term,
        sort_order=sort_order,
        parent_id=parent_id,
        fields=fields,
        exclude_item_types=exclude_item_types,
        include_item_types=include_item_types,
        any_provider_id_equals=any_provider_id_equals,
        filters=filters,
        is_favorite=is_favorite,
        is_movie=is_movie,
        is_series=is_series,
        is_folder=is_folder,
        is_news=is_news,
        is_kids=is_kids,
        is_sports=is_sports,
        project_to_media=project_to_media,
        media_types=media_types,
        image_types=image_types,
        sort_by=sort_by,
        is_played=is_played,
        genres=genres,
        official_ratings=official_ratings,
        tags=tags,
        years=years,
        enable_images=enable_images,
        enable_user_data=enable_user_data,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        person=person,
        person_ids=person_ids,
        person_types=person_types,
        studios=studios,
        studio_ids=studio_ids,
        artists=artists,
        artist_ids=artist_ids,
        albums=albums,
        ids=ids,
        video_types=video_types,
        containers=containers,
        audio_codecs=audio_codecs,
        audio_layouts=audio_layouts,
        video_codecs=video_codecs,
        subtitle_codecs=subtitle_codecs,
        path=path,
        user_id=user_id,
        min_official_rating=min_official_rating,
        is_locked=is_locked,
        is_place_holder=is_place_holder,
        has_official_rating=has_official_rating,
        group_items_into_collections=group_items_into_collections,
        is_3d=is_3d,
        series_status=series_status,
        name_starts_with_or_greater=name_starts_with_or_greater,
        artist_starts_with_or_greater=artist_starts_with_or_greater,
        album_artist_starts_with_or_greater=album_artist_starts_with_or_greater,
        name_starts_with=name_starts_with,
        name_less_than=name_less_than,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    artist_type: Union[Unset, None, str] = UNSET,
    max_official_rating: Union[Unset, None, str] = UNSET,
    has_theme_song: Union[Unset, None, bool] = UNSET,
    has_theme_video: Union[Unset, None, bool] = UNSET,
    has_subtitles: Union[Unset, None, bool] = UNSET,
    has_special_feature: Union[Unset, None, bool] = UNSET,
    has_trailer: Union[Unset, None, bool] = UNSET,
    adjacent_to: Union[Unset, None, str] = UNSET,
    min_index_number: Union[Unset, None, int] = UNSET,
    min_players: Union[Unset, None, int] = UNSET,
    max_players: Union[Unset, None, int] = UNSET,
    parent_index_number: Union[Unset, None, int] = UNSET,
    has_parental_rating: Union[Unset, None, bool] = UNSET,
    is_hd: Union[Unset, None, bool] = UNSET,
    location_types: Union[Unset, None, str] = UNSET,
    exclude_location_types: Union[Unset, None, str] = UNSET,
    is_missing: Union[Unset, None, bool] = UNSET,
    is_unaired: Union[Unset, None, bool] = UNSET,
    min_community_rating: Union[Unset, None, float] = UNSET,
    min_critic_rating: Union[Unset, None, float] = UNSET,
    aired_during_season: Union[Unset, None, int] = UNSET,
    min_premiere_date: Union[Unset, None, str] = UNSET,
    min_date_last_saved: Union[Unset, None, str] = UNSET,
    min_date_last_saved_for_user: Union[Unset, None, str] = UNSET,
    max_premiere_date: Union[Unset, None, str] = UNSET,
    has_overview: Union[Unset, None, bool] = UNSET,
    has_imdb_id: Union[Unset, None, bool] = UNSET,
    has_tmdb_id: Union[Unset, None, bool] = UNSET,
    has_tvdb_id: Union[Unset, None, bool] = UNSET,
    exclude_item_ids: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    recursive: Union[Unset, None, bool] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    exclude_item_types: Union[Unset, None, str] = UNSET,
    include_item_types: Union[Unset, None, str] = UNSET,
    any_provider_id_equals: Union[Unset, None, str] = UNSET,
    filters: Union[Unset, None, str] = UNSET,
    is_favorite: Union[Unset, None, bool] = UNSET,
    is_movie: Union[Unset, None, bool] = UNSET,
    is_series: Union[Unset, None, bool] = UNSET,
    is_folder: Union[Unset, None, bool] = UNSET,
    is_news: Union[Unset, None, bool] = UNSET,
    is_kids: Union[Unset, None, bool] = UNSET,
    is_sports: Union[Unset, None, bool] = UNSET,
    project_to_media: Union[Unset, None, bool] = UNSET,
    media_types: Union[Unset, None, str] = UNSET,
    image_types: Union[Unset, None, str] = UNSET,
    sort_by: Union[Unset, None, str] = UNSET,
    is_played: Union[Unset, None, bool] = UNSET,
    genres: Union[Unset, None, str] = UNSET,
    official_ratings: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    years: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    person: Union[Unset, None, str] = UNSET,
    person_ids: Union[Unset, None, str] = UNSET,
    person_types: Union[Unset, None, str] = UNSET,
    studios: Union[Unset, None, str] = UNSET,
    studio_ids: Union[Unset, None, str] = UNSET,
    artists: Union[Unset, None, str] = UNSET,
    artist_ids: Union[Unset, None, str] = UNSET,
    albums: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    video_types: Union[Unset, None, str] = UNSET,
    containers: Union[Unset, None, str] = UNSET,
    audio_codecs: Union[Unset, None, str] = UNSET,
    audio_layouts: Union[Unset, None, str] = UNSET,
    video_codecs: Union[Unset, None, str] = UNSET,
    subtitle_codecs: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    min_official_rating: Union[Unset, None, str] = UNSET,
    is_locked: Union[Unset, None, bool] = UNSET,
    is_place_holder: Union[Unset, None, bool] = UNSET,
    has_official_rating: Union[Unset, None, bool] = UNSET,
    group_items_into_collections: Union[Unset, None, bool] = UNSET,
    is_3d: Union[Unset, None, bool] = UNSET,
    series_status: Union[Unset, None, str] = UNSET,
    name_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    artist_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    album_artist_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    name_starts_with: Union[Unset, None, str] = UNSET,
    name_less_than: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, QueryResultUserLibraryTagItem]]:
    """Gets items based on a query.

     Requires authentication as user

    Args:
        artist_type (Union[Unset, None, str]):
        max_official_rating (Union[Unset, None, str]):
        has_theme_song (Union[Unset, None, bool]):
        has_theme_video (Union[Unset, None, bool]):
        has_subtitles (Union[Unset, None, bool]):
        has_special_feature (Union[Unset, None, bool]):
        has_trailer (Union[Unset, None, bool]):
        adjacent_to (Union[Unset, None, str]):
        min_index_number (Union[Unset, None, int]):
        min_players (Union[Unset, None, int]):
        max_players (Union[Unset, None, int]):
        parent_index_number (Union[Unset, None, int]):
        has_parental_rating (Union[Unset, None, bool]):
        is_hd (Union[Unset, None, bool]):
        location_types (Union[Unset, None, str]):
        exclude_location_types (Union[Unset, None, str]):
        is_missing (Union[Unset, None, bool]):
        is_unaired (Union[Unset, None, bool]):
        min_community_rating (Union[Unset, None, float]):
        min_critic_rating (Union[Unset, None, float]):
        aired_during_season (Union[Unset, None, int]):
        min_premiere_date (Union[Unset, None, str]):
        min_date_last_saved (Union[Unset, None, str]):
        min_date_last_saved_for_user (Union[Unset, None, str]):
        max_premiere_date (Union[Unset, None, str]):
        has_overview (Union[Unset, None, bool]):
        has_imdb_id (Union[Unset, None, bool]):
        has_tmdb_id (Union[Unset, None, bool]):
        has_tvdb_id (Union[Unset, None, bool]):
        exclude_item_ids (Union[Unset, None, str]):
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        recursive (Union[Unset, None, bool]):
        search_term (Union[Unset, None, str]):
        sort_order (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        fields (Union[Unset, None, str]):
        exclude_item_types (Union[Unset, None, str]):
        include_item_types (Union[Unset, None, str]):
        any_provider_id_equals (Union[Unset, None, str]):
        filters (Union[Unset, None, str]):
        is_favorite (Union[Unset, None, bool]):
        is_movie (Union[Unset, None, bool]):
        is_series (Union[Unset, None, bool]):
        is_folder (Union[Unset, None, bool]):
        is_news (Union[Unset, None, bool]):
        is_kids (Union[Unset, None, bool]):
        is_sports (Union[Unset, None, bool]):
        project_to_media (Union[Unset, None, bool]):
        media_types (Union[Unset, None, str]):
        image_types (Union[Unset, None, str]):
        sort_by (Union[Unset, None, str]):
        is_played (Union[Unset, None, bool]):
        genres (Union[Unset, None, str]):
        official_ratings (Union[Unset, None, str]):
        tags (Union[Unset, None, str]):
        years (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        person (Union[Unset, None, str]):
        person_ids (Union[Unset, None, str]):
        person_types (Union[Unset, None, str]):
        studios (Union[Unset, None, str]):
        studio_ids (Union[Unset, None, str]):
        artists (Union[Unset, None, str]):
        artist_ids (Union[Unset, None, str]):
        albums (Union[Unset, None, str]):
        ids (Union[Unset, None, str]):
        video_types (Union[Unset, None, str]):
        containers (Union[Unset, None, str]):
        audio_codecs (Union[Unset, None, str]):
        audio_layouts (Union[Unset, None, str]):
        video_codecs (Union[Unset, None, str]):
        subtitle_codecs (Union[Unset, None, str]):
        path (Union[Unset, None, str]):
        user_id (Union[Unset, None, str]):
        min_official_rating (Union[Unset, None, str]):
        is_locked (Union[Unset, None, bool]):
        is_place_holder (Union[Unset, None, bool]):
        has_official_rating (Union[Unset, None, bool]):
        group_items_into_collections (Union[Unset, None, bool]):
        is_3d (Union[Unset, None, bool]):
        series_status (Union[Unset, None, str]):
        name_starts_with_or_greater (Union[Unset, None, str]):
        artist_starts_with_or_greater (Union[Unset, None, str]):
        album_artist_starts_with_or_greater (Union[Unset, None, str]):
        name_starts_with (Union[Unset, None, str]):
        name_less_than (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultUserLibraryTagItem]
    """

    return sync_detailed(
        client=client,
        artist_type=artist_type,
        max_official_rating=max_official_rating,
        has_theme_song=has_theme_song,
        has_theme_video=has_theme_video,
        has_subtitles=has_subtitles,
        has_special_feature=has_special_feature,
        has_trailer=has_trailer,
        adjacent_to=adjacent_to,
        min_index_number=min_index_number,
        min_players=min_players,
        max_players=max_players,
        parent_index_number=parent_index_number,
        has_parental_rating=has_parental_rating,
        is_hd=is_hd,
        location_types=location_types,
        exclude_location_types=exclude_location_types,
        is_missing=is_missing,
        is_unaired=is_unaired,
        min_community_rating=min_community_rating,
        min_critic_rating=min_critic_rating,
        aired_during_season=aired_during_season,
        min_premiere_date=min_premiere_date,
        min_date_last_saved=min_date_last_saved,
        min_date_last_saved_for_user=min_date_last_saved_for_user,
        max_premiere_date=max_premiere_date,
        has_overview=has_overview,
        has_imdb_id=has_imdb_id,
        has_tmdb_id=has_tmdb_id,
        has_tvdb_id=has_tvdb_id,
        exclude_item_ids=exclude_item_ids,
        start_index=start_index,
        limit=limit,
        recursive=recursive,
        search_term=search_term,
        sort_order=sort_order,
        parent_id=parent_id,
        fields=fields,
        exclude_item_types=exclude_item_types,
        include_item_types=include_item_types,
        any_provider_id_equals=any_provider_id_equals,
        filters=filters,
        is_favorite=is_favorite,
        is_movie=is_movie,
        is_series=is_series,
        is_folder=is_folder,
        is_news=is_news,
        is_kids=is_kids,
        is_sports=is_sports,
        project_to_media=project_to_media,
        media_types=media_types,
        image_types=image_types,
        sort_by=sort_by,
        is_played=is_played,
        genres=genres,
        official_ratings=official_ratings,
        tags=tags,
        years=years,
        enable_images=enable_images,
        enable_user_data=enable_user_data,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        person=person,
        person_ids=person_ids,
        person_types=person_types,
        studios=studios,
        studio_ids=studio_ids,
        artists=artists,
        artist_ids=artist_ids,
        albums=albums,
        ids=ids,
        video_types=video_types,
        containers=containers,
        audio_codecs=audio_codecs,
        audio_layouts=audio_layouts,
        video_codecs=video_codecs,
        subtitle_codecs=subtitle_codecs,
        path=path,
        user_id=user_id,
        min_official_rating=min_official_rating,
        is_locked=is_locked,
        is_place_holder=is_place_holder,
        has_official_rating=has_official_rating,
        group_items_into_collections=group_items_into_collections,
        is_3d=is_3d,
        series_status=series_status,
        name_starts_with_or_greater=name_starts_with_or_greater,
        artist_starts_with_or_greater=artist_starts_with_or_greater,
        album_artist_starts_with_or_greater=album_artist_starts_with_or_greater,
        name_starts_with=name_starts_with,
        name_less_than=name_less_than,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    artist_type: Union[Unset, None, str] = UNSET,
    max_official_rating: Union[Unset, None, str] = UNSET,
    has_theme_song: Union[Unset, None, bool] = UNSET,
    has_theme_video: Union[Unset, None, bool] = UNSET,
    has_subtitles: Union[Unset, None, bool] = UNSET,
    has_special_feature: Union[Unset, None, bool] = UNSET,
    has_trailer: Union[Unset, None, bool] = UNSET,
    adjacent_to: Union[Unset, None, str] = UNSET,
    min_index_number: Union[Unset, None, int] = UNSET,
    min_players: Union[Unset, None, int] = UNSET,
    max_players: Union[Unset, None, int] = UNSET,
    parent_index_number: Union[Unset, None, int] = UNSET,
    has_parental_rating: Union[Unset, None, bool] = UNSET,
    is_hd: Union[Unset, None, bool] = UNSET,
    location_types: Union[Unset, None, str] = UNSET,
    exclude_location_types: Union[Unset, None, str] = UNSET,
    is_missing: Union[Unset, None, bool] = UNSET,
    is_unaired: Union[Unset, None, bool] = UNSET,
    min_community_rating: Union[Unset, None, float] = UNSET,
    min_critic_rating: Union[Unset, None, float] = UNSET,
    aired_during_season: Union[Unset, None, int] = UNSET,
    min_premiere_date: Union[Unset, None, str] = UNSET,
    min_date_last_saved: Union[Unset, None, str] = UNSET,
    min_date_last_saved_for_user: Union[Unset, None, str] = UNSET,
    max_premiere_date: Union[Unset, None, str] = UNSET,
    has_overview: Union[Unset, None, bool] = UNSET,
    has_imdb_id: Union[Unset, None, bool] = UNSET,
    has_tmdb_id: Union[Unset, None, bool] = UNSET,
    has_tvdb_id: Union[Unset, None, bool] = UNSET,
    exclude_item_ids: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    recursive: Union[Unset, None, bool] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    exclude_item_types: Union[Unset, None, str] = UNSET,
    include_item_types: Union[Unset, None, str] = UNSET,
    any_provider_id_equals: Union[Unset, None, str] = UNSET,
    filters: Union[Unset, None, str] = UNSET,
    is_favorite: Union[Unset, None, bool] = UNSET,
    is_movie: Union[Unset, None, bool] = UNSET,
    is_series: Union[Unset, None, bool] = UNSET,
    is_folder: Union[Unset, None, bool] = UNSET,
    is_news: Union[Unset, None, bool] = UNSET,
    is_kids: Union[Unset, None, bool] = UNSET,
    is_sports: Union[Unset, None, bool] = UNSET,
    project_to_media: Union[Unset, None, bool] = UNSET,
    media_types: Union[Unset, None, str] = UNSET,
    image_types: Union[Unset, None, str] = UNSET,
    sort_by: Union[Unset, None, str] = UNSET,
    is_played: Union[Unset, None, bool] = UNSET,
    genres: Union[Unset, None, str] = UNSET,
    official_ratings: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    years: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    person: Union[Unset, None, str] = UNSET,
    person_ids: Union[Unset, None, str] = UNSET,
    person_types: Union[Unset, None, str] = UNSET,
    studios: Union[Unset, None, str] = UNSET,
    studio_ids: Union[Unset, None, str] = UNSET,
    artists: Union[Unset, None, str] = UNSET,
    artist_ids: Union[Unset, None, str] = UNSET,
    albums: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    video_types: Union[Unset, None, str] = UNSET,
    containers: Union[Unset, None, str] = UNSET,
    audio_codecs: Union[Unset, None, str] = UNSET,
    audio_layouts: Union[Unset, None, str] = UNSET,
    video_codecs: Union[Unset, None, str] = UNSET,
    subtitle_codecs: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    min_official_rating: Union[Unset, None, str] = UNSET,
    is_locked: Union[Unset, None, bool] = UNSET,
    is_place_holder: Union[Unset, None, bool] = UNSET,
    has_official_rating: Union[Unset, None, bool] = UNSET,
    group_items_into_collections: Union[Unset, None, bool] = UNSET,
    is_3d: Union[Unset, None, bool] = UNSET,
    series_status: Union[Unset, None, str] = UNSET,
    name_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    artist_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    album_artist_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    name_starts_with: Union[Unset, None, str] = UNSET,
    name_less_than: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, QueryResultUserLibraryTagItem]]:
    """Gets items based on a query.

     Requires authentication as user

    Args:
        artist_type (Union[Unset, None, str]):
        max_official_rating (Union[Unset, None, str]):
        has_theme_song (Union[Unset, None, bool]):
        has_theme_video (Union[Unset, None, bool]):
        has_subtitles (Union[Unset, None, bool]):
        has_special_feature (Union[Unset, None, bool]):
        has_trailer (Union[Unset, None, bool]):
        adjacent_to (Union[Unset, None, str]):
        min_index_number (Union[Unset, None, int]):
        min_players (Union[Unset, None, int]):
        max_players (Union[Unset, None, int]):
        parent_index_number (Union[Unset, None, int]):
        has_parental_rating (Union[Unset, None, bool]):
        is_hd (Union[Unset, None, bool]):
        location_types (Union[Unset, None, str]):
        exclude_location_types (Union[Unset, None, str]):
        is_missing (Union[Unset, None, bool]):
        is_unaired (Union[Unset, None, bool]):
        min_community_rating (Union[Unset, None, float]):
        min_critic_rating (Union[Unset, None, float]):
        aired_during_season (Union[Unset, None, int]):
        min_premiere_date (Union[Unset, None, str]):
        min_date_last_saved (Union[Unset, None, str]):
        min_date_last_saved_for_user (Union[Unset, None, str]):
        max_premiere_date (Union[Unset, None, str]):
        has_overview (Union[Unset, None, bool]):
        has_imdb_id (Union[Unset, None, bool]):
        has_tmdb_id (Union[Unset, None, bool]):
        has_tvdb_id (Union[Unset, None, bool]):
        exclude_item_ids (Union[Unset, None, str]):
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        recursive (Union[Unset, None, bool]):
        search_term (Union[Unset, None, str]):
        sort_order (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        fields (Union[Unset, None, str]):
        exclude_item_types (Union[Unset, None, str]):
        include_item_types (Union[Unset, None, str]):
        any_provider_id_equals (Union[Unset, None, str]):
        filters (Union[Unset, None, str]):
        is_favorite (Union[Unset, None, bool]):
        is_movie (Union[Unset, None, bool]):
        is_series (Union[Unset, None, bool]):
        is_folder (Union[Unset, None, bool]):
        is_news (Union[Unset, None, bool]):
        is_kids (Union[Unset, None, bool]):
        is_sports (Union[Unset, None, bool]):
        project_to_media (Union[Unset, None, bool]):
        media_types (Union[Unset, None, str]):
        image_types (Union[Unset, None, str]):
        sort_by (Union[Unset, None, str]):
        is_played (Union[Unset, None, bool]):
        genres (Union[Unset, None, str]):
        official_ratings (Union[Unset, None, str]):
        tags (Union[Unset, None, str]):
        years (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        person (Union[Unset, None, str]):
        person_ids (Union[Unset, None, str]):
        person_types (Union[Unset, None, str]):
        studios (Union[Unset, None, str]):
        studio_ids (Union[Unset, None, str]):
        artists (Union[Unset, None, str]):
        artist_ids (Union[Unset, None, str]):
        albums (Union[Unset, None, str]):
        ids (Union[Unset, None, str]):
        video_types (Union[Unset, None, str]):
        containers (Union[Unset, None, str]):
        audio_codecs (Union[Unset, None, str]):
        audio_layouts (Union[Unset, None, str]):
        video_codecs (Union[Unset, None, str]):
        subtitle_codecs (Union[Unset, None, str]):
        path (Union[Unset, None, str]):
        user_id (Union[Unset, None, str]):
        min_official_rating (Union[Unset, None, str]):
        is_locked (Union[Unset, None, bool]):
        is_place_holder (Union[Unset, None, bool]):
        has_official_rating (Union[Unset, None, bool]):
        group_items_into_collections (Union[Unset, None, bool]):
        is_3d (Union[Unset, None, bool]):
        series_status (Union[Unset, None, str]):
        name_starts_with_or_greater (Union[Unset, None, str]):
        artist_starts_with_or_greater (Union[Unset, None, str]):
        album_artist_starts_with_or_greater (Union[Unset, None, str]):
        name_starts_with (Union[Unset, None, str]):
        name_less_than (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultUserLibraryTagItem]]
    """

    kwargs = _get_kwargs(
        client=client,
        artist_type=artist_type,
        max_official_rating=max_official_rating,
        has_theme_song=has_theme_song,
        has_theme_video=has_theme_video,
        has_subtitles=has_subtitles,
        has_special_feature=has_special_feature,
        has_trailer=has_trailer,
        adjacent_to=adjacent_to,
        min_index_number=min_index_number,
        min_players=min_players,
        max_players=max_players,
        parent_index_number=parent_index_number,
        has_parental_rating=has_parental_rating,
        is_hd=is_hd,
        location_types=location_types,
        exclude_location_types=exclude_location_types,
        is_missing=is_missing,
        is_unaired=is_unaired,
        min_community_rating=min_community_rating,
        min_critic_rating=min_critic_rating,
        aired_during_season=aired_during_season,
        min_premiere_date=min_premiere_date,
        min_date_last_saved=min_date_last_saved,
        min_date_last_saved_for_user=min_date_last_saved_for_user,
        max_premiere_date=max_premiere_date,
        has_overview=has_overview,
        has_imdb_id=has_imdb_id,
        has_tmdb_id=has_tmdb_id,
        has_tvdb_id=has_tvdb_id,
        exclude_item_ids=exclude_item_ids,
        start_index=start_index,
        limit=limit,
        recursive=recursive,
        search_term=search_term,
        sort_order=sort_order,
        parent_id=parent_id,
        fields=fields,
        exclude_item_types=exclude_item_types,
        include_item_types=include_item_types,
        any_provider_id_equals=any_provider_id_equals,
        filters=filters,
        is_favorite=is_favorite,
        is_movie=is_movie,
        is_series=is_series,
        is_folder=is_folder,
        is_news=is_news,
        is_kids=is_kids,
        is_sports=is_sports,
        project_to_media=project_to_media,
        media_types=media_types,
        image_types=image_types,
        sort_by=sort_by,
        is_played=is_played,
        genres=genres,
        official_ratings=official_ratings,
        tags=tags,
        years=years,
        enable_images=enable_images,
        enable_user_data=enable_user_data,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        person=person,
        person_ids=person_ids,
        person_types=person_types,
        studios=studios,
        studio_ids=studio_ids,
        artists=artists,
        artist_ids=artist_ids,
        albums=albums,
        ids=ids,
        video_types=video_types,
        containers=containers,
        audio_codecs=audio_codecs,
        audio_layouts=audio_layouts,
        video_codecs=video_codecs,
        subtitle_codecs=subtitle_codecs,
        path=path,
        user_id=user_id,
        min_official_rating=min_official_rating,
        is_locked=is_locked,
        is_place_holder=is_place_holder,
        has_official_rating=has_official_rating,
        group_items_into_collections=group_items_into_collections,
        is_3d=is_3d,
        series_status=series_status,
        name_starts_with_or_greater=name_starts_with_or_greater,
        artist_starts_with_or_greater=artist_starts_with_or_greater,
        album_artist_starts_with_or_greater=album_artist_starts_with_or_greater,
        name_starts_with=name_starts_with,
        name_less_than=name_less_than,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    artist_type: Union[Unset, None, str] = UNSET,
    max_official_rating: Union[Unset, None, str] = UNSET,
    has_theme_song: Union[Unset, None, bool] = UNSET,
    has_theme_video: Union[Unset, None, bool] = UNSET,
    has_subtitles: Union[Unset, None, bool] = UNSET,
    has_special_feature: Union[Unset, None, bool] = UNSET,
    has_trailer: Union[Unset, None, bool] = UNSET,
    adjacent_to: Union[Unset, None, str] = UNSET,
    min_index_number: Union[Unset, None, int] = UNSET,
    min_players: Union[Unset, None, int] = UNSET,
    max_players: Union[Unset, None, int] = UNSET,
    parent_index_number: Union[Unset, None, int] = UNSET,
    has_parental_rating: Union[Unset, None, bool] = UNSET,
    is_hd: Union[Unset, None, bool] = UNSET,
    location_types: Union[Unset, None, str] = UNSET,
    exclude_location_types: Union[Unset, None, str] = UNSET,
    is_missing: Union[Unset, None, bool] = UNSET,
    is_unaired: Union[Unset, None, bool] = UNSET,
    min_community_rating: Union[Unset, None, float] = UNSET,
    min_critic_rating: Union[Unset, None, float] = UNSET,
    aired_during_season: Union[Unset, None, int] = UNSET,
    min_premiere_date: Union[Unset, None, str] = UNSET,
    min_date_last_saved: Union[Unset, None, str] = UNSET,
    min_date_last_saved_for_user: Union[Unset, None, str] = UNSET,
    max_premiere_date: Union[Unset, None, str] = UNSET,
    has_overview: Union[Unset, None, bool] = UNSET,
    has_imdb_id: Union[Unset, None, bool] = UNSET,
    has_tmdb_id: Union[Unset, None, bool] = UNSET,
    has_tvdb_id: Union[Unset, None, bool] = UNSET,
    exclude_item_ids: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    recursive: Union[Unset, None, bool] = UNSET,
    search_term: Union[Unset, None, str] = UNSET,
    sort_order: Union[Unset, None, str] = UNSET,
    parent_id: Union[Unset, None, str] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    exclude_item_types: Union[Unset, None, str] = UNSET,
    include_item_types: Union[Unset, None, str] = UNSET,
    any_provider_id_equals: Union[Unset, None, str] = UNSET,
    filters: Union[Unset, None, str] = UNSET,
    is_favorite: Union[Unset, None, bool] = UNSET,
    is_movie: Union[Unset, None, bool] = UNSET,
    is_series: Union[Unset, None, bool] = UNSET,
    is_folder: Union[Unset, None, bool] = UNSET,
    is_news: Union[Unset, None, bool] = UNSET,
    is_kids: Union[Unset, None, bool] = UNSET,
    is_sports: Union[Unset, None, bool] = UNSET,
    project_to_media: Union[Unset, None, bool] = UNSET,
    media_types: Union[Unset, None, str] = UNSET,
    image_types: Union[Unset, None, str] = UNSET,
    sort_by: Union[Unset, None, str] = UNSET,
    is_played: Union[Unset, None, bool] = UNSET,
    genres: Union[Unset, None, str] = UNSET,
    official_ratings: Union[Unset, None, str] = UNSET,
    tags: Union[Unset, None, str] = UNSET,
    years: Union[Unset, None, str] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    person: Union[Unset, None, str] = UNSET,
    person_ids: Union[Unset, None, str] = UNSET,
    person_types: Union[Unset, None, str] = UNSET,
    studios: Union[Unset, None, str] = UNSET,
    studio_ids: Union[Unset, None, str] = UNSET,
    artists: Union[Unset, None, str] = UNSET,
    artist_ids: Union[Unset, None, str] = UNSET,
    albums: Union[Unset, None, str] = UNSET,
    ids: Union[Unset, None, str] = UNSET,
    video_types: Union[Unset, None, str] = UNSET,
    containers: Union[Unset, None, str] = UNSET,
    audio_codecs: Union[Unset, None, str] = UNSET,
    audio_layouts: Union[Unset, None, str] = UNSET,
    video_codecs: Union[Unset, None, str] = UNSET,
    subtitle_codecs: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    min_official_rating: Union[Unset, None, str] = UNSET,
    is_locked: Union[Unset, None, bool] = UNSET,
    is_place_holder: Union[Unset, None, bool] = UNSET,
    has_official_rating: Union[Unset, None, bool] = UNSET,
    group_items_into_collections: Union[Unset, None, bool] = UNSET,
    is_3d: Union[Unset, None, bool] = UNSET,
    series_status: Union[Unset, None, str] = UNSET,
    name_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    artist_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    album_artist_starts_with_or_greater: Union[Unset, None, str] = UNSET,
    name_starts_with: Union[Unset, None, str] = UNSET,
    name_less_than: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, QueryResultUserLibraryTagItem]]:
    """Gets items based on a query.

     Requires authentication as user

    Args:
        artist_type (Union[Unset, None, str]):
        max_official_rating (Union[Unset, None, str]):
        has_theme_song (Union[Unset, None, bool]):
        has_theme_video (Union[Unset, None, bool]):
        has_subtitles (Union[Unset, None, bool]):
        has_special_feature (Union[Unset, None, bool]):
        has_trailer (Union[Unset, None, bool]):
        adjacent_to (Union[Unset, None, str]):
        min_index_number (Union[Unset, None, int]):
        min_players (Union[Unset, None, int]):
        max_players (Union[Unset, None, int]):
        parent_index_number (Union[Unset, None, int]):
        has_parental_rating (Union[Unset, None, bool]):
        is_hd (Union[Unset, None, bool]):
        location_types (Union[Unset, None, str]):
        exclude_location_types (Union[Unset, None, str]):
        is_missing (Union[Unset, None, bool]):
        is_unaired (Union[Unset, None, bool]):
        min_community_rating (Union[Unset, None, float]):
        min_critic_rating (Union[Unset, None, float]):
        aired_during_season (Union[Unset, None, int]):
        min_premiere_date (Union[Unset, None, str]):
        min_date_last_saved (Union[Unset, None, str]):
        min_date_last_saved_for_user (Union[Unset, None, str]):
        max_premiere_date (Union[Unset, None, str]):
        has_overview (Union[Unset, None, bool]):
        has_imdb_id (Union[Unset, None, bool]):
        has_tmdb_id (Union[Unset, None, bool]):
        has_tvdb_id (Union[Unset, None, bool]):
        exclude_item_ids (Union[Unset, None, str]):
        start_index (Union[Unset, None, int]):
        limit (Union[Unset, None, int]):
        recursive (Union[Unset, None, bool]):
        search_term (Union[Unset, None, str]):
        sort_order (Union[Unset, None, str]):
        parent_id (Union[Unset, None, str]):
        fields (Union[Unset, None, str]):
        exclude_item_types (Union[Unset, None, str]):
        include_item_types (Union[Unset, None, str]):
        any_provider_id_equals (Union[Unset, None, str]):
        filters (Union[Unset, None, str]):
        is_favorite (Union[Unset, None, bool]):
        is_movie (Union[Unset, None, bool]):
        is_series (Union[Unset, None, bool]):
        is_folder (Union[Unset, None, bool]):
        is_news (Union[Unset, None, bool]):
        is_kids (Union[Unset, None, bool]):
        is_sports (Union[Unset, None, bool]):
        project_to_media (Union[Unset, None, bool]):
        media_types (Union[Unset, None, str]):
        image_types (Union[Unset, None, str]):
        sort_by (Union[Unset, None, str]):
        is_played (Union[Unset, None, bool]):
        genres (Union[Unset, None, str]):
        official_ratings (Union[Unset, None, str]):
        tags (Union[Unset, None, str]):
        years (Union[Unset, None, str]):
        enable_images (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        person (Union[Unset, None, str]):
        person_ids (Union[Unset, None, str]):
        person_types (Union[Unset, None, str]):
        studios (Union[Unset, None, str]):
        studio_ids (Union[Unset, None, str]):
        artists (Union[Unset, None, str]):
        artist_ids (Union[Unset, None, str]):
        albums (Union[Unset, None, str]):
        ids (Union[Unset, None, str]):
        video_types (Union[Unset, None, str]):
        containers (Union[Unset, None, str]):
        audio_codecs (Union[Unset, None, str]):
        audio_layouts (Union[Unset, None, str]):
        video_codecs (Union[Unset, None, str]):
        subtitle_codecs (Union[Unset, None, str]):
        path (Union[Unset, None, str]):
        user_id (Union[Unset, None, str]):
        min_official_rating (Union[Unset, None, str]):
        is_locked (Union[Unset, None, bool]):
        is_place_holder (Union[Unset, None, bool]):
        has_official_rating (Union[Unset, None, bool]):
        group_items_into_collections (Union[Unset, None, bool]):
        is_3d (Union[Unset, None, bool]):
        series_status (Union[Unset, None, str]):
        name_starts_with_or_greater (Union[Unset, None, str]):
        artist_starts_with_or_greater (Union[Unset, None, str]):
        album_artist_starts_with_or_greater (Union[Unset, None, str]):
        name_starts_with (Union[Unset, None, str]):
        name_less_than (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultUserLibraryTagItem]
    """

    return (
        await asyncio_detailed(
            client=client,
            artist_type=artist_type,
            max_official_rating=max_official_rating,
            has_theme_song=has_theme_song,
            has_theme_video=has_theme_video,
            has_subtitles=has_subtitles,
            has_special_feature=has_special_feature,
            has_trailer=has_trailer,
            adjacent_to=adjacent_to,
            min_index_number=min_index_number,
            min_players=min_players,
            max_players=max_players,
            parent_index_number=parent_index_number,
            has_parental_rating=has_parental_rating,
            is_hd=is_hd,
            location_types=location_types,
            exclude_location_types=exclude_location_types,
            is_missing=is_missing,
            is_unaired=is_unaired,
            min_community_rating=min_community_rating,
            min_critic_rating=min_critic_rating,
            aired_during_season=aired_during_season,
            min_premiere_date=min_premiere_date,
            min_date_last_saved=min_date_last_saved,
            min_date_last_saved_for_user=min_date_last_saved_for_user,
            max_premiere_date=max_premiere_date,
            has_overview=has_overview,
            has_imdb_id=has_imdb_id,
            has_tmdb_id=has_tmdb_id,
            has_tvdb_id=has_tvdb_id,
            exclude_item_ids=exclude_item_ids,
            start_index=start_index,
            limit=limit,
            recursive=recursive,
            search_term=search_term,
            sort_order=sort_order,
            parent_id=parent_id,
            fields=fields,
            exclude_item_types=exclude_item_types,
            include_item_types=include_item_types,
            any_provider_id_equals=any_provider_id_equals,
            filters=filters,
            is_favorite=is_favorite,
            is_movie=is_movie,
            is_series=is_series,
            is_folder=is_folder,
            is_news=is_news,
            is_kids=is_kids,
            is_sports=is_sports,
            project_to_media=project_to_media,
            media_types=media_types,
            image_types=image_types,
            sort_by=sort_by,
            is_played=is_played,
            genres=genres,
            official_ratings=official_ratings,
            tags=tags,
            years=years,
            enable_images=enable_images,
            enable_user_data=enable_user_data,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            person=person,
            person_ids=person_ids,
            person_types=person_types,
            studios=studios,
            studio_ids=studio_ids,
            artists=artists,
            artist_ids=artist_ids,
            albums=albums,
            ids=ids,
            video_types=video_types,
            containers=containers,
            audio_codecs=audio_codecs,
            audio_layouts=audio_layouts,
            video_codecs=video_codecs,
            subtitle_codecs=subtitle_codecs,
            path=path,
            user_id=user_id,
            min_official_rating=min_official_rating,
            is_locked=is_locked,
            is_place_holder=is_place_holder,
            has_official_rating=has_official_rating,
            group_items_into_collections=group_items_into_collections,
            is_3d=is_3d,
            series_status=series_status,
            name_starts_with_or_greater=name_starts_with_or_greater,
            artist_starts_with_or_greater=artist_starts_with_or_greater,
            album_artist_starts_with_or_greater=album_artist_starts_with_or_greater,
            name_starts_with=name_starts_with,
            name_less_than=name_less_than,
        )
    ).parsed
