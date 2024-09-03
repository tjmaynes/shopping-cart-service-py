from os import getenv


def get_env_var_or_throw(key: str) -> str:
    found = getenv(key)
    if found is None:
        raise ValueError(f"Unable to find required environment variable '{key}'...")
    else:
        return found
