"""A playlists class."""
"""Keeps the individual video playlist"""

from .video_playlist import VideoPlaylist

class Playlists:
	"""A class used to represent a Playlists containing video playlists"""
	def __init__(self):
		self._playlist = {}

	def number_of_playlists(self):
		return len(self._playlist)

	def get_all_playlists(self):
		"""Returns all available playlist information from the playlist library."""
		return list(self._playlist.values())

	def get_playlist(self, playlist_name):
		"""Returns the videoplaylist object (name, content) from the playlists.

        Args:
            playlist_name: Name of playlist

        Returns:
            The VideoPlaylist object for the requested playlist_name. None if the playlist does not exist.
        """
		for i in self._playlist:
			if i.lower() == playlist_name.lower():
				return self._playlist[i]

	def add_playlist(self, playlist: VideoPlaylist):
		"""Adds a playlist into the dic of playlists

        Args:
            playlist: VideoPlaylist object
        """
		lower = [i.lower() for i in self._playlist.keys()]
		if playlist.name.lower() in lower:
			return False
		else:
			self._playlist[playlist.name] = playlist
			return True

	def remove_playlist(self, name):
		"""Remove a playlist from the dic of playlists

		Args:
			name: name of playlist
		"""
		lower = [i.lower() for i in self._playlist.keys()]
		if name.lower() in lower:
			self._playlist.pop(self.get_playlist(name).name)
			return True
		else:
			return False

