from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3
from flask import Flask, jsonify


app = Flask(__name__)
DATA_FILE = 'rankings.db'
    
def page_scraper():
    driver = webdriver.Chrome()
    url = 'https://www.atptour.com/en/rankings/singles?rankRange=0-5000&region=all'
    driver.get(url)
    driver.implicitly_wait(0.5)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    table_data = soup.find_all('tbody')[1]

    rank_list = [elem.get_text() for elem in table_data.find_all(class_='rank bold heavy tiny-cell')]
    name_list = [elem.get_text().strip() for elem in table_data.find_all(class_='name')]
    age_list = [elem.get_text() for elem in table_data.find_all(class_='age')]
    points_list = [elem.get_text().strip() for elem in table_data.find_all(class_='points center bold extrabold small-cell')]
    country_list = [elem['href'][-3:].upper() for elem in table_data.find_all('use')]
    
    ranking_data = []
    for i in range(len(rank_list)):
        ranking_data.append((rank_list[i], name_list[i], age_list[i], points_list[i], country_list[i]))
        
    return ranking_data

def init_db():
    conn = sqlite3.connect(DATA_FILE)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS rankings')
    cur.execute('''
        CREATE TABLE rankings (
            rank INT,
            name TEXT,
            age INT,
            points INT,
            country TEXT        
        )
    ''')

    ranking_data = page_scraper()
    cur.executemany('''
        INSERT INTO rankings (rank, name, age, points, country)
        VALUES (?, ?, ?, ?, ?)
    ''', ranking_data)
    conn.commit()
    conn.close()

@app.route('/get_data')
def get_data():
    conn = sqlite3.connect(DATA_FILE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM rankings')
    rows = cur.fetchall()
    conn.close()
    data = [
        {
            'rank': row[0],
            'name': row[1],
            'age': row[2],
            'points': row[3],
            'country': row[4]
        }
        for row in rows
    ]
    
    return jsonify(data)


if __name__ == '__main__':
    page_scraper()
    init_db()
    app.run()
