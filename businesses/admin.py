from django.contrib import admin
from .models import Business, GiftCard, QRCode

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name','category','city','owner','auto_send_positive_replies','is_active','created_at']
    list_filter = ['category','is_active','auto_send_positive_replies']
    search_fields = ['name','city','owner__email']
    readonly_fields = ['id','slug','created_at','updated_at']

@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = ['title','business','gift_type','value','total_issued','is_active']
    list_filter = ['business','gift_type','is_active']

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ['label','business','scan_count','is_active','created_at']
    list_filter = ['business','is_active']
    readonly_fields = ['token','qr_image','scan_count']
