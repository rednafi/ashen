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
├── address_map             [primary module]
│   ├── index_data.py       [create redis index]
│   ├── __init__.py
│   ├── insert_data.py      [insert data from csv]
│   ├── search_data.py      [run query]
│   └── utils.py
├── data
│   └── address.csv
├── docker-compose.yml
├── LICENSE
├── README.md
└── redisearch-data         [redis persistent backup]
    └── dump.rdb
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
* To index new data, add the data in csv format in `./data` folder
* Data must look like this:
    ```csv
    index | areaId | areaTile | areaBody
    ```

* From the root folder run:
    ```bash
    python -m address_map.insert_data
    ```

### Run Query
* From the root folder run,
    ```python
    python -m address_map.search_data
    ```
