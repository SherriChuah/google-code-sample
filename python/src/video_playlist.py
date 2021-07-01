"""A video playlist class."""


class VideoPlaylist:
    """A class used to represent a Playlist."""

    def __init__(self, name: str):
        """VideoPlaylist constructor"""
        self._name = name
        self._content = []

    @property
    def name(self) -> str:
        """Returns the name of a playlist."""
        return self._name

    def number_of_contents(self):
        return len(self._content)

    def get_content(self):
        return self._content

    def add_to_content(self, video_id):
        if video_id in self._content:
            return False
        else:
            self._content += [video_id]
            return True

    def remove_from_content(self, video_id):
        if video_id in self._content:
            self._content.remove(video_id)
            return True
        else:
            return False

    def remove_all_content(self):
        self._content.clear()










