# TEC-Discord-Oauth2
Testing repo to try out discord's Oauth2 API to give privileged access to users that complete Captcha.

## How to get a local instance running?
- Make a new Application on [Discord Developer Platform](https://discord.com/developers/) and add a bot to that application. Go to the Oauth section, and add `http://127.0.0.1/callback` to the Redirect URI section.
- Log in to hCaptcha, add a new site, copy the `site-key` generated.
- Clone this repo(\*if you're contributing to the project, fork the repo and clone your fork)
  ```
  git clone https://github.com/Vyvy-vi/TEC-Discord-Oauth2/
  ```
- Copy contents of `.env.example` to a new file - `.env`
  ```
  cp app/.env.example app/.env
  ```
- Add the requisite environment variables to the `.env` file in the `app` folder:
  - `DISCORD_CLIENT_ID`: Client ID of the Discord Application from Discord Developer Portal
  - `DISCORD_CLIENT_SECRET`: Client Secret of the Discord Application from Discord Developer Portal
  - `DISCORD_GUILD_ID`: Guild ID of the server, for which you want to run this application. (Server to invite to)
  - `SECRET_KEY`: Pick any value. (up to you, however a key that is hard to crack, is recommended)
  - `DISCORD_BOT_TOKEN`: Bot Token of the Bot added on the Application made on Discord Developer Portal
  - `CAPTCHA_KEY`: hCaptcha Key from https://www.hcaptcha.com/
  - `SITE_KEY`: hCaptcha site-key(to be obtained by adding a domain on the hcaptcha dashboard)
  - `HOST DOMAIN`: If deploying locally, set this as "http://127.0.0.1:5000"
- Install pipenv
  ```
  pip install pipenv
  ```
- Install dependencies
  ```
  pipenv sync --dev
  ```
- Run the application
  ```
  pipenv run start
  ```

## How to set up the discord Application?
- Go to https://discord.com/developers/applications and create a `New Application`. Give it suitable name and suitable profile picture.
- Go to the `Oauth` tab for the application, and add `http://127.0.0.1/callback` and `<your-site-link/callback>` to the the Redirect URI field.
- Go to the `Bot` tab for the application, and create a new bot. Invite this bot to your discord server, with the following permissions- [CREATE INVITE]. (The one, on which you want to run the invite application)
- Copy the Client ID, Client Secret and the BOT_TOKEN and add these to the `.env` file.
