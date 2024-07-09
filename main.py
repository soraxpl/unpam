from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

# List of URLs to check
urls = [
    {"name": "E-Learning Server 1", "url": "https://e-learning.unpam.id/"},
    {"name": "E-Learning Server 2", "url": "https://e-learning.unpam.ac.id/"},
    {"name": "My Unpam", "url": "https://my.unpam.ac.id/"},
    {"name": "Presensi Unpam", "url": "https://my.unpam.ac.id/presensi/"},
    {"name": "Website Unpam", "url": "https://unpam.ac.id/"}
]

@app.route('/unpam')
def index():
    return render_template('unpam.html', urls=urls)

@app.route('/check_status', methods=['POST'])
def check_status():
    url = request.json['url']
    
    # Add http/https if missing
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    try:
        response = requests.get(url, timeout=30, verify=False, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
        if response.status_code == 200:
            status = "200 OK"
        elif 400 <= response.status_code < 500:
            status = f"{response.status_code} Client Error"
        elif 500 <= response.status_code < 600:
            status = f"{response.status_code} Server Error"
        else:
            status = f"{response.status_code} Error"
    except requests.RequestException as e:
        status = str(e)
    return jsonify({"url": url, "status": status})

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0')
    # app.run()
