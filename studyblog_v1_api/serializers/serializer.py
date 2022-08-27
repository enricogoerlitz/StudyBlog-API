from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.forms.models import model_to_dict

from studyblog_v1_api.utils import type_check


def model_to_json(model, top_records=None):
    print(type(model))
    print(type(QuerySet()))
    print(isinstance(model, QuerySet))
    if not isinstance(model, QuerySet):
        print("QUERYSET !!!!!")
        return model

    model_values = model.values()
    type(model_values)
    if not type_check.is_int(top_records, or_float=False): 
        return model_values
    
    if top_records != 1:
        return model_values[:top_records]

    if len(model_values) == 0:
        raise ObjectDoesNotExist("Object does not exists.")

    return model_values[0]
    

