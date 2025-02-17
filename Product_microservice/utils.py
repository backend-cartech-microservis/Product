import requests
from rest_framework import status
from rest_framework.response import Response

def verify_user_by_token(access_token):
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get("http://127.0.0.1:8001/user/auth/", headers=headers, timeout=4)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None
    except Exception as a:
        return False, a
    
def take_access_token_and_validation(request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", None)
        if not auth_header.startswith("Bearer "):
            return Response({"Error": "Authorization header missing or invalid."}
                            ,status=status.HTTP_401_UNAUTHORIZED)
        access_token = auth_header.split()[1]
        
        is_valid, user_info = verify_user_by_token(access_token=access_token)
        if not is_valid:
            return Response(data={"Error": "invalid or expired token."}
                            ,status=status.HTTP_401_UNAUTHORIZED)
        return user_info
