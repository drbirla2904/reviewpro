from django.db import models
from django.conf import settings
import uuid, random, string

def gen_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

CATEGORY_CHOICES = [
    ('Cafe', 'Cafe / Coffee Shop'),
    ('Restaurant', 'Restaurant'),
    ('Hotel', 'Hotel / Resort'),
    ('Salon', 'Salon / Spa'),
    ('Gym', 'Gym / Fitness'),
    ('Bakery', 'Bakery'),
    ('Bar', 'Bar / Pub'),
    ('Clinic', 'Clinic / Healthcare'),
    ('Retail', 'Retail Shop'),
    ('Other', 'Other'),
]

GIFT_TYPE_CHOICES = [
    ('free_drink', 'Free Drink'),
    ('free_item', 'Free Item'),
    ('free_dessert', 'Free Dessert'),
    ('discount', 'Discount %'),
    ('store_credit', 'Store Credit'),
]

GIFT_COLOR_CHOICES = [
    ('orange', 'Orange'),
    ('purple', 'Purple'),
    ('pink', 'Pink'),
    ('green', 'Green'),
    ('blue', 'Blue'),
    ('teal', 'Teal'),
]


class Business(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Restaurant')
    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    logo_emoji = models.CharField(max_length=10, default='🏪')
    primary_color = models.CharField(max_length=7, default='#6366f1')
    google_place_id = models.CharField(max_length=300, blank=True)
    google_access_token = models.TextField(blank=True)
    google_refresh_token = models.TextField(blank=True)
    auto_send_positive_replies = models.BooleanField(default=True)
    min_rating_for_gift = models.IntegerField(default=4)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base = slugify(self.name)
            slug = base
            n = 1
            while Business.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'; n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def google_review_url(self):
        if self.google_place_id:
            return f'https://search.google.com/local/writereview?placeid={self.google_place_id}'
        return f"https://www.google.com/search?q={self.name.replace(' ', '+')}+{self.city}&action=reviews"

    @property
    def avg_rating(self):
        from reviews.models import Review
        agg = Review.objects.filter(business=self, is_verified=True).aggregate(models.Avg('rating'))
        v = agg['rating__avg']
        return round(v, 1) if v else 0

    @property
    def total_reviews(self):
        from reviews.models import Review
        return Review.objects.filter(business=self, is_verified=True).count()


class GiftCard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='gift_cards')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    gift_type = models.CharField(max_length=20, choices=GIFT_TYPE_CHOICES)
    value = models.CharField(max_length=50, help_text='e.g. ₹180 or 20%')
    icon = models.CharField(max_length=10, default='🎁')
    color = models.CharField(max_length=20, choices=GIFT_COLOR_CHOICES, default='purple')
    is_active = models.BooleanField(default=True)
    total_issued = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_active', 'title']

    def __str__(self):
        return f'{self.business.name} — {self.title}'


class QRCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='qr_codes')
    label = models.CharField(max_length=100, default='Main Entrance')
    token = models.CharField(max_length=64, default=gen_token, unique=True)
    qr_image = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    scan_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.business.name} — {self.label}'

    @property
    def review_url(self):
        return f"{settings.APP_URL}/r/{self.token}/"
