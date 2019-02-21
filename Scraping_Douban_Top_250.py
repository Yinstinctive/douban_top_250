import requests
from bs4 import BeautifulSoup
from time import sleep
from csv import DictWriter
base_url = r'https://movie.douban.com/top250'
records = []
for start in [x*25 for x in range(10)]:
    #Every single page
    url = base_url+f'?start={start}&filter='
    response = requests.get(url).text
    soup = BeautifulSoup(response,'html.parser')
    movies = soup.find(class_='grid_view').find_all('li')
    rank=1+start
    for movie in movies:
        #Every single movie on the page
        movie_link = movie.find(class_='info').find(class_='hd').find('a')['href']
        movie_dict = {'rank':rank, 'link':movie_link}
        records.append(movie_dict)
        rank += 1
#Use the scapped link to further scrape movie details
for record in records:
    rank = record.get('rank')
    print(f'Scarpping rank {rank} of 250')
    link = record.get('link')
    response = requests.get(link).text
    soup = BeautifulSoup(response,'html.parser')
    record['title'] = soup.find('h1').find('span').get_text()
    record['year'] = soup.find('h1').find(class_='year').get_text()[1:5]
    record['director'] = soup.find(id='info').find(class_='attrs').find('a').get_text()
    record['length'] = soup.find(id='info').find(property='v:runtime').get_text()[:-2]
    
    attrs = soup.find(id='info').find_all(class_='pl')
    for attr in attrs:
        if attr.get_text().startswith('制片国家'):
            record['country_region']=attr.nextSibling.strip()
        elif attr.get_text().startswith('语言'):
            record['language']=attr.nextSibling.strip()
    
    record['avg_rating'] = soup.find(class_='ll rating_num').get_text()
    record['num_of_ratings'] = soup.find(class_='rating_people').find('span').get_text()
    interests = soup.find(class_='subject-others-interests-ft').find_all('a')
    record['people_watched'] = interests[0].get_text()[:-3]
    record['people_wants_to_watch'] = interests[1].get_text()[:-3]
    record['num_comment'] = soup.find(id='comments-section').find('h2').find('a').get_text().split()[1]
    record['num_reviews'] = soup.find(class_='reviews mod movie-content').find('h2').find('a').get_text().split()[1]
    #Set scrapping interval in case of ip blocking
    sleep(5)
#Write the 250 movies into a csv file
with open('douban_top_250.csv','w', newline='', encoding='utf-8-sig') as file:
    headers = [key for key in records[0].keys()]
    csv_writer = DictWriter(file, fieldnames=headers)
    csv_writer.writeheader()
    for record in records:
        csv_writer.writerow(record)