"""Keep track of flagged videos"""


class Flagged:
	def __init__(self):
		"""Flagged class innitiated"""
		self._flag_videos = {}

	def get_flag_videos(self):
		return self._flag_videos

	def add_flag_video(self, video_id, reason):
		if video_id in self._flag_videos:
			return False
		else:
			self._flag_videos[video_id] = reason
			return True

	def find_flag_video(self, video_id):
		if video_id in self._flag_videos:
			return True
		else:
			return False

