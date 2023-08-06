from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.live_tv_channel_type import LiveTvChannelType
from ...models.query_result_live_tv_api_epg_row import QueryResultLiveTVApiEpgRow
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    type: Union[Unset, None, LiveTvChannelType] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    genre_ids: Union[Unset, None, str] = UNSET,
    min_start_date: Union[Unset, None, str] = UNSET,
    max_start_date: Union[Unset, None, str] = UNSET,
    min_end_date: Union[Unset, None, str] = UNSET,
    max_end_date: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    is_movie: Union[Unset, None, bool] = UNSET,
    is_series: Union[Unset, None, bool] = UNSET,
    is_news: Union[Unset, None, bool] = UNSET,
    is_kids: Union[Unset, None, bool] = UNSET,
    is_sports: Union[Unset, None, bool] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    is_favorite: Union[Unset, None, bool] = UNSET,
    is_liked: Union[Unset, None, bool] = UNSET,
    is_disliked: Union[Unset, None, bool] = UNSET,
    enable_favorite_sorting: Union[Unset, None, bool] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    add_current_program: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    channel_ids: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/LiveTv/EPG".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_type: Union[Unset, None, str] = UNSET
    if not isinstance(type, Unset):
        json_type = type.value if type else None

    params["Type"] = json_type

    params["UserId"] = user_id

    params["GenreIds"] = genre_ids

    params["MinStartDate"] = min_start_date

    params["MaxStartDate"] = max_start_date

    params["MinEndDate"] = min_end_date

    params["MaxEndDate"] = max_end_date

    params["StartIndex"] = start_index

    params["IsMovie"] = is_movie

    params["IsSeries"] = is_series

    params["IsNews"] = is_news

    params["IsKids"] = is_kids

    params["IsSports"] = is_sports

    params["Limit"] = limit

    params["IsFavorite"] = is_favorite

    params["IsLiked"] = is_liked

    params["IsDisliked"] = is_disliked

    params["EnableFavoriteSorting"] = enable_favorite_sorting

    params["EnableImages"] = enable_images

    params["ImageTypeLimit"] = image_type_limit

    params["EnableImageTypes"] = enable_image_types

    params["Fields"] = fields

    params["AddCurrentProgram"] = add_current_program

    params["EnableUserData"] = enable_user_data

    params["ChannelIds"] = channel_ids

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


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, QueryResultLiveTVApiEpgRow]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = QueryResultLiveTVApiEpgRow.from_dict(response.json())

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


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, QueryResultLiveTVApiEpgRow]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    type: Union[Unset, None, LiveTvChannelType] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    genre_ids: Union[Unset, None, str] = UNSET,
    min_start_date: Union[Unset, None, str] = UNSET,
    max_start_date: Union[Unset, None, str] = UNSET,
    min_end_date: Union[Unset, None, str] = UNSET,
    max_end_date: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    is_movie: Union[Unset, None, bool] = UNSET,
    is_series: Union[Unset, None, bool] = UNSET,
    is_news: Union[Unset, None, bool] = UNSET,
    is_kids: Union[Unset, None, bool] = UNSET,
    is_sports: Union[Unset, None, bool] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    is_favorite: Union[Unset, None, bool] = UNSET,
    is_liked: Union[Unset, None, bool] = UNSET,
    is_disliked: Union[Unset, None, bool] = UNSET,
    enable_favorite_sorting: Union[Unset, None, bool] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    add_current_program: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    channel_ids: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, QueryResultLiveTVApiEpgRow]]:
    """Gets the epg.

     Requires authentication as user

    Args:
        type (Union[Unset, None, LiveTvChannelType]):
        user_id (Union[Unset, None, str]):
        genre_ids (Union[Unset, None, str]):
        min_start_date (Union[Unset, None, str]):
        max_start_date (Union[Unset, None, str]):
        min_end_date (Union[Unset, None, str]):
        max_end_date (Union[Unset, None, str]):
        start_index (Union[Unset, None, int]):
        is_movie (Union[Unset, None, bool]):
        is_series (Union[Unset, None, bool]):
        is_news (Union[Unset, None, bool]):
        is_kids (Union[Unset, None, bool]):
        is_sports (Union[Unset, None, bool]):
        limit (Union[Unset, None, int]):
        is_favorite (Union[Unset, None, bool]):
        is_liked (Union[Unset, None, bool]):
        is_disliked (Union[Unset, None, bool]):
        enable_favorite_sorting (Union[Unset, None, bool]):
        enable_images (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        fields (Union[Unset, None, str]):
        add_current_program (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        channel_ids (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultLiveTVApiEpgRow]]
    """

    kwargs = _get_kwargs(
        client=client,
        type=type,
        user_id=user_id,
        genre_ids=genre_ids,
        min_start_date=min_start_date,
        max_start_date=max_start_date,
        min_end_date=min_end_date,
        max_end_date=max_end_date,
        start_index=start_index,
        is_movie=is_movie,
        is_series=is_series,
        is_news=is_news,
        is_kids=is_kids,
        is_sports=is_sports,
        limit=limit,
        is_favorite=is_favorite,
        is_liked=is_liked,
        is_disliked=is_disliked,
        enable_favorite_sorting=enable_favorite_sorting,
        enable_images=enable_images,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        fields=fields,
        add_current_program=add_current_program,
        enable_user_data=enable_user_data,
        channel_ids=channel_ids,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    type: Union[Unset, None, LiveTvChannelType] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    genre_ids: Union[Unset, None, str] = UNSET,
    min_start_date: Union[Unset, None, str] = UNSET,
    max_start_date: Union[Unset, None, str] = UNSET,
    min_end_date: Union[Unset, None, str] = UNSET,
    max_end_date: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    is_movie: Union[Unset, None, bool] = UNSET,
    is_series: Union[Unset, None, bool] = UNSET,
    is_news: Union[Unset, None, bool] = UNSET,
    is_kids: Union[Unset, None, bool] = UNSET,
    is_sports: Union[Unset, None, bool] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    is_favorite: Union[Unset, None, bool] = UNSET,
    is_liked: Union[Unset, None, bool] = UNSET,
    is_disliked: Union[Unset, None, bool] = UNSET,
    enable_favorite_sorting: Union[Unset, None, bool] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    add_current_program: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    channel_ids: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, QueryResultLiveTVApiEpgRow]]:
    """Gets the epg.

     Requires authentication as user

    Args:
        type (Union[Unset, None, LiveTvChannelType]):
        user_id (Union[Unset, None, str]):
        genre_ids (Union[Unset, None, str]):
        min_start_date (Union[Unset, None, str]):
        max_start_date (Union[Unset, None, str]):
        min_end_date (Union[Unset, None, str]):
        max_end_date (Union[Unset, None, str]):
        start_index (Union[Unset, None, int]):
        is_movie (Union[Unset, None, bool]):
        is_series (Union[Unset, None, bool]):
        is_news (Union[Unset, None, bool]):
        is_kids (Union[Unset, None, bool]):
        is_sports (Union[Unset, None, bool]):
        limit (Union[Unset, None, int]):
        is_favorite (Union[Unset, None, bool]):
        is_liked (Union[Unset, None, bool]):
        is_disliked (Union[Unset, None, bool]):
        enable_favorite_sorting (Union[Unset, None, bool]):
        enable_images (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        fields (Union[Unset, None, str]):
        add_current_program (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        channel_ids (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultLiveTVApiEpgRow]
    """

    return sync_detailed(
        client=client,
        type=type,
        user_id=user_id,
        genre_ids=genre_ids,
        min_start_date=min_start_date,
        max_start_date=max_start_date,
        min_end_date=min_end_date,
        max_end_date=max_end_date,
        start_index=start_index,
        is_movie=is_movie,
        is_series=is_series,
        is_news=is_news,
        is_kids=is_kids,
        is_sports=is_sports,
        limit=limit,
        is_favorite=is_favorite,
        is_liked=is_liked,
        is_disliked=is_disliked,
        enable_favorite_sorting=enable_favorite_sorting,
        enable_images=enable_images,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        fields=fields,
        add_current_program=add_current_program,
        enable_user_data=enable_user_data,
        channel_ids=channel_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    type: Union[Unset, None, LiveTvChannelType] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    genre_ids: Union[Unset, None, str] = UNSET,
    min_start_date: Union[Unset, None, str] = UNSET,
    max_start_date: Union[Unset, None, str] = UNSET,
    min_end_date: Union[Unset, None, str] = UNSET,
    max_end_date: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    is_movie: Union[Unset, None, bool] = UNSET,
    is_series: Union[Unset, None, bool] = UNSET,
    is_news: Union[Unset, None, bool] = UNSET,
    is_kids: Union[Unset, None, bool] = UNSET,
    is_sports: Union[Unset, None, bool] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    is_favorite: Union[Unset, None, bool] = UNSET,
    is_liked: Union[Unset, None, bool] = UNSET,
    is_disliked: Union[Unset, None, bool] = UNSET,
    enable_favorite_sorting: Union[Unset, None, bool] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    add_current_program: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    channel_ids: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, QueryResultLiveTVApiEpgRow]]:
    """Gets the epg.

     Requires authentication as user

    Args:
        type (Union[Unset, None, LiveTvChannelType]):
        user_id (Union[Unset, None, str]):
        genre_ids (Union[Unset, None, str]):
        min_start_date (Union[Unset, None, str]):
        max_start_date (Union[Unset, None, str]):
        min_end_date (Union[Unset, None, str]):
        max_end_date (Union[Unset, None, str]):
        start_index (Union[Unset, None, int]):
        is_movie (Union[Unset, None, bool]):
        is_series (Union[Unset, None, bool]):
        is_news (Union[Unset, None, bool]):
        is_kids (Union[Unset, None, bool]):
        is_sports (Union[Unset, None, bool]):
        limit (Union[Unset, None, int]):
        is_favorite (Union[Unset, None, bool]):
        is_liked (Union[Unset, None, bool]):
        is_disliked (Union[Unset, None, bool]):
        enable_favorite_sorting (Union[Unset, None, bool]):
        enable_images (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        fields (Union[Unset, None, str]):
        add_current_program (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        channel_ids (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResultLiveTVApiEpgRow]]
    """

    kwargs = _get_kwargs(
        client=client,
        type=type,
        user_id=user_id,
        genre_ids=genre_ids,
        min_start_date=min_start_date,
        max_start_date=max_start_date,
        min_end_date=min_end_date,
        max_end_date=max_end_date,
        start_index=start_index,
        is_movie=is_movie,
        is_series=is_series,
        is_news=is_news,
        is_kids=is_kids,
        is_sports=is_sports,
        limit=limit,
        is_favorite=is_favorite,
        is_liked=is_liked,
        is_disliked=is_disliked,
        enable_favorite_sorting=enable_favorite_sorting,
        enable_images=enable_images,
        image_type_limit=image_type_limit,
        enable_image_types=enable_image_types,
        fields=fields,
        add_current_program=add_current_program,
        enable_user_data=enable_user_data,
        channel_ids=channel_ids,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    type: Union[Unset, None, LiveTvChannelType] = UNSET,
    user_id: Union[Unset, None, str] = UNSET,
    genre_ids: Union[Unset, None, str] = UNSET,
    min_start_date: Union[Unset, None, str] = UNSET,
    max_start_date: Union[Unset, None, str] = UNSET,
    min_end_date: Union[Unset, None, str] = UNSET,
    max_end_date: Union[Unset, None, str] = UNSET,
    start_index: Union[Unset, None, int] = UNSET,
    is_movie: Union[Unset, None, bool] = UNSET,
    is_series: Union[Unset, None, bool] = UNSET,
    is_news: Union[Unset, None, bool] = UNSET,
    is_kids: Union[Unset, None, bool] = UNSET,
    is_sports: Union[Unset, None, bool] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    is_favorite: Union[Unset, None, bool] = UNSET,
    is_liked: Union[Unset, None, bool] = UNSET,
    is_disliked: Union[Unset, None, bool] = UNSET,
    enable_favorite_sorting: Union[Unset, None, bool] = UNSET,
    enable_images: Union[Unset, None, bool] = UNSET,
    image_type_limit: Union[Unset, None, int] = UNSET,
    enable_image_types: Union[Unset, None, str] = UNSET,
    fields: Union[Unset, None, str] = UNSET,
    add_current_program: Union[Unset, None, bool] = UNSET,
    enable_user_data: Union[Unset, None, bool] = UNSET,
    channel_ids: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, QueryResultLiveTVApiEpgRow]]:
    """Gets the epg.

     Requires authentication as user

    Args:
        type (Union[Unset, None, LiveTvChannelType]):
        user_id (Union[Unset, None, str]):
        genre_ids (Union[Unset, None, str]):
        min_start_date (Union[Unset, None, str]):
        max_start_date (Union[Unset, None, str]):
        min_end_date (Union[Unset, None, str]):
        max_end_date (Union[Unset, None, str]):
        start_index (Union[Unset, None, int]):
        is_movie (Union[Unset, None, bool]):
        is_series (Union[Unset, None, bool]):
        is_news (Union[Unset, None, bool]):
        is_kids (Union[Unset, None, bool]):
        is_sports (Union[Unset, None, bool]):
        limit (Union[Unset, None, int]):
        is_favorite (Union[Unset, None, bool]):
        is_liked (Union[Unset, None, bool]):
        is_disliked (Union[Unset, None, bool]):
        enable_favorite_sorting (Union[Unset, None, bool]):
        enable_images (Union[Unset, None, bool]):
        image_type_limit (Union[Unset, None, int]):
        enable_image_types (Union[Unset, None, str]):
        fields (Union[Unset, None, str]):
        add_current_program (Union[Unset, None, bool]):
        enable_user_data (Union[Unset, None, bool]):
        channel_ids (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResultLiveTVApiEpgRow]
    """

    return (
        await asyncio_detailed(
            client=client,
            type=type,
            user_id=user_id,
            genre_ids=genre_ids,
            min_start_date=min_start_date,
            max_start_date=max_start_date,
            min_end_date=min_end_date,
            max_end_date=max_end_date,
            start_index=start_index,
            is_movie=is_movie,
            is_series=is_series,
            is_news=is_news,
            is_kids=is_kids,
            is_sports=is_sports,
            limit=limit,
            is_favorite=is_favorite,
            is_liked=is_liked,
            is_disliked=is_disliked,
            enable_favorite_sorting=enable_favorite_sorting,
            enable_images=enable_images,
            image_type_limit=image_type_limit,
            enable_image_types=enable_image_types,
            fields=fields,
            add_current_program=add_current_program,
            enable_user_data=enable_user_data,
            channel_ids=channel_ids,
        )
    ).parsed
