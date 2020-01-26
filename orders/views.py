from django.shortcuts import render, redirect
from django.urls import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():

            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )

            # clear the cart
            cart.clear()

            order_created.delay(order.id)

            context = {
                'cart': cart
            }

            # set the order i?n the session
            request.session['order_id'] = order.id

            #  redirect for payment
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm(request.POST)
        context = {
            'cart': cart,
            'form': form
        }
        return render(request, 'orders/order/create.html', context)


def order_created(request):
    return render(request, 'orders/order/created.html')
