import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

def extract(page):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
    url = f'https://www.jobstreet.com.ph/software-engineer-jobs?page={page}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    job_cards = soup.find_all('article', attrs={'data-card-type': 'JobCard'})
    jobs = []
    
    for job_card in job_cards:
        title = job_card.find('a', attrs={'data-automation': 'jobTitle'}).text.strip()
        company = job_card.find('a', attrs={'data-automation': 'jobCompany'}).text.strip()
        location = job_card.find('a', attrs={'data-automation': 'jobLocation'}).text.strip()
        salary = job_card.find('span', attrs={'data-automation': 'jobSalary'})
        salary_text = salary.text.strip() if salary else 'Salary not provided'
        
        job = {'title': title, 'company': company, 'location': location, 'salary': salary_text}
        jobs.append(job)
    
    return jobs

@app.route('/')
def index():
    soup = extract(0)
    jobs = transform(soup)
    return render_template('index.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
