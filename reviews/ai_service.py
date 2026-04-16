"""
AI service — sentiment analysis, language detection, chip suggestions, auto-reply.

Chips are now category-specific and FIXED (not AI-generated randomly).
They are curated per business category and rating level so they are
always relevant, professional, and consistent.
"""
import json, urllib.request
from django.conf import settings

# ── Sentiment word banks ────────────────────────────────────────────────────
POS_WORDS = {
    'great','amazing','excellent','fantastic','wonderful','love','best','perfect',
    'awesome','good','friendly','clean','fast','delicious','helpful','brilliant',
    'superb','outstanding','impressive','recommend','pleasant','enjoyed','happy',
    'satisfied','quality','professional','efficient','polite','comfortable',
}
NEG_WORDS = {
    'bad','terrible','awful','horrible','worst','hate','dirty','slow','rude','poor',
    'disappointing','disgusting','waste','overpriced','cold','stale','broken',
    'never','pathetic','unhelpful','unprofessional','unclean','filthy','noisy',
    'late','wrong','missing','ignored','waited','damaged',
}

# ── Script detection for language ───────────────────────────────────────────
_SCRIPT_RANGES = [
    ('Hindi',    0x0900, 0x097F), ('Arabic',  0x0600, 0x06FF),
    ('Chinese',  0x4E00, 0x9FFF), ('Japanese',0x3040, 0x30FF),
    ('Korean',   0xAC00, 0xD7AF), ('Cyrillic',0x0400, 0x04FF),
    ('Greek',    0x0370, 0x03FF), ('Hebrew',  0x0590, 0x05FF),
    ('Thai',     0x0E00, 0x0E7F), ('Bengali', 0x0980, 0x09FF),
    ('Tamil',    0x0B80, 0x0BFF), ('Telugu',  0x0C00, 0x0C7F),
]
_SCRIPT_LANG = {
    'Hindi':'Hindi','Arabic':'Arabic','Chinese':'Simplified Chinese',
    'Japanese':'Japanese','Korean':'Korean','Cyrillic':'Russian',
    'Greek':'Greek','Hebrew':'Hebrew','Thai':'Thai',
    'Bengali':'Bengali','Tamil':'Tamil','Telugu':'Telugu',
}

