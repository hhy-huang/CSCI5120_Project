# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""Cache key generation utils."""

import hashlib


def _llm_string(params: dict) -> str:
    # New version of the cache is not including n in the params dictionary
    # This avoids creating a new cache key for the same prompt
    if "max_tokens" in params and "n" not in params:
        params["n"] = None
    return str(sorted((k, v) for k, v in params.items()))


def _hash(_input: str) -> str:
    """Use a deterministic hashing approach."""
    return hashlib.md5(_input.encode()).hexdigest()  # noqa S324


def create_hash_key(operation: str, prompt: str, parameters: dict) -> str:
    """Compute cache key from prompt and associated model and settings.

    Args:
        prompt (str): The prompt run through the language model.
        llm_string (str): The language model version and settings.

    Returns
    -------
        str: The cache key.
    """
    llm_string = _llm_string(parameters)
    return f"{operation}-{_hash(prompt + llm_string)}"
