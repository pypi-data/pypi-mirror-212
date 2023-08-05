from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.codegen.schema import CodeGen
from pathlib import Path


def gen_graphql_schema(url: str, token: str, output_file: str | Path):
    headers = {'Authorization': f'Token {token}', 'Accept': 'application/json'}
    with open(Path(__file__).parent / "schema_query.gql") as f:
        query = f.read().replace('\n', '')

    endpoint = HTTPEndpoint(url, headers, method='GET')
    res = endpoint(query=query)

    def filter_response_dict(schema):
        if not isinstance(schema, dict):
            raise SystemExit('schema must be a JSON object')

        if schema.get('types'):
            return schema
        elif schema.get('data', {}).get('__schema', None):
            return schema['data']['__schema']  # plain HTTP endpoint result
        elif schema.get('__schema'):
            return schema['__schema']  # introspection field
        else:
            raise SystemExit('schema must be introspection object or query result')

    with open(output_file,'w+') as f:
        a = CodeGen(schema=filter_response_dict(res), schema_name='schema', writer=f.write, docstrings=False)
        a.write()
