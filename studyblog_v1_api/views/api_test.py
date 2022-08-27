from rest_framework.views import APIView
from rest_framework.response import Response

from studyblog_v1_api.db import query, roles
from studyblog_v1_api.models import (
    RoleModel,
    UserProfileModel,
    UserRoleModel,
    BlogPostModel,
    BlogPostCommentModel
)


class TestAPIView(APIView):
    """Tests the API without any permissions"""
    #authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        init_db()
        test_orm()

        return Response({
            "response": "successful", 
            "message": "You successful send a request to this api! Use /v1/api/login to get your token or /v1/api/register to register and get your token.",
        })

def init_db():
    # - - - - - - users - - - - - - 
    PASSWORD = "test"
    if not UserProfileModel.objects.filter(username="teddy").exists():
        UserProfileModel.objects.create_user(username="teddy", password=PASSWORD)

    for i in range(1, 7):
        username = f"user{i}"
        if not UserProfileModel.objects.filter(username=username).exists():
            UserProfileModel.objects.create_user(username=username, password=PASSWORD)
    
    if not UserProfileModel.objects.filter(username="visitor").exists():
        UserProfileModel.objects.create_user(username="visitor", password=PASSWORD)

    # - - - - - - roles - - - - - - 
    roles_ = [roles.ADMIN, roles.STUDENT, roles.VISITOR, "role4", "role5"]
    for role in roles_:
        if not RoleModel.objects.filter(role_name=role):
            RoleModel.objects.create(role_name=role)
    
    # - - - - - - user roles - - - - - - 
    user_roles_map = {
        "teddy": [roles.ADMIN, roles.STUDENT, "role4", "role5"],
        "user1": [roles.STUDENT, "role4", "role5"],
        "user2": [roles.STUDENT, "role4", "role5"],
        "user3": [roles.STUDENT, "role4", "role5"],
        "user4": [roles.STUDENT, "role5"],
        "user5": [roles.STUDENT, "role4"],
        "user6": [roles.STUDENT],
        "visitor": [roles.VISITOR]
    }

    for username in user_roles_map:
        user_id = UserProfileModel.objects.filter(username=username).values()[0]["id"]
        for role_name in user_roles_map[username]:
            role_id = RoleModel.objects.filter(role_name=role_name).values()[0]["id"]
            if UserRoleModel.objects.filter(user_id=user_id, role_id=role_id).exists():
                continue
            UserRoleModel.objects.create(user_id=user_id, role_id=role_id)
    
    # - - - - - - blogpost - - - - - -
    teddy_user = UserProfileModel.objects.get(username="teddy")
    user_1_user = UserProfileModel.objects.get(username="user1")
    user_4_user = UserProfileModel.objects.get(username="user4")
    user_5_user = UserProfileModel.objects.get(username="user5")
    user_6_user = UserProfileModel.objects.get(username="user6")

    title_1 = "Ich liebe Eis!"
    title_2 = "I like DataScience."
    title_3 = "Warum bin ich immer hungrig?"

    blogposts = [
        {
            "user_id": user_1_user.id,
            "title": title_1,
            "content": "Ich liebe Eis. Was ist eure lieblingssorte?"
        },
        {
            "user_id": teddy_user.id,
            "title": title_2,
            "content": "Get the data, clean it, Analyze it, build models and and grow."
        },
        {
            "user_id": user_4_user.id,
            "title": title_3,
            "content": "Hey Leute. Ich bin immer hungrig?\nMorgens, vormittags, mittags, abends und nachts. Ich bin immer am essen.\n\nWoran kann das liegen?"
        },
    ]

    for blogpost in blogposts:
        if BlogPostModel.objects.filter(title=blogpost["title"]).exists():
            continue
        BlogPostModel.objects.create(**blogpost)


    # - - - - - - blogpost comment - - - - - - 
    blogpost_1 = BlogPostModel.objects.get(title=title_1)
    blogpost_2 = BlogPostModel.objects.get(title=title_2)
    blogpost_3 = BlogPostModel.objects.get(title=title_3)

    blogpost_comments = [
            # blogpost 1
            {
                "user_id": user_4_user.id,
                "blogpost_id": blogpost_1.id,
                "content": "Ich liebe Schlumpfeis.\nUnd auch wenn ich damit langweilig klinge, Vanille ist auch super lecker!"
            },
            {
                "user_id": user_5_user.id,
                "blogpost_id": blogpost_1.id,
                "content": "Ich liebe Schlumpfeis.\nUnd auch wenn ich damit langweilig klinge, Vanille ist auch super lecker!"
            },
            {
                "user_id": user_5_user.id,
                "blogpost_id": blogpost_1.id,
                "content": "ICH SAGE NUR: SCHOKOEISSSSS!!!🥳"
            },

            # blogpost 2
            {
                "user_id": user_6_user.id,
                "blogpost_id": blogpost_2.id,
                "content": "Großartig! I Like. :)"
            },

            # blogpost 3
            {
                "user_id": user_1_user.id,
                "blogpost_id": blogpost_3.id,
                "content": "Ach... mir gehts genau so. Alles gut ;)."
            },
            {
                "user_id": user_4_user.id,
                "blogpost_id": blogpost_3.id,
                "content": "[WERBUNG]: WIE DU IN 4 WOCHEN 80kg ABNEHMEN. KLICKE HIER!"
            },
        ]

    for blogpost_comment in blogpost_comments:
        if BlogPostCommentModel.objects.filter(content=blogpost_comment["content"]).exists():
            continue
        BlogPostCommentModel.objects.create(**blogpost_comment)
    

        
    
def test_orm():
    qs = UserRoleModel.objects.all().select_related("user", "role")
    print("- - - - - - - - TEST ORM START- - - - - - - -")
    print(qs.query)
    print(qs[0].user)
    print(qs[0].role)
    print("- - - - - - - - TEST ORM END- - - - - - - -")