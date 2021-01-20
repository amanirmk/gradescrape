from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

def steal_page(session, url, data=None):
    if data:
        page = session.post(url, data=data)
    else:
        page = session.get(url)

    html = page.content

    try:
        json = page.json()
    except:
        json = None

    soup = bs(html, "html.parser")

    for script in soup.find_all('script'):
        src = script.attrs.get('src')
        if src:
            script['src'] = urljoin(url, src)
    
    for css in soup.find_all('link'):
        href = css.attrs.get('href')
        if href:
            css['href'] = urljoin(url, href)
    
    for img in soup.find_all('img'):
        src = img.attrs.get('src')
        data_src = img.attrs.get('data-src')
        if src:
            img['src'] = urljoin(url, src)
        elif data_src:
            img['data-src'] = urljoin(url, data_src)
    
    for vid in soup.find_all('vid'):
        src = vid.attrs.get('src')
        data_src = vid.attrs.get('data-src')
        if src:
            vid['src'] = urljoin(url, src)
        elif data_src:
            vid['data-src'] = urljoin(url, data_src)

    return soup, page.url, json, page.ok