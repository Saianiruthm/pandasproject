from datetime import datetime
from collections import Counter
import pandas as pd
import numpy as np

#Read csv file
df = pd.read_csv("data.csv")

#----Start of Data preprocessing----#

counts = df['title'].value_counts()
values = counts[counts > 1].index.tolist()
i = [5964,5965,5966]
df=df.drop(i)

temp = df.loc[df.loc[df['rating'] == '66 min' ].index.tolist(), 'rating']
df.loc[df.loc[df['rating'] == '66 min' ].index.tolist(), 'rating'] = df.loc[df.loc[df['rating'] == '66 min' ].index.tolist(), 'duration']
df.loc[df.loc[df['rating'] == '66 min' ].index.tolist(), 'duration'] = temp

temp = df.loc[df.loc[df['rating'] == '84 min' ].index.tolist(), 'rating']
df.loc[df.loc[df['rating'] == '84 min' ].index.tolist(), 'rating'] = df.loc[df.loc[df['rating'] == '84 min' ].index.tolist(), 'duration']
df.loc[df.loc[df['rating'] == '84 min' ].index.tolist(), 'duration'] = temp

temp = df.loc[df.loc[df['rating'] == '74 min' ].index.tolist(), 'rating']
df.loc[df.loc[df['rating'] == '74 min' ].index.tolist(), 'rating'] = df.loc[df.loc[df['rating'] == '74 min' ].index.tolist(), 'duration']
df.loc[df.loc[df['rating'] == '74 min' ].index.tolist(), 'duration'] = temp

df['duration'] = df['duration'].str.replace(' Seasons', '')

df['duration'] = df['duration'].str.replace(' Season', '')

df['duration'] = df['duration'].str.replace(' min', '')

df['duration'] = df['duration'].fillna('0')

df['duration'] = df['duration'].apply(int)

def fill_nan_based_on_datatype(column):
    if column.dtype == 'object':
        return column.fillna('Not available')
    elif column.dtype in ['int64', 'float64', 'int32', 'float32', 'bool']:
        return column.fillna(0)
    else:
        return column

df = df.apply(fill_nan_based_on_datatype)

df_movie = df.groupby('type').get_group('Movie')
df_tvshow = df.groupby('type').get_group('TV Show')

df_tvshow.rename(columns={'duration': 'No. of seasons'}, inplace=True)
df_movie.rename(columns={'duration': 'duration (in min)'}, inplace=True)

df_tvshow.reset_index(drop=True, inplace=True)
df_movie.reset_index(drop=True, inplace=True)

df_tvshow.index = df_tvshow.index + 1
df_movie.index = df_movie.index + 1
#----Start of TV show Data preprocessing----#

#adding column year_added
df_tvshow['date_added'] = df_tvshow[df_tvshow['date_added'] != 'Not available']['date_added'].str.replace(' D', 'D')
df_tvshow['date_added'] = df_tvshow[df_tvshow['date_added'] != 'Not available']['date_added'].str.replace(' J', 'J')
df_tvshow['date_added'] = df_tvshow[df_tvshow['date_added'] != 'Not available']['date_added'].str.replace(' F', 'F')
df_tvshow['date_added'] = df_tvshow[df_tvshow['date_added'] != 'Not available']['date_added'].str.replace(' M', 'M')
df_tvshow['date_added'] = df_tvshow[df_tvshow['date_added'] != 'Not available']['date_added'].str.replace(' A', 'A')
df_tvshow['date_added'] = df_tvshow[df_tvshow['date_added'] != 'Not available']['date_added'].str.replace(' S', 'S')
df_tvshow['date_added'] = df_tvshow[df_tvshow['date_added'] != 'Not available']['date_added'].str.replace(' O', 'O')
df_tvshow['date_added'] = df_tvshow[df_tvshow['date_added'] != 'Not available']['date_added'].str.replace(' N', 'N')

df_tvshow['date_added'] = pd.to_datetime(df_tvshow['date_added'], format='%B %d, %Y', errors='coerce')

# Filtering out rows where 'date_added' is 'Not available'
df_tvshow = df_tvshow[df_tvshow['date_added'].notnull()]

# Extracting the year from the 'date_added' column
df_tvshow['year_added'] = df_tvshow['date_added'].dt.year

#----End of TV show Data preprocessing----#

#----Start of Movie Data preprocessing----#