# ── FIXED chips per category — curated, not AI-generated ───────────────────
# These are consistent, professional, and relevant for each business type.
# Positive = what went well | Negative = what could be better
CHIPS = {
    'Cafe': {
        'positive': [
            'Great coffee taste', 'Friendly & welcoming staff', 'Cozy & comfortable atmosphere',
            'Good value for money', 'Fast & efficient service', 'Clean & hygienic space',
            'Nice seating & ambience', 'Good food & snack options', 'Great WiFi',
            'Loved the cold brew', 'Perfect for working', 'Good loyalty programme',
        ],
        'negative': [
            'Long waiting time', 'Overpriced for quality', 'Coffee taste was average',
            'Staff was unfriendly', 'Too noisy & crowded', 'Limited seating available',
            'Service was slow', 'Not clean enough', 'Poor WiFi connection',
            'Limited food options', 'Uncomfortable seating', 'Small portion size',
        ],
    },
    'Restaurant': {
        'positive': [
            'Delicious & flavorful food', 'Generous portion sizes', 'Friendly & attentive staff',
            'Great value for money', 'Clean & well-maintained', 'Quick table service',
            'Beautiful ambience & decor', 'Wide variety on menu', 'Fresh ingredients used',
            'Good veg & non-veg options', 'Great dessert selection', 'Easy parking nearby',
        ],
        'negative': [
            'Long wait for food', 'Food was cold when served', 'Overpriced for portions',
            'Staff was rude or inattentive', 'Small portion sizes', 'Hygiene concerns',
            'Service was very slow', 'Incorrect order received', 'Limited menu variety',
            'Noisy & uncomfortable', 'No good parking', 'Not worth the price',
        ],
    },
    'Hotel': {
        'positive': [
            'Clean & comfortable rooms', 'Helpful & courteous staff', 'Excellent location',
            'Good breakfast included', 'Smooth & quick check-in', 'Great amenities',
            'Quiet & peaceful stay', 'Good security & safety', 'Spacious rooms',
            'Great pool & gym facility', 'Good room service', 'Excellent housekeeping',
        ],
        'negative': [
            'Room was not clean', 'Unhelpful & rude staff', 'Poor location',
            'Bad breakfast quality', 'Slow & delayed check-in', 'Poor amenities',
            'Very noisy rooms', 'Overpriced for quality', 'Small & cramped rooms',
            'No hot water', 'Poor room service', 'Bed was uncomfortable',
        ],
    },
    'Salon': {
        'positive': [
            'Skilled & experienced stylists', 'Very clean & hygienic', 'Excellent results',
            'Friendly & helpful staff', 'Reasonable & fair pricing', 'On-time service',
            'Relaxing & pleasant experience', 'Good quality products used',
            'Great hair cut & styling', 'Loved the facial treatment',
            'Professional & attentive', 'Easy appointment booking',
        ],
        'negative': [
            'Not happy with results', 'Had to wait too long', 'Overpriced services',
            'Hygiene was a concern', 'Staff was rough & careless', 'Unfriendly attitude',
            'Service took very long', 'Wrong style or colour done',
            'Poor quality products', 'Not professional enough',
            'Difficult to book appointment', 'Not worth the price',
        ],
    },
    'Gym': {
        'positive': [
            'Good & modern equipment', 'Clean & well-maintained', 'Helpful & knowledgeable trainers',
            'Motivating atmosphere', 'Reasonable membership fees', 'Convenient timing & hours',
            'Good variety of machines', 'Great group classes', 'Spacious workout area',
            'Good locker & shower facility', 'Helpful staff', 'Good cardio section',
        ],
        'negative': [
            'Old & broken equipment', 'Too overcrowded', 'Hygiene & cleanliness issues',
            'Trainers not helpful', 'Limited opening hours', 'Too expensive',
            'Poor ventilation & AC', 'Not enough equipment', 'Dirty locker rooms',
            'Too noisy', 'Difficult to park', 'Poor customer service',
        ],
    },
    'Bakery': {
        'positive': [
            'Very fresh baked goods', 'Great variety of items', 'Tasty & delicious products',
            'Friendly & helpful staff', 'Reasonable prices', 'Clean & tidy shop',
            'Good quality ingredients', 'Beautiful presentation', 'Loved the sourdough',
            'Great birthday cakes', 'Good custom order service', 'Daily fresh stock',
        ],
        'negative': [
            'Products not fresh', 'Limited variety available', 'Overpriced items',
            'Taste was disappointing', 'Unfriendly staff', 'Shop was not clean',
            'Small portion sizes', 'Inconsistent quality', 'Dry & stale products',
            'Long wait time', 'Custom orders not done well', 'Not worth the price',
        ],
    },
    'Clinic': {
        'positive': [
            'Professional & experienced doctors', 'Clean & hygienic facility',
            'Short waiting time', 'Helpful & caring staff', 'Accurate diagnosis',
            'Affordable consultation fees', 'Thorough examination done',
            'Good follow-up care', 'Clear explanation of treatment',
            'Good medical equipment', 'Easy appointment booking', 'Friendly environment',
        ],
        'negative': [
            'Very long waiting time', 'Expensive consultation fees',
            'Staff was unhelpful & rude', 'Diagnosis was not accurate',
            'Facility not clean', 'Rushed & brief consultation',
            'Difficult to book appointment', 'Poor follow-up', 'No clear explanation',
            'Overcrowded waiting area', 'Poor communication', 'Not satisfied with treatment',
        ],
    },
    'Retail': {
        'positive': [
            'Wide product variety', 'Helpful & knowledgeable staff', 'Good & fair pricing',
            'Clean & organised store', 'Easy to find products', 'Good quality products',
            'Quick billing & checkout', 'Good return & exchange policy',
            'Attractive offers & discounts', 'Good stock availability',
            'Pleasant shopping experience', 'Good loyalty rewards',
        ],
        'negative': [
            'Limited product variety', 'Overpriced items', 'Unhelpful staff',
            'Messy & unorganised store', 'Items hard to find', 'Poor product quality',
            'Long billing queue', 'Poor return policy', 'Out of stock items',
            'No good offers', 'Overcrowded store', 'Staff ignores customers',
        ],
    },
    'Pharmacy': {
        'positive': [
            'Medicines always available', 'Knowledgeable & helpful staff',
            'Good pricing', 'Clean & organised', 'Quick service',
            'Good variety of products', 'Helpful advice given',
            'Convenient location', 'Open late hours', 'Good generic options available',
        ],
        'negative': [
            'Medicines out of stock', 'Staff not knowledgeable', 'Overpriced',
            'Unhygienic', 'Long waiting time', 'Limited product range',
            'No proper advice given', 'Inconvenient location', 'Limited hours',
            'Poor customer service',
        ],
    },
    'School': {
        'positive': [
            'Excellent teaching quality', 'Safe & secure environment', 'Good infrastructure',
            'Caring & supportive teachers', 'Good extracurricular activities',
            'Strong academic results', 'Good communication with parents',
            'Clean & well-maintained campus', 'Good sports facilities',
            'Holistic development focus',
        ],
        'negative': [
            'Teaching quality is poor', 'Safety concerns', 'Poor infrastructure',
            'Teachers not caring', 'Limited activities', 'Poor academic results',
            'Poor communication with parents', 'Not clean', 'No sports facilities',
            'Too much homework pressure',
        ],
    },
    'Hospital': {
        'positive': [
            'Excellent doctors & specialists', 'Clean & hygienic facility',
            'Caring & attentive nurses', 'Short waiting time', 'Good diagnostic equipment',
            'Affordable treatment', 'Good emergency response', 'Clear treatment explanation',
            'Good post-operative care', 'Helpful support staff',
        ],
        'negative': [
            'Very long waiting time', 'Expensive treatment', 'Unhelpful staff',
            'Not clean', 'Poor emergency response', 'Overcrowded',
            'No clear communication', 'Poor post-operative care',
            'Diagnostic equipment not working', 'Billing issues',
        ],
    },
    'Spa': {
        'positive': [
            'Very relaxing experience', 'Skilled & professional therapists',
            'Clean & peaceful environment', 'Good range of treatments',
            'Excellent massage quality', 'Friendly & attentive staff',
            'Great ambience & aroma', 'Good value packages',
            'On-time appointments', 'Felt completely refreshed',
        ],
        'negative': [
            'Not relaxing at all', 'Inexperienced therapists', 'Not clean',
            'Limited treatment options', 'Rough & painful massage',
            'Unfriendly staff', 'Poor ambience', 'Overpriced',
            'Long waiting time', 'Appointment not honoured',
        ],
    },
}
# Default fallback
CHIPS['default'] = {
    'positive': [
        'Excellent service', 'Friendly & helpful staff', 'Clean & well-maintained',
        'Good value for money', 'Professional & courteous', 'Would highly recommend',
        'Very satisfied with experience', 'Exceeded my expectations',
        'Prompt & efficient', 'Great overall experience',
    ],
    'negative': [
        'Poor service quality', 'Unfriendly staff', 'Not clean',
        'Overpriced for value', 'Unprofessional behaviour', 'Would not recommend',
        'Below expectations', 'Very slow response', 'Lack of attention',
        'Not satisfied overall',
    ],
}

