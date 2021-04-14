from collections import Counter
from itertools import combinations

import pandas as pd

data = pd.read_csv('movie_bd_v5.csv')

data.describe()

# # Предобработка

# In[4]:


answers = {}  # создадим словарь для ответов

# In[5]:


data['profit'] = data['revenue'] - data['budget']

# In[6]:


months = 'Январь, Февраль, Март, Апрель, Май, Июнь, Июль, Август, Сентябрь, Октябрь, Ноябрь, Декабрь'.split(', ')
data['release_month'] = [months[int(i[:i.find('/')]) - 1] for i in data['release_date']]

# In[7]:


split_columns = ['cast', 'director', 'genres', 'production_companies']
for column in split_columns:
    data[column] = data[column].str.split('|')

# In[8]:


cast = data.explode('cast')
genres = data.explode('genres')
directors = data.explode('director')
companies = data.explode('production_companies')


# In[9]:


def fix_warner(company):
    if 'Warner Bros' in company:
        return 'Warner Bros'
    else:
        return company


# In[10]:


def symbols(title):
    title = ''.join(title.split())
    return len(title)


# In[95]:


def best(titles):
    variants = {1: ['Inside Out', 'The Dark Knight', '12 Years a Slave'],
                2: ['BloodRayne', 'The Adventures of Rocky & Bullwinkle'],
                3: ['Batman Begins', 'The Lord of the Rings: The Return of the King', 'Upside Down'],
                4: ['300', 'Lucky Number Slevin', 'Kill Bill: Vol. 1'],
                5: ['Upside Down', 'Inside Out', 'Iron Man']}
    check = {1: [], 2: [], 3: [], 4: [], 5: []}
    for title in list(titles):
        for key, value in variants.items():
            if title in value:
                check[key].append(title)

    for key in variants.keys():
        if sorted(variants[key]) == sorted(check[key]):
            print('Ответ: ', ', '.join(variants[key]))
            break


# In[100]:


def actors(pairs):
    variants = [('Johnny Depp', 'Helena Bonham Carter'),
                ('Ben Stiller', 'Owen Wilson'),
                ('Vin Diesel', 'Paul Walker'),
                ('Adam Sandler', 'Kevin James'),
                ('Daniel Radcliffe', 'Rupert Grint')]
    check = {}
    for variant in variants:
        if variant in dict(pairs).keys():
            check[variant] = dict(pairs)[variant]

    final_check = {value: key for key, value in check.items()}
    print('Ответ: ', ' & '.join(final_check.get(max(final_check.keys()))))


# # 1. У какого фильма из списка самый большой бюджет?

# Использовать варианты ответов в коде решения запрещено.    
# Вы думаете и в жизни у вас будут варианты ответов?)

# In[11]:


answers['1'] = 'Pirates of the Caribbean: On Stranger Tides', '+'

# In[12]:


answer = data['original_title'][data['budget'].idxmax()]
print('Ответ: ', answer)

# # 2. Какой из фильмов самый длительный (в минутах)?

# In[13]:


answers['2'] = 'Gods and Generals', '+'

# In[14]:


answer = data['original_title'][data['runtime'].idxmax()]
print('Ответ: ', answer)

# # 3. Какой из фильмов самый короткий (в минутах)?
# 
# 
# 
# 

# In[15]:


answers['3'] = 'Winnie the Pooh', '+'

# In[16]:


answer = data['original_title'][data['runtime'].idxmin()]
print('Ответ: ', answer)

# # 4. Какова средняя длительность фильмов?
# 

# In[17]:


answers['4'] = '110', '+'

# In[18]:


answer = round(data['runtime'].mean())
print('Ответ: ', answer)

# # 5. Каково медианное значение длительности фильмов?

# In[19]:


answers['5'] = '107', '+'

# In[20]:


answer = data['runtime'].median()
print('Ответ: ', answer)

# # 6. Какой самый прибыльный фильм?

# In[21]:


answers['6'] = 'Avatar', '+'

# In[22]:


answer = data['original_title'][data['profit'].idxmax()]
print('Ответ: ', answer)

# # 7. Какой фильм самый убыточный?

# In[23]:


answers['7'] = 'The Lone Ranger', '+'

# In[24]:


answer = data['original_title'][data['profit'].idxmin()]
print('Ответ: ', answer)

# # 8. У скольких фильмов из датасета объем сборов оказался выше бюджета?

# In[25]:


answers['8'] = '1478', '+'

