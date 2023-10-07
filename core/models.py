from django.db.models.signals import post_save
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.utils.translation import gettext_lazy as _

LABEL_CHOICES = (
    ('aliceblue', 'aliceblue'),
    ('antiquewhite', 'antiquewhite'),
    ('aqua', 'aqua'),
    ('aquamarine', 'aquamarine'),
    ('azure', 'azure'),
    ('beige', 'beige'),
    ('bisque', 'bisque'),
    ('black', 'black'),
    ('blanchedalmond', 'blanchedalmond'),
    ('blue', 'blue'),
    ('blueviolet', 'blueviolet'),
    ('brown', 'brown'),
    ('burlywood', 'burlywood'),
    ('cadetblue', 'cadetblue'),
    ('chartreuse', 'chartreuse'),
    ('chocolate', 'chocolate'),
    ('coral', 'coral'),
    ('cornflowerblue', 'cornflowerblue'),
    ('cornsilk', 'cornsilk'),
    ('crimson', 'crimson'),
    ('cyan', 'cyan'),
    ('darkblue', 'darkblue'),
    ('darkcyan', 'darkcyan'),
    ('darkgoldenrod', 'darkgoldenrod'),
    ('darkgray', 'darkgray'),
    ('darkgrey', 'darkgrey'),
    ('darkgreen', 'darkgreen'),
    ('darkkhaki', 'darkkhaki'),
    ('darkmagenta', 'darkmagenta'),
    ('darkolivegreen', 'darkolivegreen'),
    ('darkorange', 'darkorange'),
    ('darkorchid', 'darkorchid'),
    ('darkred', 'darkred'),
    ('darksalmon', 'darksalmon'),
    ('darkseagreen', 'darkseagreen'),
    ('darkslateblue', 'darkslateblue'),
    ('darkslategray', 'darkslategray'),
    ('darkslategrey', 'darkslategrey'),
    ('darkturquoise', 'darkturquoise'),
    ('darkviolet', 'darkviolet'),
    ('deeppink', 'deeppink'),
    ('deepskyblue', 'deepskyblue'),
    ('dimgray', 'dimgray'),
    ('dimgrey', 'dimgrey'),
    ('dodgerblue', 'dodgerblue'),
    ('firebrick', 'firebrick'),
    ('floralwhite', 'floralwhite'),
    ('forestgreen', 'forestgreen'),
    ('fuchsia', 'fuchsia'),
    ('gainsboro', 'gainsboro'),
    ('ghostwhite', 'ghostwhite'),
    ('gold', 'gold'),
    ('goldenrod', 'goldenrod'),
    ('gray', 'gray'),
    ('grey', 'grey'),
    ('green', 'green'),
    ('greenyellow', 'greenyellow'),
    ('honeydew', 'honeydew'),
    ('hotpink', 'hotpink'),
    ('indianred', 'indianred'),
    ('indigo', 'indigo'),
    ('ivory', 'ivory'),
    ('khaki', 'khaki'),
    ('lavender', 'lavender'),
    ('lavenderblush', 'lavenderblush'),
    ('lawngreen', 'lawngreen'),
    ('lemonchiffon', 'lemonchiffon'),
    ('lightblue', 'lightblue'),
    ('lightcoral', 'lightcoral'),
    ('lightcyan', 'lightcyan'),
    ('lightgoldenrodyellow', 'lightgoldenrodyellow'),
    ('lightgray', 'lightgray'),
    ('lightgrey', 'lightgrey'),
    ('lightgreen', 'lightgreen'),
    ('lightpink', 'lightpink'),
    ('lightsalmon', 'lightsalmon'),
    ('lightseagreen', 'lightseagreen'),
    ('lightskyblue', 'lightskyblue'),
    ('lightslategray', 'lightslategray'),
    ('lightslategrey', 'lightslategrey'),
    ('lightsteelblue', 'lightsteelblue'),
    ('lightyellow', 'lightyellow'),
    ('lime', 'lime'),
    ('limegreen', 'limegreen'),
    ('linen', 'linen'),
    ('magenta', 'magenta'),
    ('maroon', 'maroon'),
    ('mediumaquamarine', 'mediumaquamarine'),
    ('mediumblue', 'mediumblue'),
    ('mediumorchid', 'mediumorchid'),
    ('mediumpurple', 'mediumpurple'),
    ('mediumseagreen', 'mediumseagreen'),
    ('mediumslateblue', 'mediumslateblue'),
    ('mediumspringgreen', 'mediumspringgreen'),
    ('mediumturquoise', 'mediumturquoise'),
    ('mediumvioletred', 'mediumvioletred'),
    ('midnightblue', 'midnightblue'),
    ('mintcream', 'mintcream'),
    ('mistyrose', 'mistyrose'),
    ('moccasin', 'moccasin'),
    ('navajowhite', 'navajowhite'),
    ('navy', 'navy'),
    ('oldlace', 'oldlace'),
    ('olive', 'olive'),
    ('oc', 'olivedrab'),
    ('orange', 'orange'),
    ('orangered', 'orangered'),
    ('orchid', 'orchid'),
    ('palegoldenrod', 'palegoldenrod'),
    ('palegreen', 'palegreen'),
    ('paleturquoise', 'paleturquoise'),
    ('palevioletred', 'palevioletred'),
    ('papayawhip', 'papayawhip'),
    ('peachpuff', 'peachpuff'),
    ('peru', 'peru'),
    ('pink', 'pink'),
    ('plum', 'plum'),
    ('powderblue', 'powderblue'),
    ('purple', 'purple'),
    ('red', 'red'),
    ('rosybrown', 'rosybrown'),
    ('royalblue', 'royalblue'),
    ('saddlebrown', 'saddlebrown'),
    ('salmon', 'salmon'),
    ('sandybrown', 'sandybrown'),
    ('seagreen', 'seagreen'),
    ('seashell', 'seashell'),
    ('sienna', 'sienna'),
    ('silver', 'silver'),
    ('skyblue', 'skyblue'),
    ('slateblue', 'slateblue'),
    ('slategray', 'slategray'),
    ('slategrey', 'slategrey'),
    ('snow', 'snow'),
    ('springgreen', 'springgreen'),
    ('steelblue', 'steelblue'),
    ('tan', 'tan'),
    ('teal', 'teal'),
    ('thistle', 'thistle'),
    ('tomato', 'tomato'),
    ('turquoise', 'turquoise'),
    ('violet', 'violet'),
    ('wheat', 'wheat'),
    ('white', 'white'),
    ('whitesmoke', 'whitesmoke'),
    ('yellow', 'yellow'),
    ('yellowgreen', 'yellowgreen'),
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Brand(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    banner = models.ImageField(null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:brand", kwargs={
            'brand': self.name
        })


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    banner = models.ImageField(null=True)
    image = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:category', kwargs={
            'cat': self.name
        })


