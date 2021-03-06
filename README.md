# Feel The Beat!

<img  src="/app/static/img/feelthebeatanimals.svg" width="500"></img>

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

Make sure you have [Docker](https://docs.docker.com/engine/install/) installed and running. 
```bash
$ docker-compose up
```
## Features

### Users

The application requires visitors to create accounts on the site in order for it to be used. Upon registration, the user is redirected to an authorization link provided by Spotify that allows them to either accept or decline our application accessing certain data about their Spotify listening history. Each user on our application will thus be linked to their Spotify account. This is so that users are able to retrieve specific data about their listening habits.

### Mood Tracking Calendar
When the user visits the site, if they have not already submitted their mood and song for the day, they are given a list of their five most recently played songs on spotify and are asked to select one and their current mood. Once they submit, that data is stored in the database so that when they click on specific dates on the calendar, they can see their mood and song for the day. This is so they can see how they were feeling on a certain day, and if there's any type of songs they like to listen to in particular moods.

### Site

#### Home Page
In the Home Page you can find the cover page of Feel The Beat!, the register and the login box where you have to create an user and a password or just login into the site.

<img  src="/app/static/img/HomePage.png" width="700"></img><br>

#### Dashboard 
Once you put your Spotify data it redirects to the Feel The Beat! dashboard where you can see your most recently played tracks from the day and choose an emoji mood to that song.After you click the Submit button it will appear a confirm message at the top of the page

<img  src="/app/static/img/Dashboard.png" width="700"></img>

And if you click on a date from the calendar you can see the song and the mood you had in that certain date.

<img  src="/app/static/img/Calendar.png" width="700"></img>

## Technology Stack
* Python, Flask
* Javascript
* HTML/CSS, Bootstrap
* PostgreSQL
* Docker
* cAdvisor
* Prometheus
* Grafana
* NGINX

### Monitoring 
This project was monitored through a combination of cAdvisor, Prometheus and Grafana. 
First, cAdvisor was setup as a basic monitoring system of the docker containers.
Next, we used Prometheus. This could be accessed on port 9090. Here are some of the screenshots of the data that Prometheus generated in tabular form. (Specifically, memory usage of the containers)
![image](https://user-images.githubusercontent.com/70787342/130284027-ec86ee3c-c533-465c-9797-9bdc5fe7b0ff.png)
![image](https://user-images.githubusercontent.com/70787342/130284596-9ce9686a-ef9f-4d1f-a99d-fcdabae10fa8.png)
In order to better understand the data, Grafana utilized Prometheus as a data source. From there, a basic dashboard was created which detailed the memory/CPU usage of each container, as well as the bytes transmitted. This can all be accessed from port 3000. Grafana is password-protected, ensuring only administrators of the team can look at the monitoring data. 
Here we can see Prometheus listed as a source.
![image](https://user-images.githubusercontent.com/70787342/130284933-2be42d6b-90a0-4828-aa1a-b43f31f2397d.png)
From there, the dashboard is created. We can see both a compiled, total memory usage graph, as well as individual graphs for the memory usage of each of the containers. The same is true with respect to the 
CPU usage.
![image](https://user-images.githubusercontent.com/70787342/130286408-da2f4e67-3eb1-46e4-a924-a9fc9bfa5239.png)

## AWS Configuration (Security)
![image](https://user-images.githubusercontent.com/70787342/130305460-a5dd8f2a-e98b-4b47-8f7d-2cc8dfbac8a0.png)

