# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the Random Forest Classifier model
filename = 'first-innings-score-lr-model1.pkl'
regressor = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

# Function to encode team names
def encode_team(team_name):
    teams = ['Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab', 'Kolkata Knight Riders',
             'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad']
    return [1 if team_name == team else 0 for team in teams]

# Function to encode stadium names
def encode_venue(venue_name):
    venues = ['venue_Barabati Stadium', 'venue_Brabourne Stadium', 'venue_Buffalo Park', 'venue_De Beers Diamond Oval',
              'venue_Dr DY Patil Sports Academy', 'venue_Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
              'venue_Dr Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium', 'venue_Dubai International Cricket Stadium',
              'venue_Eden Gardens', 'venue_Feroz Shah Kotla', 'venue_Himachal Pradesh Cricket Association Stadium',
              'venue_Holkar Cricket Stadium', 'venue_JSCA International Stadium Complex', 'venue_Kingsmead',
              'venue_M Chinnaswamy Stadium', 'venue_MA Chidambaram Stadium, Chepauk', 'venue_Maharashtra Cricket Association Stadium',
              'venue_New Wanderers Stadium', 'venue_Newlands', 'venue_OUTsurance Oval', 'venue_Punjab Cricket Association IS Bindra Stadium, Mohali',
              'venue_Punjab Cricket Association Stadium, Mohali', 'venue_Sardar Patel Stadium, Motera', 'venue_Sawai Mansingh Stadium',
              'venue_Shaheed Veer Narayan Singh International Stadium', 'venue_Sharjah Cricket Stadium', 'venue_Sheikh Zayed Stadium',
              "venue_St George's Park", 'venue_Subrata Roy Sahara Stadium', 'venue_SuperSport Park', 'venue_Wankhede Stadium']
    return [1 if venue_name == venue else 0 for venue in venues]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_features = []

    if request.method == 'POST':
        batting_team = request.form['batting-team']
        input_features.extend(encode_team(batting_team))

        bowling_team = request.form['bowling-team']
        input_features.extend(encode_team(bowling_team))

        venue = request.form['venue']
        input_features.extend(encode_venue(venue))

        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])

        input_features.extend([overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5])

        data = np.array([input_features])
        prediction = int(regressor.predict(data)[0])

        # Adjust the predicted score range based on your requirements
        lower_limit = max(0, prediction - 10)
        upper_limit = prediction + 5

        return render_template('result.html', lower_limit=lower_limit, upper_limit=upper_limit)

if __name__ == '__main__':
    app.run(debug=True)