_CAT_NORMALIZE = {
    # Cafe variants
    'cafe': 'Cafe', 'café': 'Cafe', 'coffee': 'Cafe', 'coffee shop': 'Cafe',
    'tea shop': 'Cafe', 'canteen': 'Cafe', 'bar': 'Cafe', 'pub': 'Cafe',
    'juice bar': 'Cafe', 'bakery cafe': 'Cafe',
    # Restaurant variants
    'restaurant': 'Restaurant', 'dining': 'Restaurant', 'food': 'Restaurant',
    'dhaba': 'Restaurant', 'eatery': 'Restaurant', 'bistro': 'Restaurant',
    'fast food': 'Restaurant', 'food court': 'Restaurant', 'cloud kitchen': 'Restaurant',
    # Hotel variants
    'hotel': 'Hotel', 'hostel': 'Hotel', 'resort': 'Hotel', 'motel': 'Hotel',
    'guest house': 'Hotel', 'inn': 'Hotel', 'lodge': 'Hotel', 'b&b': 'Hotel',
    # Salon variants
    'salon': 'Salon', 'spa': 'Spa', 'barbershop': 'Salon', 'beauty': 'Salon',
    'hair salon': 'Salon', 'nail salon': 'Salon', 'beauty parlour': 'Salon',
    'unisex salon': 'Salon',
    # Gym variants
    'gym': 'Gym', 'fitness': 'Gym', 'crossfit': 'Gym', 'yoga': 'Gym',
    'fitness center': 'Gym', 'fitness centre': 'Gym', 'health club': 'Gym',
    # Bakery variants
    'bakery': 'Bakery', 'patisserie': 'Bakery', 'cake shop': 'Bakery',
    'pastry shop': 'Bakery', 'confectionery': 'Bakery',
    # Medical
    'clinic': 'Clinic', 'doctor': 'Clinic', 'healthcare': 'Clinic',
    'dental': 'Clinic', 'dentist': 'Clinic', 'eye clinic': 'Clinic',
    'hospital': 'Hospital', 'nursing home': 'Hospital', 'medical centre': 'Hospital',
    'pharmacy': 'Pharmacy', 'chemist': 'Pharmacy', 'medical store': 'Pharmacy',
    # Retail
    'retail': 'Retail', 'shop': 'Retail', 'store': 'Retail', 'boutique': 'Retail',
    'supermarket': 'Retail', 'grocery': 'Retail', 'clothing': 'Retail',
    'electronics': 'Retail', 'mobile shop': 'Retail', 'showroom': 'Retail',
    # Education
    'school': 'School', 'college': 'School', 'institute': 'School',
    'coaching': 'School', 'tuition': 'School', 'academy': 'School',
    # Other
    'other': 'default',
}


