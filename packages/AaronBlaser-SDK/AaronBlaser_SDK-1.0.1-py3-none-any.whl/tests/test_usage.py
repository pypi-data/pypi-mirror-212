from lordoftherings import LordOfTheRings
# Add your api token to test
api = LordOfTheRings('YOUR API TOKEN')

# Uncomment and run the uses you wish to test. Due to rate limits it is not recommended that you run all at the same time

# /movie
# all_movies = api.movies().get_all().fetch()

# /movie with filters
# match = api.movies().get_all().filter_by(name='Gandalf').fetch()  # match
# negate_match = api.movies().get_all().filter_by(name=('not', 'Frodo')).fetch()  # negate match
# include = api.movies().get_all().filter_by(name=['The Lord of the Rings Series', 'The Desolation of Smaug']).fetch()  # include
# exclude = api.movies().get_all().filter_by(name=[('not', 'The Lord of the Rings Series'), ('not', 'The Desolation of Smaug')]).fetch()  # exclude
# less_than = api.movies().get_all().filter_by(budgetInMillions=('<', 100)).fetch()  # less than
# greater_than = api.movies().get_all().filter_by(runtimeInMinutes=('>', 160)).fetch()  # greater than or equal to

# /movie with sorting
# sorted_movies = api.movies().get_all().sort_by("name:asc").fetch()

# /movie with sorting and filtering
# sorted_filtered = api.movies().get_all().sort_by("name:asc").filter_by().fetch()

# /movie with pagination
# paged_movies_1 = api.movies().get_all().limit(2).fetch()
# paged_movies_2 = api.movies().get_all().limit(3).page(2).fetch()
# paged_movies_3 = api.movies().get_all().limit(1).page(1).offset(1).fetch()

# /movie/5cd95395de30eff6ebccde56
# movie = api.movies("5cd95395de30eff6ebccde56").get()

# /movie/5cd95395de30eff6ebccde56/quote
# movie_quotes = api.movies("5cd95395de30eff6ebccde5b").quotes.get_all().fetch()

# /movie/5cd95395de30eff6ebccde56/quote with sorting
# movie_quotes_sorted = api.movies("5cd95395de30eff6ebccde5b").quotes.get_all().sort_by("dialog:asc").fetch()

# /quote
# quotes = api.quotes().get_all().fetch()

# /quote with sorting
# sorted_quotes = api.quotes().get_all().sort_by('dialog:desc').fetch()

# /quote/5cd96e05de30eff6ebccebc9
# single_quote = api.quotes("5cd96e05de30eff6ebccebc9").get()
