from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from subscriptions.models import User, Subscription
import json
from datetime import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
@login_required
@csrf_exempt
def subscriptions_page(request):
    if request.method == 'POST':
        try:
            # Create Checkout session with stripe to Charge User
            user = request.user
            stripe_id = user.stripeId
            if stripe_id is not None:
                stripe_customer = stripe.Customer.retrieve(stripe_id)
            else:
                stripe_customer = stripe.Customer.create(email=user.email)
                user.stripeId = stripe_customer.id
                user.save()
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=user.id,
                line_items=[
                    {
                        'price': 'price_1LVe0cEexlX9H8teNNfbBo5H',
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                subscription_data={
                    'trial_period_days': 7
                },
                customer=stripe_customer,
                success_url='http://localhost:8000' + reverse('home'),
                cancel_url='http://localhost:8000' + reverse('cancel'),
            )
        except Exception as e:
            return JsonResponse({'error': str(e)})

        return redirect(checkout_session.url, code=303)

    if request.method == 'GET':
        user = request.user
        if not user.subscribed:
            return render(request, 'subscribe.html', {'user': request.user})
        else:
            subscription = stripe.Subscription.retrieve(user.user_subscription.stripeSubscriptionId)
            product = stripe.Product.retrieve(subscription.plan.product)
            trial_ends = datetime.fromtimestamp(subscription.trial_end)
            subscription_ends = datetime.fromtimestamp(subscription.trial_end)
            subscription_status = user.user_subscription.status
            return render(request, 'home.html', {'user': request.user, 'subscription': subscription,
                                                 'product': product, "trial_ends": trial_ends,
                                                 "subscription_ends": subscription_ends,
                                                 "subscription_status": subscription_status})


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')


# view to cancel current subscription at end cycle.
@login_required
def cancel_subscription(request):
    user = request.user
    stripe_subscription_id = user.user_subscription.stripeSubscriptionId
    try:
        stripe.Subscription.modify(
            stripe_subscription_id,
            cancel_at_period_end=True
        )
    except Exception as e:
        return JsonResponse({'error': str(e)})
    return render(request, 'cancelled.html')


# webhook that handles event sent from stripe
@csrf_exempt
def stripe_webhook(request):
    # Webhook To securely assign Value of Confirmation of Payment
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle invoice payment. 

    # we have two scenario here.
    # First payment - trial
    # subsequent payment

    if event['type'] == 'invoice.payment_succeeded':
        data = event['data']['object']

        # Fetch all the required data from session
        stripe_customer_id = data.get('customer')
        stripe_subscription_id = data.get('subscription')

        # Get the user.
        user = User.objects.get(stripeId=stripe_customer_id)

        # recurring payments
        try:
            subscription = Subscription.objects.get(user=user)
            subscription.status = "active"
            subscription.save()
        except Subscription.DoesNotExist:
            # First_time  subscription has not been made before.
            Subscription.objects.create(
                user=user,
                status="active",
                stripeSubscriptionId=stripe_subscription_id,
            )

        # update the subscribed column
        user.subscribed = True
        user.save()
        return HttpResponse(status=200)

    # if subscription is deleted after trial ended or user card payment fails
    if event['type'] == 'customer.subscription.deleted':
        # get info needed
        data = event['data']['object']
        stripe_customer_id = data.get('customer')

        # update the current status of subscription to cancel.
        user = User.objects.get(stripeId=stripe_customer_id)
        user.user_subscription.status = "cancelled"
        user.user_subscription.save()

        # update user
        user.subscribed = False
        user.save()

        return HttpResponse(status=200)

    if event['type'] == 'customer.subscription.updated':
        data = event['data']['object']
        stripe_customer_id = data.get('customer')

        # check if the user want's to cancel
        if data.get('cancel_at_period_end'):
            # update the current status of subscription to cancel.
            user = User.objects.get(stripeId=stripe_customer_id)
            user.user_subscription.status = "scheduled_to_cancel"
            user.user_subscription.save()
            return HttpResponse(status=200)
        return HttpResponse(status=200)
