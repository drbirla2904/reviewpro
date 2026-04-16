from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.utils import timezone
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from datetime import timedelta
import json, random

from businesses.models import Business, GiftCard, QRCode
from .models import Review
from .ai_service import (analyze_sentiment, detect_language, get_chips,
                          suggest_review_text, generate_auto_reply, should_auto_send)

def _get_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR', '0.0.0.0')

def _owned_business(request, business_id):
    return get_object_or_404(Business, id=business_id, owner=request.user, is_active=True)

# ── Customer QR Journey ─────────────────────────────────────────────────────

def review_landing(request, token):
    qr = get_object_or_404(QRCode, token=token, is_active=True)
    qr.scan_count += 1
    qr.save(update_fields=['scan_count'])
    return render(request, 'reviews/review.html', {'qr': qr, 'business': qr.business})

def api_chips(request, token, rating):
    qr = get_object_or_404(QRCode, token=token, is_active=True)
    chips = get_chips(qr.business.name, qr.business.category, int(rating))
    return JsonResponse({'chips': chips})

@require_POST
def api_suggest(request, token):
    qr = get_object_or_404(QRCode, token=token, is_active=True)
    body = json.loads(request.body)
    text = suggest_review_text(body.get('chips', []), body.get('rating', 5), qr.business.name)
    return JsonResponse({'suggestion': text})

@require_POST
def api_submit_review(request):
    body = json.loads(request.body)
    qr = get_object_or_404(QRCode, token=body.get('qr_token', ''), is_active=True)
    business = qr.business
    ip = _get_ip(request)

    if Review.objects.filter(business=business, ip_address=ip, created_at__gte=timezone.now()-timedelta(days=7)).exists():
        return JsonResponse({'error': 'You have already reviewed this business recently.'}, status=429)

    rating = int(body.get('rating', 0))
    text = body.get('review_text', '').strip()
    chips = body.get('selected_chips', [])
    reviewer_name = body.get('reviewer_name', '').strip()

    if not text or not (1 <= rating <= 5):
        return JsonResponse({'error': 'Invalid data'}, status=400)

    sentiment, score = analyze_sentiment(text, rating)
    language = detect_language(text)

    gift = None
    if sentiment != 'negative' and rating >= business.min_rating_for_gift:
        gifts = list(business.gift_cards.filter(is_active=True))
        if gifts:
            gift = random.choice(gifts)
            gift.total_issued += 1
            gift.save(update_fields=['total_issued'])

    auto_reply = generate_auto_reply(business.name, business.category, reviewer_name, rating, text, sentiment, chips, contact=business.phone or business.email, language=language)

    review = Review.objects.create(
        business=business, qr_code=qr,
        reviewer_name=reviewer_name, rating=rating, review_text=text,
        selected_chips=chips, sentiment=sentiment, sentiment_score=score,
        detected_language=language, status='escalated' if sentiment=='negative' else 'pending',
        is_verified=True, gift_issued=gift, ip_address=ip,
        auto_reply_text=auto_reply, reply_edited_text=auto_reply,
    )

    if should_auto_send(rating, sentiment, business.auto_send_positive_replies):
        review.reply_approved = True
        review.auto_reply_sent = True
        review.auto_reply_sent_at = timezone.now()
        review.reply_auto_sent_reason = f'Auto-sent: {rating}★ {sentiment} (lang: {language})'
        review.save(update_fields=['reply_approved','auto_reply_sent','auto_reply_sent_at','reply_auto_sent_reason'])

    resp = {'sentiment': sentiment, 'google_review_url': business.google_review_url}
    if gift:
        resp['gift'] = {'title': gift.title, 'description': gift.description, 'value': gift.value, 'icon': gift.icon, 'color': gift.color, 'claim_token': review.gift_claim_token}
    else:
        resp['gift'] = None
        resp['contact'] = {'phone': business.phone, 'email': business.email}
    return JsonResponse(resp, status=201)

