import random
import string

import stripe
from datetime import datetime
from io import BytesIO
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView, View
from xhtml2pdf import pisa

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete

from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm, Product
from .models import *

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        ratings = Review.objects.all()
        category = Category.objects.all()
        brand = Brand.objects.all()
        collection = Collection.objects.all()
        promos = HomePromotion.objects.all()
        banner = HomeBanner.objects.all()
        logo = HomeLogo.objects.all()
        footer = FooterDetail.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"], context["brand_menu"], context["collection_menu"], context[
            'promo_menu'], context['banner_image'], context['logo'], context['footers'], context['ratings'] = \
            category, brand, collection, promos, banner, logo, footer, ratings
        return context


def vendor_view(request):
    logo = HomeLogo.objects.all()
    footer = FooterDetail.objects.all()
    if request.user.is_staff:
        items = Item.objects.all()
        return render(request, 'vendor.html', {'objects': items, 'logo': logo, 'footers': footer})
    else:
        return render(request, '403.html')


class BrandsView(ListView):
    model = Brand
    paginate_by = 10
    template_name = 'brands.html'

    def get_context_data(self, *args, **kwargs):
        logo = HomeLogo.objects.all()
        footer = FooterDetail.objects.all()
        context = super(BrandsView, self).get_context_data(*args, **kwargs)
        context['logo'], context['footers'] = logo, footer
        return context


class SellerView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'sellers.html'

    def get_context_data(self, *args, **kwargs):
        logo = HomeLogo.objects.all()
        footer = FooterDetail.objects.all()
        context = super(SellerView, self).get_context_data(*args, **kwargs)
        context['logo'], context['footers'] = logo, footer
        return context


class CategoriesView(ListView):
    model = Category
    paginate_by = 10
    template_name = 'categories.html'

    def get_context_data(self, *args, **kwargs):
        logo = HomeLogo.objects.all()
        footer = FooterDetail.objects.all()
        context = super(CategoriesView, self).get_context_data(*args, **kwargs)
        context['logo'], context['footers'] = logo, footer
        return context


class CollectionsView(ListView):
    model = Collection
    paginate_by = 10
    template_name = 'collections.html'

    def get_context_data(self, *args, **kwargs):
        logo = HomeLogo.objects.all()
        footer = FooterDetail.objects.all()
        context = super(CollectionsView, self).get_context_data(*args, **kwargs)
        context['logo'], context['footers'] = logo, footer
        return context


def category_view(request, cat):
    category_item = Category.objects.filter(name=cat)
    logo = HomeLogo.objects.all()
    footer = FooterDetail.objects.all()
    for x in category_item:
        cats = Item.objects.all().filter(category=x)
        return render(request, 'category.html', {'cat': cat, 'category': category_item, 'objects': cats, 'logo': logo,
                                                 'footers': footer})


def seller_view(request, seller):
    seller_menu = Item.objects.filter(seller=seller)
    logo = HomeLogo.objects.all()
    footer = FooterDetail.objects.all()
    return render(request, 'seller.html', {'objects': seller_menu, 'logo': logo, 'footers': footer})


def brand_view(request, brand):
    brand_item = Brand.objects.filter(name=brand)
    logo = HomeLogo.objects.all()
    footer = FooterDetail.objects.all()
    for x in brand_item:
        brands = Item.objects.all().filter(brand=x)
        return render(request, 'brand.html', {'brand': brand, 'objects': brands, 'logo': logo, 'footers': footer})


def collection_view(request, collect):
    collection_items = Collection.objects.filter(name=collect)
    logo = HomeLogo.objects.all()
    footer = FooterDetail.objects.all()
    for x in collection_items:
        collections = Item.objects.all().filter(collection=x)
        return render(request, 'collection.html', {'collection': collect, 'objects': collections, 'logo': logo,
                                                   'footers': footer})


