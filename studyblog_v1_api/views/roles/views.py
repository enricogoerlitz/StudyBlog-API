from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from studyblog_v1_api.serializers import RoleSerializer
from studyblog_v1_api.models.RoleModel import *
from studyblog_v1_api.utils.request import get_id_obj


class RoleApiView(APIView):
    #authentication_classes = (TokenAuthentication, )
    serializer_class = RoleSerializer

    def get_by_id(self, request):
        id = request.query_params.get("id")
        try:
            return (id, self._serialize(RoleModel.objects.get(pk=id)))
        except Exception as _:
            return (id, None)

    @get_id_obj(RoleModel, RoleSerializer)
    def get(self, request, format=None):
        roles = self._serialize(RoleModel.objects.all(), many=True)
        return Response(roles)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors})
        
        new_role = RoleModel.objects.create(role_name=serializer.data.get(DB_FIELD_ROLE_NAME))
        new_role.save()
        return Response({"OK": self._serialize(new_role)})

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass

    def _serialize(self, data, many=False):
        return None if not data else RoleSerializer(data, many=many).data
