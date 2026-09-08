ReadMe Section
1. Insights
Spotify Wrapped ranks your year by total play count. However, total play count does not capture how concentrated someone's listening was over a short period. For example, a song streamed 200 times over several years may have a very different meaning from a song streamed 5 times repeatedly in one afternoon. While the first song has a higher total play count, the second represents a much more concentrated period of listening.


This is a gap that Spotify Wrapped does not directly address: it tells you what you listened to, but not when a particular song dominated your listening within a short period. A song that is repeatedly played over a day or two may be associated with a particular event, mood, or memory, although the streaming data itself cannot determine the reason behind that listening pattern. Most people may not remember simply that they streamed a song 200 times; instead, they may remember a specific period when they could not stop listening to it.


Therefore, instead of ranking songs solely by total plays, this analysis also looks for days where one track accounted for a disproportionate share of that day's listening. This provides another way to interpret listening behaviour by identifying periods of unusually concentrated listening, or "repeat days." The method is also reusable: anyone with access to their own Spotify streaming history could apply the same analysis to identify their own periods of concentrated listening.
2. Tools and Libraries
I obtained my data directly from Spotify in the form of JSON files. My data covers the period from January 28, 2021, to August 20, 2026, containing approximately 56,508 audio streaming records. To create this Spotify Wrapped analysis, I used Visual Studio Code as my IDE and Python as my main programming language. I used libraries including JSON, pandas, Matplotlib, and textwrap to process, analyse, and visualise the dataset. It is important to note that this is not my complete Spotify streaming history. My analysis only considers audio streaming history; podcasts and other types of Spotify streams were not included.


3. Features
Throughout this project, I calculated several statistics that are similar to those presented in Spotify Wrapped, including the top 10 artists and tracks for each year, the number of unique artists, and daily listening time. However, I also explored statistics that are not typically highlighted by Spotify Wrapped. These include artists ranked by total minutes played, the most-streamed artist during each hour of the day, the total number of streams occurring during each hour, total streams by day of the week, and daily listening time throughout each year. Together, these statistics provide a more detailed view of not only what I listened to, but also when and how intensely I listened.


4. Loading and Combining Data 


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


Spotify splits large streaming histories into multiple JSON files, so I had to create a dictionary containing the files belonging to each year.


for year, file_paths in years.items():
   print(f"\n=== {year} STATISTICS ===")


   all_data = []
   for file_path in file_paths:
       with open(file_path, "r") as file:
           data = json.load(file)
  
       all_data.extend(data)


Each year’s Spotify history may be divided across several JSON files. The program therefore opens each file, loads its data using JSON, and combines all records into one list using extend(). This allows the entire year’s listening history to be analysed together rather than treating each file separately. 




5. Data Cleaning 
   spotify = pd.DataFrame(all_data)
   spotify = spotify.drop(columns=["ip_addr"])


After combining the JSON files, the data is converted into a pandas DataFrame. The ip_addr column is removed because it is not relevant to the analysis and is a danger to my own safety if distributed. 


spotify = spotify.rename(columns={
       "ts": "timestamp",
       "master_metadata_track_name": "track",
       "master_metadata_album_artist_name": "artist",
       "master_metadata_album_album_name": "album"
   })


Spotify originally gave me their standard column names, which were relatively long and difficult to work with. I renamed the relevant columns to shorter and more straightforward names such as track, artist, and album to make the subsequent analysis easier to read and understand. 


6. Date and Time Processing
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


The original Spotify timestamp contains the exact date and time of each listening event. I converted this column into pandas’ datetime format so that I could extract the year, month, day of the week, hour, and date. These new columns allow me to analyse listening behaviour across different time periods. 


For example,
Original: 
2024-06-15 21:43:12 


Extracted:
Year: 2024
Month: June
Day: Saturday
Hour: 21 (9:00 PM)
Date: June 15, 2024


if "ms_played" in spotify.columns:
       spotify["minutes_played"] = spotify["ms_played"] / 60000


Spotify records listening duration in milliseconds. Since milliseconds are difficult to interpret directly, I converted them into minutes by dividing by 60,000. This allows listening duration to be presented in a more understandable format.


7. Analysis
7.1  Top Artists
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




This will produce an output that ranks the top 10 artists in a year. I will get this output from the use of value_counts(), which counts how many times each artist appears in the dataset, alongside head(10), which gives the ten artists with the highest number of streams. 


I visualised these results using a bar chart so that the differences in streaming frequency between artists can be compared more easily. 


7.2  Top Tracks
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


These lines of code produce the ranks of the top tracks as well as the number of streams. I used a similar approach in this formula with the top artist, just with altered variables. I’ve also made a bar graph set with x as the track names and y as the number of streams, which will help visualize the difference in streams.


#Unique Artists
   print("\n=== Number of Unique Artists ===")
   if "artist" in spotify.columns:
       unique_artist = spotify["artist"].nunique()
       print(f"You have listened to {unique_artist} unique artists.")


This section calculates the number of unique artists one has streamed in one year. It calculates the values using nunique(), which basically counts all the unique values so it doesn’t double-count. 


7.3  Most Listened Artist
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




Unlike the Top Artists statistic, which ranks artists by number of streams, this analysis ranks artists by the total amount of time spent listening to them. I grouped the data by artist and summed the minutes_played values for each artist. This produces a different perspective because an artist with fewer streams can rank highly if their songs have longer average durations. I’ve also made a graph with X as the artists and Y as their streams. 




7.4  Listening Hour
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


I grouped all streaming records according to the hour in which they occurred. This shows when during the day I tend to listen to Spotify the most. I converted the 24-hour format into a 12-hour AM/PM format to make the output easier to interpret.


7.5  Listening Day of the Week
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


I counted the number of streams occurring on each day of the week and arranged the results from Monday to Sunday. This allows me to identify which days I tend to listen to music most frequently.




7.6  Daily Listening Time
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


Instead of counting individual streams, I grouped the data by calendar date and added the listening duration of all streams occurring on that day. This shows how much time I spent listening to Spotify on each day.




7.7  Most Played Artist In Each Hour
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


For each of the 24 hours in a day, I filtered the dataset to include only streams occurring during that hour. I then counted how many times each artist appeared during that hour and selected the artist with the highest count. This allows me to identify not only my overall favourite artists, but also which artist dominated my listening during each specific hour.




Limitations:
* My data only goes from January 2021 until August 2026, which isn’t a complete year
* Ms_played measures Spotify’s recorded listening duration, which isn’t necessarily identical to consciously listening to the entire song 
* My analysis is dependent on what Spotify included in the exported history 


Graphs
2021
  



  

  



2022
  
  
  



2023
  

  
  



2024
  

  

  



2025
  

  

  



2026  
  
  







Conclusion
This project demonstrates that Spotify streaming history can reveal much more about listening behaviour than simply identifying the songs and artists with the highest number of streams. By analysing approximately 56,508 audio streaming records from January 28, 2021, to August 20, 2026, I was able to identify patterns in not only what I listened to, but also when and how I listened.
The analysis reproduced some of the familiar statistics found in Spotify Wrapped, such as the most-streamed artists and tracks, while also introducing additional perspectives including listening time by artist, listening patterns by hour and day of the week, and daily listening duration. These statistics show that the same listening history can tell different stories depending on how the data is measured. For example, ranking artists by total streams can produce different results from ranking them by total minutes listened.
Most importantly, this project explores the idea of concentrated listening through "repeat days." Rather than only asking which songs were played the most across an entire year, the analysis looks for periods where a single song dominated a person's listening. This provides a different way of interpreting streaming behaviour and may identify moments that are more memorable than a simple yearly play count.
However, the data cannot explain the reason behind these listening patterns. A song being repeatedly played on one day does not necessarily mean it was connected to an important memory or event. That interpretation ultimately belongs to the listener. Therefore, the purpose of this project is not to replace Spotify Wrapped, but to demonstrate how personal streaming data can be analysed in different ways to uncover patterns that a standard yearly ranking may overlook.
Overall, this project shows how programming and data analysis can transform a large collection of personal streaming records into meaningful and personalised insights. Rather than simply asking "What did I listen to the most?", this analysis asks a broader question: "What can my listening history tell me about the way I listened?"


Output
=== 2021 STATISTICS ===
=== Basic Statistics ===


=== Top Artists ===
1. The Neighbourhood - 5224 streams
2. Arctic Monkeys - 2914 streams
3. Clairo - 1898 streams
4. Cigarettes After Sex - 1654 streams
5. Taylor Swift - 1144 streams
6. Rex Orange County - 1030 streams
7. Olivia Rodrigo - 832 streams
8. Cage The Elephant - 804 streams
9. Chase Atlantic - 696 streams
10. Steve Lacy - 620 streams
/Users/nadyafahrani/Desktop/SPOTIFY PERSONAL PROJ/main.py:109: UserWarning: The figure layout has changed to tight
  plt.tight_layout()


=== Top Tracks ===
1. Dark Red - 557 streams
2. I Wanna Be Yours - 553 streams
3. Cry Baby - 472 streams
4. Sofia - 423 streams
5. I Love You So - 339 streams
6. Something About You - 339 streams
7. R U Mine? - 324 streams
8. Single - 309 streams
9. Sparks - 305 streams
10. Flawless - 300 streams


=== Number of Unique Artists ===
You have listened to 1731 unique artists.


=== Artists By Listening Time ===
1. The Neighbourhood - 11302.4 minutes played
2. Arctic Monkeys - 5844.44 minutes played
3. Cigarettes After Sex - 4626.7 minutes played
4. Clairo - 3763.02 minutes played
5. Taylor Swift - 2684.15 minutes played
6. Rex Orange County - 2319.93 minutes played
7. Olivia Rodrigo - 1651.28 minutes played
8. Chase Atlantic - 1538.4 minutes played
9. Steve Lacy - 1435.12 minutes played
10. Coldplay - 1424.14 minutes played


=== Listening By Hour ===
12:00 AM - 1913 streams
1:00 AM - 2046 streams
2:00 AM - 2793 streams
3:00 AM - 2629 streams
4:00 AM - 3005 streams
5:00 AM - 2975 streams
6:00 AM - 2643 streams
7:00 AM - 2783 streams
8:00 AM - 3171 streams
9:00 AM - 3020 streams
10:00 AM - 3299 streams
11:00 AM - 2545 streams
12:00 PM - 3305 streams
1:00 PM - 2690 streams
2:00 PM - 2112 streams
3:00 PM - 2372 streams
4:00 PM - 2836 streams
5:00 PM - 2574 streams
6:00 PM - 2175 streams
7:00 PM - 1558 streams
8:00 PM - 952 streams
9:00 PM - 599 streams
10:00 PM - 1023 streams
11:00 PM - 1490 streams


=== Listening Day of the Week ===
Monday - 6678 streams
Tuesday - 8198 streams
Wednesday - 6976 streams
Thursday - 7954 streams
Friday - 8895 streams
Saturday - 8927 streams
Sunday - 8880 streams


