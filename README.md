# speedtrap.io
For when you're pretty sure that CenturyLink isn't give you consistent gigabit speeds.

# Introduction
TL;DR: I wanted to write a tool that measured my download speeds throughout the day to see if I was consistently getting the speeds that I am paying for.

The project is still in its infancy and I'm using it to explore containers, APIs, and microservices (which will eventually host data created by the client script).

## `client`
This is currently a poorly written Python script that calls various tools to measure bandwidth.

It currently only runs on Windows and is generally pretty terrible. I'll make it better, I promise.

### Usage
`python3 speedtrap-client.py` without any arguments will log the results to a local `report.csv` file.

`python3 speedtrap-client.py -k APIKEY` will attempt to send the results to the web services for reporting on the web site. **Note**: an API key can also be entered by adding an `API_KEY` value to `settings.py`.

I currently have this running as a scheduled task that executes every 5.5 hours.

## `speedtrap-web-services`
My first attempt at using Docker to standup and configure a set of web services.

It speedtrap's web services currently consist of 5 containers:
* an NGINX server acting as an API gateway,
* a `certbot` image ensuring that TLS certs from Let's Encrypt stay updated,
* a Flask app that serves API functions from behind the API gateway,
* a Flask app that serves Web functions from behind the API gateway,
* a MongoDB that receives and serves data via the Flask apps


This will eventually build out to be a larger set of services.

### Usage
From the `speedtrap-web-services` directory, run `docker compose up --build -d` and all the services should come up after some initial configuration.

In an effort to keep passwords, secrets, and keys stored in a reasonably secure manner (and to keep them out of this GitHub repo), the services take advantage of Docker Secrets. As seen in the `docker-compose.yml` file, there are a few secret files in the `speedtrap-web-services/data/secrets/` directory that need to be populated:
* `speedtest-db_root_username`: This gets passed into the MongoDB container to configure the intial root username.
* `speedtest-db_root_password`: This gets passed into the MongoDB container to configure the intial root password.
* `speedtest-db_api_username`: This gets passed into the MongoDB container to configure the username that the Flask apps use to interact with the database.
* `speedtest-db_api_password`: This gets passed into the MongoDB container to configure the passowrd that the Flask apps use to interact with the database.
* `api_keys`: This gets passed into the NGINX API gateway to conduct basic authentication to the API.

# Goals
## Overall
I've had CenturyLink's residential gigabit fiber service for a few months now and didn't really feel like I was getting full gigabit speeds consistently.

Running speedtests from various web browsers yielded varying results. Sometimes things would get up into the 500Mbps range but often I was sitting at around 100Mbps.

I wanted to put together a quick script that I would be able to run on a system at random times throughout the day to measure what my bandwidth looked like during peak and non-peak hours.

Granted, this tool is currently only running on a single laptop so I may never consistently see consistent gigabit speeds based on whatever else is going on with that system or on my network at any given time.

## Tooling
I wanted to vary the tools that I was using to measure my speeds. As of `v0.0.1`, this script calls utilities implemented in Go and Python and also makes use of Powershell.

This is all strung together very haphazardly. Ideally I'd like to make this more modular and extensible.

## Output
The script currently outputs to a (poorly generated) CSV that I dump into Excel to generate charts and metrics. It is not modular, extensible, or even implemented correctly.

Ideally, I would like to get this into a more robust datastore and then toss it up to a web server to generate and display charts and metrics more easily.

Once the kinks are worked out and I get a stable set of testing utilities, I'd love to implement a Twitter bot or mailbot that sends a politely worded email to CenturyLink at certain thresholds (e.g. when observed speeds fall below 50% of purchased service more than 5 times in a row.)

# 3rd Party Tools
* [ddo](https://github.com/ddo)'s Go implementation of [Fast.com](https://fast.com): https://github.com/ddo/fast
	* Used in: `v0.0.1`
* [Speedtest.net](https://speedtest.net)'s CLI app: https://www.speedtest.net/apps/cli
	* Used in: `v0.0.1`
* [sivel](https://github.com/sivel)'s Python implementation of [Speedtest.net](https://speedtest.net): https://github.com/sivel/speedtest-cli/blob/master/speedtest.py
	* Used in `v0.0.1`
* [Turnkey Internet](https://turnkeyinternet.net)'s Speed Test: https://turnkeyinternet.net/speed-test/
	* Used in: `v0.0.1`