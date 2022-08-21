""""""

from rest_framework import serializers

class UserProfileDetailsSerializer(serializers.Serializer):
    
    class Meta:
        id = serializers.IntegerField()
        user_id = serializers.IntegerField()
        username = serializers.CharField()
        role_id = serializers.IntegerField()
        role_name = serializers.CharField()
        #fields = ("id", "user_id", "username", "role_id", "role_name")
        #"ur.id, ur.user_id, u.username, ur.role_id, r.role_name"
        #create_db_table = False