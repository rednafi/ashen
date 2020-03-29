# address2id
Mapping fuzzy address string to id

##

## Development

### Run Redisearch
* Run the container via:
    `docker-compose up -d`
* Check the backup configs defined in the `docker-compose.yml` via:
    `docker exec -it redisearch redis-cli -a password config get save`

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
