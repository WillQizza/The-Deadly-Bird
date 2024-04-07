import stripe
from django.shortcuts import render

# KEY = sk_test_51OIZXzLmClgbbAeLhE6c2Ji2YmVtNSSGWq91H8xBDl7BKGwKz5QaeutsBEXWtL495ysuRBXDHypPiBQvzGyPo5Hb00RIPGJiOU
# PRODUCT = price_1P2fzcLmClgbbAeLjS9LdyXx

# Create your views here.
def checkout():
  stripe.checkout.Session.create(
    
  )