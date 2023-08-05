r"""
:mod:`godto` is a Data Transfer Object (DTO) codegen library to produce Python dataclass
interfaces from JSON schemas following the OpenAPI spec."""

__all__ = ["openapi"]

__author__ = "Louis Maddox"
__license__ = "MIT"
__description__ = "Data Transfer Object (DTO) codegen from JSON schemas following the OpenAPI spec"
__url__ = "https://github.com/lmmx/godto"
__uri__ = __url__
__email__ = "louismmx@gmail.com"

from . import openapi
