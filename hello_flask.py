from flask import Flask, render_template, request, redirect, escape
from vsearch import search4letters
from use_database import UseDatabase

app = Flask(__name__)

app.config['dbconfig'] = {"host": "127.0.0.1",
                          "user": "cone021",
                          "password": "klisa021ns",
                          "database": "vsearchlogdb"}


@app.route('/index')
def hello() -> '302':
    return redirect('/entry')


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    result = search4letters(phrase, letters)
    log_request(req=request, res=str(result))
    return render_template('results.html', page_title='Here are your results', results=result,
                           phrase=phrase, letters=letters)


@app.route('/')
@app.route('/entry')
def get_index() -> 'html':
    return render_template('index.html',
                           page_title='Welcome to the search4letters on Web')


@app.route("/viewlog")
def view_the_log() -> 'html':

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select phrase,letters,browser,ip,ts,response from log"""
        cursor.execute(_SQL)
        data = cursor.fetchall()

    row_titles = ('Phrase', 'Letters', 'User Agent','Ip address', 'Timestamp','Response')
    return render_template('viewlog.html',
                           row_titles=row_titles, row_data=data)

# save user request to db


def log_request(req: 'flask_request', res: str) -> None:

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
            (phrase,letters,ip,browser,response)
             values(%s,%s,%s,%s,%s)
            """
        # execute statement
        cursor.execute(_SQL, (req.form['phrase'], req.form['letters'],
                              req.remote_addr, req.user_agent.browser, res,))


if __name__ == '__main__':
    app.run(debug=True)
