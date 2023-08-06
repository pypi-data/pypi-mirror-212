Generated with `datamodel-code-generator`

```sh
datamodel-codegen --input data/openapi/v3.0/schema.yaml --output openapi/v3.py --strict-nullable --enum-field-as-literal one
```

- source: OpenAPI v3 YAML schema (in `data` subdir of this package)

- flags `--strict-nullable` and `--enum-fields-as-literal one` flags

- manually edited `Union[Parameter,Reference]` list types to be conlist types and moved the
  `unique_items=True` into the `conlist()` call, leaving the annotation as just `Field(None)`

- manually removed all the `Config` inner classes from the generated models (no flag for this?)
  using vim `:g/class Config/d` and `:g/Extra.forbid/d` then run black linting
