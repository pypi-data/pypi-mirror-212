# Last.FM API Client

A partially complete Python wrapper for the Last.FM API that implements the functions that I need for my Album of the day website.

The wrapper uses `pydantic` models to parse responses which allows better type validation.

### Implemented API methods

The following [Last.FM API methods](https://www.last.fm/api/intro) are implemented:
* `album.getInfo` - get information about an album
* `artist.getInfo` - get information about an artist
* `tag.getInfo` - get information about a tag
* `user.getRecentTracks` - retrieve scrobbles