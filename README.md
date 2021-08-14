# Feel The Beat!

[Feel the Beat!](http://feelthebeat.tech/) is a tool that allows you to track your mood for each day along with the song you feel best represents how you're feeling, in order to see patterns of your moods and listening habits. Feel the Beat! draws on the Spotify API and thus requires users to have a Spotify account. 

## Getting Started

To run this application, you need to have authorization to use the Spotify API. To do this, go to [Spotify for Developers](https://developer.spotify.com/dashboard/) and create an application. You will then get a `CLIENT_ID` and `CLIENT_SECRET` which will be necessary to access the API.  

### Environmental Files
You need to create two environment files: `.env` and `nginx-certbot.env.`

#### .env

* `CLIENT_ID` = This will be the Client ID of your Spotify application that you get from registering your application with [Spotify for Developers](https://developer.spotify.com/dashboard/).  
* `CLIENT_SECRET` = This will be the Client Secret of your Spotify application that you get from registering your application with the link above.  
* `REDIRECT_URI` = The URI the user is redirected to after they grant access for the application to access some of their Spotify data. Please note that you must whitelist this URI for your app from the Spotify for Developers dashboard.
* `POSTGRES_USER` = The name of the user you will be using to access your database.  
* `POSTGRES_PASSWORD` = The password of the user you will be using to access your database.  
* `POSTGRES_HOST` = What is hosting your database, ex. localhost. When running this application using docker-compose up, the host will be the container `db`.  
* `POSTGRES_DB` = The name of your database.  
* `SECRET_KEY` = The secret key of your app that you come up with yourself.  

#### nginx-certbot.env

* `CERTBOT_EMAIL` = Your email that you will be using to issue a SSL certificate to your site.
* `USE_LOCAL_CA` = Set to `1` when running in development, `0` when running in production. This variable indicates whether or not to issue a local certificate so the application can be run locally. For more information, view the docs for the [docker-nginx-certbot](https://github.com/JonasAlfredsson/docker-nginx-certbot) Docker image.

### Running the application

Make sure you have Docker installed and running. 
```bash
$ docker-compose up
```

