from flask import Flask, send_from_directory, jsonify, send_file
import boto3
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')
