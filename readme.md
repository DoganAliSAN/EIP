
# Erdemin IMDB Projesi (EIP)

EIP (the program) fetches movie data from the IMDB website. First, it requires a text file from the user containing a list of movie categories. EIP then searches for movies in each category and checks if they have a rating of 7 stars or higher.

Next, EIP checks the trivia section for each movie to identify useful comments. The usefulness of a comment is determined by two factors: the number of people who liked the comment and the total number of reviews. If the total number of reviews is greater than 1000 and the ratio of likes to reviews is greater than 85%, the comment is considered useful and is fetched.

For example, if a comment has 1500 total reviews and 1305 likes, the ratio of likes to reviews would be calculated as follows:
1305 / 1500 * 100 = 87

If this ratio exceeds 85%, the comment is fetched and stored in a database. This database prevents EIP from fetching the same movie or comment twice.

V2
