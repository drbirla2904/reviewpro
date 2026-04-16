from django.db import models
from businesses.models import Business, GiftCard, QRCode
import uuid, random, string

def gen_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

SENTIMENT_CHOICES = [('positive','Positive'),('negative','Negative'),('neutral','Neutral')]
STATUS_CHOICES = [('pending','Pending'),('posted','Posted'),('escalated','Escalated')]


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    qr_code = models.ForeignKey(QRCode, on_delete=models.SET_NULL, null=True, blank=True)
    # Reviewer
    reviewer_name = models.CharField(max_length=100, blank=True)
    reviewer_email = models.CharField(max_length=200, blank=True)
    # Content
    rating = models.IntegerField()
    review_text = models.TextField()
    selected_chips = models.JSONField(default=list)
    # AI Analysis
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES)
    sentiment_score = models.FloatField(default=0.0)
    detected_language = models.CharField(max_length=60, default='English')
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_verified = models.BooleanField(default=False)
    posted_to_google = models.BooleanField(default=False)
    # Gift
    gift_issued = models.ForeignKey(GiftCard, on_delete=models.SET_NULL, null=True, blank=True)
    gift_claim_token = models.CharField(max_length=64, default=gen_token, unique=True)
    gift_claimed = models.BooleanField(default=False)
    gift_claimed_at = models.DateTimeField(null=True, blank=True)
    # Reply
    auto_reply_text = models.TextField(blank=True)
    reply_edited_text = models.TextField(blank=True)
    reply_approved = models.BooleanField(default=False)
    auto_reply_sent = models.BooleanField(default=False)
    auto_reply_sent_at = models.DateTimeField(null=True, blank=True)
    reply_auto_sent_reason = models.CharField(max_length=150, blank=True)
    # Meta
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.business.name} — {self.rating}★ {self.sentiment}'

    @property
    def final_reply(self):
        return self.reply_edited_text or self.auto_reply_text

    @property
    def star_range(self):
        return range(self.rating)

    @property
    def empty_star_range(self):
        return range(5 - self.rating)