# ── Auto-reply templates per category ──────────────────────────────────────
# Structured, professional templates — one per category × sentiment.
# Placeholders: {name} {rating} {business} {highlight} {issue} {contact}
REPLY_TEMPLATES = {
    'Cafe': {
        'positive': (
            "Dear {name},\n\nThank you so much for your wonderful {rating}-star review! "
            "We are delighted that {highlight} made your visit special. "
            "Your kind words mean a lot to our entire team and motivate us to keep delivering our best every day. "
            "We look forward to welcoming you back to {business} very soon!\n\n"
            "Warm regards,\nThe {business} Team"
        ),
        'neutral': (
            "Dear {name},\n\nThank you for visiting {business} and taking the time to share your feedback. "
            "We appreciate your honest comments — they help us improve our service every day. "
            "We are committed to giving you a better experience on your next visit "
            "and hope to see you again soon.\n\n"
            "Best regards,\nThe {business} Team"
        ),
        'negative': (
            "Dear {name},\n\nThank you for your feedback. We sincerely apologise that your experience with {issue} "
            "did not meet the standards we hold ourselves to. "
            "This is not the experience we want for our valued customers. "
            "Please reach out to us at {contact} so we can understand what went wrong "
            "and make it right for you personally.\n\n"
            "Sincerely,\nThe {business} Team"
        ),
    },
    'Restaurant': {
        'positive': (
            "Dear {name},\n\nThank you for your generous {rating}-star review! "
            "We are so pleased that {highlight} stood out during your visit. "
            "Our team works hard every day to ensure every guest has a memorable experience, "
            "and it is truly rewarding to hear that we delivered. "
            "We hope to see you at {business} again very soon!\n\n"
            "With gratitude,\nThe {business} Team"
        ),
        'neutral': (
            "Dear {name},\n\nThank you for dining at {business} and sharing your experience with us. "
            "We value all feedback as it helps us continuously improve. "
            "We hope to have the opportunity to provide you with an even better experience on your next visit.\n\n"
            "Kind regards,\nThe {business} Team"
        ),
        'negative': (
            "Dear {name},\n\nWe sincerely apologise for the experience you had regarding {issue}. "
            "This is certainly not the standard we aim for at {business}. "
            "We take all feedback very seriously and would appreciate the chance to resolve this for you. "
            "Please contact us at {contact} and we will personally ensure this is addressed.\n\n"
            "Apologies,\nThe {business} Team"
        ),
    },
    'Hotel': {
        'positive': (
            "Dear {name},\n\nThank you for choosing {business} and for your lovely {rating}-star review! "
            "We are so glad that {highlight} made your stay comfortable and memorable. "
            "It is always a pleasure to host guests who appreciate our efforts. "
            "We look forward to welcoming you back whenever your travels bring you our way!\n\n"
            "Warm wishes,\nThe {business} Team"
        ),
        'neutral': (
            "Dear {name},\n\nThank you for staying at {business} and for sharing your feedback. "
            "We appreciate your candid comments and will use them to improve our services. "
            "We hope you will give us another opportunity to exceed your expectations.\n\n"
            "Best regards,\nThe {business} Team"
        ),
        'negative': (
            "Dear {name},\n\nWe sincerely apologise for the inconvenience caused during your stay, "
            "particularly regarding {issue}. Every guest deserves a comfortable and pleasant experience, "
            "and we clearly fell short on this occasion. "
            "Please contact us at {contact} so we can address your concerns directly.\n\n"
            "With apologies,\nThe {business} Team"
        ),
    },
    'Salon': {
        'positive': (
            "Dear {name},\n\nThank you for your wonderful {rating}-star review! "
            "We are so happy to hear that {highlight} made your visit a great experience. "
            "Our team is dedicated to making every customer feel their best, "
            "and your feedback truly inspires us. We look forward to seeing you again at {business}!\n\n"
            "With gratitude,\nThe {business} Team"
        ),
        'neutral': (
            "Dear {name},\n\nThank you for visiting {business} and for your honest feedback. "
            "We are always looking to improve and your input is very valuable to us. "
            "We hope your next visit will be an even better experience.\n\n"
            "Best regards,\nThe {business} Team"
        ),
        'negative': (
            "Dear {name},\n\nWe are truly sorry to hear that {issue} did not meet your expectations. "
            "Your satisfaction is very important to us and we would like to make this right. "
            "Please contact us at {contact} so we can address your concerns personally.\n\n"
            "Sincerely,\nThe {business} Team"
        ),
    },
    'Gym': {
        'positive': (
            "Dear {name},\n\nThank you for your great {rating}-star review! "
            "We are glad that {highlight} has been part of your fitness journey with us. "
            "Our team works hard to provide the best training environment, "
            "and your encouragement keeps us going. See you at the next session!\n\n"
            "The {business} Team"
        ),
        'neutral': (
            "Dear {name},\n\nThank you for your feedback about {business}. "
            "We appreciate you sharing your experience and will use it to improve our facilities and services. "
            "We look forward to supporting your fitness goals!\n\n"
            "The {business} Team"
        ),
        'negative': (
            "Dear {name},\n\nWe apologise that {issue} affected your experience at {business}. "
            "Every member deserves a clean, well-equipped, and supportive training environment. "
            "Please reach us at {contact} so we can address this directly.\n\n"
            "The {business} Team"
        ),
    },
}
_DEFAULT_REPLY = {
    'positive': (
        "Dear {name},\n\nThank you for your wonderful {rating}-star review! "
        "We are delighted that {highlight} made a positive impression. "
        "Your feedback motivates our team to continue delivering great service. "
        "We look forward to seeing you again at {business}!\n\n"
        "Warm regards,\nThe {business} Team"
    ),
    'neutral': (
        "Dear {name},\n\nThank you for your feedback about {business}. "
        "We appreciate you taking the time to share your experience "
        "and will use your comments to improve our services.\n\n"
        "Best regards,\nThe {business} Team"
    ),
    'negative': (
        "Dear {name},\n\nWe sincerely apologise that your experience did not meet your expectations, "
        "particularly regarding {issue}. "
        "Please contact us at {contact} so we can resolve this for you personally.\n\n"
        "Sincerely,\nThe {business} Team"
    ),
}


