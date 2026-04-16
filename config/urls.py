from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts import views as av
from reviews import views as rv

urlpatterns = [
    path('admin/', admin.site.urls),
    # Public
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    # Accounts
    path('accounts/register/', av.register, name='register'),
    path('accounts/login/', av.login_view, name='login'),
    path('accounts/logout/', av.logout_view, name='logout'),
    path('accounts/profile/', av.profile, name='profile'),
    # Customer review journey
    path('r/<str:token>/', rv.review_landing, name='review_landing'),
    path('r/<str:token>/chips/<int:rating>/', rv.api_chips, name='api_chips'),
    path('r/<str:token>/suggest/', rv.api_suggest, name='api_suggest'),
    path('submit-review/', rv.api_submit_review, name='api_submit_review'),
    path('gift/verify/<str:claim_token>/', rv.gift_verify, name='gift_verify'),
    path('gift/claim/<str:claim_token>/', rv.gift_claim, name='gift_claim'),
    # Onboarding
    path('dashboard/', rv.dashboard_home, name='dashboard_home'),
    path('onboarding/', rv.onboarding, name='onboarding'),
    path('business/new/', rv.business_new, name='business_new'),
    # Dashboard (per business, slug-based)
    path('dashboard/<slug:slug>/',           rv.biz_dashboard,   name='biz_dashboard'),
    path('dashboard/<slug:slug>/reviews/',   rv.reviews_list,    name='reviews_list'),
    path('dashboard/<slug:slug>/replies/',   rv.replies_list,    name='replies_list'),
    path('dashboard/<slug:slug>/replies/<uuid:review_id>/save/',       rv.reply_save,       name='reply_save'),
    path('dashboard/<slug:slug>/replies/<uuid:review_id>/send/',       rv.reply_send,       name='reply_send'),
    path('dashboard/<slug:slug>/replies/<uuid:review_id>/regenerate/', rv.reply_regenerate, name='reply_regenerate'),
    path('dashboard/<slug:slug>/qrcodes/',   rv.qrcodes_page,    name='qrcodes_page'),
    path('dashboard/<slug:slug>/gifts/',     rv.gifts_page,      name='gifts_page'),
    path('dashboard/<slug:slug>/settings/',  rv.settings_page,   name='settings_page'),
    # Google OAuth
    path('api/auth/google/<uuid:business_id>/', rv.google_auth_init,     name='google_auth_init'),
    path('api/auth/google/callback/',           rv.google_auth_callback, name='google_auth_callback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)