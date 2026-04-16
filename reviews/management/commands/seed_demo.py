from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import User
from businesses.models import Business, GiftCard, QRCode
from reviews.models import Review
from reviews.ai_service import analyze_sentiment, generate_auto_reply, detect_language, should_auto_send
import random

class Command(BaseCommand):
    help = 'Seed demo data'
    def handle(self, *args, **kw):
        User.objects.filter(email='demo@reviewpro.app').delete()
        user = User.objects.create_user(username='demo@reviewpro.app', email='demo@reviewpro.app', password='demo1234', full_name='Rahul Sharma', plan='pro')
        biz = Business.objects.create(owner=user, name='Cafe Aroma', category='Cafe', address='12 Connaught Place', city='New Delhi', phone='+91 98765 43210', email='manager@cafearoma.in', logo_emoji='☕', google_place_id='ChIJdemo123', auto_send_positive_replies=True)
        gifts = [
            GiftCard.objects.create(business=biz,title='Free Coffee',description='Any hot or cold brew',gift_type='free_drink',value='180',icon='☕',color='orange'),
            GiftCard.objects.create(business=biz,title='20% Off',description='On your entire bill',gift_type='discount',value='20%',icon='🏷️',color='purple'),
            GiftCard.objects.create(business=biz,title='Free Dessert',description='Any slice or pastry',gift_type='free_dessert',value='150',icon='🍰',color='pink'),
            GiftCard.objects.create(business=biz,title='Store Credit',description='Credit for any purchase',gift_type='store_credit',value='100',icon='💳',color='green'),
        ]
        qr1 = QRCode.objects.create(business=biz, label='Main Entrance', token='demo-token-cafe-aroma-main')
        QRCode.objects.create(business=biz, label='Table QR', token='demo-token-cafe-aroma-table')
        samples = [
            (5,'The cappuccino was perfect and the staff was so friendly!',['Amazing coffee','Friendly staff'],'Priya S.'),
            (5,'Great ambience for working. Cold brew is a must try!',['Great wifi','Cozy ambience'],'Ananya K.'),
            (4,'Good coffee, quick service. Will visit again.',['Good coffee','Fast service'],'Rohan M.'),
            (2,'Waited 20 minutes for my order. Very slow service.',['Long wait time'],'Vikram T.'),
            (5,'Fresh pastries every morning, incredible staff!',['Fresh pastries','Friendly staff'],'Neha R.'),
            (3,'Coffee was okay but overpriced for the size.',['Overpriced'],'Amit J.'),
        ]
        for rating,text,chips,name in samples:
            sentiment,score = analyze_sentiment(text,rating)
            lang = detect_language(text)
            gift = random.choice(gifts) if (sentiment!='negative' and rating>=biz.min_rating_for_gift) else None
            if gift: gift.total_issued+=1; gift.save()
            reply = generate_auto_reply(biz.name,biz.category,name,rating,text,sentiment,chips,contact=biz.phone,language=lang)
            auto = should_auto_send(rating,sentiment,biz.auto_send_positive_replies)
            Review.objects.create(business=biz,qr_code=qr1,rating=rating,review_text=text,selected_chips=chips,reviewer_name=name,sentiment=sentiment,sentiment_score=score,detected_language=lang,status='escalated' if sentiment=='negative' else 'pending',is_verified=True,gift_issued=gift,auto_reply_text=reply,reply_edited_text=reply,reply_approved=auto,auto_reply_sent=auto,auto_reply_sent_at=timezone.now() if auto else None,reply_auto_sent_reason=f'Auto-sent: {rating}star {sentiment} (lang:{lang})' if auto else '')
        self.stdout.write(self.style.SUCCESS(f'Demo ready!\n  Login: demo@reviewpro.app / demo1234\n  Dashboard: http://localhost:8000/dashboard/{biz.slug}/\n  Review: http://localhost:8000/r/demo-token-cafe-aroma-main/\n  Admin: http://localhost:8000/admin/'))
