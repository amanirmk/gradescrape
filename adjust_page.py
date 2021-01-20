import help_scrape as hs
import graphing as g

BASE = 'https://www.gradescope.com/'
def adjust_page(soup, url, session):
    if 'gradescope' in url:
        fix_generic(soup)
        if 'login' in url:
            fix_login_page(soup)
        elif url == BASE + 'account':
            fix_account_page(soup, session)
        elif 'assignments' in url: # order matters here
            fix_assignment_page(soup, session, url[url.index('assignments')+12:url.index('submissions')-1])
        elif 'courses' in url:
            fix_course_page(soup, session, url[url.index('courses')+8:])
    page = str(soup)
    return page

def fix_generic(soup):
    # change page title
    if soup.title:
        soup.title.string = soup.title.text[:-10] + 'Gradescrape'
    # change other titles
    titles = soup.find_all('div', {'class':'logo--text'})
    for title in titles:
        title.string = "gradescrape"
    # fix links
    root_links = soup.find_all('a', {'href':'/'})
    for link in root_links:
        link['href'] = '/account'
    logout_links = soup.find_all('a', {'href':'/logout'})
    for link in logout_links:
        link['href'] = '/'

def fix_login_page(soup):
    #delete unwanted elements
    header = soup.find('a', {'class':'logo'})
    header.decompose()
    for span in soup.find_all('span'):
        classlist = span.attrs.get('class')
        if classlist and ('form--choice' in classlist or 'btnv7--textWithIcon' in classlist):
            span.decompose()
    for div in soup.find_all('div'):
        if div.attrs:
            classlist = div.attrs.get('class')
            if classlist and ('formDividerWithText' in classlist or 'btnContainerv7' in classlist):
                div.decompose()

def fix_account_page(soup, session):
    # change intro text
    intro = soup.find('div', {'class':'sidebar--introText'})
    if intro:
        intro_text = intro.p
        intro_text.string = intro_text.text.replace('Gradescope', 'Gradescrape')
    # add due notifications to course boxes
    current_section = soup.find('div', {'class':'courseList--coursesForTerm'})
    courseboxes = [box for box in current_section.find_all('a', {'class':'courseBox'})]
    hrefs = [box.attrs.get('href') for box in courseboxes]
    graded, due_tuples = hs.graded_and_due(hrefs, session)
    for i, box in enumerate(courseboxes):
        due_soon, due_today = due_tuples[i]
        if due_soon:
            due_notif_tag = soup.new_tag('div', attrs={"style" : "display: flex; flex-direction: row; margin-top: 20px; justify-content: space-between"})
            due_soon_tag = soup.new_tag("div", attrs={"style" : "color: darkred; font-size: 16px"})
            due_soon_tag.string = str(due_soon) + ' due this week'
            due_notif_tag.append(due_soon_tag)
            if due_today:
                due_today_tag = soup.new_tag("div", attrs={"style" : "color: red; font-size: 16px"})
                due_today_tag.string = str(due_today) + ' due within 24hrs' 
                due_notif_tag.insert(0, due_today_tag)
            box.insert(2, due_notif_tag)
    for course_section in soup.find_all('div', {'class':'courseList--coursesForTerm'})[1:]:
        course_section.decompose()
    for course_header in soup.find_all('h2', {'class':'pageSubheading'})[1:]:
        course_header.decompose()
    inactive = soup.find('div', {'class':'courseList--inactiveCourses'})
    if inactive:
        inactive.decompose()
    button = soup.find('button', {'class':'js-viewInactive'})
    if button:
        button.decompose()
    create_table(soup, graded)

def create_table(soup, graded):

    if not graded:
        return
        
    table = soup.new_tag('table', attrs={'class':'table dataTable no-footer', 'role':'grid'})
    theader = soup.new_tag('thead')
    header_row = soup.new_tag('tr', {'role':'row'})
    
    attributes = {'role':'columnheader', 'scope':'col', 'tabindex':'0', 'rowspan':'1', 'colspan':'1', 'style':'font-size: 18px;'}
    name = soup.new_tag('th', attrs=attributes)
    name.string = 'Recent Graded Assignments'
    score = soup.new_tag('th', attrs=attributes)
    score.string = 'Score'
    course = soup.new_tag('th', attrs=attributes)
    course.string = 'Course'

    header_row.append(name)
    header_row.append(score)
    header_row.append(course)

    tbody = soup.new_tag('tbody')
    for assignment in graded:
        tbody.append(assignment)

    theader.append(header_row)
    table.append(header_row)
    table.append(tbody)

    soup.find('div', {'class':'courseList'}).append(table)

def fix_course_page(soup, session, cid):
    scores = hs.scrape_for_graphs(cid, session)

    content = soup.find('div', {'class':'l-content'})
    div = soup.new_tag('div', attrs={'style':'display:flex; flex-direction:row; justify-content: space-between'})

    cum_pct, success = g.cum_pct(scores)
    if success:
        cum_pct_img = soup.new_tag('img', attrs={'src':'data:image/png;base64, {}'.format(cum_pct), 'style':'max-width: 50%; max-height: 350px; height: auto;'})
        div.append(cum_pct_img)

    pie_chart, success = g.pie_chart(scores)
    if success:
        pie_img = soup.new_tag('img', attrs={'src':'data:image/png;base64, {}'.format(pie_chart), 'style':'max-width: 50%; max-height: 350px; height: auto;'})
        div.append(pie_img)
    
    content.insert(1, div)

def fix_assignment_page(soup, session, aid):
    #no adjustments implemented yet
    pass