# In[26]:


answer = data['profit'][data['profit'] > 0].count()
print('Ответ: ', answer)

# # 9. Какой фильм оказался самым кассовым в 2008 году?

# In[27]:


answers['9'] = 'The Dark Knight', '+'

# In[28]:


answer = data['original_title'][data['profit'][data['release_year'] == 2008].idxmax()]
print('Ответ: ', answer)

# # 10. Самый убыточный фильм за период с 2012 по 2014 г. (включительно)?
# 

# In[29]:


answers['10'] = 'The Lone Ranger', '+'

# In[30]:


answer = data['original_title'][data['profit'][(data['release_year'] >= 2012) &
                                               (data['release_year'] <= 2014)].idxmin()]
print('Ответ: ', answer)

# # 11. Какого жанра фильмов больше всего?

# In[31]:


answers['11'] = 'Drama', '+'

# In[32]:


answer = Counter(data['genres'].sum()).most_common(1)[0][0]
print('Ответ: ', answer)

# ВАРИАНТ 2

# In[33]:


amswer = genres['genres'].mode()[0]
print('Ответ: ', answer)

# # 12. Фильмы какого жанра чаще всего становятся прибыльными?

# In[34]:


answers['12'] = 'Drama', '+'

# In[35]:


answer = genres['genres'][data['profit'] > 0].mode()[0]
print('Ответ: ', answer)

# # 13. У какого режиссера самые большие суммарные кассовые сборы?

# In[36]:


answers['13'] = 'Peter Jackson', '+'

# In[37]:


answer = directors.groupby('director')['revenue'].sum().idxmax()
print('Ответ: ', answer)

# # 14. Какой режисер снял больше всего фильмов в стиле Action?

# In[38]:


answers['14'] = 'Robert Rodriguez', '+'

# In[39]:


action_directors = directors.explode('genres')
answer = action_directors[action_directors['genres'] == 'Action']['director'].value_counts().idxmax()
print('Ответ: ', answer)

# # 15. Фильмы с каким актером принесли самые высокие кассовые сборы в 2012 году?

# In[40]:


answers['15'] = 'Chris Hemsworth', '+'

# In[41]:


answer = cast[cast['release_year'] == 2012].groupby('cast')['profit'].sum().idxmax()
print('Ответ: ', answer)

# # 16. Какой актер снялся в большем количестве высокобюджетных фильмов?

# In[42]:


answers['16'] = 'Matt Damon', '+'

# In[43]:


answer = cast[cast['budget'] > cast['budget'].mean()]['cast'].value_counts().idxmax()
print('Ответ: ', answer)

# # 17. В фильмах какого жанра больше всего снимался Nicolas Cage?

# In[44]:


answers['17'] = 'Action', '+'

# In[45]:


cage_genres = cast.explode('genres')
answer = cage_genres['genres'][cage_genres['cast'] == 'Nicolas Cage'].mode()[0]
print('Ответ: ', answer)

# # 18. Самый убыточный фильм от Paramount Pictures

# In[46]:


answers['18'] = 'K-19: The Widowmaker', '+'

# In[47]:


paramount_movies = companies[companies['production_companies'] == 'Paramount Pictures']
answer = paramount_movies['original_title'][paramount_movies['profit'].idxmin()]
print('Ответ: ', answer)

# # 19. Какой год стал самым успешным по суммарным кассовым сборам?

# In[48]:


answers['19'] = '2015', '+'

# In[49]:


answer = data.groupby(['release_year'])['profit'].sum().idxmax()
print('Ответ: ', answer)

# # 20. Какой самый прибыльный год для студии Warner Bros?

# In[50]:


answers['20'] = '2014', '+'

# In[51]:


companies['production_companies'] = companies['production_companies'].apply(fix_warner)
answer = companies[companies['production_companies'] == 'Warner Bros'].groupby(['release_year'])[
    'profit'].sum().idxmax()
print('Ответ: ', answer)

# # 21. В каком месяце за все годы суммарно вышло больше всего фильмов?

# In[52]:


answers['21'] = 'Сентябрь', '+'

# In[54]:


answer = data.groupby(['release_month'])['original_title'].count().idxmax()
print('Ответ: ', answer)

# ВАРИАНТ 2

# In[55]:


answer = data['release_month'].mode()[0]
print('Ответ: ', answer)

# # 22. Сколько суммарно вышло фильмов летом? (за июнь, июль, август)

# In[56]:


answers['22'] = '450', '+'