def gift_verify(request, claim_token):
    try:
        review = Review.objects.select_related('gift_issued').get(gift_claim_token=claim_token)
        return JsonResponse({
            'valid': not review.gift_claimed,
            'already_claimed': review.gift_claimed,
            'reviewer': review.reviewer_name or 'Customer',
            'rating': review.rating,
            'gift': {'title': review.gift_issued.title, 'icon': review.gift_issued.icon, 'description': review.gift_issued.description} if review.gift_issued else None,
        })
    except Review.DoesNotExist:
        return JsonResponse({'valid': False, 'error': 'Invalid token'}, status=404)

@require_POST
def gift_claim(request, claim_token):
    review = get_object_or_404(Review, gift_claim_token=claim_token, gift_claimed=False)
    review.gift_claimed = True
    review.gift_claimed_at = timezone.now()
    review.save(update_fields=['gift_claimed', 'gift_claimed_at'])
    return JsonResponse({'claimed': True})

# ── Dashboard ───────────────────────────────────────────────────────────────

@login_required
def dashboard_home(request):
    businesses = request.user.businesses.filter(is_active=True)
    if not businesses.exists():
        return redirect('business_new')
    # Default to first business, or selected
    biz_id = request.session.get('active_business')
    business = businesses.filter(id=biz_id).first() or businesses.first()
    request.session['active_business'] = str(business.id)
    return redirect('biz_dashboard', slug=business.slug)

@login_required
def biz_dashboard(request, slug):
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    request.session['active_business'] = str(business.id)
    qs = Review.objects.filter(business=business, is_verified=True)
    now = timezone.now()
    qs_30 = qs.filter(created_at__gte=now-timedelta(days=30))
    qs_7  = qs.filter(created_at__gte=now-timedelta(days=7))
    total_issued = qs.filter(gift_issued__isnull=False).count()
    total_claimed = qs.filter(gift_claimed=True).count()

    # Rating distribution
    rating_dist = [qs.filter(rating=i).count() for i in range(1,6)]
    max_rd = max(rating_dist) or 1

    # Top chips
    from collections import Counter
    import itertools
    all_chips = list(itertools.chain.from_iterable(qs.values_list('selected_chips', flat=True)))
    top_chips = Counter(all_chips).most_common(10)

    ctx = {
        'business': business,
        'active': 'dashboard',
        'stats': {
            'total': qs.count(),
            'total_30d': qs_30.count(),
            'total_7d': qs_7.count(),
            'avg_rating': qs.aggregate(a=Avg('rating'))['a'] or 0,
            'avg_30d': qs_30.aggregate(a=Avg('rating'))['a'] or 0,
            'positive': qs.filter(sentiment='positive').count(),
            'negative': qs.filter(sentiment='negative').count(),
            'neutral': qs.filter(sentiment='neutral').count(),
            'pending_replies': qs.filter(auto_reply_sent=False).count(),
            'sent_replies': qs.filter(auto_reply_sent=True).count(),
            'auto_sent': qs.filter(auto_reply_sent=True).exclude(reply_auto_sent_reason='').count(),
            'gifts_issued': total_issued,
            'gifts_claimed': total_claimed,
            'redemption_rate': round(total_claimed/total_issued*100) if total_issued else 0,
        },
        'recent_reviews': qs.select_related('gift_issued')[:8],
        'gift_stats': qs.filter(gift_issued__isnull=False).values('gift_issued__title','gift_issued__icon').annotate(c=Count('id')).order_by('-c')[:5],
        'top_chips': [{'chip':k,'count':v} for k,v in top_chips],
        'rating_dist': [{'rating':i+1,'count':rating_dist[i],'pct':round(rating_dist[i]/max_rd*100)} for i in range(5)],
        'qrcodes': business.qr_codes.filter(is_active=True)[:4],
    }
    return render(request, 'dashboard/home.html', ctx)

