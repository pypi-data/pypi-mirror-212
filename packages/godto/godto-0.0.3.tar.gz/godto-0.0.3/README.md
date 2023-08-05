# godto

Data Transfer Object (DTO) codegen from JSON schemas following the OpenAPI spec 

## Usage

To work with an OpenAPI schema, load it with the `Model` class,
which is a [Dataclass Wizard](https://github.com/rnag/dataclass-wizard/) deserialiser.

```py
from godto.openapi.v3 import Model

model = Model.from_json(schema_json)
```

For example the Transport for London `StopPoint` API schema
is [shipped as package data][StopPoint_schema] in `tubeulator`.

[StopPoint_schema]: https://github.com/lmmx/tubeulator/blob/master/src/tubeulator/data/openapi/StopPoint/StopPoint.json

```py
from pathlib import Path

path_to_schema = Path("data/openapi/StopPoint/StopPoint.json")
schema_json = path_to_schema.read_text()
```

## Requirements

Python 3.9 or 3.10

- Awaiting [bugfix](https://github.com/rnag/dataclass-wizard/issues/89) for 3.11+
