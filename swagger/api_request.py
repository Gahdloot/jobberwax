from drf_yasg import openapi

login_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
    },
)

login_response = {
    "200": openapi.Response(
        description="Login Successful",
        examples={
            "application/json": {
                "auth_credentials": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiODQwODMzZGI1YzhlNDYyYmJmNjEyYzk4OTgzNTFmYzciLCJleHAiOjE3MjQ5NTM2MjQsImlhdCI6MTcyNDk1MTUyNH0.0L_2VH9f6_G1FBkpUnjoDmq0on6nrc9xcS0KSIYRrag",
                "user": {
                    "id": "840833db-5c8e-462b-bf61-2c9898351fc7",
                    "full_name": "fist list",
                    "email": "testtest1@test.com"
                }
            }
        },
    )
}

signup_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        "first_name": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        "last_name": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
    },
)

signup_response = {
    "200": openapi.Response(
        description="Login Successful",
        examples={
            "application/json": {
                "auth_credentials": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiODQwODMzZGI1YzhlNDYyYmJmNjEyYzk4OTgzNTFmYzciLCJleHAiOjE3MjQ5NTM2MjQsImlhdCI6MTcyNDk1MTUyNH0.0L_2VH9f6_G1FBkpUnjoDmq0on6nrc9xcS0KSIYRrag",
                "user": {
                    "id": "840833db-5c8e-462b-bf61-2c9898351fc7",
                    "full_name": "fist list",
                    "email": "testtest1@test.com"
                }
            }
        },
    )
}



org_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        "city": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        "state": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        "country": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        "valuation": openapi.Schema(
            type=openapi.TYPE_INTEGER
        ),
    },
)

join_org_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access_code": openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
    },
)

test_response = {
    "200": openapi.Response(
        description="Login Successful",
        examples={
            "application/json": {
                "auth_credentials": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiODQwODMzZGI1YzhlNDYyYmJmNjEyYzk4OTgzNTFmYzciLCJleHAiOjE3MjQ5NTM2MjQsImlhdCI6MTcyNDk1MTUyNH0.0L_2VH9f6_G1FBkpUnjoDmq0on6nrc9xcS0KSIYRrag",
                "user": {
                    "id": "840833db-5c8e-462b-bf61-2c9898351fc7",
                    "full_name": "fist list",
                    "email": "testtest1@test.com"
                }
            }
        },
    )
}

accept_invite_params = openapi.Parameter(
                name='user',
                description='User ID',
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY
            )