=== Daily Listening Time ===
January 28, 2021 - 150 minutes
January 29, 2021 - 283 minutes
January 30, 2021 - 252 minutes
January 31, 2021 - 245 minutes
February 01, 2021 - 46 minutes
February 02, 2021 - 317 minutes
February 03, 2021 - 177 minutes
February 04, 2021 - 379 minutes
February 05, 2021 - 286 minutes
February 06, 2021 - 359 minutes
February 07, 2021 - 182 minutes
February 08, 2021 - 193 minutes
February 09, 2021 - 356 minutes
February 10, 2021 - 290 minutes
February 11, 2021 - 302 minutes
February 12, 2021 - 282 minutes
February 13, 2021 - 278 minutes
February 14, 2021 - 251 minutes
February 15, 2021 - 103 minutes
February 16, 2021 - 119 minutes
February 17, 2021 - 148 minutes
February 18, 2021 - 81 minutes
February 19, 2021 - 374 minutes
February 20, 2021 - 288 minutes
February 21, 2021 - 253 minutes
February 22, 2021 - 152 minutes
February 23, 2021 - 168 minutes
February 24, 2021 - 155 minutes
February 25, 2021 - 211 minutes
February 26, 2021 - 201 minutes
February 27, 2021 - 207 minutes
February 28, 2021 - 146 minutes
March 01, 2021 - 214 minutes
March 02, 2021 - 167 minutes
March 03, 2021 - 216 minutes
March 04, 2021 - 169 minutes
March 05, 2021 - 242 minutes
March 06, 2021 - 170 minutes
March 07, 2021 - 276 minutes
March 08, 2021 - 196 minutes
March 09, 2021 - 227 minutes
March 10, 2021 - 115 minutes
March 11, 2021 - 101 minutes
March 12, 2021 - 123 minutes
March 13, 2021 - 173 minutes
March 14, 2021 - 116 minutes
March 15, 2021 - 16 minutes
March 16, 2021 - 99 minutes
March 17, 2021 - 73 minutes
March 18, 2021 - 327 minutes
March 19, 2021 - 152 minutes
March 20, 2021 - 450 minutes
March 21, 2021 - 275 minutes
March 22, 2021 - 120 minutes
March 23, 2021 - 399 minutes
March 24, 2021 - 103 minutes
March 25, 2021 - 122 minutes
March 26, 2021 - 212 minutes
March 27, 2021 - 308 minutes
March 28, 2021 - 134 minutes
March 29, 2021 - 245 minutes
March 30, 2021 - 195 minutes
March 31, 2021 - 39 minutes
April 01, 2021 - 204 minutes
April 02, 2021 - 354 minutes
April 03, 2021 - 173 minutes
April 04, 2021 - 291 minutes
April 05, 2021 - 287 minutes
April 06, 2021 - 253 minutes
April 07, 2021 - 183 minutes
April 08, 2021 - 225 minutes
April 09, 2021 - 388 minutes
April 10, 2021 - 224 minutes
April 11, 2021 - 167 minutes
April 12, 2021 - 63 minutes
April 13, 2021 - 182 minutes
April 14, 2021 - 44 minutes
April 15, 2021 - 328 minutes
April 16, 2021 - 257 minutes
April 17, 2021 - 250 minutes
April 18, 2021 - 313 minutes
April 19, 2021 - 159 minutes
April 20, 2021 - 354 minutes
April 21, 2021 - 654 minutes
April 22, 2021 - 442 minutes
April 23, 2021 - 513 minutes
April 24, 2021 - 364 minutes
April 25, 2021 - 481 minutes
April 26, 2021 - 549 minutes
April 27, 2021 - 491 minutes
April 28, 2021 - 297 minutes
April 29, 2021 - 428 minutes
April 30, 2021 - 447 minutes
May 01, 2021 - 412 minutes
May 02, 2021 - 512 minutes
May 03, 2021 - 405 minutes
May 04, 2021 - 286 minutes
May 05, 2021 - 359 minutes
May 06, 2021 - 535 minutes
May 07, 2021 - 531 minutes
May 08, 2021 - 553 minutes
May 09, 2021 - 543 minutes
May 10, 2021 - 487 minutes
May 11, 2021 - 366 minutes
May 12, 2021 - 535 minutes
May 13, 2021 - 467 minutes
May 14, 2021 - 311 minutes
May 15, 2021 - 362 minutes
May 16, 2021 - 481 minutes
May 17, 2021 - 246 minutes
May 18, 2021 - 537 minutes
May 19, 2021 - 425 minutes
May 20, 2021 - 370 minutes
May 21, 2021 - 596 minutes
May 22, 2021 - 534 minutes
May 23, 2021 - 720 minutes
May 24, 2021 - 396 minutes
May 25, 2021 - 212 minutes
May 26, 2021 - 294 minutes
May 27, 2021 - 297 minutes
May 28, 2021 - 618 minutes
May 29, 2021 - 618 minutes
May 30, 2021 - 398 minutes
May 31, 2021 - 295 minutes
June 01, 2021 - 343 minutes
June 02, 2021 - 257 minutes
June 03, 2021 - 452 minutes
June 04, 2021 - 429 minutes
June 05, 2021 - 388 minutes
June 06, 2021 - 229 minutes
June 07, 2021 - 244 minutes
June 08, 2021 - 416 minutes
June 09, 2021 - 589 minutes
June 10, 2021 - 397 minutes
June 11, 2021 - 459 minutes
June 12, 2021 - 438 minutes
June 13, 2021 - 583 minutes
June 14, 2021 - 482 minutes
June 15, 2021 - 295 minutes
June 16, 2021 - 232 minutes
June 17, 2021 - 293 minutes
June 18, 2021 - 286 minutes
June 19, 2021 - 474 minutes
June 20, 2021 - 597 minutes
June 21, 2021 - 248 minutes
June 22, 2021 - 69 minutes
June 23, 2021 - 127 minutes
June 24, 2021 - 199 minutes
June 25, 2021 - 327 minutes
June 26, 2021 - 254 minutes
June 27, 2021 - 409 minutes
June 28, 2021 - 276 minutes
June 29, 2021 - 393 minutes
June 30, 2021 - 142 minutes
July 01, 2021 - 276 minutes
July 02, 2021 - 466 minutes
July 03, 2021 - 487 minutes
July 04, 2021 - 259 minutes
July 05, 2021 - 475 minutes
July 06, 2021 - 471 minutes
July 07, 2021 - 249 minutes
July 08, 2021 - 246 minutes
July 09, 2021 - 326 minutes
July 10, 2021 - 381 minutes
July 11, 2021 - 497 minutes
July 12, 2021 - 512 minutes
July 13, 2021 - 343 minutes
July 14, 2021 - 430 minutes
July 15, 2021 - 517 minutes
July 16, 2021 - 386 minutes
July 17, 2021 - 307 minutes
July 18, 2021 - 352 minutes
July 19, 2021 - 130 minutes
July 20, 2021 - 314 minutes
July 21, 2021 - 421 minutes
July 22, 2021 - 366 minutes
July 23, 2021 - 513 minutes
July 24, 2021 - 234 minutes
July 25, 2021 - 495 minutes
July 26, 2021 - 78 minutes
July 27, 2021 - 367 minutes
July 28, 2021 - 391 minutes
July 29, 2021 - 426 minutes
July 30, 2021 - 699 minutes
July 31, 2021 - 491 minutes
August 01, 2021 - 626 minutes
August 02, 2021 - 404 minutes
August 03, 2021 - 657 minutes
August 04, 2021 - 327 minutes
August 05, 2021 - 231 minutes
August 06, 2021 - 238 minutes
August 07, 2021 - 382 minutes
August 08, 2021 - 413 minutes
August 09, 2021 - 496 minutes
August 10, 2021 - 423 minutes
August 11, 2021 - 524 minutes
August 12, 2021 - 189 minutes
August 13, 2021 - 405 minutes
August 14, 2021 - 719 minutes
August 15, 2021 - 363 minutes
August 16, 2021 - 357 minutes
August 17, 2021 - 497 minutes
August 18, 2021 - 163 minutes
August 19, 2021 - 296 minutes
August 20, 2021 - 378 minutes
August 21, 2021 - 605 minutes
August 22, 2021 - 457 minutes
August 23, 2021 - 235 minutes
August 24, 2021 - 742 minutes
August 25, 2021 - 411 minutes
August 26, 2021 - 273 minutes
August 27, 2021 - 846 minutes
August 28, 2021 - 670 minutes
August 29, 2021 - 204 minutes
August 30, 2021 - 176 minutes
August 31, 2021 - 58 minutes
September 01, 2021 - 346 minutes
September 02, 2021 - 235 minutes
September 03, 2021 - 73 minutes
September 04, 2021 - 411 minutes
September 05, 2021 - 565 minutes
September 06, 2021 - 289 minutes
September 07, 2021 - 273 minutes
September 08, 2021 - 250 minutes
September 09, 2021 - 26 minutes
September 10, 2021 - 311 minutes
September 11, 2021 - 320 minutes
September 12, 2021 - 114 minutes
September 13, 2021 - 155 minutes
September 14, 2021 - 126 minutes
September 15, 2021 - 117 minutes
September 16, 2021 - 328 minutes
September 17, 2021 - 291 minutes
September 18, 2021 - 238 minutes
September 19, 2021 - 346 minutes
September 20, 2021 - 218 minutes
September 21, 2021 - 368 minutes
September 22, 2021 - 57 minutes
September 23, 2021 - 259 minutes
September 24, 2021 - 114 minutes
September 25, 2021 - 605 minutes
September 26, 2021 - 395 minutes
September 27, 2021 - 413 minutes
September 28, 2021 - 313 minutes
September 29, 2021 - 634 minutes
September 30, 2021 - 465 minutes
October 01, 2021 - 370 minutes
October 02, 2021 - 355 minutes
October 03, 2021 - 494 minutes
October 04, 2021 - 615 minutes
October 05, 2021 - 58 minutes
October 06, 2021 - 510 minutes
October 07, 2021 - 359 minutes
October 08, 2021 - 273 minutes
October 09, 2021 - 542 minutes
October 10, 2021 - 383 minutes
October 11, 2021 - 95 minutes
October 12, 2021 - 210 minutes
October 13, 2021 - 219 minutes
October 14, 2021 - 161 minutes
October 15, 2021 - 372 minutes
October 16, 2021 - 466 minutes
October 17, 2021 - 722 minutes
October 18, 2021 - 323 minutes
October 19, 2021 - 457 minutes
October 20, 2021 - 537 minutes
October 21, 2021 - 358 minutes
October 22, 2021 - 456 minutes
October 23, 2021 - 706 minutes
October 24, 2021 - 535 minutes
October 25, 2021 - 114 minutes
October 26, 2021 - 252 minutes
October 27, 2021 - 298 minutes
October 28, 2021 - 471 minutes
October 29, 2021 - 305 minutes
October 30, 2021 - 220 minutes
October 31, 2021 - 258 minutes
November 01, 2021 - 285 minutes
November 02, 2021 - 192 minutes
November 03, 2021 - 315 minutes
November 04, 2021 - 319 minutes
November 05, 2021 - 364 minutes
November 06, 2021 - 365 minutes
November 07, 2021 - 466 minutes
November 08, 2021 - 97 minutes
November 09, 2021 - 494 minutes
November 10, 2021 - 247 minutes
November 11, 2021 - 526 minutes
November 12, 2021 - 488 minutes
November 13, 2021 - 337 minutes
November 14, 2021 - 322 minutes
November 15, 2021 - 171 minutes
November 16, 2021 - 206 minutes
November 17, 2021 - 443 minutes
November 18, 2021 - 304 minutes
November 19, 2021 - 348 minutes
November 20, 2021 - 507 minutes
November 21, 2021 - 276 minutes
November 22, 2021 - 497 minutes
November 23, 2021 - 183 minutes
November 24, 2021 - 112 minutes
November 25, 2021 - 137 minutes
November 26, 2021 - 240 minutes
November 27, 2021 - 294 minutes
November 28, 2021 - 629 minutes
November 29, 2021 - 148 minutes
November 30, 2021 - 187 minutes
December 01, 2021 - 249 minutes
December 02, 2021 - 441 minutes
December 03, 2021 - 310 minutes
December 04, 2021 - 524 minutes
December 05, 2021 - 300 minutes
December 06, 2021 - 565 minutes
December 07, 2021 - 235 minutes
December 08, 2021 - 313 minutes
December 09, 2021 - 576 minutes
December 10, 2021 - 381 minutes
December 11, 2021 - 503 minutes
December 12, 2021 - 326 minutes
December 13, 2021 - 407 minutes
December 14, 2021 - 306 minutes
December 15, 2021 - 208 minutes
December 16, 2021 - 208 minutes
December 17, 2021 - 664 minutes
December 18, 2021 - 351 minutes
December 19, 2021 - 431 minutes
December 20, 2021 - 436 minutes
December 21, 2021 - 641 minutes
December 22, 2021 - 598 minutes
December 23, 2021 - 709 minutes
December 24, 2021 - 478 minutes
December 25, 2021 - 478 minutes
December 26, 2021 - 748 minutes
December 27, 2021 - 405 minutes
December 28, 2021 - 799 minutes
December 29, 2021 - 432 minutes
December 30, 2021 - 404 minutes
December 31, 2021 - 493 minutes


=== Artist by Hour ===
12:00 AM -> The Neighbourhood
1:00 AM -> The Neighbourhood
2:00 AM -> The Neighbourhood
3:00 AM -> The Neighbourhood
4:00 AM -> The Neighbourhood
5:00 AM -> The Neighbourhood
6:00 AM -> The Neighbourhood
7:00 AM -> The Neighbourhood
8:00 AM -> The Neighbourhood
9:00 AM -> The Neighbourhood
10:00 AM -> The Neighbourhood
11:00 AM -> The Neighbourhood
12:00 PM -> The Neighbourhood
1:00 PM -> The Neighbourhood
2:00 PM -> The Neighbourhood
3:00 PM -> The Neighbourhood
4:00 PM -> The Neighbourhood
5:00 PM -> The Neighbourhood
6:00 PM -> The Neighbourhood
7:00 PM -> The Neighbourhood
8:00 PM -> The Neighbourhood
9:00 PM -> The Neighbourhood
10:00 PM -> The Neighbourhood
11:00 PM -> The Neighbourhood


=== 2022 STATISTICS ===
=== Basic Statistics ===


=== Top Artists ===
1. The Neighbourhood - 4359 streams
2. ENHYPEN - 2960 streams
3. Taylor Swift - 2474 streams
4. Cigarettes After Sex - 1825 streams
5. TOMORROW X TOGETHER - 1821 streams
6. boy pablo - 1633 streams
7. Chase Atlantic - 1464 streams
8. Matt Maltese - 1161 streams
9. The Weeknd - 1023 streams
10. Clairo - 1010 streams
/Users/nadyafahrani/Desktop/SPOTIFY PERSONAL PROJ/main.py:109: UserWarning: The figure layout has changed to tight
  plt.tight_layout()


=== Top Tracks ===
1. Drunk-Dazed - 1042 streams
2. Good Boy Gone Bad - 844 streams
3. Be My Baby - 722 streams
4. 0X1=LOVESONG (I Know I Love You) feat. Seori - 627 streams
5. FEVER - 457 streams
6. Mystery - 437 streams
7. Come Inside Of My Heart - 408 streams
8. Apocalypse - 389 streams
9. Sex, Drugs, Etc. - 360 streams
10. I Wanna Be Yours - 360 streams


=== Number of Unique Artists ===
You have listened to 1810 unique artists.


=== Artists By Listening Time ===
1. The Neighbourhood - 7879.79 minutes played
2. ENHYPEN - 6164.77 minutes played
3. Taylor Swift - 5603.22 minutes played
4. Cigarettes After Sex - 4876.45 minutes played
5. TOMORROW X TOGETHER - 4378.88 minutes played
6. boy pablo - 2735.11 minutes played
7. Chase Atlantic - 2467.64 minutes played
8. Matt Maltese - 2109.72 minutes played
9. The Weeknd - 1975.35 minutes played
10. The Ronettes - 1772.21 minutes played


=== Listening By Hour ===
12:00 AM - 3218 streams
1:00 AM - 2100 streams
2:00 AM - 2520 streams
3:00 AM - 2867 streams
4:00 AM - 3367 streams
5:00 AM - 2895 streams
6:00 AM - 2823 streams
7:00 AM - 3379 streams
8:00 AM - 4149 streams
9:00 AM - 3606 streams
10:00 AM - 3117 streams
11:00 AM - 3541 streams
12:00 PM - 4012 streams
1:00 PM - 4111 streams
2:00 PM - 2984 streams
3:00 PM - 2552 streams
4:00 PM - 3726 streams
5:00 PM - 3064 streams
6:00 PM - 1669 streams
7:00 PM - 959 streams
8:00 PM - 573 streams
9:00 PM - 462 streams
10:00 PM - 719 streams
11:00 PM - 1196 streams


