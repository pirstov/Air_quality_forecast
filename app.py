from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, send_file
import base64
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

@app.route('/get-forecast-plots')
def get_forecast_plots():
    variable = request.args.get('variable')
    prefix = f'pm_plots/{variable}_'

    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    contents = response.get('Contents', [])

    if not contents:
        return jsonify({'error': 'No images found for the given variable'}), 404

    images = []
    for obj in contents:
        key = obj['Key']
        
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': key},
            ExpiresIn=3600  # valid for 1 hour
        )
        
        images.append({
            'key': key,
            'url': url
        })

    return jsonify(images)

@app.route('/get-aerosol-plots')
def get_aerosol_plots():
    variable = request.args.get('variable')
    prefix = f'aerosol_plots/{variable}_'

    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    contents = response.get('Contents', [])

    if not contents:
        return jsonify({'error': 'No images found for the given variable'}), 404

    images = []
    for obj in contents:
        key = obj['Key']
        
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': key},
            ExpiresIn=3600  # valid for 1 hour
        )
        
        images.append({
            'key': key,
            'url': url
        })

    return jsonify(images)

@app.route('/get-meteo-plots')
def get_meteo_plots():
    prefix = f'pressure_plots/air_press_'
    f_pattern = re.compile(r'^pressure_plots/air_press_\d{2}\.png$')

    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    contents = response.get('Contents', [])

    if not contents:
        return jsonify({'error': 'No images found'}), 404

    images = []
    for obj in contents:
        key = obj['Key']

        # Filter out files: there were some extra files
        if not f_pattern.match(key):
            continue

        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': key},
            ExpiresIn=3600  # valid for 1 hour
        )
        
        images.append({
            'key': key,
            'url': url
        })

    return jsonify(images)

def get_available_dates():
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='pm_plots')
    dates = set()

    for obj in response.get('Contents', []):
        key = obj['Key']
        match = filename_pattern_fcast.match(key)
        if match:
            dates.add(match.group(1))

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