def search_view(request):
    logo = HomeLogo.objects.all()
    footer = FooterDetail.objects.all()
    if request.method == "POST":
        inquiry = request.POST['inquiry']
        items = Item.objects.filter(title__contains=inquiry)
        return render(request, 'search_result.html', {"objects": items, 'search': inquiry, 'logo': logo,
                                                      'footers': footer})
    else:
        return render(request, 'search_result.html', {'logo': logo, 'footers': footer})


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, _("You do not have an active order"))
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the default shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, _("No default shipping address available"))
                        return redirect('core:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')
                    phone_number = form.cleaned_data.get('phone_number')
                    shipping_city = form.cleaned_data.get('shipping_city')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip, phone_number, shipping_city]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            city=shipping_city,
                            phone=phone_number,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, _("Please fill in the required shipping address fields"))

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the default billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, _("No default billing address available"))
                        return redirect('core:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')
                    phone_number = form.cleaned_data.get('phone_number')
                    billing_city = form.cleaned_data.get('billing_city')
                    if is_valid_form([billing_address1, billing_country, billing_zip, phone_number, billing_city]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            city=billing_city,
                            phone=phone_number,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, _("Please fill in the required billing address fields"))

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                elif payment_option == 'CoD':
                    order.save()
                    payment = Payment()
                    payment.user = self.request.user
                    payment.amount = order.get_total()
                    payment.save()

                    order_items = order.items.all()
                    order_items.update(ordered=True)
                    for item in order_items:
                        item.save()

                    order.ordered = True
                    order.payment = payment
                    order.ref_code = create_ref_code()
                    order.save()
                    messages.success(self.request, _("Your order was successful!"))
                    return redirect('core:home')
                else:
                    messages.info(
                        self.request, _("Please fill in the required shipping address fields"))
                    redirect('core:checkout')

            else:
                messages.warning(
                    self.request, _("Invalid payment option selected"))
                return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, _("You do not have an active order"))
            return redirect("core:order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
            }
            if UserProfile.objects.filter(user=self.request.user):
                userprofile = UserProfile.objects.get_or_create(user=self.request.user)[0]
                userprofile.stripe_customer_id = random.choices(string.ascii_uppercase)
                if userprofile.one_click_purchasing:
                    # fetch the users card list
                    cards = stripe.Customer.list_sources(
                        userprofile.stripe_customer_id,
                        limit=3,
                        object='card'
                    )
                    card_list = cards['data']
                    if len(card_list) > 0:
                        # update the context with the default card
                        context.update({
                            'card': card_list[0]
                        })
                return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, _("You have not added a billing address"))
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, _("Your order was successful!"))
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, _(f"{err.get('message')}"))
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, _("Rate limit error"))
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, _("Invalid parameters"))
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, _("Not authenticated"))
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, _("Network error"))
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, _("Something went wrong. You were not charged. Please try again."))
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, _("A serious error occurred. We have been notifed."))
                return redirect("/")

        messages.warning(self.request, _("Invalid data received"))
        return redirect("/payment/stripe/")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            logo = HomeLogo.objects.all()
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
                'logo': logo
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, _("You do not have an active order"))
            return redirect("/")


def render_pdf_invoice(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@login_required
def admin_pdf(request, order_id):
    if request.user.is_superuser:
        order = Order.objects.get(pk=order_id, ordered=True)
        items = OrderItem.objects.filter(user=order.user)
        address = Address.objects.filter(user=order.user)
        print(order)
        pdf = render_pdf_invoice('invoice.html', {'order': order, 'items': items, 'address': address})

        if pdf:
            response = HttpResponse(pdf, content_type='application/odf')
            content = "attachment; filename=%s.pdf" % order_id
            response['Content-Disposition'] = content

            return response

        return HttpResponse("Not found")


def error_404(request, exception):
    return render(request, '404.html')


def error_403(request, exception):
    return render(request, '403.html')


def error_500(request, exception):
    return render(request, '500.html')


def item_details(request, slug):
    items = Item.objects.filter(slug=slug)
    user = request.user
    for i in items:
        if request.user.is_authenticated:
            if Analysis.objects.filter(item=i, visited_by=request.user).exists():
                analysis = Analysis.objects.filter(item__title=i, visited_by=request.user, anonymous=False)
                for a in analysis:
                    if a.item == i and a.visited_by == request.user:
                        a.visits = a.visits + 1
                        a.last_visit = datetime.now()
                        a.save()
            if Analysis.objects.filter(item=i) and not Analysis.objects.filter(visited_by=request.user):
                analysis = Analysis.objects.create(
                    item=i,
                    visited_by=request.user,
                    visits=+ 1,
                    last_visit=datetime.now()
                )
                analysis.save()
        else:
            if Analysis.objects.filter(item=i, visited_by=None).exists():
                analysis = Analysis.objects.filter(item__slug=i.slug, anonymous=True)
                for a in analysis:
                    if a.item == i:
                        a.visits = a.visits + 1
                        a.last_visit = datetime.now()
                        a.save()
            else:
                analysis = Analysis.objects.create(
                    item=i,
                    visits=+ 1,
                    anonymous=True,
                    last_visit=datetime.now()
                )
                analysis.save()

    item_rating = Item.objects.get(slug=slug)
    logo = HomeLogo.objects.all()
    footer = FooterDetail.objects.all()
    rate = Review.objects.filter(item=item_rating)
    context = {'objects': items, "logo": logo, "rates": rate, 'footers': footer}
    return render(request, 'product.html', context)


def product_rating(request):
    if request.method == 'GET' and request.user.is_authenticated:
        item_slug = request.GET.get('item_slug')
        item = Item.objects.get(slug=item_slug)
        content = request.GET.get('content')
        rating = request.GET.get('rating')
        user = request.user
        Review(
            created_by=user,
            item=item,
            content=content,
            rating=rating
        ).save()
        messages.success(request, 'Review Added!')

        return redirect('core:product', slug=item_slug)


def delete_rating(request, pk):
    if request.user.is_authenticated:
        rate = Review.objects.get(id=pk)
        if request.user == rate.created_by:
            rate.delete()
            item = Item.objects.get(slug=rate.item.slug)
            messages.success(request, 'Review deleted!')
            return redirect('core:product', slug=item.slug)
        else:
            return render(request, Http404)


def comment(request):
    if request.method == 'GET' and request.user.is_authenticated:
        item_slug = request.GET.get('item_slug')
        item = Item.objects.get(slug=item_slug)
        content = request.GET.get('content')
        user = request.user

        if content:
            Comment(
                name=user,
                item=item,
                content=content,
            ).save()

        return redirect('core:product', slug=item_slug)


def delete_comment(request, pk):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=pk)
        if request.user == comment.name:
            comment.delete()
            item = Item.objects.get(slug=comment.item.slug)
            messages.success(request, 'Comment deleted!')
            return redirect('core:product', slug=item.slug)
        else:
            return render(request, Http404)


