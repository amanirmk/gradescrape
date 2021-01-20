import requests
from flask_session import Session
from steal_page import steal_page
from adjust_page import adjust_page
from flask import Flask, request, render_template_string, session, redirect

app = Flask(__name__)
app.config["SECRET_KEY"] = "this is going on github anyways"
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
Session(app)

BASE = 'https://www.gradescope.com/'

@app.route("/")
def index():
    session.pop('s', None)
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    session['s'] = s
    soup, url, _, ok = steal_page(s, BASE+'login')
    if not ok:
        return redirect('/')
    page = adjust_page(soup, url, session['s'])
    return render_template_string(page)

@app.route('/<path:text>', methods=['GET', 'POST'])
def redirects(text):
    if request.method == 'POST':
        soup, url, json, ok = steal_page(session['s'], BASE+text, request.values)
    else:
        soup, url, json, ok = steal_page(session['s'], BASE+text)
    
    if not ok:
            return redirect('/')
    elif text == 'login':
            return redirect('/account')
    elif json:
        # also viewing the submitted files on programming assignments doesnt work
        # figure out how to handle gradescope json
        return redirect(url)

    page = adjust_page(soup, url, session['s'])
    return render_template_string(page)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)