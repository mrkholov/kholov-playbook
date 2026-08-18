import zipfile, io, os
from PIL import Image

SRC = r'C:\Users\Kholov\Downloads\Playbook - Egor Kholov.pptx'
OUT = r'C:\Users\Kholov\Работа с VS Code\kholov-playbook\assets\img'
MAXW = 1500

MAP = {
    'image29.png': 'tankday-interview',
    'image30.png': 'tankday-crowd',
    'image34.jpg': 'tankday-aerial',
    'image37.jpg': 'tankday-stage',
    'image38.jpg': 'belavia-plane',
    'image57.jpg': 'belaz-front',
    'image40.jpg': 'belaz-side',
    'image32.jpg': 'navigator-splash',
    'image42.png': 'navigator-map',
    'image33.png': 'navigator-studio',
    'image35.png': 'field-logo',
    'image36.png': 'tiktok-creator',
    'image39.png': 'tiktok-key',
    'image41.png': 'tiktok-portrait',
    'image18.png': 'landing-generic',
    'image20.png': 'landing-personal',
    'image31.png': 'landing-winback',
    'image58.png': 'back-to-past-landing',
    'image45.png': 'back-to-past-heroes',
    'image48.png': 'back-to-past-scene',
    'image52.png': 'back-to-past-level',
    'image49.png': 'back-to-past-film',
    'image53.png': 'back-to-past-production',
    'image51.png': 'back-to-past-crew',
    'image44.png': 'soyuzmult-key',
    'image28.png': 'soyuzmult-iss',
    'image47.png': 'norris-key',
    'image54.png': 'schwarzenegger',
    'image55.png': 'newyear-key',
    'image5.png':  'influencer-team',
    'image3.png':  'influencer-tracker',
    'image11.png': 'postview-report',
    'image10.png': 'brandlift-table',
    'image13.png': 'frequency-cuts',
    'image9.png':  'campaign-cuts',
    'image12.png': 'antifraud-browsers',
    'image21.png': 'creative-matrix',
    'image14.png': 'price-test-table',
    'image16.png': 'price-test-result',
    'image17.png': 'post-lead-scenario',
    'image22.png': 'ai-product',
    'image19.png': 'ai-presentation',
    'image8.png':  'sales-heatmap',
    'image23.png': 'talks-stage',
    'image24.png': 'talks-letters',
    'image25.png': 'talks-hall',
    'image26.png': 'webinar-room',
    'image27.png': 'webinar-page',
    'image6.png':  'smm-brazil',
    'image7.png':  'smm-mexico',
    'image1.png':  'agency-team',
    'image15.png': 'landing-ux',
}

z = zipfile.ZipFile(SRC)
total = 0
for src, name in MAP.items():
    data = z.read('ppt/media/' + src)
    im = Image.open(io.BytesIO(data)).convert('RGB')
    w, h = im.size
    if w > MAXW:
        im = im.resize((MAXW, round(h * MAXW / w)), Image.LANCZOS)
    dst = os.path.join(OUT, name + '.webp')
    im.save(dst, 'WEBP', quality=82, method=6)
    sz = os.path.getsize(dst)
    total += sz
    print(f'{name}.webp  {im.width}x{im.height}  {sz//1024} KB')
print('TOTAL', round(total/1e6, 2), 'MB', len(MAP), 'files')
