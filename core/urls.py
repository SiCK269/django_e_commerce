from django.template.defaulttags import url
from django.urls import path, include, re_path, translate_url
from django.utils.translation import gettext_lazy as _
from django.conf.urls import handler404, handler500, handler403

from .views import (
    item_details,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    add_to_wishlist,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    category_view,
    brand_view,
    CollectionsView,
    CategoriesView,
    BrandsView,
    collection_view,
    search_view,
    seller_view,
    wishlist_view,
    SellerView,
    vendor_view,
    add_product,
    edit_product,
    delete_product,
    product_rating,
    delete_rating,
    comment,
    delete_comment,
    error_403,
    error_404,
    admin_pdf
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/order_pdf/<int:order_id>/', admin_pdf, name='admin_pdf'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', item_details, name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-to-wishlist/<slug>', add_to_wishlist, name="add-to-wishlist"),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path(r'^i18n/', include('django.conf.urls.i18n')),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('category/<str:cat>/', category_view, name='category'),
    path('brand/<str:brand>/', brand_view, name='brand'),
    path('collection/<str:collect>/', collection_view, name='collect'),
    path('seller/<str:seller>/', seller_view, name='seller'),
    path('vendor/', vendor_view, name='vendor'),
    path('add_product/', add_product, name='add_product'),
    path('edit-product/<int:pk>/', edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', delete_product, name='delete-product'),
    path('sellers/', SellerView.as_view(), name='sellers'),
    path('brands/', BrandsView.as_view(), name='brand'),
    path('collections/', CollectionsView.as_view(), name='collection'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('search/', search_view, name='search'),
    path('wishlist/add_to_wishlist/<int:id>', add_to_wishlist, name="user_wishlist"),
    path('wishlist/', wishlist_view, name="wishlist"),
    path('review/', product_rating, name="review"),
    path('delete-review/<int:pk>', delete_rating, name="delete-review"),
    path('comment/', comment, name="comment"),
    path('comment/<int:pk>', delete_comment, name="delete-comment"),
]

handler404 = error_404
handler403 = error_403