@login_required
def reviews_list(request, slug):
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    qs = Review.objects.filter(business=business, is_verified=True).select_related('gift_issued')
    f = request.GET.get('f', 'all')
    q = request.GET.get('q', '').strip()
    if f == 'positive': qs = qs.filter(sentiment='positive')
    elif f == 'negative': qs = qs.filter(sentiment='negative')
    elif f == 'neutral': qs = qs.filter(sentiment='neutral')
    elif f == 'no_reply': qs = qs.filter(auto_reply_sent=False)
    elif f == 'gift': qs = qs.filter(gift_issued__isnull=False)
    if q: qs = qs.filter(Q(review_text__icontains=q)|Q(reviewer_name__icontains=q))
    paginator = Paginator(qs, 20)
    page = paginator.get_page(request.GET.get('page', 1))
    base = Review.objects.filter(business=business, is_verified=True)
    counts = {'all':base.count(),'positive':base.filter(sentiment='positive').count(),'negative':base.filter(sentiment='negative').count(),'neutral':base.filter(sentiment='neutral').count(),'no_reply':base.filter(auto_reply_sent=False).count(),'gift':base.filter(gift_issued__isnull=False).count()}
    filter_tabs = [('all','All',counts['all']),('positive','✓ Positive',counts['positive']),('negative','⚠ Negative',counts['negative']),('neutral','~ Neutral',counts['neutral']),('no_reply','⏳ No reply',counts['no_reply']),('gift','🎁 With gift',counts['gift'])]
    return render(request, 'dashboard/reviews.html', {
        'business': business, 'active': 'reviews',
        'reviews': page, 'filter': f, 'query': q,
        'filter_tabs': filter_tabs,
        'pending_reply_count': base.filter(auto_reply_sent=False).count(),
    })

@login_required
def replies_list(request, slug):
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    qs = Review.objects.filter(business=business, is_verified=True)
    f = request.GET.get('f', 'pending')
    if f == 'pending': fqs = qs.filter(auto_reply_sent=False)
    elif f == 'sent': fqs = qs.filter(auto_reply_sent=True)
    else: fqs = qs
    paginator = Paginator(fqs, 15)
    page = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'dashboard/replies.html', {
        'business': business, 'active': 'replies',
        'reviews': page, 'filter': f,
        'pending_count': qs.filter(auto_reply_sent=False).count(),
        'sent_count': qs.filter(auto_reply_sent=True).count(),
        'auto_count': qs.filter(auto_reply_sent=True).exclude(reply_auto_sent_reason='').count(),
        'pending_reply_count': qs.filter(auto_reply_sent=False).count(),
    })

@login_required
@require_POST
def reply_save(request, slug, review_id):
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    review = get_object_or_404(Review, id=review_id, business=business)
    body = json.loads(request.body)
    review.reply_edited_text = body.get('text', '').strip()
    review.save(update_fields=['reply_edited_text'])
    return JsonResponse({'ok': True})

@login_required
@require_POST
def reply_send(request, slug, review_id):
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    review = get_object_or_404(Review, id=review_id, business=business)
    from .ai_service import post_reply_to_google
    review.reply_approved = True
    review.auto_reply_sent = True
    review.auto_reply_sent_at = timezone.now()
    review.save(update_fields=['reply_approved','auto_reply_sent','auto_reply_sent_at'])
    # Attempt Google posting (only succeeds if GMB API is fully configured)
    google_result = post_reply_to_google(business, review.reply_edited_text or review.auto_reply_text)
    return JsonResponse({
        'ok': True,
        'sent_at': review.auto_reply_sent_at.strftime('%d %b %Y, %H:%M'),
        'posted_to_google': google_result['success'],
        'google_note': google_result.get('error', ''),
    })

