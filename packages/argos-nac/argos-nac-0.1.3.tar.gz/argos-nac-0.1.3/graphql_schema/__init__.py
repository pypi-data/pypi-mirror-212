from .gen_schema import gen_graphql_schema
from os import environ
from pathlib import Path

schema_file = Path(__file__).parent / "schema.py"

if not schema_file.exists():
    gen_graphql_schema(url=environ.get('GRAPHQL_URL'), token=environ.get('GRAPHQL_TOKEN'), output_file=schema_file)
from .schema import *

