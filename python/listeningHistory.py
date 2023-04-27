from datetime import datetime, timedelta

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read user-read-recently-played"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

recent_tracks = sp.current_user_recently_played(limit=50)

track_names = [track["track"]["name"] for track in recent_tracks["items"]]
timestamps = [track["played_at"] for track in recent_tracks["items"]]

import pandas as pd

df = pd.DataFrame({"track": track_names, "timestamp": timestamps})
df["timestamp"] = pd.to_datetime(df["timestamp"])
df.set_index("timestamp", inplace=True)

daily_counts = df.resample("D").count()

import matplotlib.pyplot as plt

plt.plot(daily_counts.index, daily_counts["track"])
plt.xlabel("Date")
plt.ylabel("Tracks played")
plt.show()

# Calculate listening history
total_play_time = 0
played_at_list = []

today = datetime.now()
week_ago = today - timedelta(days=365)

# Get the first batch of recently played tracks
results = sp.current_user_recently_played(limit=50)

while results["items"]:
    for item in results["items"]:
        played_at = datetime.strptime(item["played_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if played_at > week_ago: 
            track_play_time_ms = item["track"]["duration_ms"] / 1000
            total_play_time += track_play_time_ms / 60000  # Convert milliseconds to minutes
            played_at_list.append(played_at)
    
    # Get the next batch of recently played tracks
    results = sp.current_user_recently_played(limit=50, after=results["cursors"]["after"])

# Print the results
print("You have spent {:.2f} minutes listening to music on Spotify.".format(total_play_time))
