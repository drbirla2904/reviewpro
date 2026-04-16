"""
Category theme data — passed to the review template.
Each theme defines:
  - colors (bg, accent, text)
  - stickers: list of SVG inline strings placed as decorative elements
  - font style suggestion
"""

THEMES = {
    'cafe': {
        'bg':        '#1a0d00',
        'bg2':       '#2a1500',
        'accent':    '#e8820c',
        'accent2':   '#f5a623',
        'text':      '#fff8f0',
        'text2':     '#c8855a',
        'border':    'rgba(232,130,12,.22)',
        'glow':      'rgba(232,130,12,.28)',
        'font':      "'Playfair Display', serif",
        'label':     'Coffee & Café',
        # SVG stickers drawn inline — coffee cup, beans, steam
        'stickers': [
            # Coffee cup — top right
            {'x':'78%','y':'8%','size':'90px','delay':'0s','dur':'6s','svg':'''
<svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- steam lines -->
  <path d="M28 18 Q30 12 28 6" stroke="#e8820c" stroke-width="2" stroke-linecap="round" opacity=".6"/>
  <path d="M36 18 Q38 11 36 4" stroke="#f5a623" stroke-width="2" stroke-linecap="round" opacity=".5"/>
  <path d="M44 18 Q46 12 44 6" stroke="#e8820c" stroke-width="2" stroke-linecap="round" opacity=".6"/>
  <!-- cup body -->
  <path d="M18 22 L24 60 H56 L62 22 Z" fill="#3d1a00" stroke="#e8820c" stroke-width="1.5"/>
  <!-- liquid surface -->
  <ellipse cx="40" cy="22" rx="22" ry="4" fill="#7a3d00" stroke="#e8820c" stroke-width="1"/>
  <!-- coffee surface -->
  <ellipse cx="40" cy="22" rx="18" ry="2.5" fill="#5a2d00"/>
  <!-- handle -->
  <path d="M62 30 Q74 30 74 40 Q74 50 62 50" stroke="#e8820c" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <!-- saucer -->
  <ellipse cx="40" cy="62" rx="28" ry="5" fill="#3d1a00" stroke="#e8820c" stroke-width="1"/>
</svg>'''},
            # Coffee beans — bottom left
            {'x':'-5%','y':'72%','size':'80px','delay':'1.5s','dur':'8s','svg':'''
<svg viewBox="0 0 70 70" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="20" cy="25" rx="12" ry="8" fill="#3d1a00" stroke="#e8820c" stroke-width="1.5" transform="rotate(-20 20 25)"/>
  <path d="M14 22 Q20 25 26 28" stroke="#e8820c" stroke-width="1" stroke-linecap="round" transform="rotate(-20 20 25)" opacity=".7"/>
  <ellipse cx="45" cy="20" rx="11" ry="7" fill="#2d1200" stroke="#f5a623" stroke-width="1.5" transform="rotate(15 45 20)"/>
  <path d="M39 17 Q45 20 51 23" stroke="#f5a623" stroke-width="1" stroke-linecap="round" transform="rotate(15 45 20)" opacity=".7"/>
  <ellipse cx="35" cy="48" rx="13" ry="8.5" fill="#3d1a00" stroke="#e8820c" stroke-width="1.5" transform="rotate(5 35 48)"/>
  <path d="M28 46 Q35 49 42 52" stroke="#e8820c" stroke-width="1" stroke-linecap="round" transform="rotate(5 35 48)" opacity=".7"/>
</svg>'''},
            # Spoon — scattered
            {'x':'85%','y':'55%','size':'50px','delay':'2s','dur':'8s','svg':'''
<svg viewBox="0 0 30 80" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="15" cy="12" rx="10" ry="11" fill="#3d1a00" stroke="#e8820c" stroke-width="1.5"/>
  <rect x="13" y="23" width="4" height="48" rx="2" fill="#3d1a00" stroke="#e8820c" stroke-width="1.2"/>
</svg>'''},
        ],
    },

    'restaurant': {
        'bg':        '#0e0800',
        'bg2':       '#1c0f00',
        'accent':    '#c0392b',
        'accent2':   '#e74c3c',
        'text':      '#fff5f0',
        'text2':     '#c07060',
        'border':    'rgba(192,57,43,.22)',
        'glow':      'rgba(192,57,43,.28)',
        'font':      "'Lora', serif",
        'label':     'Restaurant & Dining',
        'stickers': [
            # Chef hat — top right
            {'x':'72%','y':'4%','size':'100px','delay':'0s','dur':'6s','svg':'''
<svg viewBox="0 0 90 80" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- hat body -->
  <path d="M15 55 Q15 35 45 28 Q75 35 75 55 Z" fill="#1c0f00" stroke="#c0392b" stroke-width="1.5"/>
  <!-- hat top puff -->
  <ellipse cx="45" cy="25" rx="22" ry="22" fill="#1c0f00" stroke="#c0392b" stroke-width="1.5"/>
  <ellipse cx="30" cy="32" rx="14" ry="14" fill="#1c0f00" stroke="#c0392b" stroke-width="1.2"/>
  <ellipse cx="60" cy="32" rx="14" ry="14" fill="#1c0f00" stroke="#c0392b" stroke-width="1.2"/>
  <!-- brim -->
  <rect x="10" y="53" width="70" height="10" rx="3" fill="#1c0f00" stroke="#c0392b" stroke-width="1.5"/>
  <!-- stripe -->
  <rect x="10" y="57" width="70" height="3" rx="1" fill="#c0392b" opacity=".3"/>
</svg>'''},
            # Fork & knife — left
            {'x':'-2%','y':'60%','size':'70px','delay':'1s','dur':'8s','svg':'''
<svg viewBox="0 0 50 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- fork -->
  <rect x="8" y="45" width="3" height="40" rx="1.5" fill="#3d1a00" stroke="#c0392b" stroke-width="1"/>
  <rect x="8" y="10" width="2" height="22" rx="1" fill="#3d1a00" stroke="#c0392b" stroke-width="1"/>
  <rect x="13" y="10" width="2" height="18" rx="1" fill="#3d1a00" stroke="#c0392b" stroke-width="1"/>
  <rect x="18" y="10" width="2" height="22" rx="1" fill="#3d1a00" stroke="#c0392b" stroke-width="1"/>
  <path d="M8 32 Q13 36 18 32" fill="#3d1a00" stroke="#c0392b" stroke-width="1"/>
  <!-- knife -->
  <rect x="28" y="10" width="3" height="75" rx="1.5" fill="#3d1a00" stroke="#e74c3c" stroke-width="1"/>
  <path d="M31 10 Q40 15 31 35" fill="#3d1a00" stroke="#e74c3c" stroke-width="1"/>
</svg>'''},
            # Plate with food — bottom right
            {'x':'75%','y':'68%','size':'85px','delay':'2s','dur':'8s','svg':'''
<svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="40" cy="40" rx="36" ry="36" fill="#1c0f00" stroke="#c0392b" stroke-width="1.5"/>
  <ellipse cx="40" cy="40" rx="28" ry="28" fill="#150a00" stroke="#c0392b" stroke-width=".8" opacity=".6"/>
  <!-- food on plate -->
  <ellipse cx="35" cy="37" rx="10" ry="7" fill="#4a1a00" stroke="#e74c3c" stroke-width="1" transform="rotate(-10 35 37)"/>
  <ellipse cx="47" cy="43" rx="8" ry="6" fill="#3d1500" stroke="#c0392b" stroke-width="1" transform="rotate(15 47 43)"/>
  <circle cx="33" cy="45" r="4" fill="#2d0f00" stroke="#e74c3c" stroke-width="1"/>
  <!-- steam -->
  <path d="M38 28 Q40 23 38 18" stroke="#c0392b" stroke-width="1.5" stroke-linecap="round" opacity=".5"/>
  <path d="M44 26 Q46 20 44 15" stroke="#e74c3c" stroke-width="1.5" stroke-linecap="round" opacity=".4"/>
</svg>'''},
        ],
    },

    'salon': {
        'bg':        '#120018',
        'bg2':       '#1e0028',
        'accent':    '#c026a0',
        'accent2':   '#e040b0',
        'text':      '#fff0fc',
        'text2':     '#cc80bb',
        'border':    'rgba(192,38,160,.22)',
        'glow':      'rgba(192,38,160,.32)',
        'font':      "'Cormorant Garamond', serif",
        'label':     'Salon & Beauty',
        'stickers': [
            # Scissors — top right
            {'x':'74%','y':'5%','size':'95px','delay':'0s','dur':'6s','svg':'''
<svg viewBox="0 0 80 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- blade 1 -->
  <path d="M40 45 L10 10" stroke="#c026a0" stroke-width="3" stroke-linecap="round"/>
  <circle cx="14" cy="14" r="10" fill="#1e0028" stroke="#c026a0" stroke-width="2"/>
  <circle cx="14" cy="14" r="5" fill="#1e0028" stroke="#e040b0" stroke-width="1.5"/>
  <!-- blade 2 -->
  <path d="M40 45 L70 10" stroke="#e040b0" stroke-width="3" stroke-linecap="round"/>
  <circle cx="66" cy="14" r="10" fill="#1e0028" stroke="#e040b0" stroke-width="2"/>
  <circle cx="66" cy="14" r="5" fill="#1e0028" stroke="#c026a0" stroke-width="1.5"/>
  <!-- handle 1 -->
  <path d="M40 45 L20 80" stroke="#c026a0" stroke-width="2.5" stroke-linecap="round"/>
  <ellipse cx="17" cy="84" rx="8" ry="5" fill="#1e0028" stroke="#c026a0" stroke-width="2" transform="rotate(-30 17 84)"/>
  <!-- handle 2 -->
  <path d="M40 45 L55 80" stroke="#e040b0" stroke-width="2.5" stroke-linecap="round"/>
  <ellipse cx="58" cy="84" rx="8" ry="5" fill="#1e0028" stroke="#e040b0" stroke-width="2" transform="rotate(20 58 84)"/>
  <!-- screw -->
  <circle cx="40" cy="45" r="4" fill="#2a0038" stroke="#e040b0" stroke-width="1.5"/>
</svg>'''},
            # Nail polish — left
            {'x':'-4%','y':'55%','size':'75px','delay':'1.2s','dur':'8s','svg':'''
<svg viewBox="0 0 40 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- bottle body -->
  <rect x="8" y="35" width="24" height="45" rx="5" fill="#1e0028" stroke="#c026a0" stroke-width="1.5"/>
  <!-- liquid inside -->
  <rect x="10" y="50" width="20" height="28" rx="3" fill="#3d0050" opacity=".8"/>
  <!-- cap -->
  <rect x="12" y="18" width="16" height="20" rx="3" fill="#2a0038" stroke="#e040b0" stroke-width="1.5"/>
  <!-- brush -->
  <rect x="19" y="5" width="2" height="15" fill="#c026a0"/>
  <path d="M18 20 Q20 25 22 20" fill="#e040b0" opacity=".8"/>
  <!-- shine -->
  <path d="M12 42 Q14 38 16 42" stroke="#e040b0" stroke-width="1" stroke-linecap="round" opacity=".6"/>
  <!-- sparkles -->
  <path d="M32 30 L34 28 M34 30 L32 28" stroke="#e040b0" stroke-width="1.2" stroke-linecap="round"/>
  <path d="M5 42 L7 40 M7 42 L5 40" stroke="#c026a0" stroke-width="1" stroke-linecap="round"/>
</svg>'''},
            # Mirror — bottom right
            {'x':'78%','y':'65%','size':'80px','delay':'2.5s','dur':'8s','svg':'''
<svg viewBox="0 0 70 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- mirror frame -->
  <ellipse cx="35" cy="32" rx="28" ry="30" fill="#1e0028" stroke="#c026a0" stroke-width="2"/>
  <!-- mirror glass -->
  <ellipse cx="35" cy="32" rx="22" ry="24" fill="#2a0038" stroke="#e040b0" stroke-width="1"/>
  <!-- reflection shimmer -->
  <path d="M22 20 Q26 16 30 20" stroke="#e040b0" stroke-width="1.5" stroke-linecap="round" opacity=".5"/>
  <path d="M24 26 Q27 23 30 26" stroke="#c026a0" stroke-width="1" stroke-linecap="round" opacity=".4"/>
  <!-- handle -->
  <rect x="30" y="62" width="10" height="22" rx="4" fill="#1e0028" stroke="#c026a0" stroke-width="1.5"/>
  <!-- base decoration -->
  <path d="M24 82 Q35 86 46 82" stroke="#e040b0" stroke-width="1.5" stroke-linecap="round"/>
</svg>'''},
            # Comb — scattered
            {'x':'60%','y':'75%','size':'55px','delay':'3s','dur':'8s','svg':'''
<svg viewBox="0 0 80 30" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="2" y="2" width="76" height="14" rx="7" fill="#1e0028" stroke="#c026a0" stroke-width="1.5"/>
  <line x1="15" y1="16" x2="15" y2="28" stroke="#e040b0" stroke-width="2" stroke-linecap="round"/>
  <line x1="23" y1="16" x2="23" y2="28" stroke="#c026a0" stroke-width="2" stroke-linecap="round"/>
  <line x1="31" y1="16" x2="31" y2="28" stroke="#e040b0" stroke-width="2" stroke-linecap="round"/>
  <line x1="39" y1="16" x2="39" y2="28" stroke="#c026a0" stroke-width="2" stroke-linecap="round"/>
  <line x1="47" y1="16" x2="47" y2="28" stroke="#e040b0" stroke-width="2" stroke-linecap="round"/>
  <line x1="55" y1="16" x2="55" y2="28" stroke="#c026a0" stroke-width="2" stroke-linecap="round"/>
  <line x1="63" y1="16" x2="63" y2="28" stroke="#e040b0" stroke-width="2" stroke-linecap="round"/>
</svg>'''},
        ],
    },

    'gym': {
        'bg':        '#000e0e',
        'bg2':       '#001818',
        'accent':    '#00897b',
        'accent2':   '#26a69a',
        'text':      '#f0fffc',
        'text2':     '#50b8b0',
        'border':    'rgba(0,137,123,.25)',
        'glow':      'rgba(0,137,123,.3)',
        'font':      "'Barlow Condensed', sans-serif",
        'label':     'Gym & Fitness',
        'stickers': [
            # Dumbbell — top right
            {'x':'70%','y':'4%','size':'110px','delay':'0s','dur':'6s','svg':'''
<svg viewBox="0 0 110 50" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- left plates -->
  <rect x="2" y="8" width="16" height="34" rx="4" fill="#001818" stroke="#00897b" stroke-width="2"/>
  <rect x="12" y="12" width="10" height="26" rx="3" fill="#001818" stroke="#26a69a" stroke-width="1.5"/>
  <!-- bar -->
  <rect x="22" y="21" width="66" height="8" rx="3" fill="#001818" stroke="#00897b" stroke-width="1.5"/>
  <!-- right plates -->
  <rect x="82" y="12" width="10" height="26" rx="3" fill="#001818" stroke="#26a69a" stroke-width="1.5"/>
  <rect x="92" y="8" width="16" height="34" rx="4" fill="#001818" stroke="#00897b" stroke-width="2"/>
</svg>'''},
            # Lightning bolt — motivational
            {'x':'-3%','y':'45%','size':'65px','delay':'0.8s','dur':'8s','svg':'''
<svg viewBox="0 0 40 80" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M28 4 L8 44 L20 44 L12 76 L36 32 L22 32 Z" fill="#001818" stroke="#00897b" stroke-width="2" stroke-linejoin="round"/>
  <path d="M28 4 L8 44 L20 44 L12 76 L36 32 L22 32 Z" fill="#00897b" opacity=".15"/>
</svg>'''},
            # Kettle bell — bottom right
            {'x':'76%','y':'65%','size':'80px','delay':'1.8s','dur':'8s','svg':'''
<svg viewBox="0 0 70 80" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- handle -->
  <path d="M20 28 Q20 8 35 8 Q50 8 50 28" fill="none" stroke="#00897b" stroke-width="4" stroke-linecap="round"/>
  <!-- body -->
  <ellipse cx="35" cy="50" rx="28" ry="26" fill="#001818" stroke="#00897b" stroke-width="2"/>
  <!-- shine -->
  <path d="M22 38 Q26 34 30 38" stroke="#26a69a" stroke-width="1.5" stroke-linecap="round" opacity=".5"/>
  <!-- flat base -->
  <ellipse cx="35" cy="74" rx="18" ry="4" fill="#001818" stroke="#26a69a" stroke-width="1" opacity=".5"/>
</svg>'''},
        ],
    },

    'hotel': {
        'bg':        '#00080e',
        'bg2':       '#001020',
        'accent':    '#1565c0',
        'accent2':   '#1976d2',
        'text':      '#f0f6ff',
        'text2':     '#6090cc',
        'border':    'rgba(21,101,192,.25)',
        'glow':      'rgba(21,101,192,.3)',
        'font':      "'EB Garamond', serif",
        'label':     'Hotel & Hospitality',
        'stickers': [
            # Building/hotel — top right
            {'x':'70%','y':'3%','size':'95px','delay':'0s','dur':'6s','svg':'''
<svg viewBox="0 0 80 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- main building -->
  <rect x="15" y="20" width="50" height="70" rx="2" fill="#001020" stroke="#1565c0" stroke-width="1.5"/>
  <!-- roof triangles -->
  <path d="M15 20 L40 5 L65 20" fill="#001020" stroke="#1976d2" stroke-width="1.5"/>
  <!-- windows row 1 -->
  <rect x="22" y="28" width="10" height="10" rx="1" fill="#001835" stroke="#1976d2" stroke-width="1"/>
  <rect x="35" y="28" width="10" height="10" rx="1" fill="#001835" stroke="#1565c0" stroke-width="1"/>
  <rect x="48" y="28" width="10" height="10" rx="1" fill="#001835" stroke="#1976d2" stroke-width="1"/>
  <!-- windows row 2 -->
  <rect x="22" y="44" width="10" height="10" rx="1" fill="#001835" stroke="#1565c0" stroke-width="1"/>
  <rect x="35" y="44" width="10" height="10" rx="1" fill="#001835" stroke="#1976d2" stroke-width="1"/>
  <rect x="48" y="44" width="10" height="10" rx="1" fill="#001835" stroke="#1565c0" stroke-width="1"/>
  <!-- door -->
  <rect x="31" y="72" width="18" height="18" rx="2" fill="#001835" stroke="#1976d2" stroke-width="1.2"/>
  <circle cx="44" cy="81" r="1.5" fill="#1976d2"/>
  <!-- star on roof -->
  <path d="M40 7 L41.5 11.5 L46 11.5 L42.5 14 L44 18.5 L40 16 L36 18.5 L37.5 14 L34 11.5 L38.5 11.5 Z" fill="#1976d2" opacity=".7"/>
</svg>'''},
            # Key — left
            {'x':'-3%','y':'58%','size':'72px','delay':'1.2s','dur':'8s','svg':'''
<svg viewBox="0 0 40 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="20" cy="22" r="17" fill="#001020" stroke="#1565c0" stroke-width="2"/>
  <circle cx="20" cy="22" r="9" fill="#001020" stroke="#1976d2" stroke-width="1.5"/>
  <rect x="17" y="39" width="6" height="44" rx="2" fill="#001020" stroke="#1565c0" stroke-width="1.5"/>
  <rect x="23" y="56" width="8" height="5" rx="1" fill="#001020" stroke="#1976d2" stroke-width="1.2"/>
  <rect x="23" y="67" width="6" height="5" rx="1" fill="#001020" stroke="#1565c0" stroke-width="1.2"/>
</svg>'''},
            # Bell concierge — bottom right
            {'x':'76%','y':'66%','size':'75px','delay':'2s','dur':'8s','svg':'''
<svg viewBox="0 0 70 80" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- bell dome -->
  <path d="M10 50 Q10 20 35 15 Q60 20 60 50 Z" fill="#001020" stroke="#1565c0" stroke-width="1.8"/>
  <!-- clapper -->
  <line x1="35" y1="50" x2="35" y2="60" stroke="#1976d2" stroke-width="2"/>
  <circle cx="35" cy="63" r="4" fill="#001020" stroke="#1976d2" stroke-width="1.5"/>
  <!-- base -->
  <rect x="6" y="50" width="58" height="6" rx="3" fill="#001020" stroke="#1565c0" stroke-width="1.5"/>
  <!-- handle top -->
  <circle cx="35" cy="15" r="4" fill="#001020" stroke="#1976d2" stroke-width="1.5"/>
  <!-- shimmer -->
  <path d="M18 32 Q21 28 24 32" stroke="#1976d2" stroke-width="1.2" stroke-linecap="round" opacity=".5"/>
</svg>'''},
        ],
    },

    'bakery': {
        'bg':        '#140800',
        'bg2':       '#201200',
        'accent':    '#d4820a',
        'accent2':   '#f0a830',
        'text':      '#fffaf0',
        'text2':     '#c8a060',
        'border':    'rgba(212,130,10,.22)',
        'glow':      'rgba(212,130,10,.28)',
        'font':      "'Libre Baskerville', serif",
        'label':     'Bakery & Sweets',
        'stickers': [
            # Cupcake — top right
            {'x':'72%','y':'4%','size':'95px','delay':'0s','dur':'6s','svg':'''
<svg viewBox="0 0 80 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- frosting top -->
  <path d="M40 8 Q36 16 30 18 Q25 20 28 26 Q22 26 24 32 Q18 33 22 40 Q30 38 40 38 Q50 38 58 40 Q62 33 56 32 Q58 26 52 26 Q55 20 50 18 Q44 16 40 8 Z" fill="#201200" stroke="#d4820a" stroke-width="1.5"/>
  <!-- cherry on top -->
  <circle cx="40" cy="9" r="5" fill="#201200" stroke="#f0a830" stroke-width="1.5"/>
  <path d="M40 9 Q43 5 46 8" fill="none" stroke="#d4820a" stroke-width="1.2"/>
  <!-- cake body -->
  <path d="M18 42 L22 70 H58 L62 42 Q50 38 40 38 Q30 38 18 42 Z" fill="#201200" stroke="#d4820a" stroke-width="1.5"/>
  <!-- wrapper -->
  <path d="M18 42 Q40 46 62 42 Q60 48 40 52 Q20 48 18 42Z" fill="#2a1000" stroke="#f0a830" stroke-width="1"/>
  <!-- wrapper lines -->
  <line x1="25" y1="43" x2="22" y2="70" stroke="#d4820a" stroke-width="1" opacity=".4"/>
  <line x1="33" y1="44" x2="31" y2="70" stroke="#d4820a" stroke-width="1" opacity=".4"/>
  <line x1="40" y1="45" x2="40" y2="70" stroke="#f0a830" stroke-width="1" opacity=".4"/>
  <line x1="47" y1="44" x2="49" y2="70" stroke="#d4820a" stroke-width="1" opacity=".4"/>
  <line x1="55" y1="43" x2="58" y2="70" stroke="#d4820a" stroke-width="1" opacity=".4"/>
</svg>'''},
            # Rolling pin — left
            {'x':'-4%','y':'52%','size':'65px','delay':'1.4s','dur':'8s','svg':'''
<svg viewBox="0 0 30 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="11" y="2" width="8" height="14" rx="4" fill="#201200" stroke="#d4820a" stroke-width="1.5"/>
  <rect x="8" y="16" width="14" height="58" rx="6" fill="#201200" stroke="#f0a830" stroke-width="1.8"/>
  <line x1="14" y1="22" x2="14" y2="68" stroke="#d4820a" stroke-width=".8" opacity=".5"/>
  <line x1="18" y1="22" x2="18" y2="68" stroke="#f0a830" stroke-width=".8" opacity=".5"/>
  <rect x="11" y="74" width="8" height="14" rx="4" fill="#201200" stroke="#d4820a" stroke-width="1.5"/>
</svg>'''},
            # Stars/sprinkles scattered
            {'x':'78%','y':'62%','size':'60px','delay':'2.2s','dur':'8s','svg':'''
<svg viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M15 8 L16.5 12.5 L21 12.5 L17.5 15 L19 19.5 L15 17 L11 19.5 L12.5 15 L9 12.5 L13.5 12.5 Z" fill="#d4820a" opacity=".8"/>
  <path d="M45 20 L46 23 L49 23 L47 24.8 L48 28 L45 26 L42 28 L43 24.8 L41 23 L44 23 Z" fill="#f0a830" opacity=".7"/>
  <path d="M20 42 L21 45 L24 45 L22 46.8 L23 50 L20 48 L17 50 L18 46.8 L16 45 L19 45 Z" fill="#d4820a" opacity=".6"/>
  <path d="M48 42 L49.5 46.5 L54 46.5 L50.5 49 L52 53.5 L48 51 L44 53.5 L45.5 49 L42 46.5 L46.5 46.5 Z" fill="#f0a830" opacity=".75"/>
</svg>'''},
        ],
    },

    'clinic': {
        'bg':        '#000c14',
        'bg2':       '#001828',
        'accent':    '#0277bd',
        'accent2':   '#0288d1',
        'text':      '#f0f8ff',
        'text2':     '#5090b8',
        'border':    'rgba(2,119,189,.22)',
        'glow':      'rgba(2,119,189,.28)',
        'font':      "'Source Serif 4', serif",
        'label':     'Clinic & Healthcare',
        'stickers': [
            # Stethoscope — top right
            {'x':'68%','y':'4%','size':'100px','delay':'0s','dur':'6s','svg':'''
<svg viewBox="0 0 90 90" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- tube left -->
  <path d="M15 15 Q15 45 40 55 Q65 45 65 15" fill="none" stroke="#0277bd" stroke-width="3" stroke-linecap="round"/>
  <!-- ear pieces -->
  <circle cx="15" cy="12" r="6" fill="#001828" stroke="#0288d1" stroke-width="2"/>
  <circle cx="65" cy="12" r="6" fill="#001828" stroke="#0288d1" stroke-width="2"/>
  <!-- tube down -->
  <line x1="40" y1="55" x2="40" y2="75" stroke="#0277bd" stroke-width="3"/>
  <!-- chest piece -->
  <circle cx="40" cy="79" r="9" fill="#001828" stroke="#0288d1" stroke-width="2.5"/>
  <circle cx="40" cy="79" r="4" fill="#001828" stroke="#0277bd" stroke-width="1.5"/>
  <!-- cross on chest piece -->
  <line x1="40" y1="75" x2="40" y2="83" stroke="#0288d1" stroke-width="1.5"/>
  <line x1="36" y1="79" x2="44" y2="79" stroke="#0288d1" stroke-width="1.5"/>
</svg>'''},
            # Red cross — left
            {'x':'-3%','y':'55%','size':'65px','delay':'1s','dur':'8s','svg':'''
<svg viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="6" y="0" width="38" height="50" rx="8" fill="#001828" stroke="#0277bd" stroke-width="1.5"/>
  <rect x="0" y="6" width="50" height="38" rx="8" fill="#001828" stroke="#0277bd" stroke-width="1.5"/>
  <!-- red cross fill -->
  <rect x="8" y="2" width="34" height="46" rx="6" fill="#0277bd" opacity=".12"/>
  <rect x="2" y="8" width="46" height="34" rx="6" fill="#0277bd" opacity=".12"/>
  <line x1="25" y1="12" x2="25" y2="38" stroke="#0288d1" stroke-width="3" stroke-linecap="round"/>
  <line x1="12" y1="25" x2="38" y2="25" stroke="#0288d1" stroke-width="3" stroke-linecap="round"/>
</svg>'''},
            # Pill capsule — bottom right
            {'x':'76%','y':'64%','size':'75px','delay':'2s','dur':'8s','svg':'''
<svg viewBox="0 0 80 35" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="2" y="2" width="76" height="31" rx="15.5" fill="#001828" stroke="#0277bd" stroke-width="2"/>
  <path d="M40 2 L40 33" stroke="#0277bd" stroke-width="1.5" opacity=".4"/>
  <rect x="2" y="2" width="38" height="31" rx="15.5" fill="#0277bd" opacity=".2"/>
  <rect x="4" y="4" width="34" height="27" rx="13.5" fill="#0277bd" opacity=".1"/>
</svg>'''},
        ],
    },

    'default': {
        'bg':        '#0b0b14',
        'bg2':       '#10101c',
        'accent':    '#6366f1',
        'accent2':   '#8b5cf6',
        'text':      '#eeedf0',
        'text2':     '#9ca3af',
        'border':    'rgba(99,102,241,.22)',
        'glow':      'rgba(99,102,241,.28)',
        'font':      "'Inter', sans-serif",
        'label':     'Business',
        'stickers': [
            # Star burst
            {'x':'72%','y':'5%','size':'80px','delay':'0s','dur':'6s','svg':'''
<svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M40 5 L44 32 L70 28 L50 45 L62 70 L40 55 L18 70 L30 45 L10 28 L36 32 Z" fill="#10101c" stroke="#6366f1" stroke-width="1.8"/>
  <path d="M40 15 L43 34 L60 31 L47 42 L55 62 L40 51 L25 62 L33 42 L20 31 L37 34 Z" fill="#6366f1" opacity=".1"/>
</svg>'''},
            # Thumbs up
            {'x':'-3%','y':'58%','size':'65px','delay':'1.5s','dur':'8s','svg':'''
<svg viewBox="0 0 50 60" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M20 28 L14 28 L10 52 H38 L42 28 H30 L32 12 Q32 6 26 6 Q22 6 22 12 Z" fill="#10101c" stroke="#6366f1" stroke-width="1.8"/>
  <rect x="4" y="28" width="10" height="24" rx="3" fill="#10101c" stroke="#8b5cf6" stroke-width="1.5"/>
</svg>'''},
        ],
    },
}

def get_theme(category: str) -> dict:
    """Return theme dict for a given category string."""
    cat = category.lower().strip()
    if any(k in cat for k in ['cafe','coffee','bar','pub','tea','juice','canteen']):
        return THEMES['cafe']
    if any(k in cat for k in ['restaurant','dining','food','dhaba','bistro','eatery','kitchen']):
        return THEMES['restaurant']
    if any(k in cat for k in ['salon','beauty','hair','nail','barbershop','parlour']):
        return THEMES['salon']
    if any(k in cat for k in ['gym','fitness','yoga','crossfit','health club']):
        return THEMES['gym']
    if any(k in cat for k in ['hotel','resort','hostel','motel','inn','lodge']):
        return THEMES['hotel']
    if any(k in cat for k in ['bakery','cake','pastry','patisserie','confectionery']):
        return THEMES['bakery']
    if any(k in cat for k in ['clinic','doctor','hospital','dental','pharmacy','healthcare','nursing']):
        return THEMES['clinic']
    return THEMES['default']