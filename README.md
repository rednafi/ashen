# Area Search Engine

Cross language area search from fuzzy descriptions

## Stack

* Redis
* Redisearch
* RedisInsight
* Pandas
* Flask
* Docker


## Directory Structure

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

## Development

### Run Redisearch

* Run the container via:
    `docker-compose up -d`

* Check the backup configs defined in the `docker-compose.yml` via:

    ```bash
    docker exec -it redisearch redis-cli -a password config get save
    ```

### Prepare Python Environment
* Prepare python environment via (you might need to install `python3.8 venv`):

    ```bash
    python3.8 -m venv venv
    source venv/bin/activate
    ```

* Install the dependencies via:
    ```bash
    pip install -r requirements.txt
    ```

### Index Data
* To index new data, add the data in `area.csv` format to `./index-data` folder. Look into the `placeholder-area.csv` file to see the data format.

* Data must look like this:
    ```csv
    index, areaId, areaTile, areaBody
    0    , 1     , Azimpur , Example area in Azimpur
    1    , 2     , Lalbagh , Some are in lalbagh
    2    , 3     , Feni    , Sadar road, Feni
    ```

* From the root folder run:
    ```bash
    python -m index.insert_data
    ```

### Run Query
* From the root folder run,
    ```python
    python -m address_map.search_data
    ```


## Deployment
* Run all the containers at once in detached mode:

    ```bash
    docker-compose up -d
    ```