class Collection(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    banner = models.ImageField(null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:collect', kwargs={
            'collect': self.name
        })


class Item(models.Model):
    seller = models.ForeignKey(User, related_name='items', null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True, null=True)
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(
        Category, blank=True, default='uncategorized', on_delete=models.DO_NOTHING)
    brand = models.ForeignKey(
        Brand, blank=True, null=True, on_delete=models.DO_NOTHING)
    collection = models.ForeignKey(
        Collection, blank=True, null=True, on_delete=models.DO_NOTHING)
    label = models.CharField(choices=LABEL_CHOICES, max_length=20, blank=True)
    slug = models.SlugField()
    detailed_description = RichTextField(null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    width = models.FloatField(default=0, blank=True, null=True)
    height = models.FloatField(default=0, blank=True, null=True)
    depth = models.FloatField(default=0, blank=True, null=True)
    weight = models.FloatField(default=0, blank=True, null=True)
    user_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="wishlist", blank=True)
    banner_image = models.ImageField(null=True)
    image_main = models.ImageField(null=True)
    image_1 = models.ImageField(null=True)
    image_2 = models.ImageField(null=True)
    image_3 = models.ImageField(null=True)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_add_to_wishlist_url(self):
        return reverse("core:add-to-wishlist", kwargs={
            'slug': self.slug
        })

    def get_remove_from_wishlist_url(self):
        return reverse("core:remove-from-wishlist", kwargs={
            'slug': self.slug
        })

    def get_discount_tag(self):
        if self.discount_price:
            return round(((self.price - self.discount_price) / self.price) * 100, 2)


