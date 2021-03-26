import os
import requests

from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = Flask(__name__)
load_dotenv()
app.secret_key = os.environ["SECRET_KEY"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "false"      # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_CLIENT_ID"]  # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]              # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = os.environ["DISCORD_BOT_TOKEN"]
app.config["DISCORD_GUILD_ID"] = os.environ["DISCORD_GUILD_ID"]

discord = DiscordOAuth2Session(app)

@app.route('/')
def index():
    return render_template('index.html', _link='/login')

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

@app.route("/me/")
@requires_authorization
def me():
    user = discord.fetch_user()
    return render_template('join.html', user=user.name, img=user.avatar_url, _link='/join')

@app.route("/join/")
@requires_authorization
def join():
    _id = discord.fetch_user().id
    data = {'access_token': discord.get_authorization_token()['access_token']}
    url = f"https://discord.com/api/guilds/{app.config['DISCORD_GUILD_ID']}/members/{_id}"
    headers = {
            "Authorization" : f"Bot {app.config['DISCORD_BOT_TOKEN']}",
            'Content-Type': 'application/json'
            }
    res =requests.put(url=url, json=data, headers=headers)
    print(res.status_code)
    return "You have been added to the server"

if __name__ == "__main__":
    app.run()