@login_required
def add_product(request):
    logo = HomeLogo.objects.all()
    footer = FooterDetail.objects.all()
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            form = Product(request.POST, request.FILES)

            if form.is_valid():
                title = request.POST.get('title')
                slug = slugify(title)

                product = form.save(commit=False)
                product.seller = request.user
                product.slug = slug
                product.save()

                messages.success(request, 'Product added successfully!')
                return redirect('core:vendor')
    else:
        return render(request, '403.html')

    form = Product()

    return render(request, 'account/add_product.html', {'form': form, 'logo': logo, 'footers': footer})


@login_required
def edit_product(request, pk):
    logo = HomeLogo.objects.all()
    footer = FooterDetail.objects.all()
    if request.user.is_authenticated and request.user.is_staff:
        product = Item.objects.filter(seller=request.user).get(pk=pk)

        if request.method == 'POST':
            form = Product(request.POST, request.FILES, instance=product)

            if form.is_valid():
                form.save()

                messages.success(request, 'Changes were saved!')
                return redirect('core:vendor')
        else:
            form = Product(instance=product)

        return render(request, 'account/edit_product.html', {'form': form, 'logo': logo, 'footers': footer})


@login_required
def delete_product(request, pk):
    if request.user.is_authenticated and request.user.is_staff:
        product = Item.objects.filter(seller=request.user).get(pk=pk)
        product.delete()

        messages.success(request, 'Product deleted successfully!')
        return redirect('core:vendor')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists() and order_item.quantity < item.quantity:
            order_item.quantity += 1
            order_item.save()
            messages.info(request, _("This item quantity was updated."))
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, _("This item was added to your cart."))
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, _("This item was added to your cart."))
        return redirect("core:order-summary")


@login_required
def add_to_wishlist(request, id):
    item = get_object_or_404(Item, id=id)
    if item.user_wishlist.filter(id=request.user.id).exists():
        item.user_wishlist.remove(request.user)
        messages.success(request, "The item '" + item.title + "' has been removed to your wishlist.")
    else:
        item.user_wishlist.add(request.user)
        messages.success(request, "The item '" + item.title + "' has been added to your wishlist.")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def wishlist_view(request):
    logo = HomeLogo.objects.all()
    footer = FooterDetail.objects.all()
    wished_items = Item.objects.filter(user_wishlist=request.user)
    return render(request, "wished.html", {"objects": wished_items, 'logo': logo, 'footers': footer})


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, _("This item was removed from your cart."))
            return redirect("core:order-summary")
        else:
            messages.info(request, _("This item was not in your cart"))
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, _("You do not have an active order"))
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, _("This item quantity was updated."))
            return redirect("core:order-summary")
        else:
            messages.info(request, _("This item was not in your cart"))
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, _("You do not have an active order"))
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, _("This coupon does not exist"))
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, _("Successfully added coupon"))
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, _("You do not have an active order"))
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        logo = HomeLogo.objects.all()
        footer = FooterDetail.objects.all()
        form = RefundForm()
        context = {
            'form': form,
            'logo': logo,
            'footers': footer
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, _("Your request was received."))
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, _("This order does not exist."))
                return redirect("core:request-refund")