@login_required
@require_POST
def reply_regenerate(request, slug, review_id):
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    review = get_object_or_404(Review, id=review_id, business=business)
    new_reply = generate_auto_reply(business.name, business.category, review.reviewer_name, review.rating, review.review_text, review.sentiment, review.selected_chips, contact=business.phone or business.email, language=review.detected_language)
    review.auto_reply_text = new_reply
    review.reply_edited_text = new_reply
    review.reply_approved = False
    review.save(update_fields=['auto_reply_text','reply_edited_text','reply_approved'])
    return JsonResponse({'ok': True, 'reply': new_reply})

@login_required
def qrcodes_page(request, slug):
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    if request.method == 'POST':
        label = request.POST.get('label', 'Main Entrance').strip()
        from businesses.models import QRCode as QR
        import qrcode as qrlib, io
        from django.core.files.base import ContentFile
        qr_obj = QR.objects.create(business=business, label=label)
        url = qr_obj.review_url
        img = qrlib.QRCode(version=1, box_size=10, border=4)
        img.add_data(url); img.make(fit=True)
        pil = img.make_image(fill_color='#1a1a2e', back_color='white')
        buf = io.BytesIO(); pil.save(buf, format='PNG')
        qr_obj.qr_image.save(f'qr-{qr_obj.token[:8]}.png', ContentFile(buf.getvalue()))
        messages.success(request, f'QR Code "{label}" generated!')
        return redirect('qrcodes_page', slug=slug)
    return render(request, 'dashboard/qrcodes.html', {
        'business': business, 'active': 'qrcodes',
        'qrcodes': business.qr_codes.all(),
    })

@login_required
def gifts_page(request, slug):
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            GiftCard.objects.create(
                business=business,
                title=request.POST.get('title','').strip(),
                description=request.POST.get('description','').strip(),
                value=request.POST.get('value','').strip(),
                icon=request.POST.get('icon','🎁').strip(),
                gift_type=request.POST.get('gift_type','free_item'),
                color=request.POST.get('color','purple'),
            )
            messages.success(request, 'Gift card added!')
        elif action == 'toggle':
            g = get_object_or_404(GiftCard, id=request.POST.get('gift_id'), business=business)
            g.is_active = not g.is_active; g.save(update_fields=['is_active'])
            messages.success(request, f'Gift card {"activated" if g.is_active else "deactivated"}.')
        elif action == 'delete':
            g = get_object_or_404(GiftCard, id=request.POST.get('gift_id'), business=business)
            g.delete(); messages.success(request, 'Gift card deleted.')
        return redirect('gifts_page', slug=slug)
    qs = Review.objects.filter(business=business, is_verified=True)
    ti = qs.filter(gift_issued__isnull=False).count()
    tc = qs.filter(gift_claimed=True).count()
    return render(request, 'dashboard/gifts.html', {
        'business': business, 'active': 'gifts',
        'gifts': business.gift_cards.all(),
        'total_issued': ti, 'total_claimed': tc,
        'redemption_rate': round(tc/ti*100) if ti else 0,
        'gift_type_choices': GiftCard._meta.get_field('gift_type').choices if hasattr(GiftCard,'_meta') else [],
    })

@login_required
def settings_page(request, slug):
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    if request.method == 'POST':
        a = request.POST.get('action')
        if a == 'info':
            for f in ['name','category','address','city','phone','email','website','logo_emoji']:
                setattr(business, f, request.POST.get(f, getattr(business, f, '')).strip())
            business.save(); messages.success(request, 'Business info updated.')
        elif a == 'replies':
            business.auto_send_positive_replies = 'auto_send' in request.POST
            business.min_rating_for_gift = int(request.POST.get('min_rating', 4))
            business.save(update_fields=['auto_send_positive_replies','min_rating_for_gift'])
            messages.success(request, 'Reply settings saved.')
        elif a == 'google':
            business.google_place_id = request.POST.get('google_place_id','').strip()
            business.save(update_fields=['google_place_id']); messages.success(request, 'Google Place ID saved.')
        elif a == 'delete_reviews':
            n = business.reviews.count(); business.reviews.all().delete()
            messages.warning(request, f'Deleted {n} reviews.')
        return redirect('settings_page', slug=slug)
    return render(request, 'dashboard/settings.html', {
        'business': business, 'active': 'settings',
        'categories': [c[0] for c in business._meta.get_field('category').choices],
        'ai_enabled': bool(settings.ANTHROPIC_API_KEY),
    })

