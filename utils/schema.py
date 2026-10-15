from jsonschema import Draft202012Validator

from test_data.loader import load_json


def assert_schema(instance: dict, schema_file: str) -> None:
    """Fail with every schema violation listed, not just the first one."""
    schema = load_json(f"schemas/{schema_file}")
    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        details = "\n".join(f"- {'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors)
        raise AssertionError(f"Schema '{schema_file}' violated:\n{details}")
