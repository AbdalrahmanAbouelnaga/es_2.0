import requests
import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework import permissions,authentication
from .serializers import PaymobOrderSerializer,StripeOrderSerializer
# Create your views here.




@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def paymob_payment(request):
    serializer = PaymobOrderSerializer(data=request.data)

    if serializer.is_valid():
        api_key = settings.PAYMOB_SECRET_KEY
        first_response = requests.post(url='https://accept.paymob.com/api/auth/tokens',
                                       headers={'Content-Type':'application/json'},
                                       json={"api_key":api_key})
        first_json = first_response.json()
        auth_token = first_json["token"]
        items = []
        for item in serializer.validated_data["items"]:
            items.append({
                "name":item.get('product').title,
                "amount_cents":int(item.get('quantity')*item.get('product').price * 100),
                "quantity":item.get('quantity')
            })
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])*100
        print(paid_amount)
        second_data = {
            "auth_token":auth_token,
            "delivery_needed":"false",
            "amount_cents": int(paid_amount),
            "currency": "EGP",
            "items":items
        }
        second_response = requests.post(url='https://accept.paymob.com/api/ecommerce/orders',
                                        headers={'Content-Type':'application/json'},
                                        json=second_data)
        second_json = second_response.json()
        order_id = second_json["id"]
        third_data = {
            "auth_token": auth_token,
            "amount_cents": "100", 
            "expiration": 3600, 
            "order_id": order_id,
            "billing_data": {
                "apartment": "NA",
                "floor": "NA", 
                "street": "NA", 
                "building": "NA", 
                "city": "NA", 
                "country": "NA",
                "email": serializer.validated_data["email"], 
                "first_name": serializer.validated_data["first_name"], 
                "phone_number": serializer.validated_data["phone"], 
                "last_name": serializer.validated_data["last_name"], 
            }, 
            "currency": "EGP", 
            "integration_id": 3317273
        }
        third_response = requests.post(url='https://accept.paymob.com/api/acceptance/payment_keys',
                                        headers={'Content-Type':'application/json'},
                                        json=third_data)
        third_json = third_response.json()
        token =  third_json["token"]
        serializer.save(user = request.user)
        return Response(data={"token":token},status=200)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = StripeOrderSerializer(data=request.data)

    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

        try:
            charge = stripe.Charge.create(
                amount=int(paid_amount * 100),
                currency='USD',
                description='Charge from E Store',
                source=serializer.validated_data['stripe_token']
            )

            serializer.save(user=request.user, paid_amount=paid_amount)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