# ── Business CRUD ───────────────────────────────────────────────────────────

@login_required
def business_new(request):
    from businesses.models import CATEGORY_CHOICES
    if request.method == 'POST':
        b = Business.objects.create(
            owner=request.user,
            name=request.POST.get('name','').strip(),
            category=request.POST.get('category','Restaurant'),
            city=request.POST.get('city','').strip(),
            address=request.POST.get('address','').strip(),
            phone=request.POST.get('phone','').strip(),
            email=request.POST.get('email','').strip(),
            logo_emoji=request.POST.get('logo_emoji','🏪').strip(),
        )
        # Auto-create 4 default gift cards
        defaults = [
            ('Free Visit', 'On your next visit', 'free_item', '₹150', '🎁', 'purple'),
            ('10% Off', 'On your next bill', 'discount', '10%', '🏷️', 'blue'),
        ]
        for title, desc, gtype, val, icon, color in defaults:
            GiftCard.objects.create(business=b, title=title, description=desc, gift_type=gtype, value=val, icon=icon, color=color)
        messages.success(request, f'Business "{b.name}" created!')
        return redirect('biz_dashboard', slug=b.slug)
    return render(request, 'businesses/new.html', {'categories': [c[0] for c in CATEGORY_CHOICES]})

@login_required
def onboarding(request):
    return render(request, 'businesses/onboarding.html')


# ── Google OAuth ──────────────────────────────────────────────────────────────

@login_required
def google_auth_init(request, business_id):
    """Redirect the browser to Google's OAuth consent screen."""
    business = get_object_or_404(Business, id=business_id, owner=request.user)
    scope = 'https://www.googleapis.com/auth/business.manage'
    auth_url = (
        'https://accounts.google.com/o/oauth2/v2/auth'
        f'?client_id={settings.GOOGLE_CLIENT_ID}'
        f'&redirect_uri={settings.GOOGLE_REDIRECT_URI}'
        f'&response_type=code'
        f'&scope={scope}'
        f'&state={business.id}'
        f'&access_type=offline&prompt=consent'
    )
    if not settings.GOOGLE_CLIENT_ID:
        messages.error(request, 'Google Client ID is not configured. Set GOOGLE_CLIENT_ID in your .env file.')
        return redirect('settings_page', slug=business.slug)
    return redirect(auth_url)


def google_auth_callback(request):
    """Handle Google OAuth callback — save tokens to business."""
    import urllib.request, json as jsonlib, urllib.parse
    code        = request.GET.get('code')
    business_id = request.GET.get('state')

    if not code or not business_id:
        messages.error(request, 'Google authorisation failed — missing code or state.')
        return redirect('dashboard_home')

    try:
        business = Business.objects.get(id=business_id)
    except Business.DoesNotExist:
        messages.error(request, 'Business not found.')
        return redirect('dashboard_home')

    token_data = urllib.parse.urlencode({
        'code':          code,
        'client_id':     settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri':  settings.GOOGLE_REDIRECT_URI,
        'grant_type':    'authorization_code',
    }).encode()

    try:
        req = urllib.request.Request(
            'https://oauth2.googleapis.com/token',
            data=token_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            tokens = jsonlib.loads(r.read())

        business.google_access_token  = tokens.get('access_token', '')
        business.google_refresh_token = tokens.get('refresh_token', '')
        business.save(update_fields=['google_access_token', 'google_refresh_token'])
        messages.success(request, f'Google Business Profile connected for {business.name}!')
    except Exception as e:
        messages.error(request, f'Google authorisation error: {e}')

    return redirect('settings_page', slug=business.slug)