=== Listening Day of the Week ===
Monday - 9078 streams
Tuesday - 8397 streams
Wednesday - 9718 streams
Thursday - 8635 streams
Friday - 8288 streams
Saturday - 9215 streams
Sunday - 10278 streams


=== Daily Listening Time ===
January 01, 2022 - 559 minutes
January 02, 2022 - 584 minutes
January 03, 2022 - 434 minutes
January 04, 2022 - 411 minutes
January 05, 2022 - 186 minutes
January 06, 2022 - 316 minutes
January 07, 2022 - 183 minutes
January 08, 2022 - 307 minutes
January 09, 2022 - 276 minutes
January 10, 2022 - 147 minutes
January 11, 2022 - 269 minutes
January 12, 2022 - 298 minutes
January 13, 2022 - 186 minutes
January 14, 2022 - 272 minutes
January 15, 2022 - 599 minutes
January 16, 2022 - 113 minutes
January 17, 2022 - 521 minutes
January 18, 2022 - 228 minutes
January 19, 2022 - 425 minutes
January 20, 2022 - 431 minutes
January 21, 2022 - 663 minutes
January 22, 2022 - 425 minutes
January 23, 2022 - 569 minutes
January 24, 2022 - 523 minutes
January 25, 2022 - 258 minutes
January 26, 2022 - 387 minutes
January 27, 2022 - 177 minutes
January 28, 2022 - 156 minutes
January 29, 2022 - 414 minutes
January 30, 2022 - 325 minutes
January 31, 2022 - 108 minutes
February 01, 2022 - 250 minutes
February 02, 2022 - 335 minutes
February 03, 2022 - 480 minutes
February 04, 2022 - 513 minutes
February 05, 2022 - 353 minutes
February 06, 2022 - 98 minutes
February 07, 2022 - 243 minutes
February 08, 2022 - 211 minutes
February 09, 2022 - 418 minutes
February 10, 2022 - 406 minutes
February 11, 2022 - 262 minutes
February 12, 2022 - 196 minutes
February 13, 2022 - 142 minutes
February 14, 2022 - 276 minutes
February 15, 2022 - 250 minutes
February 16, 2022 - 124 minutes
February 17, 2022 - 120 minutes
February 18, 2022 - 34 minutes
February 19, 2022 - 148 minutes
February 20, 2022 - 142 minutes
February 21, 2022 - 129 minutes
February 22, 2022 - 110 minutes
February 23, 2022 - 151 minutes
February 24, 2022 - 202 minutes
February 25, 2022 - 187 minutes
February 26, 2022 - 65 minutes
February 27, 2022 - 43 minutes
February 28, 2022 - 211 minutes
March 01, 2022 - 183 minutes
March 02, 2022 - 209 minutes
March 03, 2022 - 20 minutes
March 04, 2022 - 184 minutes
March 05, 2022 - 212 minutes
March 06, 2022 - 492 minutes
March 07, 2022 - 411 minutes
March 08, 2022 - 227 minutes
March 09, 2022 - 245 minutes
March 10, 2022 - 160 minutes
March 11, 2022 - 296 minutes
March 12, 2022 - 495 minutes
March 13, 2022 - 394 minutes
March 14, 2022 - 60 minutes
March 15, 2022 - 289 minutes
March 16, 2022 - 300 minutes
March 17, 2022 - 274 minutes
March 18, 2022 - 270 minutes
March 19, 2022 - 40 minutes
March 20, 2022 - 108 minutes
March 21, 2022 - 166 minutes
March 22, 2022 - 147 minutes
March 23, 2022 - 388 minutes
March 24, 2022 - 238 minutes
March 25, 2022 - 262 minutes
March 26, 2022 - 298 minutes
March 27, 2022 - 176 minutes
March 28, 2022 - 271 minutes
March 29, 2022 - 311 minutes
March 30, 2022 - 194 minutes
March 31, 2022 - 78 minutes
April 01, 2022 - 569 minutes
April 02, 2022 - 168 minutes
April 03, 2022 - 150 minutes
April 04, 2022 - 123 minutes
April 05, 2022 - 62 minutes
April 06, 2022 - 241 minutes
April 07, 2022 - 78 minutes
April 08, 2022 - 434 minutes
April 09, 2022 - 413 minutes
April 10, 2022 - 500 minutes
April 11, 2022 - 195 minutes
April 12, 2022 - 221 minutes
April 13, 2022 - 264 minutes
April 14, 2022 - 312 minutes
April 15, 2022 - 403 minutes
April 16, 2022 - 486 minutes
April 17, 2022 - 595 minutes
April 18, 2022 - 400 minutes
April 19, 2022 - 425 minutes
April 20, 2022 - 453 minutes
April 21, 2022 - 417 minutes
April 22, 2022 - 550 minutes
April 23, 2022 - 203 minutes
April 24, 2022 - 349 minutes
April 25, 2022 - 455 minutes
April 26, 2022 - 379 minutes
April 27, 2022 - 361 minutes
April 28, 2022 - 257 minutes
April 29, 2022 - 540 minutes
April 30, 2022 - 300 minutes
May 01, 2022 - 432 minutes
May 02, 2022 - 559 minutes
May 03, 2022 - 159 minutes
May 04, 2022 - 235 minutes
May 05, 2022 - 510 minutes
May 06, 2022 - 531 minutes
May 07, 2022 - 529 minutes
May 08, 2022 - 642 minutes
May 09, 2022 - 454 minutes
May 10, 2022 - 354 minutes
May 11, 2022 - 308 minutes
May 12, 2022 - 505 minutes
May 13, 2022 - 456 minutes
May 14, 2022 - 441 minutes
May 15, 2022 - 484 minutes
May 16, 2022 - 338 minutes
May 17, 2022 - 239 minutes
May 18, 2022 - 204 minutes
May 19, 2022 - 280 minutes
May 20, 2022 - 341 minutes
May 21, 2022 - 379 minutes
May 22, 2022 - 667 minutes
May 23, 2022 - 519 minutes
May 24, 2022 - 801 minutes
May 25, 2022 - 572 minutes
May 26, 2022 - 295 minutes
May 27, 2022 - 611 minutes
May 28, 2022 - 337 minutes
May 29, 2022 - 521 minutes
May 30, 2022 - 390 minutes
May 31, 2022 - 551 minutes
June 01, 2022 - 806 minutes
June 02, 2022 - 655 minutes
June 03, 2022 - 793 minutes
June 04, 2022 - 486 minutes
June 05, 2022 - 342 minutes
June 06, 2022 - 459 minutes
June 07, 2022 - 412 minutes
June 08, 2022 - 396 minutes
June 09, 2022 - 326 minutes
June 10, 2022 - 382 minutes
June 11, 2022 - 526 minutes
June 12, 2022 - 415 minutes
June 13, 2022 - 681 minutes
June 14, 2022 - 643 minutes
June 15, 2022 - 396 minutes
June 16, 2022 - 525 minutes
June 17, 2022 - 506 minutes
June 18, 2022 - 621 minutes
June 19, 2022 - 283 minutes
June 20, 2022 - 584 minutes
June 21, 2022 - 484 minutes
June 22, 2022 - 539 minutes
June 23, 2022 - 643 minutes
June 24, 2022 - 461 minutes
June 25, 2022 - 504 minutes
June 26, 2022 - 384 minutes
June 27, 2022 - 227 minutes
June 28, 2022 - 408 minutes
June 29, 2022 - 295 minutes
June 30, 2022 - 490 minutes
July 01, 2022 - 584 minutes
July 02, 2022 - 697 minutes
July 03, 2022 - 577 minutes
July 04, 2022 - 461 minutes
July 05, 2022 - 280 minutes
July 06, 2022 - 452 minutes
July 07, 2022 - 377 minutes
July 08, 2022 - 363 minutes
July 09, 2022 - 367 minutes
July 10, 2022 - 442 minutes
July 11, 2022 - 340 minutes
July 12, 2022 - 247 minutes
July 13, 2022 - 219 minutes
July 14, 2022 - 137 minutes
July 15, 2022 - 311 minutes
July 16, 2022 - 274 minutes
July 17, 2022 - 440 minutes
July 18, 2022 - 303 minutes
July 19, 2022 - 175 minutes
July 20, 2022 - 262 minutes
July 21, 2022 - 266 minutes
July 22, 2022 - 468 minutes
July 23, 2022 - 556 minutes
July 24, 2022 - 405 minutes
July 25, 2022 - 324 minutes
July 26, 2022 - 270 minutes
July 27, 2022 - 329 minutes
July 28, 2022 - 266 minutes
July 29, 2022 - 171 minutes
July 30, 2022 - 426 minutes
July 31, 2022 - 713 minutes
August 01, 2022 - 278 minutes
August 02, 2022 - 119 minutes
August 03, 2022 - 234 minutes
August 04, 2022 - 123 minutes
August 05, 2022 - 237 minutes
August 06, 2022 - 324 minutes
August 07, 2022 - 336 minutes
August 08, 2022 - 269 minutes
August 09, 2022 - 305 minutes
August 10, 2022 - 424 minutes
August 11, 2022 - 398 minutes
August 12, 2022 - 290 minutes
August 13, 2022 - 406 minutes
August 14, 2022 - 356 minutes
August 15, 2022 - 378 minutes
August 16, 2022 - 249 minutes
August 17, 2022 - 466 minutes
August 18, 2022 - 415 minutes
August 19, 2022 - 149 minutes
August 20, 2022 - 359 minutes
August 21, 2022 - 494 minutes
August 22, 2022 - 407 minutes
August 23, 2022 - 243 minutes
August 24, 2022 - 257 minutes
August 25, 2022 - 234 minutes
August 26, 2022 - 171 minutes
August 27, 2022 - 281 minutes
August 28, 2022 - 483 minutes
August 29, 2022 - 277 minutes
August 30, 2022 - 184 minutes
August 31, 2022 - 218 minutes
September 01, 2022 - 299 minutes
September 02, 2022 - 110 minutes
September 03, 2022 - 251 minutes
September 04, 2022 - 399 minutes
September 05, 2022 - 409 minutes
September 06, 2022 - 252 minutes
September 07, 2022 - 243 minutes
September 08, 2022 - 120 minutes
September 09, 2022 - 200 minutes
September 10, 2022 - 220 minutes
September 11, 2022 - 245 minutes
September 12, 2022 - 173 minutes
September 13, 2022 - 173 minutes
September 14, 2022 - 259 minutes
September 15, 2022 - 154 minutes
September 16, 2022 - 202 minutes
September 17, 2022 - 243 minutes
September 18, 2022 - 252 minutes
September 19, 2022 - 399 minutes
September 20, 2022 - 354 minutes
September 21, 2022 - 339 minutes
September 22, 2022 - 279 minutes
September 23, 2022 - 196 minutes
September 24, 2022 - 284 minutes
September 25, 2022 - 515 minutes
September 26, 2022 - 244 minutes
September 27, 2022 - 272 minutes
September 28, 2022 - 565 minutes
September 29, 2022 - 334 minutes
September 30, 2022 - 461 minutes
October 01, 2022 - 502 minutes
October 02, 2022 - 181 minutes
October 03, 2022 - 191 minutes
October 04, 2022 - 538 minutes
October 05, 2022 - 350 minutes
October 06, 2022 - 336 minutes
October 07, 2022 - 194 minutes
October 08, 2022 - 250 minutes
October 09, 2022 - 365 minutes
October 10, 2022 - 555 minutes
October 11, 2022 - 401 minutes
October 12, 2022 - 375 minutes
October 13, 2022 - 337 minutes
October 14, 2022 - 198 minutes
October 15, 2022 - 399 minutes
October 16, 2022 - 341 minutes
October 17, 2022 - 362 minutes
October 18, 2022 - 376 minutes
October 19, 2022 - 119 minutes
October 20, 2022 - 119 minutes
October 21, 2022 - 433 minutes
October 22, 2022 - 173 minutes
October 23, 2022 - 73 minutes
October 24, 2022 - 283 minutes
October 25, 2022 - 214 minutes
October 26, 2022 - 149 minutes
October 27, 2022 - 205 minutes
October 28, 2022 - 15 minutes
October 29, 2022 - 174 minutes
October 30, 2022 - 206 minutes
October 31, 2022 - 169 minutes
November 01, 2022 - 291 minutes
November 02, 2022 - 250 minutes
November 03, 2022 - 235 minutes
November 04, 2022 - 110 minutes
November 05, 2022 - 339 minutes
November 06, 2022 - 203 minutes
November 07, 2022 - 435 minutes
November 08, 2022 - 300 minutes
November 09, 2022 - 261 minutes
November 10, 2022 - 153 minutes
November 11, 2022 - 246 minutes
November 12, 2022 - 223 minutes
November 13, 2022 - 287 minutes
November 14, 2022 - 265 minutes
November 15, 2022 - 256 minutes
November 16, 2022 - 154 minutes
November 17, 2022 - 321 minutes
November 18, 2022 - 241 minutes
November 19, 2022 - 207 minutes
November 20, 2022 - 246 minutes
November 21, 2022 - 254 minutes
November 22, 2022 - 220 minutes
November 23, 2022 - 545 minutes
November 24, 2022 - 272 minutes
November 25, 2022 - 395 minutes
November 26, 2022 - 207 minutes
November 27, 2022 - 227 minutes
November 28, 2022 - 184 minutes
November 29, 2022 - 201 minutes
November 30, 2022 - 274 minutes
December 01, 2022 - 312 minutes
December 02, 2022 - 288 minutes
December 03, 2022 - 251 minutes
December 04, 2022 - 183 minutes
December 05, 2022 - 233 minutes
December 06, 2022 - 159 minutes
December 07, 2022 - 163 minutes
December 08, 2022 - 383 minutes
December 09, 2022 - 157 minutes
December 10, 2022 - 194 minutes
December 11, 2022 - 191 minutes
December 12, 2022 - 200 minutes
December 13, 2022 - 247 minutes
December 14, 2022 - 297 minutes
December 15, 2022 - 176 minutes
December 16, 2022 - 285 minutes
December 17, 2022 - 362 minutes
December 18, 2022 - 324 minutes
December 19, 2022 - 188 minutes
December 20, 2022 - 92 minutes
December 21, 2022 - 287 minutes
December 22, 2022 - 280 minutes
December 23, 2022 - 245 minutes
December 24, 2022 - 155 minutes
December 25, 2022 - 274 minutes
December 26, 2022 - 75 minutes
December 27, 2022 - 225 minutes
December 28, 2022 - 283 minutes
December 29, 2022 - 288 minutes
December 30, 2022 - 332 minutes
December 31, 2022 - 376 minutes


