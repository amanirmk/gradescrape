import lxml.html
import datetime as d
from bs4 import BeautifulSoup as bs

BASE = 'https://www.gradescope.com/'

def graded_and_due(hrefs, session):
    all_graded = []
    due_tuples = []

    for href in hrefs:
        page = session.get(BASE+href)
        due_tuples.append(due_soon(page))
        html = page.content
        soup = bs(html, "html.parser")
        
        assignments = soup.find('tbody').find_all('tr', {'role':'row'})
        graded = list(filter(lambda a: a.find('div',{'class':'submissionStatus--score'}) != None, assignments))
        title = soup.find('h1', {'class':'courseHeader--title'}).string
        for assignment in graded:
            assignment.find('span', {'class':'submissionTimeChart--releaseDate'}).string = title
        all_graded.extend(graded)
    
    all_graded.sort(key=(lambda a: lxml.html.fromstring(str(a)).xpath(r'//tr[@role="row"]//td[@class="hidden-column"][2]/text()')), reverse=True)
    all_graded = all_graded[:10]
    
    for assignment in all_graded:
        spans = assignment.find_all('span')
        for span in spans[1:]:
            span.decompose()
        hidden_tds = assignment.find_all('td', {'class':'hidden-column'})
        for td in hidden_tds:
            td.decompose()
    
    return all_graded, due_tuples

def due_soon(course_page):
    course_html = lxml.html.fromstring(course_page.text)

    due_stamps = course_html.xpath(r'//tr[@role="row"]//td[@class="hidden-column"][2]/text()')
    status_list = course_html.xpath(r'//div[starts-with(@class, "submissionStatus--")]/text()')

    due_objects = [d.datetime.strptime(due_stamp, '%Y-%m-%d %X %z').date() for due_stamp in due_stamps]

    today = d.date.today()
    due_soon = 0
    due_today = 0
    for status, due_object in list(zip(status_list, due_objects)):
        submitted = status != "No Submission"
        diff = due_object - today
        due_in_week = diff < d.timedelta(days = 7) and diff > d.timedelta(days = 0)
        due_now = diff < d.timedelta(days = 1) and diff > d.timedelta(days = 0)
        if not submitted:
            if due_in_week:
                due_soon += 1
            if due_now:
                due_today += 1

    return due_soon, due_today

def scrape_for_graphs(cid, session):
    page = session.get(BASE + '/courses/' + cid)
    html = page.content
    soup = bs(html, "html.parser")

    scores = []
    assignments = soup.find('tbody').find_all('tr', {'role':'row'})
    assignments.sort(key=(lambda a: lxml.html.fromstring(str(a)).xpath(r'//tr[@role="row"]//td[@class="hidden-column"][2]/text()')))
    for assignment in assignments:
        score_div = assignment.find('div',{'class':'submissionStatus--score'})
        if score_div:
            scores.append([float(num) for num in score_div.text.split('/')])
            
    return scores
