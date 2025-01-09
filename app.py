from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
import google.generativeai as genai  # Import Google Gemini AI
import requests
from dateutil import parser  # Import dateutil.parser to help parse dates
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MONGO_URI'] = 'Your_mongodb_connection_url'

mongo = PyMongo(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# API Configuration
GOOGLE_PLACES_API_KEY = "Your_place_api_key"
CUSTOM_SEARCH_API_KEY = "your_custom_search_api_key"
SEARCH_ENGINE_ID = "Your_search_engin_id"
OPENWEATHER_API_KEY = "Your_open_weather_api_key"  # Add your OpenWeather API key

# Gemini AI Configuration
genai.configure(api_key="Your_gemini_api_key")

# Weather keywords to trigger weather information retrieval
weather_keywords = ["weather", "forecast", "temperature", "rain", "humidity", "wind", "climate"]
future_keywords = ["tomorrow", "next", "future", "on", "for", "when"]  # Keywords indicating future queries

class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return None
    return User(user_id=str(user['_id']), username=user['username'])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=25)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = mongo.db.users.find_one({'email': form.email.data})
        if existing_user is None:
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            user_id = mongo.db.users.insert_one({
                'username': form.username.data,
                'email': form.email.data,
                'password': hashed_password
            }).inserted_id
            user = User(user_id=str(user_id), username=form.username.data)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Email already registered.')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'email': form.email.data})
        if user and check_password_hash(user['password'], form.password.data):
            user_obj = User(user_id=str(user['_id']), username=user['username'])
            login_user(user_obj)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Function to fetch place details from Google Places API
def get_place_details_from_api(place_name):
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={place_name}&inputtype=textquery&fields=name,formatted_address,rating,opening_hours,geometry&key={GOOGLE_PLACES_API_KEY}"
    response = requests.get(url)
    return response.json()

# Function to fetch search results from Google Custom Search API
def search_google_custom_api(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={CUSTOM_SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}"
    response = requests.get(url)
    return response.json()

# Function to fetch current weather details from OpenWeather API
def get_current_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return f"Current Weather: {weather_description.capitalize()}, Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s"
    else:
        return "Sorry, I couldn't retrieve the current weather details right now."

# Function to fetch weather forecast from OpenWeather API
def get_weather_forecast(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_info = []
        for entry in data['list']:
            date_time = entry['dt_txt']
            weather_description = entry['weather'][0]['description']
            temperature = entry['main']['temp']
            forecast_info.append(f"{date_time}: {weather_description.capitalize()}, Temperature: {temperature}°C")
        return "<br>".join(forecast_info)
    else:
        return "Sorry, I couldn't retrieve the weather forecast details right now."

@app.route('/start-chat', methods=['POST'])
@login_required
def start_chat():
    data = request.json
    place_name = data.get('place_name', 'India')
    session['place_name'] = place_name
    return jsonify({'status': 'success'})

@app.route('/chat')
@login_required
def chat():
    place_name = session.get('place_name', 'India')
    return render_template('chat.html', place_name=place_name)

@app.route('/ask-question', methods=['POST'])
@login_required
def ask_question():
    user_question = request.json.get('question', '')
    place_name = session.get('place_name', 'India')

    if user_question.strip() != "":
        # Fetch details about the place from Google Places API
        place_details = get_place_details_from_api(place_name)

        # Extract location coordinates if available
        if place_details.get('status') == 'OK' and place_details['candidates']:
            place_info = place_details['candidates'][0]
            lat = place_info['geometry']['location']['lat']
            lon = place_info['geometry']['location']['lng']
            place_address = place_info.get('formatted_address', 'Address not available')
            place_rating = place_info.get('rating', 'Rating not available')
            place_prompt = f"The place {place_name} is located at {place_address}. It has a rating of {place_rating}."
        else:
            lat, lon = None, None
            place_prompt = f"Information about {place_name} is limited. Here is what I know."

        # Check for weather-related keywords
        if any(keyword in user_question.lower() for keyword in weather_keywords):
            if lat and lon:  # Only fetch weather if coordinates are available
                if any(keyword in user_question.lower() for keyword in future_keywords):
                    # Attempt to extract future date from the question
                    try:
                        # Example: "What's the weather tomorrow?" or "What's the weather on 2024-11-01?"
                        if "tomorrow" in user_question.lower():
                            forecast_info = get_weather_forecast(lat, lon)  # Get the weather forecast
                            return jsonify({'response': f"Weather forecast for {place_name}: <br>{forecast_info}"})

                    except Exception as e:
                        return jsonify({'response': f"Couldn't determine the date: {str(e)}"})

                # If not a future request, get current weather
                weather_info = get_current_weather(lat, lon)
                return jsonify({'response': weather_info})

        # Search for more information about the place using Google Custom Search API
        search_query = f"{place_name} {user_question}"
        search_results = search_google_custom_api(search_query)

        # Prepare search results summary
        search_summary = ""
        if 'items' in search_results:
            for item in search_results['items']:
                search_summary += f"{item['title']}: {item['snippet']} <br>"

        response_text = place_prompt + search_summary
        return jsonify({'response': response_text})

    return jsonify({'response': "I didn't understand your question."})

if __name__ == '__main__':
    app.run(debug=True)
