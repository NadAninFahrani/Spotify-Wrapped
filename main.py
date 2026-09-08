import json
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import textwrap

years = {
    2021 : [
        "data2021/Streaming_History_Audio_2021.json", 
        "data2021/Streaming_History_Audio_2021_1.json", 
        "data2021/Streaming_History_Audio_2021_2.json",
        "data2021/Streaming_History_Audio_2021_3.json",
    ],

    2022: [
        "data2022/Streaming_History_Audio_2022.json", 
        "data2022/Streaming_History_Audio_2022_1.json", 
        "data2022/Streaming_History_Audio_2022_2.json",
        "data2022/Streaming_History_Audio_2022_3.json",
    ],

    2023 : [
         "data2023/Streaming_History_Audio_2023.json", 
        "data2023/Streaming_History_Audio_2023_1.json", 
        "data2023/Streaming_History_Audio_2023_2.json",
    ],

    2024: [
        "data2024/Streaming_History_Audio_2024_1.json",
        "data2024/Streaming_History_Audio_2024_2.json", 
        "data2024/Streaming_History_Audio_2024_3.json", 
        "data2024/Streaming_History_Audio_2024.json", 
    ],

    2025: [
        "data2025/Streaming_History_Audio_2025.json", 
        "data2025/Streaming_History_Audio_2025_1.json", 
        "data2025/Streaming_History_Audio_2025_2.json",
        "data2025/Streaming_History_Audio_2025_3.json", 
    ],
    

    2026: [
        "data2026/Streaming_History_Audio_2026.json", 
        "data2026/Streaming_History_Audio_2026_1.json",  
    ]
}

