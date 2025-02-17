from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bson.objectid import ObjectId

from .serializers import OrderAddSerializer
from utils import take_access_token_and_validation


class OrderAddView(APIView):
    serializer_class = OrderAddSerializer

    def post(self, request):

        user_info = take_access_token_and_validation(request=request)                
        ser_data = self.serializer_class(data=request.data)
        ser_data.is_valid(raise_exception=True)
        vd = ser_data.validated_data
        product = settings.PRODUCT_COLLECTION.find_one({"_id": ObjectId(vd["product_id"])})
        vd['user_id'] = str(user_info.get('_id'))
        vd["total_price"] = vd["quantity"] * product["price"]
        vd['product_price'] = product["price"]
        result = settings.ORDER_COLLECTION.insert_one(vd)
        vd['_id'] = str(result.inserted_id)
        return Response(data=vd, status=status.HTTP_201_CREATED)


class OrderGetListView(APIView):

    def get(self, request, user_id):
        try:
            orders = list(settings.ORDER_COLLECTION.find({"user_id": user_id}))

            for order in orders:
                order['_id'] = str(order['_id'])
                order['user_id'] = str(order['user_id'])
            return Response(data=orders, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)