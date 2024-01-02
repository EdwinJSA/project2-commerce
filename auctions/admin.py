from django.contrib import admin
from .models import listing, categoryModel, User, comment, bid

# Register your models here.
admin.site.register(listing)
admin.site.register(categoryModel)
admin.site.register(User)
admin.site.register(comment)
admin.site.register(bid)