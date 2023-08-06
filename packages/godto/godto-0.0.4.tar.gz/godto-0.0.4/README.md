# godto

Data Transfer Object (DTO) codegen from JSON schemas following the OpenAPI spec 

## Usage

To work with an OpenAPI schema, load it with the `Model` class,
which is a Pydantic model (however note that the class name 'Model' comes from the OpenAPI spec).

```py
from godto.openapi.v3 import Model

model = Model.parse_raw(schema_json)
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

Python 3.9+
