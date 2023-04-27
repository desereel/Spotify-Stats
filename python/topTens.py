import plotly.graph_objs as go
import plotly.offline as pyo

import matplotlib.pyplot as plt
import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up authentication
scope = "user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Get the user's top artists
time_range = "long_term"  # Can be "short_term", "medium_term", or "long_term"
limit = 10  # Number of results to return
artists = sp.current_user_top_artists(time_range=time_range, limit=limit)

# Print the top artists
print("Your top 10 artists on Spotify are:")
for i, artist in enumerate(artists["items"]):
    print(f"{i+1}. {artist['name']}")

tracks = sp.current_user_top_tracks(time_range=time_range, limit=limit)
print("Your top 10 tracks on Spotify are:")
for i, track in enumerate(tracks["items"]):
	artists = ", ".join([artist["name"] for artist in track["artists"]])
	print(f"{i+1}. {track['name']} by {artists}")

# Extract the track names and dates
track_names = []
track_dates = []
for track in tracks["items"]:
    name = track.get("name", "Unknown")
    date = track.get("album", {}).get("release_date", "Unknown")
    track_names.append(name)
    track_dates.append(date)

# Create a plotly timeline
fig = go.Figure(
    go.Scatter(
        x=track_dates,
        y=track_names,
        mode="markers+text",
        text=track_names,
        textposition="bottom right",
        marker=dict(size=10),
        hovertemplate="<b>%{y}</b><br>%{x}<extra></extra>",
    )
)
fig.update_layout(
    title="Your Top Tracks Timeline",
    xaxis_title="Release Date",
    yaxis_title="Track Name",
    hovermode="closest",
)

pyo.plot(fig, filename="top_tracks_timeline.html")


