# BatchIngestion Python Client

This is a Python client library for the [BatchIngestion](https://gitlab.the-qa-company.com/FrozenMink/batchingestionextension) MediaWiki extension, which provides an API to ingest many entities at once. This library allows you to easily ingest entities in bulk, either by parsing them from JSON or by creating them using Python objects.

## Installation

You can install this library using [pip](https://pypi.org/project/batch-ingestion-client-py/):

```bash
pip install batch-ingestion-client-py==1.0.4
```

## Usage

```python
from batch_ingestion_client_py import (
    BatchIngestor,
    Entity,
    ValueInLanguage,
)

ingestor = BatchIngestor(
    base_url="https://your-wiki.com",
    username="your-username",
    password="your-password",
)

example1 = ingestor.ingest([
    Entity.parse({
        "type": "item",
        "labels": {
            "en": {
                "language": "en",
                "value": "Hello, world!",
            },
        },
    })
])

print(example1)

example2 = ingestor.ingest([
    Entity(
        type="item",
        labels={
            "en": ValueInLanguage(
                language="en",
                value="Hello, world!",
            ),
        },
    ),
])

print(example2)
```

## Contributing

If you'd like to contribute to this library, please feel free to submit a pull request.
