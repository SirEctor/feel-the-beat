# Feel The Beat!

## About
A tool to help recommend new songs based on your moods as well give you general analytics on your musical tastes based on the Spotify API.

## Environmental Files
You need to create two environment files: `.env` and `nginx-certbot.env.`

### .env

`CLIENT_ID` = This will be the Client ID of your Spotify application that you get from registering your application with [Spotify for Developers](https://developer.spotify.com/dashboard/).  
`CLIENT_SECRET` = This will be the Client Secret of your Spotify application that you get from registering your application with the link above.  
`REDIRECT_URI` = The URI the user is redirected to after they grant access for the application to access some of their Spotify data. Please note that you must whitelist this URI for your app from the Spotify for Developers dashboard.
`POSTGRES_USER` = The name of the user you will be using to access your database.  
`POSTGRES_PASSWORD` = The password of the user you will be using to access your database.  
`POSTGRES_HOST` = What is hosting your database, ex. localhost. When running this application using docker-compose up, the host will be the container **db**.  
`POSTGRES_DB` = The name of your database.  
`SECRET_KEY` = The secret key of your app that you come up with yourself.  

## Running locally

Make sure you have Docker installed and running. 
```bash
$ docker-compose up
```