=== Artist by Hour ===
12:00 AM -> ENHYPEN
1:00 AM -> The Neighbourhood
2:00 AM -> ENHYPEN
3:00 AM -> ENHYPEN
4:00 AM -> The Neighbourhood
5:00 AM -> The Neighbourhood
6:00 AM -> The Neighbourhood
7:00 AM -> The Neighbourhood
8:00 AM -> The Neighbourhood
9:00 AM -> The Neighbourhood
10:00 AM -> The Neighbourhood
11:00 AM -> The Neighbourhood
12:00 PM -> The Neighbourhood
1:00 PM -> The Neighbourhood
2:00 PM -> The Neighbourhood
3:00 PM -> The Neighbourhood
4:00 PM -> The Neighbourhood
5:00 PM -> The Neighbourhood
6:00 PM -> The Neighbourhood
7:00 PM -> The Neighbourhood
8:00 PM -> Cigarettes After Sex
9:00 PM -> The Neighbourhood
10:00 PM -> Cigarettes After Sex
11:00 PM -> The Neighbourhood


=== 2023 STATISTICS ===
=== Basic Statistics ===


=== Top Artists ===
1. ENHYPEN - 2604 streams
2. Taylor Swift - 2151 streams
3. TOMORROW X TOGETHER - 1590 streams
4. Chase Atlantic - 1124 streams
5. Kanye West - 1051 streams
6. Giveon - 891 streams
7. The Neighbourhood - 833 streams
8. beabadoobee - 774 streams
9. The Weeknd - 714 streams
10. NIKI - 701 streams
/Users/nadyafahrani/Desktop/SPOTIFY PERSONAL PROJ/main.py:109: UserWarning: The figure layout has changed to tight
  plt.tight_layout()


=== Top Tracks ===
1. Bite Me - 494 streams
2. Good Boy Gone Bad - 391 streams
3. Let Me Love You - 327 streams
4. I Only Have Eyes for You - 319 streams
5. Drunk-Dazed - 310 streams
6. bad - 296 streams
7. Perempuan Paling Cantik Di Negriku Indonesia - 274 streams
8. The Dress - 263 streams
9. Glue Song - 254 streams
10. HEAVEN AND BACK - 239 streams


=== Number of Unique Artists ===
You have listened to 1712 unique artists.


=== Artists By Listening Time ===
1. ENHYPEN - 5160.3 minutes played
2. Taylor Swift - 4178.86 minutes played
3. TOMORROW X TOGETHER - 3180.62 minutes played
4. Chase Atlantic - 2064.49 minutes played
5. Kanye West - 1979.58 minutes played
6. Dewa 19 - 1861.24 minutes played
7. NIKI - 1539.67 minutes played
8. The Weeknd - 1429.78 minutes played
9. Giveon - 1415.65 minutes played
10. Frank Ocean - 1282.58 minutes played


=== Listening By Hour ===
12:00 AM - 2727 streams
1:00 AM - 1428 streams
2:00 AM - 1572 streams
3:00 AM - 1873 streams
4:00 AM - 2176 streams
5:00 AM - 2275 streams
6:00 AM - 1948 streams
7:00 AM - 1856 streams
8:00 AM - 2306 streams
9:00 AM - 2118 streams
10:00 AM - 2492 streams
11:00 AM - 2229 streams
12:00 PM - 2379 streams
1:00 PM - 3589 streams
2:00 PM - 2900 streams
3:00 PM - 2061 streams
4:00 PM - 1666 streams
5:00 PM - 1570 streams
6:00 PM - 1400 streams
7:00 PM - 867 streams
8:00 PM - 522 streams
9:00 PM - 433 streams
10:00 PM - 420 streams
11:00 PM - 1054 streams


=== Listening Day of the Week ===
Monday - 6271 streams
Tuesday - 6138 streams
Wednesday - 6324 streams
Thursday - 6075 streams
Friday - 5403 streams
Saturday - 6720 streams
Sunday - 6930 streams


=== Daily Listening Time ===
December 23, 2022 - 0 minutes
January 01, 2023 - 396 minutes
January 02, 2023 - 363 minutes
January 03, 2023 - 408 minutes
January 04, 2023 - 419 minutes
January 05, 2023 - 251 minutes
January 06, 2023 - 250 minutes
January 07, 2023 - 395 minutes
January 08, 2023 - 257 minutes
January 09, 2023 - 259 minutes
January 10, 2023 - 305 minutes
January 11, 2023 - 277 minutes
January 12, 2023 - 299 minutes
January 13, 2023 - 370 minutes
January 14, 2023 - 520 minutes
January 15, 2023 - 329 minutes
January 16, 2023 - 280 minutes
January 17, 2023 - 109 minutes
January 18, 2023 - 163 minutes
January 19, 2023 - 246 minutes
January 20, 2023 - 95 minutes
January 21, 2023 - 218 minutes
January 22, 2023 - 67 minutes
January 23, 2023 - 295 minutes
January 24, 2023 - 194 minutes
January 25, 2023 - 128 minutes
January 26, 2023 - 113 minutes
January 27, 2023 - 126 minutes
January 28, 2023 - 141 minutes
January 29, 2023 - 148 minutes
January 30, 2023 - 126 minutes
January 31, 2023 - 100 minutes
February 01, 2023 - 104 minutes
February 02, 2023 - 100 minutes
February 03, 2023 - 144 minutes
February 04, 2023 - 207 minutes
February 05, 2023 - 124 minutes
February 06, 2023 - 167 minutes
February 07, 2023 - 195 minutes
February 08, 2023 - 239 minutes
February 09, 2023 - 250 minutes
February 10, 2023 - 185 minutes
February 11, 2023 - 88 minutes
February 12, 2023 - 226 minutes
February 13, 2023 - 328 minutes
February 14, 2023 - 181 minutes
February 15, 2023 - 252 minutes
February 16, 2023 - 183 minutes
February 17, 2023 - 279 minutes
February 18, 2023 - 207 minutes
February 19, 2023 - 480 minutes
February 20, 2023 - 256 minutes
February 21, 2023 - 214 minutes
February 22, 2023 - 201 minutes
February 23, 2023 - 152 minutes
February 24, 2023 - 258 minutes
February 25, 2023 - 271 minutes
February 26, 2023 - 138 minutes
February 27, 2023 - 89 minutes
February 28, 2023 - 219 minutes
March 01, 2023 - 161 minutes
March 02, 2023 - 84 minutes
March 03, 2023 - 323 minutes
March 04, 2023 - 98 minutes
March 05, 2023 - 421 minutes
March 06, 2023 - 333 minutes
March 07, 2023 - 95 minutes
March 08, 2023 - 212 minutes
March 09, 2023 - 254 minutes
March 10, 2023 - 178 minutes
March 11, 2023 - 303 minutes
March 12, 2023 - 280 minutes
March 13, 2023 - 170 minutes
March 14, 2023 - 194 minutes
March 15, 2023 - 240 minutes
March 16, 2023 - 158 minutes
March 17, 2023 - 198 minutes
March 18, 2023 - 288 minutes
March 19, 2023 - 219 minutes
March 20, 2023 - 152 minutes
March 21, 2023 - 144 minutes
March 22, 2023 - 255 minutes
March 23, 2023 - 76 minutes
March 24, 2023 - 71 minutes
March 25, 2023 - 129 minutes
March 26, 2023 - 162 minutes
March 27, 2023 - 155 minutes
March 28, 2023 - 266 minutes
March 29, 2023 - 94 minutes
March 30, 2023 - 301 minutes
March 31, 2023 - 219 minutes
April 01, 2023 - 133 minutes
April 02, 2023 - 181 minutes
April 03, 2023 - 111 minutes
April 04, 2023 - 191 minutes
April 05, 2023 - 267 minutes
April 06, 2023 - 175 minutes
April 07, 2023 - 37 minutes
April 08, 2023 - 115 minutes
April 09, 2023 - 243 minutes
April 10, 2023 - 96 minutes
April 11, 2023 - 120 minutes
April 12, 2023 - 189 minutes
April 13, 2023 - 403 minutes
April 14, 2023 - 305 minutes
April 15, 2023 - 107 minutes
April 16, 2023 - 190 minutes
April 17, 2023 - 117 minutes
April 18, 2023 - 217 minutes
April 19, 2023 - 332 minutes
April 20, 2023 - 186 minutes
April 21, 2023 - 213 minutes
April 22, 2023 - 180 minutes
April 23, 2023 - 114 minutes
April 24, 2023 - 369 minutes
April 25, 2023 - 169 minutes
April 26, 2023 - 340 minutes
April 27, 2023 - 269 minutes
April 28, 2023 - 178 minutes
April 29, 2023 - 166 minutes
April 30, 2023 - 205 minutes
May 01, 2023 - 66 minutes
May 02, 2023 - 138 minutes
May 03, 2023 - 152 minutes
May 04, 2023 - 112 minutes
May 05, 2023 - 58 minutes
May 06, 2023 - 333 minutes
May 07, 2023 - 237 minutes
May 08, 2023 - 172 minutes
May 09, 2023 - 215 minutes
May 10, 2023 - 210 minutes
May 11, 2023 - 117 minutes
May 12, 2023 - 83 minutes
May 13, 2023 - 108 minutes
May 14, 2023 - 114 minutes
May 15, 2023 - 254 minutes
May 16, 2023 - 163 minutes
May 17, 2023 - 162 minutes
May 18, 2023 - 262 minutes
May 19, 2023 - 114 minutes
May 20, 2023 - 129 minutes
May 21, 2023 - 301 minutes
May 22, 2023 - 314 minutes
May 23, 2023 - 135 minutes
May 24, 2023 - 166 minutes
May 25, 2023 - 122 minutes
May 26, 2023 - 144 minutes
May 27, 2023 - 476 minutes
May 28, 2023 - 70 minutes
May 29, 2023 - 136 minutes
May 30, 2023 - 129 minutes
May 31, 2023 - 114 minutes
June 01, 2023 - 180 minutes
June 02, 2023 - 185 minutes
June 03, 2023 - 125 minutes
June 04, 2023 - 275 minutes
June 05, 2023 - 130 minutes
June 06, 2023 - 189 minutes
June 07, 2023 - 110 minutes
June 08, 2023 - 112 minutes
June 09, 2023 - 440 minutes
June 10, 2023 - 189 minutes
June 11, 2023 - 341 minutes
June 12, 2023 - 391 minutes
June 13, 2023 - 265 minutes
June 14, 2023 - 425 minutes
June 15, 2023 - 315 minutes
June 16, 2023 - 334 minutes
June 17, 2023 - 411 minutes
June 18, 2023 - 75 minutes
June 19, 2023 - 437 minutes
June 20, 2023 - 276 minutes
June 21, 2023 - 231 minutes
June 22, 2023 - 349 minutes
June 23, 2023 - 213 minutes
June 24, 2023 - 333 minutes
June 25, 2023 - 205 minutes
June 26, 2023 - 129 minutes
June 27, 2023 - 85 minutes
June 28, 2023 - 139 minutes
June 29, 2023 - 148 minutes
June 30, 2023 - 134 minutes
July 01, 2023 - 105 minutes
July 02, 2023 - 61 minutes
July 03, 2023 - 79 minutes
July 04, 2023 - 57 minutes
July 05, 2023 - 134 minutes
July 06, 2023 - 170 minutes
July 07, 2023 - 72 minutes
July 08, 2023 - 161 minutes
July 09, 2023 - 246 minutes
July 10, 2023 - 263 minutes
July 11, 2023 - 287 minutes
July 12, 2023 - 303 minutes
July 13, 2023 - 295 minutes
July 14, 2023 - 446 minutes
July 15, 2023 - 535 minutes
July 16, 2023 - 197 minutes
July 17, 2023 - 76 minutes
July 18, 2023 - 203 minutes
July 19, 2023 - 153 minutes
July 20, 2023 - 104 minutes
July 21, 2023 - 196 minutes
July 22, 2023 - 266 minutes
July 23, 2023 - 184 minutes
July 24, 2023 - 31 minutes
July 25, 2023 - 90 minutes
July 26, 2023 - 194 minutes
July 27, 2023 - 49 minutes
July 28, 2023 - 136 minutes
July 29, 2023 - 166 minutes
July 30, 2023 - 247 minutes
July 31, 2023 - 115 minutes
August 01, 2023 - 241 minutes
August 02, 2023 - 65 minutes
August 03, 2023 - 290 minutes
August 04, 2023 - 130 minutes
August 05, 2023 - 181 minutes
August 06, 2023 - 237 minutes
August 07, 2023 - 99 minutes
August 08, 2023 - 201 minutes
August 09, 2023 - 151 minutes
August 10, 2023 - 150 minutes
August 11, 2023 - 265 minutes
August 12, 2023 - 257 minutes
August 13, 2023 - 319 minutes
August 14, 2023 - 103 minutes
August 15, 2023 - 232 minutes
August 16, 2023 - 67 minutes
August 17, 2023 - 214 minutes
August 18, 2023 - 58 minutes
August 19, 2023 - 260 minutes
August 20, 2023 - 333 minutes
August 21, 2023 - 119 minutes
August 22, 2023 - 150 minutes
August 23, 2023 - 208 minutes
August 24, 2023 - 178 minutes
August 25, 2023 - 63 minutes
August 26, 2023 - 212 minutes
August 27, 2023 - 542 minutes
August 28, 2023 - 299 minutes
August 29, 2023 - 396 minutes
August 30, 2023 - 330 minutes
August 31, 2023 - 421 minutes
September 01, 2023 - 240 minutes
September 02, 2023 - 83 minutes
September 03, 2023 - 271 minutes
September 04, 2023 - 241 minutes
September 05, 2023 - 171 minutes
September 06, 2023 - 256 minutes
September 07, 2023 - 346 minutes
September 08, 2023 - 94 minutes
September 09, 2023 - 76 minutes
September 10, 2023 - 238 minutes
September 11, 2023 - 442 minutes
September 12, 2023 - 196 minutes
September 13, 2023 - 224 minutes
September 14, 2023 - 276 minutes
September 15, 2023 - 179 minutes
September 16, 2023 - 50 minutes
September 17, 2023 - 199 minutes
September 18, 2023 - 237 minutes
September 19, 2023 - 318 minutes
September 20, 2023 - 274 minutes
September 21, 2023 - 117 minutes
September 22, 2023 - 128 minutes
September 23, 2023 - 199 minutes
September 24, 2023 - 370 minutes
September 25, 2023 - 294 minutes
September 26, 2023 - 115 minutes
September 27, 2023 - 110 minutes
September 28, 2023 - 106 minutes
September 29, 2023 - 77 minutes
September 30, 2023 - 122 minutes
October 01, 2023 - 223 minutes
October 02, 2023 - 134 minutes
October 03, 2023 - 123 minutes
October 04, 2023 - 122 minutes
October 05, 2023 - 242 minutes
October 06, 2023 - 52 minutes
October 07, 2023 - 204 minutes
October 08, 2023 - 242 minutes
October 09, 2023 - 405 minutes
October 10, 2023 - 311 minutes
October 11, 2023 - 237 minutes
October 12, 2023 - 146 minutes
October 13, 2023 - 180 minutes
October 14, 2023 - 331 minutes
October 15, 2023 - 120 minutes
October 16, 2023 - 357 minutes
October 17, 2023 - 498 minutes
October 18, 2023 - 201 minutes
October 19, 2023 - 95 minutes
October 20, 2023 - 183 minutes
October 21, 2023 - 104 minutes
October 22, 2023 - 143 minutes
October 23, 2023 - 72 minutes
October 24, 2023 - 133 minutes
October 25, 2023 - 94 minutes
October 26, 2023 - 415 minutes
October 27, 2023 - 277 minutes
October 28, 2023 - 162 minutes
October 29, 2023 - 222 minutes
October 30, 2023 - 168 minutes
October 31, 2023 - 231 minutes
November 01, 2023 - 354 minutes
November 02, 2023 - 332 minutes
November 03, 2023 - 420 minutes
November 04, 2023 - 368 minutes
November 05, 2023 - 76 minutes
November 06, 2023 - 179 minutes
November 07, 2023 - 74 minutes
November 08, 2023 - 177 minutes
November 09, 2023 - 168 minutes
November 10, 2023 - 151 minutes
November 11, 2023 - 191 minutes
November 12, 2023 - 262 minutes
November 13, 2023 - 131 minutes
November 14, 2023 - 185 minutes
November 15, 2023 - 187 minutes
November 16, 2023 - 123 minutes
November 17, 2023 - 272 minutes
November 18, 2023 - 372 minutes
November 19, 2023 - 299 minutes
November 20, 2023 - 188 minutes
November 21, 2023 - 288 minutes
November 22, 2023 - 205 minutes
November 23, 2023 - 231 minutes
November 24, 2023 - 109 minutes
November 25, 2023 - 317 minutes
November 26, 2023 - 235 minutes
November 27, 2023 - 198 minutes
November 28, 2023 - 164 minutes
November 29, 2023 - 59 minutes
November 30, 2023 - 198 minutes
December 01, 2023 - 208 minutes
December 02, 2023 - 207 minutes
December 03, 2023 - 199 minutes
December 04, 2023 - 167 minutes
December 05, 2023 - 269 minutes
December 06, 2023 - 199 minutes
December 07, 2023 - 334 minutes
December 08, 2023 - 223 minutes
December 09, 2023 - 153 minutes
December 10, 2023 - 471 minutes
December 11, 2023 - 340 minutes
December 12, 2023 - 337 minutes
December 13, 2023 - 327 minutes
December 14, 2023 - 253 minutes
December 15, 2023 - 255 minutes
December 16, 2023 - 200 minutes
December 17, 2023 - 195 minutes
December 18, 2023 - 361 minutes
December 19, 2023 - 253 minutes
December 20, 2023 - 422 minutes
December 21, 2023 - 355 minutes
December 22, 2023 - 113 minutes
December 23, 2023 - 289 minutes
December 24, 2023 - 458 minutes
December 25, 2023 - 283 minutes
December 26, 2023 - 374 minutes
December 27, 2023 - 354 minutes
December 28, 2023 - 387 minutes
December 29, 2023 - 325 minutes
December 30, 2023 - 403 minutes
December 31, 2023 - 369 minutes