# ── Core helpers ─────────────────────────────────────────────────────────────

def _call_claude(prompt: str, max_tokens: int = 350) -> str | None:
    """Call Claude Haiku. Returns text or None on any failure."""
    key = settings.ANTHROPIC_API_KEY
    if not key:
        return None
    try:
        payload = json.dumps({
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }).encode()
        req = urllib.request.Request(
            'https://api.anthropic.com/v1/messages',
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'x-api-key': key,
                'anthropic-version': '2023-06-01',
            },
        )
        with urllib.request.urlopen(req, timeout=12) as r:
            return json.loads(r.read())['content'][0]['text'].strip()
    except Exception:
        return None


def _normalize_category(category: str) -> str:
    return _CAT_NORMALIZE.get(category.lower().strip(), 'default')


# ── Public API ────────────────────────────────────────────────────────────────

def analyze_sentiment(text: str, rating: int) -> tuple[str, float]:
    """Return (sentiment, confidence_score 0-1)."""
    tl = text.lower()
    pos = sum(1 for w in POS_WORDS if w in tl)
    neg = sum(1 for w in NEG_WORDS if w in tl)

    if rating >= 4:
        base = 0.7 + (rating - 4) * 0.15
    elif rating == 3:
        base = 0.5
    else:
        base = 0.15 + (rating - 1) * 0.05

    score = max(0.0, min(1.0, base + (pos - neg) * 0.05))

    if score >= 0.6:
        sentiment = 'positive'
    elif score <= 0.35:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return sentiment, round(score, 2)


