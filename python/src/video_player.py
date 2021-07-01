"""A video player class."""

from .video_library import VideoLibrary
from .playlists import Playlists
from .flag import Flagged
from .video_playlist import VideoPlaylist
from random import randint


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        """VideoPlayer Constructor"""
        self._video_library = VideoLibrary()
        self._playlists = Playlists()
        self._flagged = Flagged()
        self._curr_id = None
        self._is_pause = False

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")


    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")

        # sort the video titles in acending order
        lst = self._video_library.get_all_videos()
        lst.sort(key= lambda v: v.title)

        for video in lst:
            tags = " ".join(video.tags)

            if self._flagged.is_flag_video(video.video_id):
                print(f"{video.title} ({video.video_id}) [{tags}] - FLAGGED (reason: {self._flagged.get_flag_videos()[video.video_id]})")
            else:
                print(f"{video.title} ({video.video_id}) [{tags}]")


    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        if self._video_library.get_video(video_id):

            if self._flagged.is_flag_video(video_id):
                print(f"Cannot play video: Video is currently flagged (reason: {self._flagged.get_flag_videos()[video_id]})")

            else:
                if self._curr_id != None:
                    self.stop_video()

                print(f"Playing video: {self._video_library.get_video(video_id).title}")
                self._curr_id = video_id
                self._is_pause = False

        else:
            print("Cannot play video: Video does not exist")


    def stop_video(self):
        """Stops the current video."""
        if self._curr_id == None:
            print("Cannot stop video: No video is currently playing")
        else:
            print(f"Stopping video: {self._video_library.get_video(self._curr_id).title}")
            self._curr_id = None
            self._is_pause = False


    def play_random_video(self):
        """Plays a random video from the video library."""

        # all videos are flagged
        if len(self._flagged.get_flag_videos()) == len(self._video_library.get_all_videos()):
            print("No videos available")

        else:

            # randomly pick a number
            if self._curr_id:
                self.stop_video()

            num = randint(0, len(self._video_library.get_all_videos())-1)

            self.play_video(self._video_library.get_all_videos()[num].video_id)


    def pause_video(self):
        """Pauses the current video."""
        if self._is_pause:
            print(f"Video already paused: {self._video_library.get_video(self._curr_id).title}")
        else:
            if self._curr_id:
                print(f"Pausing video: {self._video_library.get_video(self._curr_id).title}")
                self._is_pause = True
            else:
                print("Cannot pause video: No video is currently playing")


    def continue_video(self):
        """Resumes playing the current video."""
        if self._is_pause:
            print(f"Continuing video: {self._video_library.get_video(self._curr_id).title}")
        else:
            if self._curr_id:
                print("Cannot continue video: Video is not paused")
            else:
                print("Cannot continue video: No video is currently playing")


    def show_playing(self):
        """Displays video currently playing."""
        if self._curr_id != None:
            the_video = self._video_library.get_video(self._curr_id)
            tags = " ".join(the_video.tags)

            if self._is_pause:
                print(f"Currently playing: {the_video.title} ({the_video.video_id}) [{tags}] - PAUSED")

            else:            
                print(f"Currently playing: {the_video.title} ({the_video.video_id}) [{tags}]")
        else:
            print("No video is currently playing")


    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self._playlists.add_playlist(VideoPlaylist(playlist_name)):
            print(f"Successfully created new playlist: {playlist_name}")
        else:
            print(f"Cannot create playlist: A playlist with the same name already exists")


    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if self._playlists.get_playlist(playlist_name.lower()):

            if self._flagged.is_flag_video(video_id):
                print(f"Cannot add video to my_playlist: Video is currently flagged (reason: {self._flagged.get_flag_videos()[video_id]})")

            else:
                try:
                    if self._playlists.get_playlist(playlist_name.lower()).add_to_content(video_id):
                        print(f"Added video to {playlist_name}: {self._video_library.get_video(video_id).title}")
                    else:
                        print(f"Cannot add video to {playlist_name}: Video already added")
                except:
                    print(f"Cannot add video to {playlist_name}: Video does not exist")
        else:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")


    def show_all_playlists(self):
        """Display all playlists."""
        if not self._playlists.number_of_playlists():
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")

            # sort the playlist names in acending order
            lst = self._playlists.get_all_playlists()
            lst.sort(key= lambda v: v.name)

            for playlist in lst:
                print(playlist.name)
        

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        try:
            if not self._playlists.get_playlist(playlist_name).number_of_contents():
                print(f"Showing playlist: {playlist_name}")
                print("No videos here yet")
            else:
                print(f"Showing playlist: {playlist_name}")
                for content in self._playlists.get_playlist(playlist_name).get_content():

                    # get the video from id
                    video = self._video_library.get_video(content)

                    tags = " ".join(video.tags)

                    # check if flagged
                    if self._flagged.is_flag_video(video.video_id):
                        print(f"{video.title} ({video.video_id}) [{tags}] - FLAGGED (reason: {self._flagged.get_flag_videos()[video.video_id]})")
                    else:
                        print(f"{video.title} ({video.video_id}) [{tags}]")
        except:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")


    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if self._playlists.get_playlist(playlist_name.lower()):

            if not self._video_library.get_video(video_id):
                 print(f"Cannot remove video from my_cool_playlist: Video does not exist")

            else:
                if not self._playlists.get_playlist(playlist_name.lower()).remove_from_content(video_id):
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
                else:
                    print(f"Removed video from {playlist_name}: {self._video_library.get_video(video_id).title}")
        else:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            self._playlists.get_playlist(playlist_name).remove_all_content()
            print(f"Successfully removed all videos from {playlist_name}")
        except:
            print(f"Cannot clear playlist my_cool_playlist: Playlist does not exist")


    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            if self._playlists.remove_playlist(playlist_name):
                print(f"Deleted playlist: {playlist_name}")
            else:
                print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        except:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")


    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        lst = [i for i in self._video_library.get_all_videos() if (search_term.lower() in i.title.lower()) and (not self._flagged.is_flag_video(i.video_id))]

        if len(lst):
            print(f"Here are the results for {search_term}:")

            for i in range(1,len(lst)+1):
                tags = " ".join(lst[i-1].tags)
                print(f'{i}) {lst[i-1].title} ({lst[i-1].video_id}) [{tags}]')

            print("Would you like to play any of the above? If yes, specify the number of the video.")

            print("If your answer is not a valid number, we will assume it's a no.")

            ans = input("")

            try:
                if (int(ans) <= len(lst)) and (int(ans) > 0):
                    self.play_video(lst[int(ans)-1].video_id)
            except:
                pass

        else:
            print(f"No search results for {search_term}")


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        lst = [i for i in self._video_library.get_all_videos() if (video_tag[1:].lower() in i.video_id.lower()) and (not self._flagged.is_flag_video(i.video_id))]

        if len(lst):
            print(f"Here are the results for {video_tag}:")

            for i in range(1,len(lst)+1):
                tags = " ".join(lst[i-1].tags)
                print(f'{i}) {lst[i-1].title} ({lst[i-1].video_id}) [{tags}]')

            print("Would you like to play any of the above? If yes, specify the number of the video.")

            print("If your answer is not a valid number, we will assume it's a no.")

            ans = input("")

            try:
                if (int(ans) <= len(lst)) and (int(ans) > 0):
                    self.play_video(lst[int(ans)-1].video_id)
            except:
                pass

        else:
            print(f"No search results for {video_tag}")


    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if self._video_library.get_video(video_id):

            if self._curr_id == video_id:
                self.stop_video()

            if self._flagged.add_flag_video(video_id, flag_reason):
                print(f"Successfully flagged video: {self._video_library.get_video(video_id).title} (reason: {flag_reason})")
            else:
                print("Cannot flag video: Video is already flagged")
        else:
            print("Cannot flag video: Video does not exist")


    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        if self._flagged.is_flag_video(video_id):
            self._flagged.remove_flag(video_id)
            print(f"Successfully removed flag from video: {self._video_library.get_video(video_id).title}")
        else:
            if self._video_library.get_video(video_id):
                print("Cannot remove flag from video: Video is not flagged")

            else:
                print("Cannot remove flag from video: Video does not exist")
