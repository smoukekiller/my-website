from flask import Flask, render_template, jsonify, url_for
from flask_talisman import Talisman
import config
from get_data import get_data
from compile_data import compile_data



app = Flask(__name__, template_folder="../templates", static_folder="../static")

csp = {
    'default-src': [
        "'self'"
    ],
    'script-src': [
        "'self'",
        'https://cdn.jsdelivr.net'
    ],
    'style-src': [
        "'self'",
        'https://cdn.jsdelivr.net'
    ],
}
# Talisman(app, content_security_policy=csp, force_https=True)
@app.route("/")
def home():
    return render_template("home.html", 
                           about_url=url_for('about'),
                           myroom_url = url_for('MyRoom'))
@app.route("/about")
def about():
    return render_template("about-me.html", 
                           home_url=url_for('home'),
                           myroom_url = url_for('MyRoom'))

@app.route("/MyRoom")
def MyRoom():
    temperature, humidity, last_updated = get_data()
    
    return render_template("MyRoom.html", temperature=temperature, humidity=humidity, last_updated=last_updated,
                           about_url=url_for('about'),
                           home_url=url_for('home'))


@app.route('/data')
def fetch_data():
    labels, temp, humid = compile_data()
    data = {"temperature": temp,
            "labels": labels,
            "humidity": humid
            }
    return jsonify(data)

if __name__ == "__main__":
   app.run(
    host='0.0.0.0',
    port=config.PORT
    # ssl_context=(config.PATH_TO_FULLCHAIN_PEM, config.PATH_TO_PRIVKEY_PEM)
)