def detect_language(text: str) -> str:
    """Detect language from script ranges first, then Claude for Latin scripts."""
    for name, lo, hi in _SCRIPT_RANGES:
        if sum(1 for c in text if lo <= ord(c) <= hi) > 3:
            return _SCRIPT_LANG[name]
    # For Latin-script text, ask Claude
    result = _call_claude(
        f"Detect the language of this text. Reply with ONLY the language name in English "
        f"(e.g. 'French', 'Spanish', 'English', 'Hindi'). Text: \"{text[:200]}\"",
        max_tokens=8,
    )
    if result:
        lang = result.strip().split()[0].rstrip('.,;').title()
        if lang.isalpha() and len(lang) <= 25:
            return lang
    return 'English'


def get_chips(business_name: str, category: str, rating: int) -> list:
    """
    Return fixed, curated chips for the business category and rating.
    These are NOT AI-generated — they are consistent and professional.
    """
    cat_key = _normalize_category(category)
    bucket = CHIPS.get(cat_key, CHIPS['default'])
    return bucket['positive'] if rating >= 4 else bucket['negative']


def suggest_review_text(chips: list, rating: int, business_name: str) -> str:
    """
    Generate a review text draft from selected chips.
    Uses Claude if available; falls back to a simple template.
    """
    if not chips:
        return ''

    if settings.ANTHROPIC_API_KEY:
        result = _call_claude(
            f"Write a natural, genuine 2-3 sentence Google review for '{business_name}' "
            f"({rating}/5 stars). The customer selected these highlights: {', '.join(chips)}. "
            f"Sound like a real customer, not a marketing copy. "
            f"Return ONLY the review text, nothing else.",
            max_tokens=180,
        )
        if result:
            return result

    # Fallback template
    joined = ' and '.join(chips[:2])
    if rating >= 4:
        return (
            f"Really pleased with my visit to {business_name}. "
            f"{joined} were highlights. Would definitely recommend and visit again!"
        )
    else:
        return (
            f"My visit to {business_name} was disappointing. "
            f"Issues with {joined}. Hope they improve in the future."
        )


