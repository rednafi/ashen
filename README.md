# address2id
Mapping fuzzy address string to id

## Stack
* Redis
* Redisearch
* Pandas
* Flask
* Docker


## Directory Structure
```
.
├── app                         [flask api]
│   ├── __init__.py
│   └── search_api
│       ├── __init__.py
│       ├── search_data.py
│       ├── utils.py
│       └── views.py
├── data                        [Index csv data]
│   ├── area.csv
│   └── placeholder-area.csv
├── docker-compose.yml
├── flask_run.py                [flask executor]
├── index
│   ├── index_data.py
│   ├── __init__.py
│   └── insert_data.py
├── LICENSE
├── README.md
├── redisearch-data             [redisearch backup]
│   ├── dump.rdb
│   └── placeholder.rdb
├── requirements.txt
└── settings.toml               [central configs]
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
* To index new data, add the data in `area.csv` format to `./data` folder. Look into the `placeholder-area.csv` file to see the data format.

* Data must look like this:
    ```csv
    index | areaId | areaTile | areaBody
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
