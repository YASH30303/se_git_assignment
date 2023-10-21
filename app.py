from flask import Flask, app, render_template, redirect, request, jsonify, json, make_response
app = Flask(__name__)
import pandas as pd


# Root URL
@app.route('/')
def single_converter():
    return render_template('index.html')

# state rout 
@app.route('/state', methods=['GET','POST'])
def state():
    # handle GET request
    if request.method == "GET":
        df = pd.read_csv('SuicideData.csv')
        df1 = df 
        return render_template('stateWise.html')
        # handled post request
    elif request.method == 'POST':
        state = request.form['stateSelected']
        df = pd.read_csv('SuicideData.csv')
        df = df[df['State'] == state]
      
        totalS = df['Total'].tolist()
        Stype = df['Type'].tolist()
        maleD = sum(df[df['Gender'] == 'Male']['Total'])
        femalD = sum(df[df['Gender'] == 'Female']['Total'])
        # ppass data to template plot using plotly
        return render_template('stateWise.html',totalS=[maleD,femalD],maleD=maleD,femaleD=femalD, state = state)


# cause route
@app.route('/cause', methods=['GET', 'POST'])
def cause():
    # Handle GET request
    if request.method == "GET":
        return render_template('cause.html')

    # Handle POST request
    elif request.method == 'POST':
        state = request.form['stateSelected']
        df = pd.read_csv('SuicideData.csv')
        df = df[df['State'] == state]
        newdf = df[['Type', 'Total']]
        newdf = newdf.groupby('Type').sum()

        newTotal = newdf['Total'].tolist()
        types = newdf.index.tolist()

        return render_template('cause.html', totalS=newTotal, Stype=types, state=state)

  
if __name__ == '__main__':  
   app.run()