=== Artist by Hour ===
12:00 AM -> Taylor Swift
1:00 AM -> Taylor Swift
2:00 AM -> ENHYPEN
3:00 AM -> ENHYPEN
4:00 AM -> Taylor Swift
5:00 AM -> TOMORROW X TOGETHER
6:00 AM -> ENHYPEN
7:00 AM -> ENHYPEN
8:00 AM -> Taylor Swift
9:00 AM -> ENHYPEN
10:00 AM -> Taylor Swift
11:00 AM -> ENHYPEN
12:00 PM -> Taylor Swift
1:00 PM -> ENHYPEN
2:00 PM -> TOMORROW X TOGETHER
3:00 PM -> ENHYPEN
4:00 PM -> ENHYPEN
5:00 PM -> ENHYPEN
6:00 PM -> ENHYPEN
7:00 PM -> ENHYPEN
8:00 PM -> The Flamingos
9:00 PM -> ENHYPEN
10:00 PM -> ENHYPEN
11:00 PM -> ENHYPEN


=== 2024 STATISTICS ===
=== Basic Statistics ===


=== Top Artists ===
1. Taylor Swift - 1779 streams
2. The Beatles - 1329 streams
3. Ariana Grande - 1071 streams
4. Frank Ocean - 1003 streams
5. Justin Bieber - 981 streams
6. One Direction - 859 streams
7. The Neighbourhood - 828 streams
8. Clairo - 817 streams
9. beabadoobee - 774 streams
10. Dewa 19 - 677 streams
/Users/nadyafahrani/Desktop/SPOTIFY PERSONAL PROJ/main.py:109: UserWarning: The figure layout has changed to tight
  plt.tight_layout()


=== Top Tracks ===
1. Kutukan Mantan - 528 streams
2. Missionário - 484 streams
3. Favorite Girl - 479 streams
4. DITINGGAL BANG DIKA - 394 streams
5. I Will - Remastered 2009 - 341 streams
6. Heaven - 336 streams
7. Backburner - 304 streams
8. Yank Haus - 301 streams
9. Seberapa Pantas - 296 streams
10. Goyang Dumang - 280 streams


=== Number of Unique Artists ===
You have listened to 1949 unique artists.


=== Artists By Listening Time ===
1. Taylor Swift - 2889.87 minutes played
2. Justin Bieber - 2314.46 minutes played
3. Frank Ocean - 2001.52 minutes played
4. The Beatles - 1785.95 minutes played
5. Ariana Grande - 1689.36 minutes played
6. Jakob57 - 1638.38 minutes played
7. Dika - 1544.45 minutes played
8. NIKI - 1477.98 minutes played
9. One Direction - 1425.49 minutes played
10. Dewa 19 - 1420.36 minutes played


=== Listening By Hour ===
12:00 AM - 3145 streams
1:00 AM - 2246 streams
2:00 AM - 1886 streams
3:00 AM - 2707 streams
4:00 AM - 2325 streams
5:00 AM - 2597 streams
6:00 AM - 3107 streams
7:00 AM - 3247 streams
8:00 AM - 2911 streams
9:00 AM - 3109 streams
10:00 AM - 2870 streams
11:00 AM - 3236 streams
12:00 PM - 3463 streams
1:00 PM - 3647 streams
2:00 PM - 3293 streams
3:00 PM - 2060 streams
4:00 PM - 1544 streams
5:00 PM - 1521 streams
6:00 PM - 1272 streams
7:00 PM - 968 streams
8:00 PM - 902 streams
9:00 PM - 378 streams
10:00 PM - 797 streams
11:00 PM - 2428 streams


=== Listening Day of the Week ===
Monday - 7872 streams
Tuesday - 7824 streams
Wednesday - 7495 streams
Thursday - 8094 streams
Friday - 6879 streams
Saturday - 8831 streams
Sunday - 8664 streams