def generate_auto_reply(
    business_name: str,
    category: str,
    reviewer_name: str,
    rating: int,
    review_text: str,
    sentiment: str,
    chips: list,
    contact: str = '',
    language: str = 'English',
) -> str:
    """
    Generate a professional owner reply to a review.

    Priority:
      1. Claude API — fully personalised, context-aware, language-aware
      2. Category template — structured, professional, filled with chips
    """
    name_part = reviewer_name.split()[0] if reviewer_name else 'Valued Customer'
    highlight = chips[0] if chips else 'your visit'
    issue     = chips[0] if chips else 'your experience'
    contact_str = contact or 'our team directly'

    # ── 1. Claude API reply ──────────────────────────────────────────────────
    if settings.ANTHROPIC_API_KEY:
        tone_map = {
            'positive': (
                'warm, professional and grateful. '
                'Thank them by first name. Mention the specific highlights they raised. '
                'Invite them back.'
            ),
            'neutral': (
                'professional and constructive. '
                'Acknowledge their feedback positively. '
                'Mention commitment to improvement. Invite them back.'
            ),
            'negative': (
                'sincere, empathetic and solution-focused. '
                'Apologise clearly. Address the specific issue they raised. '
                'Provide contact details for resolution. Keep it professional.'
            ),
        }
        prompt = (
            f"You are the owner of '{business_name}', a {category}.\n"
            f"Write a short, professional Google review reply (3-5 sentences).\n\n"
            f"Reviewer name: {reviewer_name or 'Anonymous'}\n"
            f"Star rating: {rating}/5\n"
            f"Review text: \"{review_text}\"\n"
            f"Key points raised: {', '.join(chips) if chips else 'general feedback'}\n"
            f"Contact for escalation: {contact_str}\n\n"
            f"Tone: {tone_map[sentiment]}\n"
            f"Language: Write the reply in {language}.\n"
            f"Format: Start with 'Dear {name_part},' and sign off with 'The {business_name} Team'.\n"
            f"Return ONLY the reply text. No preamble, no explanation."
        )
        result = _call_claude(prompt, max_tokens=350)
        if result:
            # If language is not English and Claude returned English, translate
            if language != 'English' and all(ord(c) < 128 for c in result[:50]):
                translated = _call_claude(
                    f"Translate the following text to {language}. "
                    f"Return ONLY the translated text:\n\n{result}",
                    max_tokens=400,
                )
                if translated:
                    return translated
            return result

    # ── 2. Category template fallback ────────────────────────────────────────
    cat_key = _normalize_category(category)
    templates = REPLY_TEMPLATES.get(cat_key, _DEFAULT_REPLY)
    template  = templates[sentiment]

    filled = template.format(
        name=name_part,
        rating=rating,
        business=business_name,
        highlight=highlight,
        issue=issue,
        contact=contact_str,
    )

    # Translate template if language is not English
    if language != 'English' and settings.ANTHROPIC_API_KEY:
        translated = _call_claude(
            f"Translate the following text to {language}. "
            f"Return ONLY the translated text:\n\n{filled}",
            max_tokens=400,
        )
        if translated:
            return translated

    return filled


def should_auto_send(rating: int, sentiment: str, business_setting: bool) -> bool:
    """Return True if reply should be auto-sent without manual approval."""
    return business_setting and rating >= 4 and sentiment == 'positive'


def post_reply_to_google(business, review_text: str) -> dict:
    """
    Attempt to post a reply to Google My Business API.
    Returns {'success': bool, 'error': str|None}

    NOTE: The Google My Business API requires:
    - A verified Google Business Profile
    - A review ID from the Google API (not our internal UUID)
    - Valid OAuth2 access token

    Without a real review_id from Google, this cannot post.
    The review_id must be obtained by first fetching reviews from the GMB API.
    """
    if not business.google_access_token:
        return {'success': False, 'error': 'Google Business Profile not connected'}

    if not business.google_place_id:
        return {'success': False, 'error': 'Google Place ID not set'}

    # In production, you would:
    # 1. Fetch reviews from GMB API to get the real review_id
    # 2. POST reply to: https://mybusiness.googleapis.com/v4/accounts/{account}/locations/{location}/reviews/{review_id}/reply
    # For now, we save the reply in our DB and mark it as approved.
    return {
        'success': False,
        'error': 'Direct Google posting requires fetching review IDs from GMB API first. Reply is saved in dashboard for manual posting.',
    }