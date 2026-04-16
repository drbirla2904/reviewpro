from django.contrib import admin
from django.utils import timezone
from .models import Review
from .ai_service import generate_auto_reply

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['business','rating','sentiment','reviewer_name','detected_language','auto_reply_sent','reply_approved','gift_issued','created_at']
    list_filter = ['business','sentiment','rating','auto_reply_sent','reply_approved','gift_claimed']
    search_fields = ['reviewer_name','review_text','reviewer_email']
    readonly_fields = ['id','sentiment','sentiment_score','gift_claim_token','ip_address']
    fieldsets = (
        ('Review', {'fields': ('id','business','qr_code','reviewer_name','reviewer_email','rating','review_text','selected_chips','sentiment','sentiment_score','detected_language','status','ip_address')}),
        ('Gift', {'fields': ('gift_issued','gift_claim_token','gift_claimed','gift_claimed_at')}),
        ('Auto-Reply', {'fields': ('auto_reply_text','reply_edited_text','reply_approved','auto_reply_sent','auto_reply_sent_at','reply_auto_sent_reason')}),
    )
    actions = ['mark_sent','regen_replies']

    def mark_sent(self, request, qs):
        qs.update(auto_reply_sent=True, reply_approved=True, auto_reply_sent_at=timezone.now())
        self.message_user(request, f'{qs.count()} replies marked as sent.')
    mark_sent.short_description = 'Mark replies as sent'

    def regen_replies(self, request, qs):
        for r in qs:
            reply = generate_auto_reply(r.business.name, r.business.category, r.reviewer_name, r.rating, r.review_text, r.sentiment, r.selected_chips, language=r.detected_language)
            r.auto_reply_text = reply; r.reply_edited_text = reply; r.reply_approved = False; r.save()
        self.message_user(request, f'Regenerated {qs.count()} replies.')
    regen_replies.short_description = 'Regenerate AI replies'