class Analysis(models.Model):
    class Meta:
        verbose_name_plural = 'Analysis'

    item = models.ForeignKey(Item, related_name='analysis', on_delete=models.DO_NOTHING)
    visited_by = models.ForeignKey(User, related_name="visited_by", null=True, blank=True, on_delete=models.DO_NOTHING)
    anonymous = models.BooleanField(default=False, null=True)
    visits = models.IntegerField(default=0)
    last_visit = models.DateTimeField(blank=True)


class Comment(models.Model):
    item = models.ForeignKey(Item, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.item.title, self.name)


class Review(models.Model):
    item = models.ForeignKey(Item, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def get_1_stars(self):
        rates = []
        slug = self.item.slug
        items = Item.objects.filter(slug=slug)
        for item in items:
            reviews = Review.objects.filter(item=item)
            for review in reviews:
                if review.rating == 1:
                    rates.append(review.rating)
        return len(rates)

    def get_2_stars(self):
        rates = []
        slug = self.item.slug
        items = Item.objects.filter(slug=slug)
        for item in items:
            reviews = Review.objects.filter(item=item)
            for review in reviews:
                if review.rating == 2:
                    rates.append(review.rating)
        return len(rates)

    def get_3_stars(self):
        rates = []
        slug = self.item.slug
        items = Item.objects.filter(slug=slug)
        for item in items:
            reviews = Review.objects.filter(item=item)
            for review in reviews:
                if review.rating == 3:
                    rates.append(review.rating)
        return len(rates)

    def get_4_stars(self):
        rates = []
        slug = self.item.slug
        items = Item.objects.filter(slug=slug)
        for item in items:
            reviews = Review.objects.filter(item=item)
            for review in reviews:
                if review.rating == 4:
                    rates.append(review.rating)
        return len(rates)

    def get_5_stars(self):
        rates = []
        slug = self.item.slug
        items = Item.objects.filter(slug=slug)
        for item in items:
            reviews = Review.objects.filter(item=item)
            for review in reviews:
                if review.rating == 5:
                    rates.append(review.rating)
        return len(rates)

    def get_overall_ratings(self):
        overall_rates = []
        slug = self.item.slug
        items = Item.objects.filter(slug=slug)
        for item in items:
            reviews = Review.objects.filter(item=item)
            for review in reviews:
                overall_rates.append(review.rating)
            return len(overall_rates)

    def get_avg_rates(self):
        avg_rates = []
        slug = self.item.slug
        items = Item.objects.filter(slug=slug)
        for item in items:
            reviews = Review.objects.filter(item=item)
            for review in reviews:
                avg_rates.append(review.rating)
        return round(sum(avg_rates) / len(avg_rates), 2)


class FooterDetail(models.Model):
    about = models.TextField()
    facebook = models.CharField(max_length=115)
    instagram = models.CharField(max_length=115)
    twitter = models.CharField(max_length=115)
    youtube = models.CharField(max_length=115)
    linkedin = models.CharField(max_length=115)


class HomePromotion(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)
    collection = models.ForeignKey(Collection, blank=True, null=True, on_delete=models.DO_NOTHING)
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.DO_NOTHING)


class HomeBanner(models.Model):
    banner = models.ImageField(blank=False, null=True)


class HomeLogo(models.Model):
    logo = models.ImageField(blank=False, null=True)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_quantity(self):
        return self.quantity

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class ShippingCost(models.Model):
    shipping_cost = models.IntegerField(max_length=2)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_subtotal(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        shipping_cost = ShippingCost.objects.all()
        for cost in shipping_cost:
            return total + cost.shipping_cost


@receiver(pre_save, sender=Order)
def order_submitted(sender, instance, *args, **kwargs):
    if instance.ordered:
        print('Order Submitted')
    else:
        print('nothing')


# post_save.connect(order_submitted, sender=Order)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, blank=True)
    country = CountryField(multiple=False)
    city = models.CharField(max_length=115, null=True)
    phone = models.CharField(default="07XX", max_length=15)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
