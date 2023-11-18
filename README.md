# q3logs2kafka

## install

### development

```bash
pip install -e .
```

### production

```bash
pip install .
```

## Tests

```bash
python -m unittest discover
```

## Run

[Set up a kafka stack](https://www.conduktor.io/kafka/how-to-start-kafka-using-docker/)

start event_producer:

```bash
 event_producer -vvv
 ```

 start q3logs_reader:

 ```bash
q3logs_reader -v tail -c 'docker logs -f ioquake3' -u "http://127.0.0.1:5000/event/"
```