from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from ..openapi.v3 import Model as OpenAPI_v3_Model

__all__ = ["APIOptions", "load_model", "model_paths"]


class APIOptions(Enum):
    OPENAPI_V3 = "OpenAPI_v3"


@dataclass
class ModelConfig:
    spec: APIOptions

    def load(self, source: str) -> OpenAPI_v3_Model:
        """
        Load an API.
        """
        if self.spec == APIOptions.OPENAPI_V3:
            model = OpenAPI_v3_Model.parse_raw(source)
        else:
            raise NotImplementedError("Spec not supported")
        return model


def model_paths(
    schema_json: str,
    spec: APIOptions = APIOptions.OPENAPI_V3,
    method: str = "get",
    extract: str | None = None,
) -> dict[str, dict[str, Any]]:
    """
    Load an API, extract its paths and their parameters in a convenient format.
    A specific method can be passed (HTTP method, lowercase, default: "get").
    A specific attribute to extract from the param info can be retrieved, or else
    if `extract` is None the entire parameter will be provided.
    """
    model_cfg = ModelConfig(spec=spec)
    model = model_cfg.load(source=schema_json)
    path_info = {}
    for path, path_schema in model.paths.__root__.items():
        path_info[path] = {}
        params = getattr(path_schema, method).parameters
        if params is not None:
            for param in params:
                param_info = param if extract is None else getattr(param, extract)
                path_info[path][param.name] = param_info
    return path_info
