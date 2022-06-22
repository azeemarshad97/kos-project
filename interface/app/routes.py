from flask import render_template, request, url_for, redirect, make_response
from app import app
import app.queries as qr
import app.network as nw
import app.Query_with_result_in_Dataframe as qr2




@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    The function index() returns the rendered template index.html with the title 'Home'
    :return: The index.html file is being returned.
    """
    return render_template('index.html',title='Home')


@app.route('/submit', methods=['POST','GET'])
def submit():
    """
    The function takes the query from the user, passes it to the query_results.py file, and returns the
    results to the index.html file
    """
    query = request.form.get("input-query")
    print(f'query: {query}')    

    res_df = qr2.getResults(query)
    # res_df = qr.getResults(query)

    #* for graph ----> return res_df 
    return render_template('index.html',table=res_df)




@app.route('/network',methods=['GET', 'POST'])
def network():
    """
    It returns a response object that renders the network.html template, and sets the response headers
    to prevent caching
    :return: The response is being returned.
    """
    response = make_response(render_template('network.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store,must-revalidate'
    response.headers['Pragma'] = 'no-cache'

    return response


