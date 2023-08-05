import datetime

import dateutil.parser
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Union
from bs4 import BeautifulSoup

# Functions used to normalize Last.FM data types
def convert_empty_string_to_none(cls, value)->Optional[str]:
    """Converts an empty string to None."""
    return value if value != "" else None

def convert_number_to_bool(cls, value)->bool:
    """Converts a 1 to True and 0 to False."""
    if value == "1":
        return True
    elif value == "0":
        return False
    else:
        raise ValueError(f"Could not convert expected 1 or 0 to True or False: inptu string was: \"{value}\"")

def convert_string_to_datetime(cls, value)->datetime:
    """Converts a string to a datetime. All-inclusive to catch all possible formats."""
    return dateutil.parser.parse(value)

def convert_unix_timestamp_to_datetime(cls, value)->datetime.datetime:
    """Converts a unix timestamp to a datetime."""
    return datetime.datetime.fromtimestamp(int(value))

def convert_html_to_raw_text(cls, value)->Optional[str]:
    """Converts all HTML tags to text."""
    soup = BeautifulSoup(value, "html.parser")
    parsed_content = " ".join(soup.find_all(text=True)).replace("\n", " ") # Make sure to remove any newlines.
    if len(parsed_content) > 0:
        return parsed_content
    else:
        return None

# Some generic classes: belongs to multiple model types
class Image(BaseModel):
    """Represents an image of a certain size. Could be both artist and album images."""
    size: str
    url: str = Field(alias="#text")

class Date(BaseModel):
    """Represents a certain date."""
    timestamp: datetime.datetime = Field(alias="uts")
    text: str = Field(alias="#text")
    _normalize_timestamp = validator("timestamp", allow_reuse=True, pre=True)(convert_unix_timestamp_to_datetime)

class UndetailedMetadata(BaseModel):
    """Represents data for an undetailed album or artist in Last.FM that only includes two keys: #text and mbid."""
    text: str = Field(alias="#text")
    mbid: Optional[str]

class LinkMetadata(BaseModel):
    """Represents data for a link in the Last.Fm page"""
    href: str
    text: Optional[str] = Field(alias="#text")
    rel: Optional[str]


# Tags
class Tag(BaseModel):
    """Represents data for a tag in the Last.FM database."""
    name: str
    url: Optional[str]

class TagDetailsWiki(BaseModel):
    """Represents the wiki for a detailed tag in the Last.FM database (see TagDetails)"""
    summary: Optional[str] # Summary of the tag
    content: Optional[str] # Content of the tag description
    # Add normalizers for converting content to plaintext
    _normalize_summary = validator("summary", allow_reuse=True, pre=True)(convert_html_to_raw_text)
    _normalize_content = validator("content", allow_reuse=True, pre=True)(convert_html_to_raw_text)

class TagDetails(BaseModel):
    """Represents data for a detailed tag in the Last.FM database (as retrieved from the tag.getInfo) method"""
    name: str
    total: int
    reach: int
    wiki: TagDetailsWiki

class Tags(BaseModel):
    """Represents a list of tags."""
    tag: List[Tag]

# Artist-related  things
class ArtistStats(BaseModel):
    """Represents Last.FM stats for an artist."""
    listeners: int
    playcount: int

class ArtistBiographyLinks(BaseModel):
    """Represents the links in the biography of an artist."""
    link: LinkMetadata

class ArtistBiography(BaseModel):
    """Represents the biography of an artist."""
    links: ArtistBiographyLinks
    published: datetime.datetime
    summary: Optional[str] # Summary of the biography
    content: Optional[str] # Content of the biography
    # Add converter/normalizer for the published field to datetime
    _normalize_published = validator("published", allow_reuse=True, pre=True)(convert_string_to_datetime)
    # Add normalizers for converting content to plaintext
    _normalize_summary = validator("summary", allow_reuse=True, pre=True)(convert_html_to_raw_text)
    _normalize_content = validator("content", allow_reuse=True, pre=True)(convert_html_to_raw_text)

