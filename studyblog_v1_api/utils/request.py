from rest_framework.response import Response
from rest_framework import status


class ValidDataWrapper:
    def __init__(self, data, error_msg=None):
        if data is None and error_msg is None:
            raise ValueError("You need to add an error message, if the data is None")

        self.data = data
        self.is_valid = not data is None
        self.errors = error_msg


def get_query_id_obj(model, Serializer, auto_exe=True):
    """
    Checks, whether an id was passed the a get request.

    Args:
        model (DB_Model): an DB Model
        Serializer (Model Serializer): an Model serializer to serialize the model
    """
    def decorator(func):
        def wrapper(view, *args, **kwargs):
            request = args[0]
            id = request.query_params.get("id")
            if not id:
                return func(view, *args, **kwargs)

            try:
                obj = model.objects.get(pk=id)
                id_obj = Serializer(obj, many=False).data

                if auto_exe:
                    return Response(id_obj)

                return func(view, request, ValidDataWrapper(id_obj), *args, **kwargs)
            except Exception:
                err_msg = f"Could not find an object with the id {id}"
                if auto_exe:
                    return Response({"error": err_msg}, status=status.HTTP_400_BAD_REQUEST)

                return func(view, request, ValidDataWrapper(None, err_msg), *args, **kwargs)

        return wrapper
    return decorator

def is_in_role(model, serializer, role): 
    pass    