=== Daily Listening Time ===
January 01, 2024 - 238 minutes
January 02, 2024 - 70 minutes
January 03, 2024 - 166 minutes
January 04, 2024 - 64 minutes
January 05, 2024 - 351 minutes
January 06, 2024 - 228 minutes
January 08, 2024 - 130 minutes
January 09, 2024 - 261 minutes
January 10, 2024 - 73 minutes
January 11, 2024 - 312 minutes
January 12, 2024 - 32 minutes
January 13, 2024 - 279 minutes
January 14, 2024 - 164 minutes
January 15, 2024 - 76 minutes
January 16, 2024 - 220 minutes
January 17, 2024 - 141 minutes
January 18, 2024 - 239 minutes
January 19, 2024 - 234 minutes
January 20, 2024 - 54 minutes
January 21, 2024 - 257 minutes
January 22, 2024 - 121 minutes
January 23, 2024 - 316 minutes
January 24, 2024 - 116 minutes
January 25, 2024 - 195 minutes
January 26, 2024 - 285 minutes
January 27, 2024 - 94 minutes
January 28, 2024 - 154 minutes
January 29, 2024 - 122 minutes
January 30, 2024 - 161 minutes
January 31, 2024 - 110 minutes
February 01, 2024 - 472 minutes
February 02, 2024 - 152 minutes
February 03, 2024 - 101 minutes
February 04, 2024 - 233 minutes
February 05, 2024 - 90 minutes
February 06, 2024 - 329 minutes
February 07, 2024 - 185 minutes
February 08, 2024 - 121 minutes
February 09, 2024 - 138 minutes
February 10, 2024 - 262 minutes
February 11, 2024 - 174 minutes
February 12, 2024 - 260 minutes
February 13, 2024 - 515 minutes
February 14, 2024 - 273 minutes
February 15, 2024 - 432 minutes
February 16, 2024 - 108 minutes
February 17, 2024 - 115 minutes
February 18, 2024 - 239 minutes
February 19, 2024 - 142 minutes
February 20, 2024 - 345 minutes
February 21, 2024 - 223 minutes
February 22, 2024 - 408 minutes
February 23, 2024 - 284 minutes
February 24, 2024 - 407 minutes
February 25, 2024 - 261 minutes
February 26, 2024 - 412 minutes
February 27, 2024 - 208 minutes
February 28, 2024 - 97 minutes
February 29, 2024 - 537 minutes
March 01, 2024 - 276 minutes
March 02, 2024 - 40 minutes
March 03, 2024 - 364 minutes
March 04, 2024 - 121 minutes
March 05, 2024 - 46 minutes
March 06, 2024 - 114 minutes
March 07, 2024 - 210 minutes
March 08, 2024 - 142 minutes
March 09, 2024 - 412 minutes
March 10, 2024 - 210 minutes
March 11, 2024 - 121 minutes
March 12, 2024 - 5 minutes
March 13, 2024 - 99 minutes
March 14, 2024 - 137 minutes
March 15, 2024 - 343 minutes
March 16, 2024 - 33 minutes
March 17, 2024 - 201 minutes
March 18, 2024 - 160 minutes
March 19, 2024 - 169 minutes
March 20, 2024 - 167 minutes
March 21, 2024 - 230 minutes
March 22, 2024 - 143 minutes
March 23, 2024 - 150 minutes
March 24, 2024 - 257 minutes
March 25, 2024 - 134 minutes
March 26, 2024 - 177 minutes
March 27, 2024 - 169 minutes
March 28, 2024 - 218 minutes
March 29, 2024 - 252 minutes
March 30, 2024 - 160 minutes
March 31, 2024 - 226 minutes
April 01, 2024 - 236 minutes
April 02, 2024 - 289 minutes
April 03, 2024 - 89 minutes
April 04, 2024 - 150 minutes
April 05, 2024 - 117 minutes
April 06, 2024 - 477 minutes
April 07, 2024 - 217 minutes
April 08, 2024 - 183 minutes
April 09, 2024 - 235 minutes
April 10, 2024 - 283 minutes
April 11, 2024 - 157 minutes
April 12, 2024 - 256 minutes
April 13, 2024 - 337 minutes
April 14, 2024 - 179 minutes
April 15, 2024 - 191 minutes
April 16, 2024 - 418 minutes
April 17, 2024 - 159 minutes
April 18, 2024 - 108 minutes
April 19, 2024 - 236 minutes
April 20, 2024 - 306 minutes
April 21, 2024 - 159 minutes
April 22, 2024 - 144 minutes
April 23, 2024 - 259 minutes
April 24, 2024 - 177 minutes
April 25, 2024 - 242 minutes
April 26, 2024 - 253 minutes
April 27, 2024 - 171 minutes
April 28, 2024 - 239 minutes
April 29, 2024 - 297 minutes
April 30, 2024 - 328 minutes
May 01, 2024 - 397 minutes
May 02, 2024 - 221 minutes
May 03, 2024 - 0 minutes
May 04, 2024 - 265 minutes
May 05, 2024 - 85 minutes
May 06, 2024 - 257 minutes
May 07, 2024 - 152 minutes
May 08, 2024 - 287 minutes
May 09, 2024 - 373 minutes
May 10, 2024 - 437 minutes
May 11, 2024 - 620 minutes
May 12, 2024 - 243 minutes
May 13, 2024 - 585 minutes
May 14, 2024 - 350 minutes
May 15, 2024 - 187 minutes
May 16, 2024 - 154 minutes
May 17, 2024 - 96 minutes
May 18, 2024 - 354 minutes
May 19, 2024 - 205 minutes
May 20, 2024 - 250 minutes
May 21, 2024 - 162 minutes
May 22, 2024 - 185 minutes
May 23, 2024 - 229 minutes
May 24, 2024 - 216 minutes
May 25, 2024 - 144 minutes
May 26, 2024 - 256 minutes
May 27, 2024 - 144 minutes
May 28, 2024 - 146 minutes
May 29, 2024 - 385 minutes
May 30, 2024 - 424 minutes
May 31, 2024 - 207 minutes
June 01, 2024 - 186 minutes
June 02, 2024 - 315 minutes
June 03, 2024 - 379 minutes
June 04, 2024 - 148 minutes
June 05, 2024 - 291 minutes
June 06, 2024 - 283 minutes
June 07, 2024 - 285 minutes
June 08, 2024 - 132 minutes
June 09, 2024 - 227 minutes
June 10, 2024 - 260 minutes
June 11, 2024 - 315 minutes
June 12, 2024 - 335 minutes
June 13, 2024 - 242 minutes
June 14, 2024 - 205 minutes
June 15, 2024 - 208 minutes
June 16, 2024 - 416 minutes
June 17, 2024 - 287 minutes
June 18, 2024 - 236 minutes
June 19, 2024 - 207 minutes
June 20, 2024 - 327 minutes
June 21, 2024 - 287 minutes
June 22, 2024 - 413 minutes
June 23, 2024 - 216 minutes
June 24, 2024 - 239 minutes
June 25, 2024 - 117 minutes
June 26, 2024 - 144 minutes
June 27, 2024 - 196 minutes
June 28, 2024 - 462 minutes
June 29, 2024 - 268 minutes
June 30, 2024 - 209 minutes
July 01, 2024 - 296 minutes
July 02, 2024 - 181 minutes
July 03, 2024 - 159 minutes
July 04, 2024 - 311 minutes
July 05, 2024 - 348 minutes
July 06, 2024 - 291 minutes
July 07, 2024 - 196 minutes
July 08, 2024 - 224 minutes
July 09, 2024 - 223 minutes
July 10, 2024 - 242 minutes
July 11, 2024 - 141 minutes
July 12, 2024 - 203 minutes
July 13, 2024 - 195 minutes
July 14, 2024 - 202 minutes
July 15, 2024 - 191 minutes
July 16, 2024 - 105 minutes
July 17, 2024 - 594 minutes
July 18, 2024 - 100 minutes
July 19, 2024 - 101 minutes
July 20, 2024 - 298 minutes
July 21, 2024 - 233 minutes
July 22, 2024 - 213 minutes
July 23, 2024 - 153 minutes
July 24, 2024 - 238 minutes
July 25, 2024 - 261 minutes
July 26, 2024 - 147 minutes
July 27, 2024 - 186 minutes
July 28, 2024 - 347 minutes
July 29, 2024 - 210 minutes
July 30, 2024 - 300 minutes
July 31, 2024 - 164 minutes
August 01, 2024 - 252 minutes
August 02, 2024 - 101 minutes
August 03, 2024 - 94 minutes
August 04, 2024 - 333 minutes
August 05, 2024 - 167 minutes
August 06, 2024 - 149 minutes
August 07, 2024 - 217 minutes
August 08, 2024 - 260 minutes
August 09, 2024 - 193 minutes
August 10, 2024 - 144 minutes
August 11, 2024 - 309 minutes
August 12, 2024 - 109 minutes
August 13, 2024 - 347 minutes
August 14, 2024 - 119 minutes
August 15, 2024 - 184 minutes
August 16, 2024 - 393 minutes
August 17, 2024 - 223 minutes
August 18, 2024 - 329 minutes
August 19, 2024 - 182 minutes
August 20, 2024 - 305 minutes
August 21, 2024 - 259 minutes
August 22, 2024 - 246 minutes
August 23, 2024 - 151 minutes
August 24, 2024 - 228 minutes
August 25, 2024 - 233 minutes
August 26, 2024 - 378 minutes
August 27, 2024 - 519 minutes
August 28, 2024 - 391 minutes
August 29, 2024 - 357 minutes
August 30, 2024 - 251 minutes
August 31, 2024 - 178 minutes
September 01, 2024 - 402 minutes
September 02, 2024 - 400 minutes
September 03, 2024 - 313 minutes
September 04, 2024 - 421 minutes
September 05, 2024 - 477 minutes
September 06, 2024 - 324 minutes
September 07, 2024 - 320 minutes
September 08, 2024 - 96 minutes
September 09, 2024 - 157 minutes
September 10, 2024 - 332 minutes
September 11, 2024 - 374 minutes
September 12, 2024 - 256 minutes
September 13, 2024 - 105 minutes
September 14, 2024 - 153 minutes
September 15, 2024 - 147 minutes
September 16, 2024 - 438 minutes
September 17, 2024 - 678 minutes
September 18, 2024 - 208 minutes
September 19, 2024 - 510 minutes
September 20, 2024 - 162 minutes
September 21, 2024 - 216 minutes
September 22, 2024 - 203 minutes
September 23, 2024 - 193 minutes
September 24, 2024 - 333 minutes
September 25, 2024 - 344 minutes
September 26, 2024 - 438 minutes
September 27, 2024 - 148 minutes
September 28, 2024 - 255 minutes
September 29, 2024 - 221 minutes
September 30, 2024 - 291 minutes
October 01, 2024 - 223 minutes
October 02, 2024 - 157 minutes
October 03, 2024 - 348 minutes
October 04, 2024 - 194 minutes
October 05, 2024 - 119 minutes
October 06, 2024 - 176 minutes
October 07, 2024 - 286 minutes
October 08, 2024 - 345 minutes
October 09, 2024 - 319 minutes
October 10, 2024 - 218 minutes
October 11, 2024 - 457 minutes
October 12, 2024 - 481 minutes
October 13, 2024 - 344 minutes
October 14, 2024 - 277 minutes
October 15, 2024 - 284 minutes
October 16, 2024 - 427 minutes
October 17, 2024 - 228 minutes
October 18, 2024 - 417 minutes
October 19, 2024 - 419 minutes
October 20, 2024 - 379 minutes
October 21, 2024 - 264 minutes
October 22, 2024 - 141 minutes
October 23, 2024 - 225 minutes
October 24, 2024 - 169 minutes
October 25, 2024 - 181 minutes
October 26, 2024 - 309 minutes
October 27, 2024 - 350 minutes
October 28, 2024 - 241 minutes
October 29, 2024 - 426 minutes
October 30, 2024 - 174 minutes
October 31, 2024 - 222 minutes
November 01, 2024 - 156 minutes
November 02, 2024 - 214 minutes
November 03, 2024 - 319 minutes
November 04, 2024 - 83 minutes
November 05, 2024 - 355 minutes
November 06, 2024 - 366 minutes
November 07, 2024 - 291 minutes
November 08, 2024 - 324 minutes
November 09, 2024 - 383 minutes
November 10, 2024 - 296 minutes
November 11, 2024 - 496 minutes
November 12, 2024 - 598 minutes
November 13, 2024 - 410 minutes
November 14, 2024 - 357 minutes
November 15, 2024 - 126 minutes
November 16, 2024 - 286 minutes
November 17, 2024 - 120 minutes
November 18, 2024 - 219 minutes
November 19, 2024 - 151 minutes
November 20, 2024 - 411 minutes
November 21, 2024 - 199 minutes
November 22, 2024 - 178 minutes
November 23, 2024 - 223 minutes
November 24, 2024 - 476 minutes
November 25, 2024 - 383 minutes
November 26, 2024 - 140 minutes
November 27, 2024 - 224 minutes
November 28, 2024 - 276 minutes
November 29, 2024 - 329 minutes
November 30, 2024 - 132 minutes
December 01, 2024 - 173 minutes
December 02, 2024 - 263 minutes
December 03, 2024 - 185 minutes
December 04, 2024 - 185 minutes
December 05, 2024 - 114 minutes
December 06, 2024 - 236 minutes
December 07, 2024 - 149 minutes
December 08, 2024 - 133 minutes
December 09, 2024 - 352 minutes
December 10, 2024 - 124 minutes
December 11, 2024 - 124 minutes
December 12, 2024 - 218 minutes
December 13, 2024 - 164 minutes
December 14, 2024 - 329 minutes
December 15, 2024 - 223 minutes
December 16, 2024 - 159 minutes
December 17, 2024 - 135 minutes
December 18, 2024 - 218 minutes
December 19, 2024 - 113 minutes
December 20, 2024 - 195 minutes
December 21, 2024 - 91 minutes
December 22, 2024 - 167 minutes
December 23, 2024 - 174 minutes
December 24, 2024 - 205 minutes
December 25, 2024 - 197 minutes
December 26, 2024 - 228 minutes
December 27, 2024 - 116 minutes
December 28, 2024 - 270 minutes
December 29, 2024 - 328 minutes
December 30, 2024 - 480 minutes
December 31, 2024 - 343 minutes


=== Artist by Hour ===
12:00 AM -> The Beatles
1:00 AM -> Taylor Swift
2:00 AM -> The Beatles
3:00 AM -> Taylor Swift
4:00 AM -> The Beatles
5:00 AM -> The Beatles
6:00 AM -> The Beatles
7:00 AM -> Taylor Swift
8:00 AM -> ENHYPEN
9:00 AM -> Ariana Grande
10:00 AM -> One Direction
11:00 AM -> Taylor Swift
12:00 PM -> Taylor Swift
1:00 PM -> The Beatles
2:00 PM -> Taylor Swift
3:00 PM -> Taylor Swift
4:00 PM -> Taylor Swift
5:00 PM -> Taylor Swift
6:00 PM -> Taylor Swift
7:00 PM -> Clairo
8:00 PM -> NIKI
9:00 PM -> NIKI
10:00 PM -> Clairo
11:00 PM -> Taylor Swift


=== 2025 STATISTICS ===
=== Basic Statistics ===


=== Top Artists ===
1. Tate McRae - 4576 streams
2. Charli xcx - 1480 streams
3. Troye Sivan - 1152 streams
4. Ariana Grande - 1030 streams
5. ROLE MODEL - 775 streams
6. Chappell Roan - 682 streams
7. Maroon 5 - 646 streams
8. Taylor Swift - 631 streams
9. Radiohead - 595 streams
10. KATSEYE - 561 streams
/Users/nadyafahrani/Desktop/SPOTIFY PERSONAL PROJ/main.py:109: UserWarning: The figure layout has changed to tight
  plt.tight_layout()


=== Top Tracks ===
1. Sports car - 669 streams
2. Rush - 513 streams
3. run for the hills - 471 streams
4. It's ok I'm ok - 375 streams
5. Gnarly - 331 streams
6. Talking Body - 295 streams
7. Dear god - 280 streams
8. B2b - 277 streams
9. One Of Your Girls - 274 streams
10. greedy - 262 streams


=== Number of Unique Artists ===
You have listened to 2675 unique artists.


=== Artists By Listening Time ===
1. Tate McRae - 7920.47 minutes played
2. Charli xcx - 2151.44 minutes played
3. Troye Sivan - 2000.18 minutes played
4. Ariana Grande - 1569.53 minutes played
5. Radiohead - 1407.47 minutes played
6. Maroon 5 - 1285.55 minutes played
7. ROLE MODEL - 1242.36 minutes played
8. Chappell Roan - 1194.03 minutes played
9. sombr - 980.04 minutes played
10. Tove Lo - 888.87 minutes played


=== Listening By Hour ===
12:00 AM - 2675 streams
1:00 AM - 2590 streams
2:00 AM - 3000 streams
3:00 AM - 3420 streams
4:00 AM - 3429 streams
5:00 AM - 3865 streams
6:00 AM - 3257 streams
7:00 AM - 2981 streams
8:00 AM - 2814 streams
9:00 AM - 2928 streams
10:00 AM - 2954 streams
11:00 AM - 3082 streams
12:00 PM - 2956 streams
1:00 PM - 3363 streams
2:00 PM - 2815 streams
3:00 PM - 1715 streams
4:00 PM - 890 streams
5:00 PM - 894 streams
6:00 PM - 959 streams
7:00 PM - 444 streams
8:00 PM - 245 streams
9:00 PM - 347 streams
10:00 PM - 441 streams
11:00 PM - 1566 streams


=== Listening Day of the Week ===
Monday - 7974 streams
Tuesday - 7266 streams
Wednesday - 8420 streams
Thursday - 8008 streams
Friday - 7888 streams
Saturday - 6233 streams
Sunday - 7841 streams