#adding column year_added
df_movie['date_added'] = df_movie[df_movie['date_added'] != 'Not available']['date_added'].str.replace(' D', 'D')
df_movie['date_added'] = df_movie[df_movie['date_added'] != 'Not available']['date_added'].str.replace(' J', 'J')
df_movie['date_added'] = df_movie[df_movie['date_added'] != 'Not available']['date_added'].str.replace(' F', 'F')
df_movie['date_added'] = df_movie[df_movie['date_added'] != 'Not available']['date_added'].str.replace(' M', 'M')
df_movie['date_added'] = df_movie[df_movie['date_added'] != 'Not available']['date_added'].str.replace(' A', 'A')
df_movie['date_added'] = df_movie[df_movie['date_added'] != 'Not available']['date_added'].str.replace(' S', 'S')
df_movie['date_added'] = df_movie[df_movie['date_added'] != 'Not available']['date_added'].str.replace(' O', 'O')
df_movie['date_added'] = df_movie[df_movie['date_added'] != 'Not available']['date_added'].str.replace(' N', 'N')

df_movie['date_added'] = pd.to_datetime(df_movie['date_added'], format='%B %d, %Y', errors='coerce')

# Filtering out rows where 'date_added' is 'Not available'
df_movie = df_movie[df_movie['date_added'].notnull()]

# Extracting the year from the 'date_added' column
df_movie['year_added'] = df_movie['date_added'].dt.year

#----End of Movie Data preprocessing----#

#----*********End of Data preprocessing*********----#

#----------------Analysis of TV shows--------#
print("#------------------------Analysis of TV shows-------------------------------#")
#Basic Information
print(f"Dataset Info:{df_tvshow.info()}")
df_tvshow.describe()

#Total no of TV shows
num_shows = len(df_tvshow)
print("Number of TV Shows:", num_shows)

#The number of TV shows in each country
tvshows_by_country = df_tvshow[df_tvshow['country'] != 'Not available'].groupby('country')['title'].count().sort_values(ascending=False)#.head()
print(f"\n1. The number of TV shows in each country is:\n{tvshows_by_country}")

#the top 10 TV shows by rating
top_rated_tvshows = df_tvshow.sort_values('rating', ascending=False).head(10)
print(f"\n2. The top 10 TV shows by rating are:\n{top_rated_tvshows[['title', 'rating']]}")

#the top 10 TV shows by number of seasons
top_seasons_tvshows = df_tvshow.sort_values('No. of seasons', ascending=False).head(10)
print(f"\n3. The top 10 TV shows by number of seasons are:\n{top_seasons_tvshows[['title', 'No. of seasons']]}")

#the number of TV shows released
tvshows_by_year = df_tvshow.groupby('release_year')['title'].count().sort_values(ascending=False)#.head()
print(f"\n4. The number of TV shows released each year is:\n{tvshows_by_year}")

#the most common directors for TV shows on Netflix
tvshows_by_director = df_tvshow[df_tvshow['director'] != 'Not available']['director'].str.split(', ', expand=True).stack().value_counts()
print(f"\n5. The most common directors for TV shows on Netflix are:\n{tvshows_by_director.head(10)}")

#the most common cast members for TV shows on Netflix
tvshows_by_cast = df_tvshow[df_tvshow['cast'] != 'Not available']['cast'].str.split(', ', expand=True).stack().value_counts()
print(f"\n6. The most common cast members for TV shows on Netflix are:\n{tvshows_by_cast.head(10)}")

#the most common ratings for TV shows on Netflix
tvshows_by_rating = df_tvshow[df_tvshow['rating'] != 'Not available']['rating'].value_counts()
print(f"\n7. The most common ratings for TV shows on Netflix are:\n{tvshows_by_rating}")

#the most common categories for TV shows on Netflix
tvshows_by_category = df_tvshow['listed_in'].str.split(', ', expand=True).stack().value_counts()
print(f"\n8. The most common categories for TV shows on Netflix are:\n{tvshows_by_category.head(10)}")

# the most common words used in the descriptions of TV shows on Netflix
common_stop_words = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now',
    'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn',
    'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn',
    'wasn', 'weren', 'won', 'wouldn','–','one','new','two','three','must','series'
]
all_descriptions = " ".join(df_tvshow['description'])
words = [word.lower() for word in all_descriptions.split() if word.lower() not in common_stop_words]
tvshows_words = Counter(words).most_common(10)
print(f"\n9. The most common words used in the descriptions of TV shows on Netflix are:\n{tvshows_words}")

