import datetime

from django.contrib import admin
from django.shortcuts import render
from django.urls import reverse
from django.contrib.admin import AdminSite, DateFieldListFilter
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter, NumericRangeFilter
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import *
from django.db.models.functions import TruncDay, TruncMonth
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json
from .filter import *
from .resource import *
from import_export.admin import ImportExportModelAdmin
from django.db.models import Count, Sum, F


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('admin_pdf', args=[obj.id])))


order_pdf.short_description = 'PDF'


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class AnalysisAdmin(admin.ModelAdmin):
    list_filter = (('last_visit', DateRangeFilter),)

    def changelist_view(self, request, extra_context=None):
        auth_chart_label = []
        auth_chart_data = []
        time = []
        auth_chart_time = []

        chart_data = []
        chart_label = []
        chart_time = []

        qs = Analysis.objects.order_by('-visits')
        for item in qs:
            if item.visited_by:
                if item.item.title not in auth_chart_label:
                    auth_chart_label.append(item.item.title)
                    s = Analysis.objects.filter(item__title=item.item.title, anonymous=False).aggregate(Sum('visits'))[
                        'visits__sum']
                    auth_chart_data.append(s)
                    auth_chart_time.append(item.last_visit.strftime("%m/%d/%Y"))
                else:
                    pass
            else:
                chart_label.append(item.item.title)
                chart_data.append(item.visits)
                chart_time.append(item.last_visit.strftime("%m/%d/%Y"))

        p_chart_data = []
        p_chart_label = []

        qs = Payment.objects.order_by('timestamp')
        now = datetime.now()
        for item in qs:
            if item.timestamp.strftime("%Y-%m-%d") not in p_chart_label:
                p_chart_label.append(item.timestamp.strftime("%Y-%m-%d"))
                s = Payment.objects.filter(timestamp__year=item.timestamp.year, timestamp__month=item.timestamp.month,
                                           timestamp__day=item.timestamp.day).aggregate(total_amount=Sum('amount'))[
                    'total_amount']

                p_chart_data.append(s)
                print(s)

        extra_context = extra_context or {'a_data': auth_chart_data, 'a_time': auth_chart_time,
                                          'a_labels': auth_chart_label, 'data': chart_data, 'labels': chart_label,
                                          'time': chart_time, 'p_data': p_chart_data, 'p_labels': p_chart_label}
        return super().changelist_view(request, extra_context=extra_context)


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'timestamp']
    list_filter = (('timestamp', DateTimeRangeFilter),)


class ItemResourceAdmin(ImportExportModelAdmin):
    resource_class = ItemResource


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon',
                    order_pdf
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon',
        order_pdf
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted',
                   ]
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


admin.site.register(Analysis, AnalysisAdmin)
admin.site.register(ShippingCost)
admin.site.register(FooterDetail)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(HomeLogo)
admin.site.register(HomeBanner)
admin.site.register(HomePromotion)
admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(Brand)
admin.site.register(Item, ItemResourceAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentsAdmin)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
