import stripe
from django.http import HttpRequest
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from deadlybird.settings import SITE_HOST_URL, WEBHOOK_SUBSCRIPTION_SECRET, MONTHLY_SUBSCRIPTION_ITEM_ID, YEARLY_SUBSCRIPTION_ITEM_ID
from deadlybird.util import remove_trailing_slash
from deadlybird.permissions import SessionAuthenticated

# Create your views here.

@api_view(["GET"])
@permission_classes([ SessionAuthenticated ])
def checkout(request: HttpRequest):
  if (not ("type" in request.GET)) or (not (request.GET["type"] in ["monthly", "annual"])): 
    return Response({
      "error": True,
      "message": "Did not provide subscription type"
    }, status=400)
  
  subscription_price_id = MONTHLY_SUBSCRIPTION_ITEM_ID if request.GET["type"] == "monthly" else YEARLY_SUBSCRIPTION_ITEM_ID

  session = stripe.checkout.Session.create(
    success_url=f"{remove_trailing_slash(SITE_HOST_URL)}/subscription/success?session={{CHECKOUT_SESSION_ID}}",
    cancel_url=f"{remove_trailing_slash(SITE_HOST_URL)}/subscription",
    mode="subscription",
    line_items=[
      {
        "price": subscription_price_id,
        "quantity": 1
      }
    ]
  )

  return Response({
    "url": session.url
  })

@api_view(["DELETE"])
@permission_classes([ SessionAuthenticated ])
def subscription_cancel(request: HttpRequest):
  pass

@api_view(["POST"])
def subscription_event(request: HttpRequest):
  try:
    event = stripe.Webhook.construct_event(
      payload=request.body,
      sig_header=request.META["HTTP_STRIPE_SIGNATURE"],
      secret=WEBHOOK_SUBSCRIPTION_SECRET
    )
  except (ValueError, stripe.error.SignatureVerificationError) as exception:
    return Response({
      "error": True,
      "message": "Invalid webhook event"
    }, status=400)
  
  if event.type == "checkout.session.completed":
    # Payment purchased
    checkout_session_id = event.data.object["id"]

    purchase = stripe.checkout.Session.retrieve(
      checkout_session_id,
      expand=["subscription", "customer"]
    )
    subscription_purchase_id = purchase.subscription.id
    customer_id = purchase.customer.id

    # Process subscription

  elif event.type == "checkout.session.expired":
    # Payment cancelled
    checkout_session_id = event.data.object["id"]

  elif event.type == "customer.subscription.deleted":
    # Subscription cancelled
    subscription_purchase_id = event.data.object.id
    customer_id = event.data.object.customer

  return Response({
    "error": False,
    "message": "Success"
  }, status=201)