#the number of TV shows added to Netflix each year
tvshows_by_year = df_tvshow.groupby('year_added')['title'].count().sort_values(ascending=False)#.head()
print(f"\n10. The number of TV shows added each year is:\n{tvshows_by_year}")

#TV shows added by date
added_by_date = df_tvshow['date_added'].value_counts().head(5)
print(f"\n11. Top 5 Dates with Most TV Shows Added:\n{added_by_date}")

#the most common languages for TV shows on Netflix
tvshows_by_language = df_tvshow['description'].str.extract('\((\w+) audio\)', expand=False).value_counts()
print(f"\n12. The most common languages for TV shows on Netflix are:\n{tvshows_by_language.head(10)}")

#Distribution of the number of seasons
seasons_distribution = df_tvshow['No. of seasons'].value_counts()
print(f"\n13. Distribution of Number of Seasons:\n{seasons_distribution}")

longest_show = df_tvshow[df_tvshow['No. of seasons'] == df_tvshow['No. of seasons'].max()]
shortest_show = df_tvshow[df_tvshow['No. of seasons'] == df_tvshow['No. of seasons'].min()]
print(f"\n14(i). Longest TV Show:\n{longest_show[['title', 'No. of seasons']]}")
print(f"\n14(ii). Shortest TV Show:\n{shortest_show[['title', 'No. of seasons']]}")

# TV shows with the longest descriptions
longest_descriptions = df_tvshow[df_tvshow['description'].apply(len) == df_tvshow['description'].str.len().max()]
print(f"\n15. TV Show(s) with Longest Descriptions:\n{longest_descriptions[['title', 'description']]}")

#TV shows with the most cast members
# Sorting the DataFrame by 'num_cast_members' in descending order and getting the top entries
df_tvshow['cast_list'] = df_tvshow['cast'].str.split(', ')
df_tvshow['num_cast_members'] = df_tvshow['cast_list'].apply(lambda x: len(x) if isinstance(x, list) else 0)
significant_cast_members = df_tvshow[df_tvshow['num_cast_members'] > 5]  # Adjust '5' as needed
significant_cast_members = significant_cast_members.sort_values('num_cast_members', ascending=False)

# Displaying the top TV shows with significant cast members
top_cast_members = significant_cast_members[['title', 'cast', 'num_cast_members']].head()  # Adjust '10' for the number of shows you want
print(f"\n16. Top TV Shows with Significant Cast Members:\n{top_cast_members}")

#TV shows released in the last 5 years
recent_shows = df_tvshow[df_tvshow['release_year'] >= df_tvshow['release_year'].max() - 5]
print(f"\n17. TV Shows Released in the Last 5 Years:\n{recent_shows[['title', 'release_year']]}")

#Average number of seasons released per year
avg_seasons_per_year = df_tvshow.groupby('release_year')['No. of seasons'].mean().astype(int)#.head()
print(f"\n18. Average Number of Seasons released per Year:\n{avg_seasons_per_year}")

# Calculating the average number of seasons added each year
average_seasons_per_year = df_tvshow.groupby('year_added')['No. of seasons'].mean().astype(int)
print(f"\n19. Average number of seasons added each year:\n{average_seasons_per_year}")

#----------------************End of Analysis of TV shows*******--------#

#----------------Analysis of Movies--------#
print("#------------------------Analysis of Movies-------------------------------#")

#Basic Information
print(f"Dataset Info:{df_movie.info()}")
df_movie.describe()

#Total no of  movies
num_movies = len(df_movie)
print("Number of  movies:", num_movies)

#The number of  movies in each country
movies_by_country = df_movie[df_movie['country'] != 'Not available'].groupby('country')['title'].count().sort_values(ascending=False)#.head()
print(f"\n1. The number of  movies in each country is:\n{movies_by_country}")

#the top 10  movies by rating
top_rated_movies = df_movie.sort_values('rating', ascending=False).head(10)
print(f"\n2. The top 10  movies by rating are:\n{top_rated_movies[['title', 'rating']]}")

#the top 10  movies by duration (in min)
top_seasons_movies = df_movie.sort_values('duration (in min)', ascending=False).head(10)
print(f"\n3. The top 10  movies by duration (in min) are:\n{top_seasons_movies[['title', 'duration (in min)']]}")

#the number of  movies released
movies_by_year = df_movie.groupby('release_year')['title'].count().sort_values(ascending=False)#.head()
print(f"\n4. The number of  movies released each year is:\n{movies_by_year}")

