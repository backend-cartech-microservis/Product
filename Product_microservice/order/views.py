from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bson.objectid import ObjectId
from django.core.cache import cache
from rabbitmq_management import Rabbitmq_Producer_AuthUser
from .serializers import OrderAddSerializer
from django.core.cache import cache


class OrderAddView(APIView):
    serializer_class = OrderAddSerializer

    def post(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", None)
        access_token = auth_header.split()[1]
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        vd = ser_data.validated_data
        Rabbitmq_Producer_AuthUser(exchange_name='User', queue_name='get_order_user', headers=access_token)
        user_info = cache.get("Data")
        if not user_info.get('user_id'):
            return Response(data={"message": "user not found"}, status=status.HTTP_403_FORBIDDEN)
        try:
            product = settings.PRODUCT_COLLECTION.find_one({"_id": ObjectId(vd["product_id"])})
            vd['user_id'] = str(user_info.get('_id'))
            vd["total_price"] = vd["quantity"] * product["price"]
            vd['product_price'] = product["price"]
            result = settings.ORDER_COLLECTION.insert_one(vd)
            vd['_id'] = str(result.inserted_id)
            return Response(data=vd, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)