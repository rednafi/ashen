<div align="center">

# ASHEN: **A**rea **S**earc**H** **EN**gine

*Redisearch* based cross-language fuzzy search engine

<a href=""><img src="https://images.unsplash.com/photo-1429772011165-0c2e054367b8?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=80" align="center"/></a>



</div>

## Description

This is an implementation of a dead simple in-memory search engine built with `redis` db and `redisearch` module. A fuzzy area-description dataset has been used here for demonstrating the process if indexing and querying data. However, it can be used as a quick template to build any sort of search engine where the entire indexed data primary lives in the memory and the query response needs to be performant. While performing queries, this implementation applies [Levenstein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) based full text fuzzy matching. Also, it automatically backs up the entire index periodically in the `./redisearch-data` folder and can be configured through the `docker-compose.yml` file. The entire stack consists of:

* [Redis](https://redis.io/)
* [Redisearch](https://oss.redislabs.com/redisearch/index.html)
* [RedisInsight](https://redislabs.com/redisinsight/)
* [Pandas](https://pandas.pydata.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Docker](https://www.docker.com/)


## Running the Engine

* Before running the engine, install `docker` and `docker-compose` on your machine.
* Clone the repo and go to the root folder.
* In the `./settings.toml` file provide your internal ip as `host = <your-internal-ip>` under the `production` section.
* Run

    ```bash
    docker-compose up -d
    ```

## Making Index

To make the engine functional, you will need to provide data in a specific format that will eventually be indexed by the engine. In this case, the `area-description` dataset looks like this. You'll find a sample dataset in the `index-data` folder. Your dataset should be named as `area.csv`:

```csv
index, areaId, areaTile, areaBody
0    , 1     , Azimpur , Example area in Azimpur
1    , 2     , Lalbagh , Some are in lalbagh
2    , 3     , Feni    , Sadar road, Feni
```

* In the root folder, create a python 3.8 virtual environment, activate the environment and install the dependencies via running the following commands one by one:

    ```bash
    python3.8 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

* Place your data (should be formatted like above) in the `index-data` folder and run:

    ```bash
    python -m index.insert_data
    ```
    This should start the indexing process. It takes around a minute to insert one million key value pairs in redis.

* You can explore your dataset by going this url. This opens up a RedisInsight dashboard:

    ```url
    <yourhost>:8001
    ```
    ![img](https://i.imgur.com/LiOTehz.png)

## Running Queries

* Queries can be performed on the following `POST` API:

    ```url
    <yourhost>/area-search/
    ```

* Header:

    ```
    Content-Type: application/json
    x-api-key: 1234ABCD
    ```

* The payload should go as JSON:

    ```json
    {"query": "West Shaorapara,around Mirpur 10,\nShapla sharani.\nHouse no:438/3"}
    ```

* Response:
    ```json
    {
  "matchedArea": [
        {
        "areaBody": "House5,road1,block E,cholontica more,mirpur6,dhaka1216",
        "areaId": "315",
        "areaTitle": "Mirpur",
        "score": 48.0
        },
        {
        "areaBody": "House3 Road9 Block c Mirpur6",
        "areaId": "315",
        "areaTitle": "Mirpur",
        "score": 48.0
        },
        {
        "areaBody": "House3 Road9 Block c Mirpur6",
        "areaId": "315",
        "areaTitle": "Mirpur",
        "score": 48.0
        }
    ],
    "query": "West Shaorapara,around Mirpur 10,\nShapla sharani.\nHouse no:438/3",
    "verdictArea": "Mirpur",
    "verdictAreaId": "315"
    }
    ```


## Architecture

```
.
├── app                       [flask-application]
│   ├── __init__.py
│   └── search_api
│       ├── __init__.py
│       ├── search_data.py
│       ├── utils.py
│       └── views.py
├── docker-compose.yml
├── Dockerfile
├── flask_run.py
├── index                     [This module should be run to insert new data]
│   ├── __init__.py
│   ├── index_data.py
│   └── insert_data.py
├── index-data                [Index module pulls data from here]
│   ├── area.csv
│   └── placeholder-area.csv
├── LICENSE
├── README.md
├── redisearch-data           [Redis back lives here]
│   ├── dump.rdb
│   └── placeholder.rdb
├── requirements.txt
└── settings.toml
```

## Remarks

This application is built and tested on:

* Python 3.8
* Ubuntu 18.05
* Redis stable 5.0
* Redisearch 1.6.10
* Flask 1.1.x
* Pandas 1x