#the most common directors for  movies on Netflix
movies_by_director = df_movie[df_movie['director'] != 'Not available']['director'].str.split(', ', expand=True).stack().value_counts()
print(f"\n5. The most common directors for  movies on Netflix are:\n{movies_by_director.head(10)}")

#the most common cast members for  movies on Netflix
movies_by_cast = df_movie[df_movie['cast'] != 'Not available']['cast'].str.split(', ', expand=True).stack().value_counts()
print(f"\n6. The most common cast members for  movies on Netflix are:\n{movies_by_cast.head(10)}")

#the most common ratings for  movies on Netflix
movies_by_rating = df_movie[df_movie['rating'] != 'Not available']['rating'].value_counts()
print(f"\n7. The most common ratings for  movies on Netflix are:\n{movies_by_rating}")

#the most common categories for  movies on Netflix
movies_by_category = df_movie['listed_in'].str.split(', ', expand=True).stack().value_counts()
print(f"\n8. The most common categories for  movies on Netflix are:\n{movies_by_category.head(10)}")

# the most common words used in the descriptions of  movies on Netflix
common_stop_words = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now',
    'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn',
    'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn',
    'wasn', 'weren', 'won', 'wouldn','–','one','new','two','three','must','series'
]
all_descriptions = " ".join(df_movie['description'])
words = [word.lower() for word in all_descriptions.split() if word.lower() not in common_stop_words]
movies_words = Counter(words).most_common(10)
print(f"\n9. The most common words used in the descriptions of  movies on Netflix are:\n{movies_words}")

#the number of  movies added to Netflix each year
movies_by_year = df_movie.groupby('year_added')['title'].count().sort_values(ascending=False)#.head()
print(f"\n10. The number of  movies added each year is:\n{movies_by_year}")

# movies added by date
added_by_date = df_movie['date_added'].value_counts().head(5)
print(f"\n11. Top 5 Dates with Most  movies Added:\n{added_by_date}")

#the most common languages for  movies on Netflix
movies_by_language = df_movie['description'].str.extract('\((\w+) audio\)', expand=False).value_counts()
print(f"\n12. The most common languages for  movies on Netflix are:\n{movies_by_language.head(10)}")

#Distribution of the duration (in min)
seasons_distribution = df_movie['duration (in min)'].value_counts()
print(f"\n13. Distribution of duration (in min):\n{seasons_distribution}")

longest_show = df_movie[df_movie['duration (in min)'] == df_movie['duration (in min)'].max()]
shortest_show = df_movie[df_movie['duration (in min)'] == df_movie['duration (in min)'].min()]
print(f"\n14(i). Longest  Show:\n{longest_show[['title', 'duration (in min)']]}")
print(f"\n14(ii). Shortest  Show:\n{shortest_show[['title', 'duration (in min)']]}")

#  movies with the longest descriptions
longest_descriptions = df_movie[df_movie['description'].apply(len) == df_movie['description'].str.len().max()]
print(f"\n15.  Show(s) with Longest Descriptions:\n{longest_descriptions[['title', 'description']]}")

# movies with the most cast members
# Sorting the DataFrame by 'num_cast_members' in descending order and getting the top entries
df_movie['cast_list'] = df_movie['cast'].str.split(', ')
df_movie['num_cast_members'] = df_movie['cast_list'].apply(lambda x: len(x) if isinstance(x, list) else 0)
significant_cast_members = df_movie[df_movie['num_cast_members'] > 5]  # Adjust '5' as needed
significant_cast_members = significant_cast_members.sort_values('num_cast_members', ascending=False)

# Displaying the top  movies with significant cast members
top_cast_members = significant_cast_members[['title', 'cast', 'num_cast_members']].head()  # Adjust '10' for the number of movies you want
print(f"\n16. Top  movies with Significant Cast Members:\n{top_cast_members}")

# movies released in the last 5 years
recent_movies = df_movie[df_movie['release_year'] >= df_movie['release_year'].max() - 5]
print(f"\n17.  movies Released in the Last 5 Years:\n{recent_movies[['title', 'release_year']]}")

#Average duration (in min) released per year
avg_seasons_per_year = df_movie.groupby('release_year')['duration (in min)'].mean().astype(int)#.head()
print(f"\n18. Average duration (in min) released per Year:\n{avg_seasons_per_year}")

# Calculating the average duration (in min) added each year
average_seasons_per_year = df_movie.groupby('year_added')['duration (in min)'].mean().astype(int)
print(f"\n19. Average duration (in min) added each year:\n{average_seasons_per_year}")

#----------------End of analysis of Movies--------#
