IoT Tea Tracker - Server Setup Guide

This README documents how to set up a secure server on AWS Lightsail for running a Flask-based IoT tea tracker, hosted at a custom subdomain (iot.eedude.com) with SSL and Apache reverse proxying.

🛠 Prerequisites

AWS Lightsail Ubuntu instance with a static IP

Domain name (e.g. eedude.com) configured to point to the server

Bitnami stack (WordPress or LAMP) installed

SSH access to the server

🌐 Create DNS Record

Log into your domain registrar

Add an A record for iot.eedude.com pointing to your Lightsail server's public IP

⚙️ Set Up Flask App

sudo apt update
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install flask

tea_tracker.py

from flask import Flask, jsonify, render_template, request
import os, json

app = Flask(__name__)
DATA_FILE = 'tea_count.json'

def load_count():
    if not os.path.exists(DATA_FILE):
        return 0
    with open(DATA_FILE, 'r') as f:
        return json.load(f).get('count', 0)

def save_count(count):
    with open(DATA_FILE, 'w') as f:
        json.dump({'count': count}, f)

@app.route('/tea')
def increment_tea():
    count = load_count() + 1
    save_count(count)
    return jsonify(message="Cup of tea logged!", total_cups=count)

@app.route('/tea/status')
def get_status():
    count = load_count()
    return jsonify(total_cups=count)

@app.route('/')
def tea_button():
    return render_template('tea_button.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

Create templates/tea_button.html with a button (see repo example).

Run the app:

nohup python3 tea_tracker.py &

🔁 Apache Setup

Enable vhosts

Edit Apache config:

sudo nano /opt/bitnami/apache/conf/httpd.conf

Ensure this line is included:

Include conf/vhosts/*.conf

Create VHost for iot.eedude.com

sudo nano /opt/bitnami/apache/conf/vhosts/iot-eedude.conf

Paste:

<VirtualHost *:443>
  ServerName iot.eedude.com

  SSLEngine on
  SSLCertificateFile "/opt/bitnami/apache/conf/bitnami/certs/server.crt"
  SSLCertificateKeyFile "/opt/bitnami/apache/conf/bitnami/certs/server.key"

  ProxyPreserveHost On
  ProxyPass / http://127.0.0.1:5000/
  ProxyPassReverse / http://127.0.0.1:5000/

  ErrorLog "/opt/bitnami/apache/logs/iot_error.log"
  CustomLog "/opt/bitnami/apache/logs/iot_access.log" combined
</VirtualHost>

Restart Apache:

sudo /opt/bitnami/ctlscript.sh restart apache

🔒 Enable SSL for Subdomain

Run Let's Encrypt tool:

sudo /opt/bitnami/bncert-tool

Use these domains:

eedude.com iot.eedude.com

Agree to redirects and auto-renew.

If SSL doesn't take effect:

sudo ln -sf /opt/bitnami/letsencrypt/certificates/eedude.com.crt /opt/bitnami/apache/conf/bitnami/certs/server.crt
sudo ln -sf /opt/bitnami/letsencrypt/certificates/eedude.com.key /opt/bitnami/apache/conf/bitnami/certs/server.key
sudo /opt/bitnami/ctlscript.sh restart apache

Verify Certificate

echo | openssl s_client -connect localhost:443 -servername iot.eedude.com 2>/dev/null | openssl x509 -noout -text | grep DNS

Should show:

DNS:eedude.com, DNS:iot.eedude.com

📱 Android Button Shortcut

Visit: https://iot.eedude.com in Chrome

Tap ⋮ → Add to Home screen

Name it: Tea Button ☕

Tap it anytime to increment your tea log!

✅ Success

You now have:

HTTPS-enabled Flask app on iot.eedude.com

Apache proxy with SSL

Mobile-friendly tea logging endpoint

Next ideas:

Add /reset or timestamp logs

Store per-day stats

Build a tea dashboard with charts

Enjoy your tea-tracking server! 🍵
