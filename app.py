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
response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='pm_plots', MaxKeys=50)
print(response)

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

# Regex to match the pm plot data
filename_pattern = re.compile(r'.*_(\d{4}-\d{2}-\d{2})_\d{2}\.png')

#print(response)
