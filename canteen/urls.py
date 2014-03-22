from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'canteenapp.views.home', name='home'),

    url(r'^fooditems/$', 'canteenapp.views.index', name='index'),

    url(r'^register/$', 'canteenapp.views.register_user', name='register'),

    url(r'^register_success/$', 'canteenapp.views.register_success'),

    url(r'^login/$', 'canteenapp.views.login'),

    url(r'^admin_login/$', 'canteenapp.views.admin_login'),

    url(r'^admin_auth/$', 'canteenapp.views.admin_auth_view'),

    url(r'^auth/$', 'canteenapp.views.auth_view'),

    url(r'^admin_page/$', 'canteenapp.views.admin_page'),

    url(r'^saved/$', 'canteenapp.views.saved'),

    url(r'^admin_page/add_item/$', 'canteenapp.views.add_item'),

    url(r'^admin_page/update_user_credit/$',
                'canteenapp.views.update_user_credit'),

    url(r'^admin_page/order_today/$',
                'canteenapp.views.order_today'),

    url(r'^admin_page/edit_item/$',
                'canteenapp.views.edit_item'),

    url(r'^updated$',
                'canteenapp.views.updated'),

    url(r'^logout/$', 'canteenapp.views.logout'),

    url(r'^invalid/$', 'canteenapp.views.invalid_login'),

    url(r'^invalid_admin/$', 'canteenapp.views.invalid_admin'),

    url(r'^fooditems/(?P<itemname>\w+)/$', 'canteenapp.views.itemconfirmation'),

    url(r'^admin_page/edit_item/(?P<itemname>\w+)/$',
                            'canteenapp.views.add_nos'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
