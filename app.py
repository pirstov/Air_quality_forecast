from dotenv import load_dotenv
load_dotenv()

from flask import Flask, send_from_directory, jsonify, send_file
import boto3
import os
import re

BUCKET_NAME = '2012160-mahti-SCRATCH'

s3 = boto3.client(
    's3',
    endpoint_url='https://a3s.fi',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Access the folder with prefix
#response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='pm_plots', MaxKeys=50)
# Regex to match the forecast plot data
filename_pattern_fcast = re.compile(r'.*_(\d{4}-\d{2}-\d{2})_\d{2}\.png')

#app = Flask(__name__, static_folder='static')
app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/index.html')
def air_quality():
    return app.send_static_file('index.html')

@app.route('/model_eval.html')
def model_eval():
    return app.send_static_file('model_eval.html')

@app.route('/general.html')
def general():
    return app.send_static_file('general.html')

def get_available_dates():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='pm_plots')
    dates = set()

    print(response)

    for obj in response.get('Contents', []):
        key = obj['Key']
        match = filename_pattern_fcast.match(key)
        if match:
            dates.add(match.group(1))  # YYYYMMDD

    sorted_dates = sorted(dates, reverse=True)
    return sorted_dates

@app.route('/available-dates')
def list_available_dates():
    try:
        return jsonify(get_available_dates())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Testing to fetch available dates:")
    print(get_available_dates())
    #app.run(debug=True)