for year, file_paths in years.items():
    print(f"\n=== {year} STATISTICS ===")

    all_data = []
    for file_path in file_paths: 
        with open(file_path, "r") as file:
            data = json.load(file)
    
        all_data.extend(data)

    spotify = pd.DataFrame(all_data)
    spotify = spotify.drop(columns=["ip_addr"])

    spotify = spotify.rename(columns={
        "ts": "timestamp",
        "master_metadata_track_name": "track",
        "master_metadata_album_artist_name": "artist",
        "master_metadata_album_album_name": "album"
    })
    
    if "timestamp" in spotify.columns: 
        spotify["timestamp"] = pd.to_datetime(
            spotify["timestamp"], 
            errors="coerce"
        )

        #Extract info
        spotify["year"] = spotify["timestamp"].dt.year
        spotify["month"] = spotify["timestamp"].dt.month_name()
        spotify["day"] = spotify["timestamp"].dt.day_name()
        spotify["hour"] = spotify["timestamp"].dt.hour
        spotify["date"] = spotify["timestamp"].dt.date

    if "ms_played" in spotify.columns: 
        spotify["minutes_played"] = spotify["ms_played"] / 60000

    #THE REAL ANALYSIS
    print("=== Basic Statistics ===")

    #Top artists
    if "artist" in spotify.columns:
        print("\n=== Top Artists ===") 
        top_artists = spotify["artist"].value_counts().head(10)
        for rank, (artist, streams) in enumerate(top_artists.items(), start=1): 
            if streams > 1: 
                print(f"{rank}. {artist} - {streams} streams")
            else: 
                print(f"{rank}. {artist} - {streams} stream")

        #Bar Graph for Top Artist
        X = top_artists.index
        Y = top_artists.values
        fig, ax = plt.subplots(figsize=(12, 6), layout='constrained')   
        ax.bar(X, Y)
        fig.canvas.manager.set_window_title(f'Top Artist in {year}')
        ax.set_title(f"Top 10 Artists {year}", fontweight='bold', fontsize=20)
            
        ax.set_xlabel("Artist", fontweight='bold', fontsize=12)
        ax.set_ylabel("Streams", fontsize=12, fontweight='bold')
            
        plt.xticks(rotation=45, ha='right') 
        plt.tight_layout()   
            
        plt.show()       
    #Top tracks 
    if "track" in spotify.columns: 
        print("\n=== Top Tracks ===")
        top_tracks = spotify["track"].value_counts().head(10)
        for rank, (track, streams) in enumerate(top_tracks.items(), start=1):
            if streams > 1: 
                print(f"{rank}. {track} - {streams} streams")
            else: 
                print(f"{rank}. {track} - {streams} stream")

        #Bar Graph for Tracks
        wrapped_X = [textwrap.fill(str(track), width=15) for track in top_tracks.index]
        Y = top_tracks.values

        fig, ax = plt.subplots(figsize=(12, 6), layout='constrained')  
        ax.bar(wrapped_X, Y, width=0.5)  

        fig.canvas.manager.set_window_title(f'Top Tracks in {year}')
        ax.set_title(f"Top 10 Tracks {year}", fontweight='bold', fontsize=20)
            
        ax.set_xlabel("Tracks", fontweight='bold', fontsize=12)
        ax.set_ylabel("Streams", fontsize=12, fontweight='bold')

        plt.xticks(rotation=45, ha='right', fontsize=10) 
        plt.show()

    #Unique Artists
    print("\n=== Number of Unique Artists ===")
    if "artist" in spotify.columns: 
        unique_artist = spotify["artist"].nunique()
        print(f"You have listened to {unique_artist} unique artists.")

    #Most Listened artist 
    if "artist" in spotify.columns and "minutes_played" in spotify.columns: 
        print("\n=== Artists By Listening Time ===")
        artist_minutes = (
            spotify.groupby("artist")["minutes_played"].sum()
            .sort_values(ascending=False)
            .head(10))

        for rank, (artist, duration) in enumerate(artist_minutes.items(), start=1):
            print(f"{rank}. {artist} - {round(duration, 2)} minutes played")
        #Bar Graph for Most Listened Artist
        X = artist_minutes.index
        Y = artist_minutes.values
        fig, ax = plt.subplots(figsize=(12, 6), layout='constrained')
        ax.bar(X, Y, width=0.5)

        fig.canvas.manager.set_window_title(f"Top Artist by Listening Time in {year}")
        ax.set_title(f"Top Artists by Listening Time in {year}", fontweight="bold", fontsize=12)
        ax.set_xlabel("Artists", fontweight="bold", fontsize=12)
        ax.set_ylabel("Minutes", fontsize=12, fontweight="bold")

        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.show()


    #Listening Hour
    if "hour" in spotify.columns: 
        print("\n=== Listening By Hour ===")

        hourly_listening = (
            spotify.groupby("hour")
            .size()
            .sort_index()
        )

        for hour, streams in hourly_listening.items():
            h_12 = hour % 12 if hour % 12 != 0 else 12
            period = "AM" if hour < 12 else "PM"

            if streams > 1: 
                print(f"{h_12}:00 {period} - {streams} streams")
            else: 
                print(f"{h_12}:00 {period} - {streams} stream")


    #Listening day of the week
    if "day" in spotify.columns:
        print("\n=== Listening Day of the Week ===") 
        day_order = [
            "Monday", 
            "Tuesday", 
            "Wednesday", 
            "Thursday", 
            "Friday", 
            "Saturday",
            "Sunday"
        ]

        daily_listening = spotify["day"].value_counts()
        for day in day_order: 
            print(f"{day} - {daily_listening.get(day, 0)} streams")


    #Daily Listening Time
    if "date" in spotify.columns and "minutes_played" in spotify.columns: 
        print("\n=== Daily Listening Time ===")
        daily_minutes = (
            spotify.groupby("date")["minutes_played"]
            .sum()
        )

        for date, minutes in daily_minutes.items(): 
            formatted_date = date.strftime("%B %d, %Y")
            rounded_minutes = round(minutes)

            if rounded_minutes == 1: 
                print(f"{formatted_date} - {rounded_minutes} minute")
            else: 
                print(f"{formatted_date} - {rounded_minutes} minutes")

    #Most played artist in each hour
    if "hour" in spotify.columns and "artist" in spotify.columns:

        print("\n=== Artist by Hour ===")

        for hour in range(24):
            hour_data = spotify[spotify["hour"] == hour]
            artist_counts = hour_data["artist"].dropna().value_counts()
            h_12 = hour % 12 if hour % 12 != 0 else 12
            period = "AM" if hour < 12 else "PM"

            if len(artist_counts) > 0:
                top_artist = artist_counts.index[0]
                print(f"{h_12}:00 {period} -> {top_artist}")

            else:
                print(f"{h_12}:00 {period} -> No listening")
