"""
Module for handling serializing models to JSON objects.
"""

from typing import Union, Any

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, Model
from django.forms.models import model_to_dict
from django.contrib.auth.models import AbstractBaseUser

from studyblog_v1_api.utils import type_check


def model_to_json(model: Union[QuerySet, Model, AbstractBaseUser], *fields, **kwargs) -> Any:
    """
    Serialize a QuerySet or a DB-Model to a JSON object. 
    Raises an Value error, when the wrong type of data is passed as model.
    """
    if not isinstance(model, (QuerySet, Model, AbstractBaseUser)):
        raise ValueError("Detected an unexpected model type by parsing the model to JSON.")

    if not isinstance(model, QuerySet):
        if len(fields) == 0: return model_to_dict(model)
        return {
            field.name: getattr(model, field.name)
            for field in model._meta.fields if field.name in fields
        }

    top = kwargs.get("top")
    models = model.values(*fields)

    if not type_check.is_int(top, or_float=False): return models
    if top != 1: return models[:top]
    if len(models) == 0: raise ObjectDoesNotExist("Object does not exists.")

    return models[0]