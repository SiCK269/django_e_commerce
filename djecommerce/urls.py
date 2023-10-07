from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
import core.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/order_pdf/<int:order_id>/', core.views.admin_pdf, name='admin_pdf'),
    path(r'^i18n/', include('django.conf.urls.i18n')),
    path('rosetta/', include('rosetta.urls')),
    path("ninja/", include("core.d_ninja.urls"), name='api'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

]

urlpatterns += i18n_patterns(
    path('accounts/', include('allauth.urls')),
    (path('', include('core.urls'))),
                             )

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

handler404 = core.views.error_404
handler403 = core.views.error_403
