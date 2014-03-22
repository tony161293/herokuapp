from django.contrib import admin
from canteenapp.models import Food_item
from canteenapp.models import UserProfile
from canteenapp.models import orderDetails

admin.site.register(Food_item)
admin.site.register(UserProfile)
admin.site.register(orderDetails)