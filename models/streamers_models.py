from typing import Optional

from pydantic import AnyUrl, BaseModel


class StreamerIn(BaseModel):
    id: str
    user_id: str
    user_login: str
    user_name: str
    game_id: str
    game_name: str
    type: str
    title: str
    viewer_count: int
    started_at: str
    language: Optional[str] = None
    thumbnail_url: AnyUrl
    tag_ids: list
    tags: list[str]
    is_mature: bool


class StreamerOut(BaseModel):
    id: str
    user_name: str
    game_name: str
    type: str
    title: str
    viewer_count: int
    language: Optional[str] = None
    thumbnail_url: AnyUrl