=== Daily Listening Time ===
January 01, 2025 - 191 minutes
January 02, 2025 - 280 minutes
January 03, 2025 - 251 minutes
January 04, 2025 - 363 minutes
January 05, 2025 - 145 minutes
January 06, 2025 - 91 minutes
January 07, 2025 - 348 minutes
January 08, 2025 - 290 minutes
January 09, 2025 - 663 minutes
January 10, 2025 - 341 minutes
January 11, 2025 - 227 minutes
January 12, 2025 - 325 minutes
January 13, 2025 - 149 minutes
January 14, 2025 - 81 minutes
January 15, 2025 - 423 minutes
January 16, 2025 - 216 minutes
January 17, 2025 - 55 minutes
January 18, 2025 - 256 minutes
January 19, 2025 - 301 minutes
January 20, 2025 - 212 minutes
January 21, 2025 - 688 minutes
January 22, 2025 - 362 minutes
January 23, 2025 - 200 minutes
January 24, 2025 - 192 minutes
January 25, 2025 - 112 minutes
January 26, 2025 - 303 minutes
January 27, 2025 - 18 minutes
January 28, 2025 - 63 minutes
January 29, 2025 - 388 minutes
January 30, 2025 - 212 minutes
January 31, 2025 - 161 minutes
February 01, 2025 - 366 minutes
February 02, 2025 - 239 minutes
February 03, 2025 - 387 minutes
February 04, 2025 - 233 minutes
February 05, 2025 - 402 minutes
February 06, 2025 - 307 minutes
February 07, 2025 - 127 minutes
February 08, 2025 - 285 minutes
February 09, 2025 - 428 minutes
February 10, 2025 - 312 minutes
February 11, 2025 - 236 minutes
February 12, 2025 - 359 minutes
February 13, 2025 - 396 minutes
February 14, 2025 - 284 minutes
February 15, 2025 - 318 minutes
February 16, 2025 - 542 minutes
February 17, 2025 - 427 minutes
February 18, 2025 - 404 minutes
February 19, 2025 - 510 minutes
February 20, 2025 - 249 minutes
February 21, 2025 - 499 minutes
February 22, 2025 - 96 minutes
February 23, 2025 - 424 minutes
February 24, 2025 - 551 minutes
February 25, 2025 - 433 minutes
February 26, 2025 - 400 minutes
February 27, 2025 - 525 minutes
February 28, 2025 - 170 minutes
March 01, 2025 - 179 minutes
March 02, 2025 - 140 minutes
March 03, 2025 - 481 minutes
March 04, 2025 - 329 minutes
March 05, 2025 - 457 minutes
March 06, 2025 - 253 minutes
March 07, 2025 - 239 minutes
March 08, 2025 - 121 minutes
March 09, 2025 - 185 minutes
March 10, 2025 - 288 minutes
March 11, 2025 - 340 minutes
March 12, 2025 - 371 minutes
March 13, 2025 - 233 minutes
March 14, 2025 - 156 minutes
March 15, 2025 - 105 minutes
March 16, 2025 - 167 minutes
March 17, 2025 - 113 minutes
March 18, 2025 - 263 minutes
March 19, 2025 - 381 minutes
March 20, 2025 - 214 minutes
March 21, 2025 - 154 minutes
March 22, 2025 - 200 minutes
March 23, 2025 - 111 minutes
March 24, 2025 - 156 minutes
March 25, 2025 - 172 minutes
March 26, 2025 - 339 minutes
March 27, 2025 - 247 minutes
March 28, 2025 - 92 minutes
March 29, 2025 - 204 minutes
March 30, 2025 - 191 minutes
March 31, 2025 - 37 minutes
April 01, 2025 - 58 minutes
April 02, 2025 - 252 minutes
April 03, 2025 - 219 minutes
April 04, 2025 - 147 minutes
April 05, 2025 - 149 minutes
April 06, 2025 - 57 minutes
April 07, 2025 - 179 minutes
April 08, 2025 - 437 minutes
April 09, 2025 - 323 minutes
April 10, 2025 - 119 minutes
April 11, 2025 - 20 minutes
April 12, 2025 - 145 minutes
April 13, 2025 - 118 minutes
April 14, 2025 - 123 minutes
April 15, 2025 - 109 minutes
April 16, 2025 - 249 minutes
April 17, 2025 - 67 minutes
April 18, 2025 - 79 minutes
April 19, 2025 - 124 minutes
April 20, 2025 - 112 minutes
April 21, 2025 - 258 minutes
April 22, 2025 - 264 minutes
April 23, 2025 - 399 minutes
April 24, 2025 - 244 minutes
April 25, 2025 - 31 minutes
April 26, 2025 - 137 minutes
April 27, 2025 - 73 minutes
April 28, 2025 - 163 minutes
April 29, 2025 - 103 minutes
April 30, 2025 - 308 minutes
May 01, 2025 - 148 minutes
May 02, 2025 - 223 minutes
May 03, 2025 - 350 minutes
May 04, 2025 - 194 minutes
May 05, 2025 - 388 minutes
May 06, 2025 - 192 minutes
May 07, 2025 - 305 minutes
May 08, 2025 - 362 minutes
May 09, 2025 - 201 minutes
May 10, 2025 - 306 minutes
May 11, 2025 - 343 minutes
May 12, 2025 - 480 minutes
May 13, 2025 - 553 minutes
May 14, 2025 - 380 minutes
May 15, 2025 - 267 minutes
May 16, 2025 - 283 minutes
May 17, 2025 - 53 minutes
May 18, 2025 - 228 minutes
May 19, 2025 - 395 minutes
May 20, 2025 - 615 minutes
May 21, 2025 - 248 minutes
May 22, 2025 - 183 minutes
May 23, 2025 - 104 minutes
May 24, 2025 - 225 minutes
May 25, 2025 - 147 minutes
May 26, 2025 - 156 minutes
May 27, 2025 - 233 minutes
May 28, 2025 - 260 minutes
May 29, 2025 - 163 minutes
May 30, 2025 - 245 minutes
May 31, 2025 - 274 minutes
June 01, 2025 - 190 minutes
June 02, 2025 - 268 minutes
June 03, 2025 - 217 minutes
June 04, 2025 - 195 minutes
June 05, 2025 - 135 minutes
June 06, 2025 - 103 minutes
June 07, 2025 - 105 minutes
June 08, 2025 - 104 minutes
June 09, 2025 - 192 minutes
June 10, 2025 - 240 minutes
June 11, 2025 - 97 minutes
June 12, 2025 - 218 minutes
June 13, 2025 - 223 minutes
June 14, 2025 - 38 minutes
June 15, 2025 - 114 minutes
June 16, 2025 - 277 minutes
June 17, 2025 - 349 minutes
June 18, 2025 - 190 minutes
June 19, 2025 - 131 minutes
June 20, 2025 - 176 minutes
June 21, 2025 - 219 minutes
June 22, 2025 - 318 minutes
June 23, 2025 - 333 minutes
June 24, 2025 - 83 minutes
June 25, 2025 - 262 minutes
June 26, 2025 - 191 minutes
June 27, 2025 - 292 minutes
June 28, 2025 - 28 minutes
June 29, 2025 - 487 minutes
June 30, 2025 - 239 minutes
July 01, 2025 - 166 minutes
July 02, 2025 - 116 minutes
July 03, 2025 - 98 minutes
July 04, 2025 - 156 minutes
July 05, 2025 - 165 minutes
July 06, 2025 - 142 minutes
July 07, 2025 - 178 minutes
July 08, 2025 - 99 minutes
July 09, 2025 - 232 minutes
July 10, 2025 - 122 minutes
July 11, 2025 - 135 minutes
July 12, 2025 - 115 minutes
July 13, 2025 - 118 minutes
July 14, 2025 - 170 minutes
July 15, 2025 - 270 minutes
July 16, 2025 - 458 minutes
July 17, 2025 - 169 minutes
July 18, 2025 - 187 minutes
July 19, 2025 - 364 minutes
July 20, 2025 - 280 minutes
July 21, 2025 - 349 minutes
July 22, 2025 - 204 minutes
July 23, 2025 - 195 minutes
July 24, 2025 - 297 minutes
July 25, 2025 - 237 minutes
July 26, 2025 - 389 minutes
July 27, 2025 - 113 minutes
July 28, 2025 - 123 minutes
July 29, 2025 - 374 minutes
July 30, 2025 - 160 minutes
July 31, 2025 - 303 minutes
August 01, 2025 - 203 minutes
August 02, 2025 - 232 minutes
August 03, 2025 - 262 minutes
August 04, 2025 - 413 minutes
August 05, 2025 - 229 minutes
August 06, 2025 - 125 minutes
August 07, 2025 - 209 minutes
August 08, 2025 - 59 minutes
August 09, 2025 - 176 minutes
August 10, 2025 - 30 minutes
August 11, 2025 - 157 minutes
August 12, 2025 - 140 minutes
August 13, 2025 - 75 minutes
August 14, 2025 - 98 minutes
August 15, 2025 - 282 minutes
August 16, 2025 - 79 minutes
August 17, 2025 - 264 minutes
August 18, 2025 - 561 minutes
August 19, 2025 - 302 minutes
August 20, 2025 - 467 minutes
August 21, 2025 - 180 minutes
August 22, 2025 - 202 minutes
August 23, 2025 - 72 minutes
August 24, 2025 - 138 minutes
August 25, 2025 - 290 minutes
August 26, 2025 - 145 minutes
August 27, 2025 - 87 minutes
August 28, 2025 - 129 minutes
August 29, 2025 - 126 minutes
August 30, 2025 - 96 minutes
August 31, 2025 - 37 minutes
September 01, 2025 - 195 minutes
September 02, 2025 - 2 minutes
September 03, 2025 - 250 minutes
September 04, 2025 - 63 minutes
September 05, 2025 - 196 minutes
September 06, 2025 - 194 minutes
September 07, 2025 - 187 minutes
September 08, 2025 - 177 minutes
September 09, 2025 - 117 minutes
September 10, 2025 - 149 minutes
September 11, 2025 - 303 minutes
September 12, 2025 - 154 minutes
September 14, 2025 - 26 minutes
September 15, 2025 - 114 minutes
September 16, 2025 - 222 minutes
September 17, 2025 - 49 minutes
September 18, 2025 - 208 minutes
September 19, 2025 - 182 minutes
September 20, 2025 - 154 minutes
September 21, 2025 - 196 minutes
September 22, 2025 - 34 minutes
September 23, 2025 - 274 minutes
September 24, 2025 - 70 minutes
September 25, 2025 - 126 minutes
September 26, 2025 - 439 minutes
September 27, 2025 - 28 minutes
September 28, 2025 - 144 minutes
September 29, 2025 - 111 minutes
September 30, 2025 - 186 minutes
October 01, 2025 - 71 minutes
October 02, 2025 - 269 minutes
October 03, 2025 - 125 minutes
October 05, 2025 - 286 minutes
October 06, 2025 - 35 minutes
October 07, 2025 - 30 minutes
October 08, 2025 - 73 minutes
October 09, 2025 - 65 minutes
October 10, 2025 - 126 minutes
October 11, 2025 - 10 minutes
October 12, 2025 - 192 minutes
October 13, 2025 - 141 minutes
October 14, 2025 - 57 minutes
October 15, 2025 - 88 minutes
October 16, 2025 - 80 minutes
October 17, 2025 - 181 minutes
October 18, 2025 - 117 minutes
October 19, 2025 - 702 minutes
October 20, 2025 - 264 minutes
October 21, 2025 - 322 minutes
October 22, 2025 - 243 minutes
October 23, 2025 - 284 minutes
October 24, 2025 - 303 minutes
October 25, 2025 - 267 minutes
October 26, 2025 - 232 minutes
October 27, 2025 - 2 minutes
October 28, 2025 - 63 minutes
October 29, 2025 - 71 minutes
October 30, 2025 - 271 minutes
October 31, 2025 - 41 minutes
November 01, 2025 - 103 minutes
November 02, 2025 - 190 minutes
November 03, 2025 - 228 minutes
November 04, 2025 - 107 minutes
November 05, 2025 - 267 minutes
November 06, 2025 - 112 minutes
November 07, 2025 - 31 minutes
November 08, 2025 - 22 minutes
November 09, 2025 - 8 minutes
November 10, 2025 - 77 minutes
November 11, 2025 - 72 minutes
November 12, 2025 - 305 minutes
November 13, 2025 - 243 minutes
November 14, 2025 - 158 minutes
November 15, 2025 - 150 minutes
November 16, 2025 - 1 minute
November 17, 2025 - 82 minutes
November 18, 2025 - 105 minutes
November 19, 2025 - 72 minutes
November 20, 2025 - 59 minutes
November 21, 2025 - 106 minutes
November 22, 2025 - 155 minutes
November 23, 2025 - 136 minutes
November 24, 2025 - 213 minutes
November 25, 2025 - 62 minutes
November 26, 2025 - 96 minutes
November 27, 2025 - 190 minutes
November 28, 2025 - 30 minutes
November 29, 2025 - 35 minutes
November 30, 2025 - 81 minutes
December 01, 2025 - 52 minutes
December 02, 2025 - 97 minutes
December 03, 2025 - 145 minutes
December 04, 2025 - 78 minutes
December 05, 2025 - 3 minutes
December 06, 2025 - 88 minutes
December 07, 2025 - 108 minutes
December 08, 2025 - 43 minutes
December 09, 2025 - 79 minutes
December 10, 2025 - 126 minutes
December 11, 2025 - 61 minutes
December 12, 2025 - 68 minutes
December 13, 2025 - 81 minutes
December 14, 2025 - 23 minutes
December 15, 2025 - 56 minutes
December 16, 2025 - 99 minutes
December 17, 2025 - 26 minutes
December 18, 2025 - 86 minutes
December 19, 2025 - 115 minutes
December 20, 2025 - 223 minutes
December 21, 2025 - 140 minutes
December 22, 2025 - 75 minutes
December 23, 2025 - 136 minutes
December 24, 2025 - 185 minutes
December 25, 2025 - 261 minutes
December 26, 2025 - 213 minutes
December 27, 2025 - 192 minutes
December 28, 2025 - 330 minutes
December 29, 2025 - 52 minutes
December 30, 2025 - 127 minutes
December 31, 2025 - 76 minutes


