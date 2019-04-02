from flask import Flask,render_template,request,redirect
from vsearch import search4letters

app = Flask(__name__)

@app.route('/index')
def hello() -> '302':
    return redirect('/entry')

@app.route('/search4',methods=['POST'])
def do_search()-> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    result = search4letters(phrase,letters)
    log_request(req=request,res=result)
    return render_template('results.html'
                ,page_title='Here are your results',results = result,
                phrase = phrase , letters = letters) 

@app.route('/')
@app.route('/entry')
def get_index()->'html':
    return render_template('index.html',page_title='Welcome to the search4letters on Web')

def log_request(req:'flask_request',res:str)-> None:
    with open('vsearch.log','a') as log:
        print('request:',req,'response:',res,file=log)

if __name__ == '__main__':
    app.run(debug=True)
