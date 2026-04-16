"""
Injects business context into every authenticated request so
base.html sidebar always has the right data without each view
passing it manually.
"""
from businesses.models import Business

def dashboard_context(request):
    if not request.user.is_authenticated:
        return {}
    try:
        businesses = list(request.user.businesses.filter(is_active=True).order_by('name'))
        active_slug = request.resolver_match.kwargs.get('slug') if request.resolver_match else None
        business = None
        if active_slug:
            business = next((b for b in businesses if b.slug == active_slug), None)
        if not business and businesses:
            business = businesses[0]

        pending_reply_count = 0
        if business:
            from reviews.models import Review
            pending_reply_count = Review.objects.filter(
                business=business, is_verified=True, auto_reply_sent=False
            ).count()

        return {
            'business': business,
            'businesses': businesses,
            'pending_reply_count': pending_reply_count,
        }
    except Exception:
        return {}
