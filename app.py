import os
import google.generativeai as genai
from google.cloud import secretmanager
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Create the Secret Manager client.
client = secretmanager.SecretManagerServiceClient()

# Build the resource name of the secret version.
name = "projects/396631018769/secrets/optics-app-gemini/versions/latest"

# Access the secret version.
response = client.access_secret_version(request={"name": name})

# Extract the payload.
secret_string = response.payload.data.decode("UTF-8")


genai.configure(api_key=secret_string)
model3 = genai.GenerativeModel('gemma-3-27b-it')
model2 = genai.GenerativeModel('gemini-3-pro-preview')
model1 = genai.GenerativeModel('gemini-2.5-flash-lite')
prompt = "Tell me a 2-3 sentence historical joke or fun fact about San Diego County. MAXIMUM 2 SENTENCES!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_news_one')
def get_news_one():
    try:
        response1 = model1.generate_content(prompt)
        return jsonify({'fact1': response1.text})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_news_two')
def get_news_two():
    try:
        response2 = model2.generate_content(prompt)
        return jsonify({'fact2': response2.text})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_news_three')
def get_news_three():
    try:
        response3 = model3.generate_content(prompt)
        return jsonify({'fact3': response3.text})
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