=== Artist by Hour ===
12:00 AM -> Tate McRae
1:00 AM -> Tate McRae
2:00 AM -> Tate McRae
3:00 AM -> Tate McRae
4:00 AM -> Tate McRae
5:00 AM -> Tate McRae
6:00 AM -> Tate McRae
7:00 AM -> Tate McRae
8:00 AM -> Tate McRae
9:00 AM -> Tate McRae
10:00 AM -> Tate McRae
11:00 AM -> Tate McRae
12:00 PM -> Tate McRae
1:00 PM -> Tate McRae
2:00 PM -> Tate McRae
3:00 PM -> Tate McRae
4:00 PM -> Tate McRae
5:00 PM -> Radiohead
6:00 PM -> Tate McRae
7:00 PM -> Tate McRae
8:00 PM -> Tate McRae
9:00 PM -> Tate McRae
10:00 PM -> Tate McRae
11:00 PM -> Tate McRae


=== 2026 STATISTICS ===
=== Basic Statistics ===


=== Top Artists ===
1. The Neighbourhood - 330 streams
2. Lady Gaga - 265 streams
3. Tate McRae - 259 streams
4. Ariana Grande - 230 streams
5. One Direction - 225 streams
6. Maroon 5 - 205 streams
7. Calvin Harris - 201 streams
8. Justin Bieber - 186 streams
9. PinkPantheress - 183 streams
10. The Script - 182 streams
/Users/nadyafahrani/Desktop/SPOTIFY PERSONAL PROJ/main.py:109: UserWarning: The figure layout has changed to tight
  plt.tight_layout()


=== Top Tracks ===
1. Hall of Fame (feat. will.i.am) - 122 streams
2. All The Things She Said - 122 streams
3. Friday (feat. Mufasa & Hypeman) - Dopamine Re-Edit - 113 streams
4. Stateside + Zara Larsson - 93 streams
5. Dirty Little Secret - 78 streams
6. Outside (feat. Ellie Goulding) - 73 streams
7. Just The Way You Are - 67 streams
8. Kasih Tau Mama (Malam Minggu) - 65 streams
9. Colors - 60 streams
10. King - 57 streams


=== Number of Unique Artists ===
You have listened to 1639 unique artists.


=== Artists By Listening Time ===
1. The Neighbourhood - 562.46 minutes played
2. Lady Gaga - 550.62 minutes played
3. The Script - 356.54 minutes played
4. Maroon 5 - 342.95 minutes played
5. t.A.T.u. - 342.89 minutes played
6. One Direction - 336.87 minutes played
7. Calvin Harris - 336.31 minutes played
8. Tate McRae - 328.67 minutes played
9. Ariana Grande - 328.09 minutes played
10. Mac Miller - 295.15 minutes played


=== Listening By Hour ===
12:00 AM - 1315 streams
1:00 AM - 978 streams
2:00 AM - 1363 streams
3:00 AM - 1083 streams
4:00 AM - 1212 streams
5:00 AM - 994 streams
6:00 AM - 967 streams
7:00 AM - 954 streams
8:00 AM - 804 streams
9:00 AM - 933 streams
10:00 AM - 1101 streams
11:00 AM - 1084 streams
12:00 PM - 1142 streams
1:00 PM - 836 streams
2:00 PM - 791 streams
3:00 PM - 328 streams
4:00 PM - 177 streams
5:00 PM - 106 streams
6:00 PM - 24 streams
7:00 PM - 23 streams
8:00 PM - 12 streams
9:00 PM - 46 streams
10:00 PM - 210 streams
11:00 PM - 544 streams


=== Listening Day of the Week ===
Monday - 3015 streams
Tuesday - 2380 streams
Wednesday - 2497 streams
Thursday - 2823 streams
Friday - 1894 streams
Saturday - 1986 streams
Sunday - 2432 streams


=== Daily Listening Time ===
December 28, 2025 - 1 minute
January 01, 2026 - 178 minutes
January 02, 2026 - 40 minutes
January 03, 2026 - 141 minutes
January 04, 2026 - 17 minutes
January 05, 2026 - 182 minutes
January 06, 2026 - 78 minutes
January 07, 2026 - 144 minutes
January 08, 2026 - 158 minutes
January 09, 2026 - 147 minutes
January 10, 2026 - 33 minutes
January 11, 2026 - 225 minutes
January 12, 2026 - 163 minutes
January 13, 2026 - 180 minutes
January 14, 2026 - 187 minutes
January 15, 2026 - 208 minutes
January 16, 2026 - 5 minutes
January 17, 2026 - 93 minutes
January 18, 2026 - 436 minutes
January 19, 2026 - 209 minutes
January 20, 2026 - 233 minutes
January 21, 2026 - 9 minutes
January 22, 2026 - 128 minutes
January 23, 2026 - 244 minutes
January 24, 2026 - 128 minutes
January 25, 2026 - 120 minutes
January 26, 2026 - 27 minutes
January 27, 2026 - 188 minutes
January 28, 2026 - 102 minutes
January 29, 2026 - 353 minutes
January 30, 2026 - 61 minutes
January 31, 2026 - 39 minutes
February 01, 2026 - 43 minutes
February 02, 2026 - 10 minutes
February 03, 2026 - 161 minutes
February 04, 2026 - 39 minutes
February 05, 2026 - 71 minutes
February 06, 2026 - 2 minutes
February 08, 2026 - 64 minutes
February 09, 2026 - 177 minutes
February 10, 2026 - 162 minutes
February 11, 2026 - 176 minutes
February 12, 2026 - 11 minutes
February 13, 2026 - 64 minutes
February 14, 2026 - 84 minutes
February 15, 2026 - 192 minutes
February 16, 2026 - 177 minutes
February 17, 2026 - 161 minutes
February 18, 2026 - 1 minute
February 19, 2026 - 23 minutes
February 20, 2026 - 0 minutes
February 21, 2026 - 96 minutes
February 22, 2026 - 20 minutes
February 23, 2026 - 148 minutes
February 24, 2026 - 52 minutes
February 25, 2026 - 159 minutes
February 26, 2026 - 116 minutes
February 27, 2026 - 49 minutes
February 28, 2026 - 39 minutes
March 01, 2026 - 107 minutes
March 02, 2026 - 110 minutes
March 03, 2026 - 131 minutes
March 04, 2026 - 120 minutes
March 05, 2026 - 107 minutes
March 06, 2026 - 184 minutes
March 07, 2026 - 39 minutes
March 08, 2026 - 57 minutes
March 09, 2026 - 137 minutes
March 10, 2026 - 188 minutes
March 11, 2026 - 50 minutes
March 12, 2026 - 198 minutes
March 13, 2026 - 150 minutes
March 14, 2026 - 153 minutes
March 15, 2026 - 141 minutes
March 16, 2026 - 204 minutes
March 17, 2026 - 107 minutes
March 18, 2026 - 27 minutes
March 19, 2026 - 40 minutes
March 20, 2026 - 60 minutes
March 21, 2026 - 17 minutes
March 22, 2026 - 126 minutes
March 23, 2026 - 98 minutes
March 24, 2026 - 246 minutes
March 25, 2026 - 67 minutes
March 26, 2026 - 147 minutes
March 27, 2026 - 54 minutes
March 28, 2026 - 195 minutes
March 29, 2026 - 69 minutes
March 30, 2026 - 221 minutes
March 31, 2026 - 13 minutes
April 01, 2026 - 109 minutes
April 02, 2026 - 0 minutes
April 03, 2026 - 45 minutes
April 04, 2026 - 100 minutes
April 05, 2026 - 12 minutes
April 06, 2026 - 114 minutes
April 07, 2026 - 100 minutes
April 08, 2026 - 41 minutes
April 09, 2026 - 146 minutes
April 10, 2026 - 44 minutes
April 11, 2026 - 100 minutes
April 12, 2026 - 87 minutes
April 13, 2026 - 54 minutes
April 14, 2026 - 83 minutes
April 15, 2026 - 69 minutes
April 16, 2026 - 115 minutes
April 17, 2026 - 126 minutes
April 18, 2026 - 56 minutes
April 19, 2026 - 116 minutes
April 20, 2026 - 271 minutes
April 21, 2026 - 11 minutes
April 22, 2026 - 166 minutes
April 23, 2026 - 196 minutes
April 24, 2026 - 182 minutes
April 25, 2026 - 217 minutes
April 26, 2026 - 165 minutes
April 27, 2026 - 171 minutes
April 28, 2026 - 29 minutes
April 29, 2026 - 178 minutes
April 30, 2026 - 125 minutes
May 01, 2026 - 190 minutes
May 02, 2026 - 100 minutes
May 03, 2026 - 66 minutes
May 04, 2026 - 61 minutes
May 05, 2026 - 213 minutes
May 06, 2026 - 153 minutes
May 07, 2026 - 70 minutes
May 08, 2026 - 221 minutes
May 09, 2026 - 173 minutes
May 10, 2026 - 41 minutes
May 11, 2026 - 141 minutes
May 12, 2026 - 85 minutes
May 13, 2026 - 163 minutes
May 14, 2026 - 182 minutes
May 15, 2026 - 110 minutes
May 16, 2026 - 24 minutes
May 17, 2026 - 233 minutes
May 18, 2026 - 178 minutes
May 19, 2026 - 92 minutes
May 20, 2026 - 81 minutes
May 21, 2026 - 125 minutes
May 22, 2026 - 105 minutes
May 23, 2026 - 43 minutes
May 24, 2026 - 109 minutes
May 25, 2026 - 204 minutes
May 26, 2026 - 116 minutes
May 27, 2026 - 120 minutes
May 28, 2026 - 62 minutes
May 29, 2026 - 124 minutes
May 30, 2026 - 155 minutes
May 31, 2026 - 56 minutes
June 01, 2026 - 77 minutes
June 02, 2026 - 73 minutes
June 03, 2026 - 164 minutes
June 04, 2026 - 4 minutes
June 05, 2026 - 128 minutes
June 06, 2026 - 43 minutes
June 07, 2026 - 12 minutes
June 08, 2026 - 70 minutes
June 09, 2026 - 113 minutes
June 10, 2026 - 63 minutes
June 11, 2026 - 34 minutes
June 12, 2026 - 35 minutes
June 14, 2026 - 73 minutes
June 15, 2026 - 12 minutes
June 16, 2026 - 127 minutes
June 17, 2026 - 27 minutes
June 18, 2026 - 168 minutes
June 19, 2026 - 170 minutes
June 20, 2026 - 1 minute
June 21, 2026 - 61 minutes
June 22, 2026 - 149 minutes
June 23, 2026 - 104 minutes
June 24, 2026 - 107 minutes
June 25, 2026 - 18 minutes
June 26, 2026 - 54 minutes
June 27, 2026 - 142 minutes
June 28, 2026 - 43 minutes
June 29, 2026 - 75 minutes
June 30, 2026 - 86 minutes
July 02, 2026 - 107 minutes
July 03, 2026 - 65 minutes
July 04, 2026 - 179 minutes
July 05, 2026 - 38 minutes
July 06, 2026 - 76 minutes
July 07, 2026 - 86 minutes
July 08, 2026 - 33 minutes
July 09, 2026 - 192 minutes
July 10, 2026 - 105 minutes
July 11, 2026 - 10 minutes
July 12, 2026 - 118 minutes
July 13, 2026 - 25 minutes
July 14, 2026 - 98 minutes
July 15, 2026 - 132 minutes
July 16, 2026 - 54 minutes
July 17, 2026 - 139 minutes
July 18, 2026 - 35 minutes
July 19, 2026 - 44 minutes
July 20, 2026 - 98 minutes
July 21, 2026 - 28 minutes
July 22, 2026 - 263 minutes
July 23, 2026 - 209 minutes
July 24, 2026 - 1 minute
July 25, 2026 - 107 minutes
July 26, 2026 - 178 minutes
July 27, 2026 - 102 minutes
July 28, 2026 - 88 minutes
July 29, 2026 - 87 minutes
July 30, 2026 - 109 minutes
July 31, 2026 - 49 minutes
August 01, 2026 - 89 minutes
August 02, 2026 - 73 minutes
August 03, 2026 - 6 minutes
August 04, 2026 - 50 minutes
August 05, 2026 - 75 minutes
August 06, 2026 - 145 minutes
August 07, 2026 - 70 minutes
August 08, 2026 - 105 minutes
August 09, 2026 - 107 minutes
August 10, 2026 - 8 minutes
August 11, 2026 - 36 minutes
August 12, 2026 - 62 minutes
August 13, 2026 - 92 minutes
August 14, 2026 - 178 minutes
August 15, 2026 - 107 minutes
August 16, 2026 - 153 minutes
August 17, 2026 - 211 minutes
August 18, 2026 - 193 minutes
August 19, 2026 - 141 minutes
August 20, 2026 - 92 minutes


=== Artist by Hour ===
12:00 AM -> The Neighbourhood
1:00 AM -> Tate McRae
2:00 AM -> The Neighbourhood
3:00 AM -> The Neighbourhood
4:00 AM -> Tate McRae
5:00 AM -> The Neighbourhood
6:00 AM -> The Neighbourhood
7:00 AM -> The Neighbourhood
8:00 AM -> Lady Gaga
9:00 AM -> The Neighbourhood
10:00 AM -> Lady Gaga
11:00 AM -> Ariana Grande
12:00 PM -> PinkPantheress
1:00 PM -> The Neighbourhood
2:00 PM -> Tate McRae
3:00 PM -> Bread
4:00 PM -> Mac Miller
5:00 PM -> Bryan Adams
6:00 PM -> Bread
7:00 PM -> Starship
8:00 PM -> Bryan Adams
9:00 PM -> NewJeans
10:00 PM -> t.A.T.u.
11:00 PM -> One Direction