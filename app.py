

from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download/update')
def download_update():
    
    return send_from_directory('static', 'download.zip', as_attachment=True)

@app.route('/download/script')
def download_script():

    return send_from_directory('', 'verify.py', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
