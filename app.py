from flask import Flask, app, render_template, redirect, request, jsonify, json, make_response

import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)


# Root URL
@app.route('/')
def single_converter():
    return render_template('index.html')

@app.route('/ageGroup', methods=['GET', 'POST'])
def age_group():
    if request.method == "GET":
        return render_template('ageGroup.html', chart_data=None, state=None)

    if request.method == 'POST':
        state = request.form['stateSelected']
        df_state = df[df['State'] == state]

        # Filter out the "0-100+" age group
        df_state = df_state[df_state['Age_group'] != '0-100+']

        age_group_data = df_state.groupby('Age_group')['Total'].sum()

        plt.figure(figsize=(8, 8))
        plt.pie(age_group_data, labels=age_group_data.index, autopct='%1.1f%%', startangle=140)
        plt.title(f'Suicide Data by Age Group in {state}')
        plt.axis('equal')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        chart_data = base64.b64encode(buffer.read()).decode('utf-8')

        plt.close()  # Close the plot to release resources

        return render_template('ageGroup.html', chart_data=chart_data, state=state)


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