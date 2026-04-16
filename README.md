# ReviewPro — SaaS Google Review Platform

A production-grade Django SaaS that helps businesses collect Google reviews via QR codes, reward customers with gift cards, and auto-reply with AI-generated personalised responses.

---

## Quick Start

```bash
# 1. Clone and install
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env with your values

# 3. Database setup
python manage.py migrate
python manage.py seed_demo     # demo data + test account

# 4. Start
python manage.py runserver
```

**Demo credentials:**
| | |
|---|---|
| URL | `http://localhost:8000` |
| Email | `demo@reviewpro.app` |
| Password | `demo1234` |
| Admin | `http://localhost:8000/admin/` — `admin@reviewpro.app` / `admin123` |

---

## Project Structure

```
reviewpro_saas/
├── accounts/           Custom User model (email auth, plan, avatar)
│   ├── models.py       User with plan, full_name, avatar_initials
│   ├── views.py        register, login, logout, profile
│   └── forms.py        RegisterForm, LoginForm
│
├── businesses/         Business, GiftCard, QRCode models
│   └── models.py       Business (owner FK, slug, auto-send toggle)
│                       GiftCard (title, value, icon, color)
│                       QRCode (token, label, scan_count, qr_image)
│
├── reviews/            Core review logic
│   ├── models.py       Review (rating, sentiment, AI reply, gift, language)
│   ├── views.py        Customer QR journey + all dashboard pages
│   ├── ai_service.py   Sentiment · Language detection · Chips · Auto-reply
│   ├── context_processors.py   Sidebar business context for all pages
│   └── management/commands/seed_demo.py
│
├── config/             Django project config
│   ├── settings.py     Environment-driven, whitenoise, CORS
│   └── urls.py         All routes (landing, auth, review journey, dashboard)
│
├── templates/
│   ├── base.html           Sidebar layout + nav + toast system
│   ├── base_auth.html      Centered card for auth pages
│   ├── landing.html        Public marketing landing page
│   ├── accounts/           login.html · register.html · profile.html
│   ├── businesses/         new.html · onboarding.html
│   ├── dashboard/          home · reviews · replies · qrcodes · gifts · settings
│   └── reviews/            review.html (customer QR journey)
│
└── static/
    ├── css/app.css     Full design system (dark theme, tokens, components)
    └── js/app.js       toast() · openModal() · apiPost() · copyText()
```

---

## All URLs

### Public
| URL | Description |
|-----|-------------|
| `/` | Landing page |
| `/accounts/register/` | Create account |
| `/accounts/login/` | Sign in |
| `/accounts/logout/` | Sign out |
| `/accounts/profile/` | User profile |

### Customer Review Journey
| URL | Description |
|-----|-------------|
| `/r/<token>/` | Review page (QR scan target) |
| `/r/<token>/chips/<rating>/` | AI chip suggestions (AJAX) |
| `/r/<token>/suggest/` | AI review text draft (AJAX) |
| `/submit-review/` | Submit review (JSON POST) |
| `/gift/verify/<claim_token>/` | Verify gift at counter |
| `/gift/claim/<claim_token>/` | Redeem gift (POST) |

### Dashboard (all require login)
| URL | Description |
|-----|-------------|
| `/dashboard/` | Redirect to active business |
| `/dashboard/<slug>/` | Dashboard home |
| `/dashboard/<slug>/reviews/` | Reviews list with filters |
| `/dashboard/<slug>/replies/` | Reply management |
| `/dashboard/<slug>/qrcodes/` | QR code generator |
| `/dashboard/<slug>/gifts/` | Gift card management + counter verify |
| `/dashboard/<slug>/settings/` | Business settings |
| `/business/new/` | Add new business |
| `/onboarding/` | First-time setup |

### API (JSON)
| URL | Description |
|-----|-------------|
| `/dashboard/<slug>/replies/<id>/save/` | Save reply edits |
| `/dashboard/<slug>/replies/<id>/send/` | Approve and send |
| `/dashboard/<slug>/replies/<id>/regenerate/` | Regenerate with AI |
| `/api/auth/google/<biz_id>/` | Google OAuth init |
| `/api/auth/google/callback/` | Google OAuth callback |

---

## Key Features

### Multi-tenant Architecture
- Each user owns multiple businesses
- All data is owner-scoped — no cross-business data leaks
- Slug-based URLs instead of raw UUIDs

### Customer Review Journey
1. Customer scans QR code → review page loads
2. Star rating → AI generates contextual chips (adapts positive/negative by category)
3. Tap chips → AI drafts full review text in one click
4. Submit → real-time sentiment analysis
5. Positive (4-5★) → Gift card shown instantly
6. Negative (1-2★) → Escalated to manager, contact info shown

### AI Auto-Reply Engine
- Generates personalised replies the moment a review is submitted
- **Language detection**: 12+ scripts (Hindi, Arabic, Chinese, Japanese…) + Claude for Latin scripts
- **Category templates**: distinct voice per business type (Café, Restaurant, Hotel, Salon, Gym)
- **Auto-send**: 4-5★ positive reviews skip the approval queue
- **Fallback**: smart rule-based templates when `ANTHROPIC_API_KEY` is not set
- **Regenerate**: owner can regenerate with one click from the dashboard

### Gift Card System
- Business owner configures gift cards (title, value, icon, color, type)
- Random gift assigned on positive review
- Customer sees animated gift card with unique claim code
- Staff verification tool: enter claim code at counter → one-click redeem

---

## Production Deployment (Render / Railway / Heroku)

```bash
# 1. Set environment variables in your platform
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
ANTHROPIC_API_KEY=...   # optional

# 2. Run on deploy
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# 3. The Procfile starts gunicorn automatically
```

---

## Google Business Profile Integration

1. Create project at [console.cloud.google.com](https://console.cloud.google.com)
2. Enable **Google My Business API** and **Places API**
3. Create OAuth 2.0 credentials (Web application)
4. Add redirect URI: `https://yourdomain.com/api/auth/google/callback/`
5. Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` in `.env`
6. In **Settings → Google Business Profile** → click "Connect Google Business"
7. Set your **Google Place ID** to enable the correct review URL

Once connected, replies are POSTed directly to Google Maps via the API.