class Artist(BaseModel):
    """Reprensts a simple artist model."""
    name: str
    url: Optional[str]
    image: Optional[List[Image]]
    mbid: Optional[str]

class SimilarArtists(BaseModel):
    """Reprensts a list of similar artist for ArtistDetails."""
    artist: List[Artist]

class ArtistDetails(BaseModel):
    """Represents data for an artist retrieved using the artist search method."""
    name: str
    image: List[Image]
    url: Optional[str]
    mbid: Optional[str]
    stats: ArtistStats
    similar: SimilarArtists # Forward-reference to the artist because it hasn't been created yet.
    streamable: Optional[str]
    ontour: Optional[str]
    Tags: Optional[List[Tags]]
    bio: Optional[ArtistBiography]
    # Add normalizer to convert streamable and ontour value to True or False
    _normalize_streamable = validator("streamable", allow_reuse=True)(convert_number_to_bool)
    _normalize_ontour = validator("ontour", allow_reuse=True)(convert_number_to_bool)

# Track-related information
class TrackAttr(BaseModel):
    """Represents attributes for a track on an album."""
    rank: int

class Track(BaseModel):
    """Represents data for a track in the Last.FM database."""
    duration: Optional[int]
    artist: Artist
    url: str
    name: str
    streamable: Optional[Dict]
    attr: Optional[TrackAttr] = Field(alias="@attr")


class Tracks(BaseModel):
    """Represents a list of tracks."""
    track: List[Track]

class TracksUndetailed(BaseModel):
    """Represents a list of tracks in form of undetailed metadata."""
    track: List[UndetailedMetadata]


# Recent tracks. Note that Last.FM API calls them recenttracks rather than scrobbles,
# so we go by that in the model naming
class RecentTrack(BaseModel):
    """Represents a scrobbled track."""
    artist: UndetailedMetadata # The track artist(s)
    album: UndetailedMetadata # The album name
    image: List[Image] # The scrobble image
    mbid: str # A MusicBrainz ID
    date: Date # The data of the scrobble
    name: str # The name of the track
    url: Optional[str] # A link to the track
    # Add validator for converting an empty MusicBrainz string to None
    _normalize_mbid = validator("mbid", allow_reuse=True)(convert_empty_string_to_none)

class RecentTracksAttr(BaseModel):
    """Contains the metadata entry of RecentTracks, including username etc."""
    user: str
    page: int
    total: int
    # Some camelCase to snake_case conversion done below
    total_pages: int = Field(alias="totalPages")
    per_page: int = Field(alias="perPage")

class RecentTracks(BaseModel):
    """Represents basically what is returned from user.getRecentTracks - but it is contained within the subkey"""
    track: List[RecentTrack]
    attr: RecentTracksAttr = Field(alias="@attr")


# Album-related
class AlbumDetails(BaseModel):
    artist: str
    name: str
    listeners: int
    playcount: int
    tracks: Tracks
    image: List[Image]
    url: Optional[str]
    mbid: Optional[str]
    tags: Optional[Tags]

# Response models for API methods
class GetRecentTracksResponse(BaseModel):
    """Represents a response for the user.getRecentTracks API method."""
    recenttracks: RecentTracks

class GetAlbumDetailsResponse(BaseModel):
    """Represents a response for the album.getInfo API method."""
    album: AlbumDetails

class GetArtistResponse(BaseModel):
    """Represents a response for the artist.getInfo API method."""
    artist: ArtistDetails

class GetTagInfoResponse(BaseModel):
    """Represents a response for the tag.getInfo API method."""
    tag: TagDetails

METHOD_TO_MODEL = {
    "user.getRecentTracks": GetRecentTracksResponse,
    "album.getInfo": GetAlbumDetailsResponse,
    "artist.getInfo": GetArtistResponse,
    "tag.getInfo": GetTagInfoResponse
}

