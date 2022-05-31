from flask import render_template, request, url_for, redirect, make_response
from app import app
import app.queries as qr
import app.network as nw




@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # we should get query string
        # process it here
        # return the html file 
        # query = request.form["input-query"]
        query = request.form.get("input-quer")

        qr.getResults(query)


        # return redirect(url_for("network"))
        return render_template("network.html")
    else:
        return render_template('index.html',title='Home')


@app.route('/submit', methods=['POST','GET'])
def submit():
    query = request.form.get("input-query")
    print(f'query: {query}')    

    res_html = qr.getResults(query)

    print(f'res_html: {res_html}')

    # return redirect(url_for("network"))
    return res_html




@app.route('/network',methods=['GET', 'POST'])
def network():
    response = make_response(render_template('network.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store,must-revalidate'
    response.headers['Pragma'] = 'no-cache'

    return response