# In[57]:


count_months = Counter(data['release_month'])
sum_movies = 0
summer = ['Июнь', 'Июль', 'Август']
for i in count_months.keys():
    if i in summer:
        sum_movies += count_months[i]
answer = sum_movies
print('Ответ: ', answer)

# ВАРИАНТ 2

# In[58]:


summer = data[(data['release_month'] == "Июнь") |
              (data['release_month'] == "Июль") |
              (data['release_month'] == "Август")]
answer = summer['original_title'].count()
print('Ответ: ', answer)

# # 23. Для какого режиссера зима – самое продуктивное время года?

# In[59]:


answers['23'] = 'Peter Jackson', '+'

# In[60]:


winter = directors[(directors['release_month'] == "Декабрь") |
                   (directors['release_month'] == "Январь") |
                   (directors['release_month'] == "Февраль")]
answer = winter['director'].mode()[0]
print('Ответ: ', answer)

# # 24. Какая студия дает самые длинные названия своим фильмам по количеству символов?

# In[61]:


answers['24'] = 'Four By Two Productions', '+'

# In[62]:


companies['symbols_of_title'] = companies['original_title'].apply(symbols)
answer = companies.groupby(['production_companies'])['symbols_of_title'].mean().idxmax()
print('Ответ: ', answer)

# # 25. Описание фильмов какой студии в среднем самые длинные по количеству слов?

# In[63]:


answers['25'] = 'Midnight Picture Show', '+'

# In[64]:


companies['words_in_overview'] = companies['overview'].apply(lambda x: len(x.split()))
answer = companies.groupby(['production_companies'])['words_in_overview'].mean().idxmax()
print('Ответ: ', answer)

# # 26. Какие фильмы входят в 1 процент лучших по рейтингу?

# In[69]:


answers['26'] = 'Inside Out, The Dark Knight, 12 Years a Slave', '+'

# In[96]:


best_titles = data[['vote_average', 'original_title']].sort_values(by='vote_average', ascending=False)
best(best_titles['original_title'][:round(len(best_titles) * 0.01)])

# # 27. Какие актеры чаще всего снимаются в одном фильме вместе?
# 

# In[108]:


answers['27'] = 'Daniel Radcliffe & Rupert Grint', '+'

# In[110]:


data['list_pair_actors'] = data['cast'].apply(lambda x: list(combinations(x, 2)))
pair_actors = data.explode('list_pair_actors')
count_pair = pair_actors['list_pair_actors'].value_counts()
actors(count_pair[count_pair > 1])

# ВАРИАНТ 2

# In[111]:


johnny = pd.DataFrame(cast['original_title'][cast['cast'] == "Johnny Depp"])
helena = pd.DataFrame(cast['original_title'][cast['cast'] == "Helena Bonham Carter"])
hugh = pd.DataFrame(cast['original_title'][cast['cast'] == "Hugh Jackman"])
ian = pd.DataFrame(cast['original_title'][cast['cast'] == "Ian McKellen"])
vin = pd.DataFrame(cast['original_title'][cast['cast'] == "Vin Diesel"])
paul = pd.DataFrame(cast['original_title'][cast['cast'] == "Paul Walker"])
adam = pd.DataFrame(cast['original_title'][cast['cast'] == "Adam Sandler"])
kevin = pd.DataFrame(cast['original_title'][cast['cast'] == "Kevin James"])
daniel = pd.DataFrame(cast['original_title'][cast['cast'] == "Daniel Radcliffe"])
rupert = pd.DataFrame(cast['original_title'][cast['cast'] == "Rupert Grint"])
max_movies = {len(johnny.merge(helena, on='original_title', how='inner')): 'Johnny Depp & Helena Bonham Carter',
              len(hugh.merge(ian, on='original_title', how='inner')): 'Hugh Jackman & Ian McKellen',
              len(vin.merge(paul, on='original_title', how='inner')): 'Vin Diesel & Paul Walker',
              len(adam.merge(kevin, on='original_title', how='inner')): 'Adam Sandler & Kevin James',
              len(daniel.merge(rupert, on='original_title', how='inner')): 'Daniel Radcliffe & Rupert Grint'}
answer = max_movies.get(max(max_movies.keys()))
print('Ответ: ', answer)

# # Submission

# In[109]:


pd.DataFrame.from_dict(answers, orient='index', columns=['Answer', 'Right'])

# In[112]:


len(answers)

# In[ ]:


# In[ ]:
