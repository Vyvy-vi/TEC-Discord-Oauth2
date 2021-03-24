import os
import requests

from dotenv import load_dotenv

from flask import Flask, render_template, request, session

app = Flask(__name__)
load_dotenv()

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

client_id = os.environ["DISCORD_CLIENT_ID"]
client_secret = os.environ["DISCORD_CLIENT_SECRET"]
redirect = "http://127.0.0.1:5000/callback"
scopes = "identify%20guilds.join"
discord_login_uri="https://discord.com/api/oauth2/authorize?client_id=823513385848537119&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fcallback&response_type=code&scope=identify%20guilds.join"
discord_token_uri="https://discord.com/api/oauth2/token"
discord_api_uri="https://discord.com/api"

def user_json(token):
    url = f"{discord_api_uri}/users/@me"
    headers = {"Authorization": f"Bearer {token}"}

    user_object = requests.get(url=url, headers=headers).json()
    print(user_object)
    return user_object

def get_access_token(code):
    payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect,
            "scope": scopes
            }
    res = requests.post(url = discord_token_uri, data= payload).json()
    return res.get('access_token')

@app.route('/')
def index():
    return render_template('index.html', invite_link=discord_login_uri)

@app.route('/login')
def login():
    code = request.args.get("code")
    print(code)
    access_token = get_access_token(code)
    session['token'] = access_token

    user = user_json(access_token)
    uname, uid = user.get("username"), user.get("discriminator")
    return f'Logged in as {uname}#{uid}'

if __name__ == '__main__':
    app.run(debug=True)
