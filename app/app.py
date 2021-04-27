import os
import requests

from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template
from flask import send_from_directory, request
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = Flask(__name__, static_url_path='/')
load_dotenv()
app.secret_key = os.environ["SECRET_KEY"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "false"      # !! True Only in development environment.

app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_CLIENT_ID"]  # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]              # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = f"{os.environ['HOST_DOMAIN']}/callback"
app.config["DISCORD_BOT_TOKEN"] = os.environ["DISCORD_BOT_TOKEN"]
app.config["DISCORD_GUILD_ID"] = os.environ["DISCORD_GUILD_ID"]
CAPTCHA_KEY = os.environ["CAPTCHA_KEY"]
SITE_KEY = os.environ["SITE_KEY"]

VERIFY_URL = "https://hcaptcha.com/siteverify"

discord = DiscordOAuth2Session(app)

@app.route('/')
def index():
    return render_template('index.html', _link='/login')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/login/")
def login():
    return discord.create_session(scope=['identify', 'guilds.join'])

@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for(".me"))

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.route("/me/", methods=['GET', 'POST'])
@requires_authorization
def me():
    if request.method == 'GET':
        user = discord.fetch_user()
        return render_template('join.html', user=user.name, img=user.avatar_url, key=SITE_KEY)
    elif request.method == 'POST':
        token = request.form['h-captcha-response']
        payload = { 'secret': CAPTCHA_KEY, 'response': token }
        res = requests.post(url=VERIFY_URL, data=payload)
        if res.status_code == 200:
            if res.json()['success'] == True:
                _id = discord.fetch_user().id
                data = {'access_token': discord.get_authorization_token()['access_token']}
                url = f"https://discord.com/api/guilds/{app.config['DISCORD_GUILD_ID']}/members/{_id}"
                headers = {
                    "Authorization": f"Bot {app.config['DISCORD_BOT_TOKEN']}",
                    "Content-type": "application/json"
                }
                res = requests.put(url=url, json=data, headers=headers)
                return redirect("https://discord.com/channels/810180621930070088/810183289863798815")
    return redirect(url_for('me'))

if __name__ == "__main__":
    app.run()
