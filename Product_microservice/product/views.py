from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from bson.objectid import ObjectId


from .serializers import ProductAddSerializer


class ProductAddView(APIView):
    serializer_class = ProductAddSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        PRODUCT_COLLECTION = settings.MONGO_DB['product']
        print(ser_data.validated_data)
        result = PRODUCT_COLLECTION.insert_one(ser_data.validated_data)
        vd = ser_data.data
        vd['_id'] = str(result.inserted_id)
        return Response(data={"message": vd}, status=status.HTTP_201_CREATED)
