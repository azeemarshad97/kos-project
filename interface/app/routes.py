from flask import render_template, request, url_for, redirect, make_response
from app import app
import app.queries as qr
import app.network as nw
import app.Query_with_result_in_Dataframe as qr2




@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    return render_template('index.html',title='Home')


@app.route('/submit', methods=['POST','GET'])
def submit():
    query = request.form.get("input-query")
    print(f'query: {query}')    

    res_df = qr2.getResults(query)
    # res_df = qr.getResults(query)

    #* for graph ----> return res_df 
    return render_template('index.html',table=res_df)




@app.route('/network',methods=['GET', 'POST'])
def network():
    response = make_response(render_template('network.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store,must-revalidate'
    response.headers['Pragma'] = 'no-cache'

    return response


