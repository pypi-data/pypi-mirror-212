import os
import typing as tp


def environ_or_required(key: str) -> tp.Dict[str, tp.Any]:
    """https://stackoverflow.com/a/45392259/4204843"""
    env = os.environ.get(key)
    if env is not None:
        return {'default': env}
    return {'required': True}
