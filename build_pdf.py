#!/usr/bin/env python3
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os

W, H = letter # 612 x 792
OUTPUT = "30-Days-of-Self-Care-Journal.pdf"

# Colors
cream = HexColor("#FFFBF7")
beige = HexColor("#F5E6CC")
rose = HexColor("#D9A99A")
rose_light = HexColor("#F2D5CB")
sage = HexColor("#A8B5A2")
sage_light = HexColor("#DDE6D9")
brown = HexColor("#5C4033")
brown_light = HexColor("#8B6B55")
muted = HexColor("#A68A7A")
line_col = HexColor("#E8DDD3")
lav = HexColor("#C8B8DB")
lav_light = HexColor("#EDE7F3")

def draw_border(c):
    c.saveState()
    # outer frame
    c.setStrokeColor(rose)
    c.setLineWidth(1.2)
    c.roundRect(28, 28, W-56, H-56, 18, stroke=1, fill=0)
    c.setStrokeColor(line_col)
    c.setLineWidth(0.7)
    c.roundRect(34, 34, W-68, H-68, 14, stroke=1, fill=0)
    # corner flowers (text)
    c.setFillColor(rose)
    c.setFont("Helvetica", 9)
    for x,y in [(38, H-40),(W-45, H-40),(38,38),(W-45,38)]:
        c.drawString(x,y,"❦")
    c.restoreState()

def bg_blobs(c, blobs):
    c.saveState()
    for x,y,r, col in blobs:
        c.setFillColor(col)
        # need alpha handling
        # reportlab supports alpha via setFillAlpha
        c.setFillAlpha(0.18)
        c.circle(x,y,r, stroke=0, fill=1)
    c.setFillAlpha(1)
    c.restoreState()

def centered_text(c, text, y, font, size, color, leading=None):
    c.setFont(font, size)
    c.setFillColor(color)
    # support multiline with \n
    lines = text.split("\n")
    lh = leading or size*1.2
    for i,line in enumerate(lines):
        w = c.stringWidth(line, font, size)
        c.drawString((W-w)/2, y - i*lh, line)

def draw_lines(c, x, y, w, count, spacing=22):
    c.setStrokeColor(line_col)
    c.setLineWidth(0.6)
    for i in range(count):
        yy = y - i*spacing
        c.line(x, yy, x+w, yy)

def label_small(c, text, y):
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(muted)
    # letter spacing simulated by drawing with extra spacing? just center
    w = c.stringWidth(text, "Helvetica-Bold", 6.5)
    c.drawString((W-w)/2, y, text)

def title_text(c, text, y, size=22):
    c.setFont("Times-Bold", size)
    c.setFillColor(brown)
    lines = text.split("\n")
    for i,ln in enumerate(lines):
        w = c.stringWidth(ln, "Times-Bold", size)
        c.drawString((W-w)/2, y - i*(size*1.1), ln)

def divider(c, y):
    c.setStrokeColor(rose)
    c.setLineWidth(1.2)
    c.line(W/2-28, y, W/2+28, y)

def quote_box(c, text, y, w= 480, h=36, centered=True):
    # simple rounded rect
    x = (W-w)/2
    c.saveState()
    # bg
    c.setFillColor(HexColor("#FFF1E8"))
    c.setStrokeColor(HexColor("#F2D5CB"))
    c.setLineWidth(0.6)
    # if centered
    c.roundRect(x, y-h, w, h, 8, stroke=1, fill=1)
    if not centered:
        c.setStrokeColor(rose)
        c.setLineWidth(2)
        c.line(x, y, x, y-h)
    c.setFillColor(brown_light)
    c.setFont("Times-Italic", 8.5)
    # wrap
    lines = simpleSplit(text, "Times-Italic", 8.5, w-20)
    lh=10
    start_y = y - (h/2) + (len(lines)-1)*lh/2 + 3
    for i,ln in enumerate(lines):
        ww = c.stringWidth(ln, "Times-Italic", 8.5)
        c.drawString((W-ww)/2, start_y - i*lh, ln)
    c.restoreState()
    return h

def prompt_label(c, text, x, y):
    c.setFont("Times-Bold", 9)
    c.setFillColor(brown)
    c.drawString(x, y, text)

# Create canvas
c = canvas.Canvas(OUTPUT, pagesize=letter)
c.setTitle("30 Days of Self-Care - A Gentle Journey Back to Yourself")
c.setAuthor("Self-Care Journal")

# Helpers
margin_x = 52

# PAGE 1 COVER
c.setFillColor(cream)
c.rect(0,0,W,H, stroke=0, fill=1)
bg_blobs(c, [(W+20, H+20, 160, rose_light),( -20, -20, 130, sage_light)])
draw_border(c)
label_small(c, "A GENTLE JOURNEY BACK TO YOURSELF", H-120)
c.setStrokeColor(rose); c.setLineWidth(1); c.line(W/2-34, H-132, W/2+34, H-132)
c.setFont("Helvetica", 22); c.setFillColor(brown_light); 
# decor
centered_text(c, "☕  ✿  🕯️", H-168, "Helvetica", 18, rose)
title_text(c, "30 DAYS\nOF SELF-CARE", H-210, 38)
c.setFont("Times-Italic", 13); c.setFillColor(brown_light)
w=c.stringWidth("A Gentle Journey Back to Yourself","Times-Italic",13); c.drawString((W-w)/2, H-285, "A Gentle Journey Back to Yourself")
# circle
cx, cy = W/2, H-395
c.saveState()
c.setFillColor(HexColor("#FFF1E8")); c.setStrokeColor(line_col); c.setLineWidth(0.8)
c.circle(cx, cy, 98, stroke=1, fill=1)
c.setFillColor(HexColor("#FFFFFF"))
c.setFillAlpha(0.0)
# inner text simulation
c.setFillAlpha(1)
c.setFont("Helvetica", 36); c.setFillColor(brown_light)
c.drawCentredString(cx, cy+18, "🫖")
c.setFont("Times-Italic", 8); c.setFillColor(muted); c.drawCentredString(cx, cy-8, "tea  •  journal  •  flowers  •  candle")
c.setFont("Helvetica", 6.5); c.setFillColor(muted); c.drawCentredString(cx, cy-22, "soft sunlight through a window")
c.setFont("Helvetica", 14); c.drawString(cx+62, cy+48, "🌿"); c.drawString(cx-78, cy-52, "🌸")
c.restoreState()
# tagline box
c.setStrokeColor(line_col); c.setLineWidth(0.6)
c.line(margin_x, H-520, W-margin_x, H-520)
c.setFont("Helvetica-Bold", 6.8); c.setFillColor(muted)
tag="A 30-DAY JOURNAL FOR REST, REFLECTION & SELF-LOVE"
w=c.stringWidth(tag,"Helvetica-Bold",6.8); c.drawString((W-w)/2, H-532, tag)
c.line(margin_x, H-542, W-margin_x, H-542)
c.setFont("Helvetica", 9); c.setFillColor(rose); c.drawCentredString(W/2, H-560, "—  ✿  —  🌿  —  ✿  —")
c.showPage()

# PAGE 2 BELONGS TO
c.setFillColor(cream); c.rect(0,0,W,H, stroke=0, fill=1); draw_border(c)
centered_text(c, "🌿  ✿  🌸  ✿  🌿", H-140, "Helvetica", 14, rose)
title_text(c, "THIS JOURNAL BELONGS TO", H-190, 18)
divider(c, H-210)
# lines
c.setStrokeColor(lav); c.setLineWidth(1.1)
c.line(90, H-280, W-90, H-280)
c.setFont("Helvetica", 6); c.setFillColor(muted)
c.setFillColor(cream); c.setStrokeColor(cream); c.rect(W/2-28, H-286, 56, 12, stroke=0, fill=1)
c.setFillColor(muted); c.drawCentredString(W/2, H-283, "YOUR NAME")
c.setStrokeColor(line_col); c.setLineWidth(0.6); c.line(90, H-310, W-90, H-310)
quote_box(c, "“ I'm giving myself permission to slow down, breathe deeply, and take care of myself. ”", H-360, w=440, h=42, centered=True)
c.setFont("Helvetica", 12); c.setFillColor(rose_light)
c.drawCentredString(W/2, H-420, "🫖   📓   🕯️   🌷   🍃")
c.setFont("Times-Italic", 8); c.setFillColor(muted); c.drawCentredString(W/2, 70, "Begin gently. There is no rush.")
c.showPage()

# PAGE 3 WELCOME
c.setFillColor(cream); c.rect(0,0,W,H, stroke=0, fill=1); draw_border(c)
label_small(c, "WELCOME", H-80)
title_text(c, "WELCOME TO YOUR\n30 DAYS OF SELF-CARE", H-110, 17)
divider(c, H-158)
c.drawCentredString(W/2, H-180, "🪟  ☀️  🫖  📖  🌿")
# white box
c.saveState()
c.setFillColor(white); c.setStrokeColor(line_col); c.setLineWidth(0.7)
c.roundRect(margin_x, H-360, W-2*margin_x, 150, 12, stroke=1, fill=1)
c.setFillColor(brown); c.setFont("Helvetica", 8)
text1="Self-care doesn't have to be complicated. Sometimes it is a quiet morning, a good night's sleep, a walk outside, a nourishing meal, or simply giving yourself permission to rest."
# wrap manually
lines = simpleSplit(text1, "Helvetica", 8, W-2*margin_x-24)
yy = H-240
c.setFont("Times-Bold", 9); c.drawString(margin_x+12, yy, "Self-care doesn't have to be complicated.")
c.setFont("Helvetica", 8)
for ln in lines:
    yy-=11
    c.drawString(margin_x+12, yy, ln)
# second paragraph
yy-=10
c.setFont("Helvetica", 8)
p2="For the next 30 days, this journal is your little space to pause, listen to yourself, and reconnect with what you need."
lines2= simpleSplit(p2,"Helvetica",8,W-2*margin_x-24)
for ln in lines2:
    c.drawString(margin_x+12, yy, ln)
    yy-=11
c.restoreState()
quote_box(c, "“ You deserve the same kindness you give to others. ”", H-390, w=440, h=36)
# illustration box
c.saveState()
c.setFillColor(HexColor("#FFFBF7")); c.setStrokeColor(line_col)
c.roundRect(margin_x, H-470, W-2*margin_x, 62, 10, stroke=1, fill=1)
c.setFont("Helvetica", 22); c.drawString(margin_x+16, H-440, "🧘‍♀️")
c.setFont("Helvetica-Oblique", 7); c.setFillColor(brown_light)
c.drawString(margin_x+62, H-430, "Illustration: adult sitting beside a sunny window with tea and an open journal —")
c.drawString(margin_x+62, H-440, "soft light, cozy blanket, quiet morning.")
c.restoreState()
c.setFont("Helvetica", 8); c.setFillColor(muted); c.drawCentredString(W/2, H-500, "✿  —  breathe  —  ✿")
c.showPage()

# PAGE 4 GUIDE
c.setFillColor(cream); c.rect(0,0,W,H, stroke=0, fill=1); draw_border(c)
label_small(c, "HOW TO BEGIN", H-80)
title_text(c, "A GENTLE GUIDE", H-110, 20)
divider(c, H-132)
c.drawCentredString(W/2, H-152, "🌿  ✿  🌿")
y = H-180
boxes = [
 ("1","Take a few quiet minutes each day.","Find a calm corner, breathe, and arrive.", rose_light),
 ("2","Answer the prompts honestly — there are no wrong answers.","", sage_light),
 ("3","Skip anything that doesn't feel right for you.","", lav_light),
 ("4","Celebrate small acts of care.","", beige),
 ("5","Remember that progress doesn't have to be perfect.","", rose_light),
]
for num, title, sub, col in boxes:
    c.saveState()
    c.setFillColor(white); c.setStrokeColor(line_col); c.roundRect(margin_x, y-48, W-2*margin_x, 48, 10, stroke=1, fill=1)
    # circle
    c.setFillColor(col); c.circle(margin_x+22, y-24, 12, stroke=0, fill=1)
    c.setFillColor(brown); c.setFont("Helvetica-Bold", 8); c.drawCentredString(margin_x+22, y-27, num)
    c.setFont("Times-Bold", 9); c.setFillColor(brown); c.drawString(margin_x+44, y-20, title)
    if sub:
        c.setFont("Helvetica", 7); c.setFillColor(muted); c.drawString(margin_x+44, y-32, sub)
    c.restoreState()
    y-=58
quote_box(c, "“ Small moments of care can become a beautiful life. ”", y-14, w=440, h=34)
c.showPage()

# PAGE 5 PROMISE
c.setFillColor(cream); c.rect(0,0,W,H, stroke=0, fill=1); draw_border(c)
label_small(c, "BEFORE YOU BEGIN", H-80)
title_text(c, "MY PROMISE TO MYSELF", H-110, 19)
divider(c, H-132)
c.drawCentredString(W/2, H-152, "✿  🌿  ✿")
y = H-180
prompts = ["During these 30 days, I promise to…","I will be kinder to myself by…","I will make space for…","I give myself permission to…","When I need rest, I will…"]
for pr in prompts:
    prompt_label(c, pr, margin_x, y)
    y-=10
    draw_lines(c, margin_x, y, W-2*margin_x, 3 if "During" in pr or "When I need" in pr else 2, spacing=18)
    y-= 3*18 + 12 if "During" in pr or "When I need" in pr else 2*18+12
    if y< 80: y=80
c.setFont("Times-Italic", 7.5); c.setFillColor(muted); c.drawCentredString(W/2, 58, "Sign with kindness — this is a promise, not pressure.")
c.showPage()

# DAILY PAGES - generate 30
import textwrap

day_defs = [
 (1,"PAUSE","“ You don't always have to be moving forward. Sometimes you simply need to pause. ”",["How am I feeling today?","What has been taking up most of my energy lately?","What would feel comforting right now?"],"🫖  🪟  🌤️"),
 (2,"GRATITUDE","“ There is beauty in ordinary moments. ”",[],"🌸  ☀️  ☕  📓"),
 (3,"REST","“ Rest is not something you have to earn. ”",["What does true rest look like for me?","When do I feel most rested?","What can I let go of today?"],"🛏️  📚  🕯️  🌙"),
 (4,"MY ENERGY",None,[],"☀️  🌙  🌿"),
 (5,"MY BODY","“ Your body speaks quietly. Give yourself time to listen. ”",["What does my body need today?","Have I been giving myself enough rest?","What makes me feel comfortable and cared for?","One kind thing I can do for my body today:"],"🌿  🫖"),
 (6,"QUIET YOUR MIND",None,[],"📓  🕯️  🌙  🫖"),
 (7,"WEEK ONE — REFLECTION",None,[],"✿  🌿"),
 (8,"BOUNDARIES","“ Protecting your peace is an act of self-respect. ”",["Where do I need stronger boundaries?","What am I saying yes to when I really mean no?","What boundary would help me feel more at peace?","One boundary I can practice this week:"],"🌿"),
 (9,"SAY NO",None,[],"✿"),
 (10,"FIND YOUR JOY","“ What makes me genuinely happy? ”",[],"🌸  📚  🎶  ☕  ☀️"),
 (11,"INNER CHILD","“ Sometimes caring for yourself means remembering what once made you smile. ”",["What did I love doing as a child?","What made me feel safe and happy?","Which childhood joy could I bring back into my life?"],"🧸  🌈"),
 (12,"DIGITAL RESET",None,[],"📵  🌿  📖"),
 (13,"CREATE A PEACEFUL SPACE",None,[],"🏡  🌿  🕯️"),
 (14,"WEEK TWO — REFLECTION",None,[],"✿"),
 (15,"SELF-LOVE","“ Speak to yourself like someone you deeply care about. ”",["What would I say to a friend who felt the way I feel?","What kind words do I need to hear today?","How can I show myself more compassion?"],"🪞  🌸"),
 (16,"MY STRENGTHS",None,[],"⛰️  🌅"),
 (17,"LET GO","“ You are allowed to release what no longer belongs in your heart. ”",["Something I'm ready to forgive myself for:","Something I'm ready to stop carrying:","What would letting go make room for?"],"🍂  🌿"),
 (18,"DREAM A LITTLE","“ If I wasn't afraid of failing, what would I try? ”",["A dream I've been carrying…","Something I'd love to experience…","A place I'd love to visit…","A life I'd love to create…"],"🌙  ⭐  ☁️"),
 (19,"GENTLER ROUTINE",None,[],"🌿"),
 (20,"NOURISH YOURSELF",None,[],"🍎  🫖  🌸"),
 (21,"WEEK THREE — REFLECTION",None,[],"🌿"),
 (22,"REST WITHOUT GUILT","“ Your worth is not measured by how much you accomplish. ”",["What makes me feel guilty about resting?","What would happen if I allowed myself to rest anyway?","How can I make today slower?"],"📖  🫶"),
 (23,"CONNECTION",None,[],"💛  🌿"),
 (24,"NOTICE THE LITTLE THINGS",None,[],"✿  🌿"),
 (25,"MY IDEAL DAY","“ Imagine a day where you feel peaceful, fulfilled, and completely yourself. ”",[],"☀️  🌿"),
 (26,"WHAT REALLY MATTERS?",None,[],"🌿"),
 (27,"CELEBRATE YOURSELF","“ LOOK HOW FAR YOU'VE COME. ”",["Something I accomplished recently:","Something I'm proud of:","Something I handled better than before:","Something I want to celebrate about myself:"],"🎉  🌸"),
 (28,"A LETTER TO MY FUTURE SELF","“ Write a letter to yourself six months from now. ”",[],"✉️  🌿"),
 (29,"MY PERSONAL SELF-CARE PLAN",None,[],"🌿"),
 (30,"I CHOOSE ME","“ Taking care of myself isn't selfish. It is a way of honoring the life I'm living. ”",["What have these 30 days taught me?","What changed within me?","What will I continue doing?","What promise will I make to myself moving forward?"],"🌅"),
]

def draw_day_page(c, day, title, quote, deco):
    c.setFillColor(cream); c.rect(0,0,W,H, stroke=0, fill=1); draw_border(c)
    # header
    c.setFont("Helvetica", 6); c.setFillColor(muted)
    c.drawString(margin_x, H-52, f"DAY {day:02d}")
    c.drawRightString(W-margin_x, H-52, "30 DAYS OF SELF-CARE")
    c.setStrokeColor(line_col); c.setLineWidth(0.8); c.line(margin_x, H-60, W-margin_x, H-60)
    # title
    title_text(c, title, H-92, 18)
    divider(c, H-112)
    c.setFont("Helvetica", 9); c.setFillColor(rose); c.drawCentredString(W/2, H-132, deco)
    y = H-150
    # quote if exists
    if quote:
        # draw quote box
        c.saveState()
        # estimate height
        w= W-2*margin_x -20
        lines = simpleSplit(quote, "Times-Italic", 8, w-20)
        h = max(28, len(lines)*10+14)
        x = margin_x+10
        c.setFillColor(HexColor("#FFF1E8")); c.setStrokeColor(rose_light)
        c.roundRect(x, y-h, W-2*margin_x-20, h, 8, stroke=1, fill=1)
        c.setFillColor(brown_light); c.setFont("Times-Italic", 8)
        for i,ln in enumerate(lines):
            ww=c.stringWidth(ln,"Times-Italic",8)
            c.drawString((W-ww)/2, y-14 - i*10, ln)
        c.restoreState()
        y -= h+12
    return y

for day, title, quote, prompts, deco in day_defs:
    y = draw_day_page(c, day, title, quote, deco)
    # Now draw body per day specifics
    if day == 2:
        prompt_label(c,"Three things I'm grateful for today:", margin_x, y)
        y-=12
        for i in range(1,4):
            c.setFillColor([rose_light, sage_light, lav_light][i-1]); c.circle(margin_x+10, y-6, 9, stroke=0, fill=1)
            c.setFillColor(brown); c.setFont("Helvetica-Bold",7); c.drawCentredString(margin_x+10, y-8.5, str(i))
            c.setStrokeColor(line_col); c.line(margin_x+26, y-6, W-margin_x, y-6)
            y-=22
        y-=4
        for lab in ["A small moment that made me smile:","Something I often overlook but appreciate:"]:
            prompt_label(c, lab, margin_x, y); y-=10
            draw_lines(c, margin_x, y, W-2*margin_x, 2, spacing=18); y-= 2*18+10
    elif day == 4:
        # two boxes
        c.saveState()
        c.setFillColor(white); c.setStrokeColor(line_col)
        c.roundRect(margin_x, y-110, (W-2*margin_x-12)/2, 110, 10, stroke=1, fill=1)
        c.roundRect(margin_x+ (W-2*margin_x-12)/2 +12, y-110, (W-2*margin_x-12)/2, 110, 10, stroke=1, fill=1)
        # titles
        c.setFont("Helvetica-Bold",6); c.setFillColor(brown_light)
        c.drawCentredString(margin_x + (W-2*margin_x-12)/4, y-14, "☀️  WHAT DRAINS ME")
        c.drawCentredString(margin_x + (W-2*margin_x-12)/2 +12 + (W-2*margin_x-12)/4, y-14, "🌿  WHAT REFILLS ME")
        # lines inside
        c.setStrokeColor(line_col)
        for colx in [margin_x+8, margin_x+ (W-2*margin_x-12)/2+20]:
            yy = y-30
            for _ in range(5):
                c.line(colx, yy, colx+ (W-2*margin_x-12)/2 -16, yy)
                yy-=16
        c.restoreState()
        y-=126
        prompt_label(c,"One thing I can do today to protect my energy is…", margin_x, y); y-=10
        draw_lines(c, margin_x, y, W-2*margin_x, 2, spacing=18); y-=40
    elif day == 6:
        for lab in ["What thoughts have been occupying my mind?","Which thoughts can I release?","What deserves my attention instead?"]:
            prompt_label(c, lab, margin_x, y); y-=10; draw_lines(c, margin_x, y, W-2*margin_x,2, spacing=18); y-= 2*18+10
        # LET IT OUT box
        c.saveState()
        c.setStrokeColor(rose); c.setLineWidth(0.7); c.setDash(4,3)
        c.roundRect(margin_x, y-118, W-2*margin_x, 118, 10, stroke=1, fill=0)
        c.setDash()
        c.setFont("Helvetica-Bold",7); c.setFillColor(rose); c.drawCentredString(W/2, y-16, "—  LET IT OUT  —")
        c.setStrokeColor(line_col)
        yy=y-32
        for _ in range(5):
            c.line(margin_x+10, yy, W-margin_x-10, yy); yy-=16
        c.restoreState()
        y-=130
    elif day == 7:
        labs=["What did I learn about myself this week?","Which self-care activity felt best?","What made me feel peaceful?","What do I want more of next week?","My favorite moment this week:"]
        for lab in labs:
            prompt_label(c, lab, margin_x, y); y-=10; draw_lines(c, margin_x, y, W-2*margin_x, 2, spacing=18); y-= 2*18+10
    elif day == 9:
        c.saveState()
        c.setFillColor(HexColor("#FFF1E8")); c.setStrokeColor(rose_light)
        c.roundRect(margin_x+40, y-32, W-2*margin_x-80, 32, 8, stroke=1, fill=1)
        c.setFillColor(brown); c.setFont("Times-Bold", 11); c.drawCentredString(W/2, y-20, "“ NO IS A COMPLETE SENTENCE. ”")
        c.restoreState()
        y-=48
        for lab in ["Something I don't actually want to do:","Something I can politely decline:","Something I need to stop feeling guilty about:"]:
            prompt_label(c, lab, margin_x, y); y-=10; draw_lines(c, margin_x, y, W-2*margin_x,2, spacing=18); y-= 2*18+10
    elif day == 10:
        c.setFont("Times-Italic",8); c.setFillColor(muted); c.drawCentredString(W/2, y, "“ What makes me genuinely happy? ”"); y-=14
        c.saveState()
        c.setFillColor(white); c.setStrokeColor(line_col)
        c.roundRect(margin_x, y-420, W-2*margin_x, 420, 10, stroke=1, fill=1)
        c.setFont("Helvetica-Bold",7); c.setFillColor(brown_light); c.drawCentredString(W/2, y-16, "✿   JOY LIST   ✿")
        yy=y-32
        c.setStrokeColor(HexColor("#F0E2D6"))
        c.setFont("Helvetica",6); c.setFillColor(lav)
        for i in range(1,16):
            c.drawString(margin_x+12, yy+3, f"{i}.")
            c.line(margin_x+28, yy, W-margin_x-12, yy)
            yy-=26
        c.restoreState()
        y-=440
    elif day == 12:
        c.saveState()
        c.setFillColor(white); c.setStrokeColor(line_col)
        c.roundRect(margin_x, y-108, W-2*margin_x,108,10,stroke=1,fill=1)
        c.setFont("Helvetica-Bold",7); c.setFillColor(brown_light); c.drawCentredString(W/2, y-14, "My Digital Reset — Today I will…")
        items=["30 minutes without social media","Put my phone away during a meal","Spend time outside","Read something","Have a quiet moment"]
        yy=y-30
        c.setFont("Helvetica",8); c.setFillColor(brown)
        for it in items:
            c.setStrokeColor(sage); c.rect(margin_x+14, yy-7, 8,8, stroke=1, fill=0)
            c.drawString(margin_x+28, yy-5, it)
            yy-=16
        c.restoreState()
        y-=124
        prompt_label(c,"How did I feel afterward?", margin_x, y); y-=10; draw_lines(c, margin_x, y, W-2*margin_x,4, spacing=18); y-=80
    elif day == 13:
        for lab in ["What area of my home needs attention?","What could I remove?","What could I add to make it feel more peaceful?"]:
            prompt_label(c, lab, margin_x, y); y-=10; draw_lines(c, margin_x, y, W-2*margin_x,2, spacing=18); y-= 2*18+10
        prompt_label(c,"TODAY I WILL RESET:", margin_x, y); y-=10; draw_lines(c, margin_x, y, W-2*margin_x,2, spacing=18); y-=40
        c.setFont("Helvetica", 10); c.drawCentredString(W/2, y, "🏡  ✨  🕯️  🌿")
    elif day == 14:
        c.saveState()
        titles=["Something I released","Something I discovered","Something that brought me joy","Something I want to change"]
        # 2x2 grid
        bw=(W-2*margin_x-12)/2; bh=96
        positions=[(margin_x, y-bh),(margin_x+bw+12, y-bh),(margin_x, y-2*bh-12),(margin_x+bw+12, y-2*bh-12)]
        for ttl, (px,py) in zip(titles, positions):
            c.setFillColor(white); c.setStrokeColor(line_col); c.roundRect(px, py, bw, bh, 10, stroke=1, fill=1)
            c.setFont("Helvetica-Bold",6); c.setFillColor(brown_light); c.drawCentredString(px+bw/2, py+bh-14, ttl)
            c.setStrokeColor(line_col)
            yy=py+bh-30
            for _ in range(3):
                c.line(px+8, yy, px+bw-8, yy); yy-=16
        c.restoreState()
        y-= 2*bh+26
        prompt_label(c,"I am proud of myself for…", margin_x, y); y-=10; draw_lines(c, margin_x, y, W-2*margin_x,2, spacing=18)
    elif day == 19:
        bw=(W-2*margin_x-20)/3; bh=120
        c.saveState()
        labels=[("🌅","MORNING"),("☀️","AFTERNOON"),("🌙","EVENING")]
        for i,(ic,ttl) in enumerate(labels):
            px=margin_x + i*(bw+10)
            c.setFillColor(white); c.setStrokeColor(line_col); c.roundRect(px, y-bh, bw, bh, 10, stroke=1, fill=1)
            c.setFont("Helvetica",12); c.drawCentredString(px+bw/2, y-22, ic)
            c.setFont("Helvetica-Bold",6); c.setFillColor(brown_light); c.drawCentredString(px+bw/2, y-34, ttl)
            yy=y-50
            c.setStrokeColor(line_col)
            for _ in range(4):
                c.line(px+8, yy, px+bw-8, yy); yy-=16
        c.restoreState()
        y-= bh+18
        prompt_label(c,"One small habit I want to make easier:", margin_x, y); y-=10; draw_lines(c, margin_x, y, W-2*margin_x,2, spacing=18)
    elif day == 24:
        labs = ["👁️  Something beautiful I saw:","🍓  Something delicious I tasted:","🤲  Something comforting I felt:","👂  Something interesting I heard:","😊  Something that made me smile:"]
        for lab in labs:
            prompt_label(c, lab, margin_x, y); y-=10; draw_lines(c, margin_x, y, W-2*margin_x,2, spacing=18); y-= 2*18+10
    elif day == 26:
        bw=(W-2*margin_x-20)/3; bh=120
        c.saveState()
        cols=[(rose,"MUST MATTER"),(sage,"MATTERS TO ME"),(lav,"CAN WAIT")]
        for i,(col,ttl) in enumerate(cols):
            px=margin_x + i*(bw+10)
            c.setFillColor(white); c.setStrokeColor(line_col); c.roundRect(px, y-bh, bw, bh, 10, stroke=1, fill=1)
            c.setFillColor(col); c.rect(px, y-16, bw, 3, stroke=0, fill=1)
            c.setFont("Helvetica-Bold",6); c.setFillColor(brown_light); c.drawCentredString(px+bw/2, y-26, ttl)
            yy=y-42
            c.setStrokeColor(line_col)
            for _ in range(4):
                c.line(px+8, yy, px+bw-8, yy); yy-=16
        c.restoreState()
        y-= bh+18
        prompt_label(c,"What deserves more of my time and attention?", margin_x, y); y-=10; draw_lines(c, margin_x, y, W-2*margin_x,2, spacing=18)
    elif day == 28:
        c.setFont("Times-Italic",8); c.setFillColor(muted); c.drawCentredString(W/2, y, "“ Write a letter to yourself six months from now. ”"); y-=18
        c.saveState()
        c.setFillColor(white); c.setStrokeColor(line_col); c.roundRect(margin_x, y-360, W-2*margin_x, 360, 12, stroke=1, fill=1)
        c.setFont("Times-Italic",8); c.setFillColor(muted); c.drawString(margin_x+12, y-16, "Dear Future Me,")
        c.setStrokeColor(line_col)
        yy=y-30
        for _ in range(18):
            c.line(margin_x+12, yy, W-margin_x-12, yy); yy-=17
        c.setFont("Times-Italic",6.5); c.setFillColor(muted); c.drawCentredString(W/2, y-368+10, "“ Remember how you felt here. Remember what you wanted. Remember to be gentle with yourself. ”")
        c.restoreState()
        y-=380
    elif day == 29:
        secs=["WHEN I'M TIRED, I WILL…","WHEN I'M OVERWHELMED, I WILL…","WHEN I NEED JOY, I WILL…","WHEN I NEED CONNECTION, I WILL…"]
        for sec in secs:
            prompt_label(c, sec, margin_x, y); y-=10; draw_lines(c, margin_x, y, W-2*margin_x,2, spacing=18); y-= 2*18+8
        prompt_label(c,"The people, places, and things that help me feel grounded:", margin_x, y); y-=10; draw_lines(c, margin_x, y, W-2*margin_x,2, spacing=18)
    else:
        # generic
        generic_prompts = {
            1:["How am I feeling today?","What has been taking up most of my energy lately?","What would feel comforting right now?"],
            3:["What does true rest look like for me?","When do I feel most rested?","What can I let go of today?"],
            5:["What does my body need today?","Have I been giving myself enough rest?","What makes me feel comfortable and cared for?","One kind thing I can do for my body today:"],
            8:["Where do I need stronger boundaries?","What am I saying yes to when I really mean no?","What boundary would help me feel more at peace?","One boundary I can practice this week:"],
            11:["What did I love doing as a child?","What made me feel safe and happy?","Which childhood joy could I bring back into my life?"],
            15:["What would I say to a friend who felt the way I feel?","What kind words do I need to hear today?","How can I show myself more compassion?"],
            16:["Three things I'm good at:","Three challenges I've overcome:","Something I once thought I couldn't do:","A strength I sometimes forget I have:"],
            17:["Something I'm ready to forgive myself for:","Something I'm ready to stop carrying:","What would letting go make room for?"],
            18:["A dream I've been carrying…","Something I'd love to experience…","A place I'd love to visit…","A life I'd love to create…"],
            20:["What makes me feel nourished?","What does my mind need?","What does my body need?","What does my heart need?"],
            21:["What has changed in me?","What habit feels good?","What am I learning to prioritize?","What am I becoming more comfortable saying no to?","My biggest realization this week:"],
            22:["What makes me feel guilty about resting?","What would happen if I allowed myself to rest anyway?","How can I make today slower?"],
            23:["Who makes me feel safe and understood?","Who would I like to spend more time with?","Who could use a little kindness from me today?","Someone I want to reach out to:"],
            25:["I wake up…","I spend my morning…","I spend my afternoon…","I spend my evening…","Before bed, I feel…"],
            27:["Something I accomplished recently:","Something I'm proud of:","Something I handled better than before:","Something I want to celebrate about myself:"],
            30:["What have these 30 days taught me?","What changed within me?","What will I continue doing?","What promise will I make to myself moving forward?"],
        }
        # special visuals
        if day==15:
            c.saveState()
            c.setStrokeColor(rose); c.setFillColor(HexColor("#FFF1E8")); c.circle(W/2, y-28, 28, stroke=1, fill=1)
            c.setFont("Helvetica",20); c.setFillColor(brown_light); c.drawCentredString(W/2, y-34, "🪞")
            c.setFont("Helvetica",6); c.setFillColor(muted); c.drawCentredString(W/2, y-66, "—  surrounded by flowers  —")
            c.restoreState()
            y-=76
        if day==25:
            # ideal day has extra intro already? not
            pass
        for lab in generic_prompts.get(day, []):
            prompt_label(c, lab, margin_x, y); y-=10
            cnt = 3 if day in [25,21] else 2
            if lab.startswith("I wake") or lab.startswith("I spend") or lab.startswith("Before"):
                cnt=2
            draw_lines(c, margin_x, y, W-2*margin_x, cnt, spacing=18); y-= cnt*18+10
        if day==30:
            c.saveState()
            c.setFillColor(HexColor("#FFF1E8")); c.setStrokeColor(rose_light); c.setDash(3,3)
            c.roundRect(margin_x, y-28, W-2*margin_x, 28, 8, stroke=1, fill=1)
            c.setDash()
            c.setFont("Times-Italic",8); c.setFillColor(brown); c.drawCentredString(W/2, y-18, "“ I choose to care for myself, one small moment at a time. ”")
            c.restoreState()
            y-=36
        if day==22:
            c.setFont("Helvetica",10); c.drawCentredString(W/2, y-6, "📖  🫶  🛋️")
    # footer
    c.setFont("Helvetica",6); c.setFillColor(HexColor("#C4A99A")); c.drawCentredString(W/2, 44, f"✿  —  day {day}  —  ✿")
    c.showPage()

# BONUS PAGES

# 36 toolkit
c.setFillColor(cream); c.rect(0,0,W,H, stroke=0, fill=1); draw_border(c)
label_small(c,"BONUS", H-80)
title_text(c,"MY SELF-CARE TOOLKIT", H-110, 18)
divider(c, H-132); c.drawCentredString(W/2, H-152, "🌿  ✿  🌿")
y=H-180
for ttl, ic in [("WHEN I NEED REST","🤲"),("WHEN I NEED COMFORT","💛"),("WHEN I NEED MOTIVATION","✨"),("WHEN I NEED CONNECTION","🤝"),("WHEN I NEED QUIET","🤫")]:
    c.saveState()
    c.setFillColor(white); c.setStrokeColor(line_col); c.roundRect(margin_x, y-66, W-2*margin_x,66,10,stroke=1,fill=1)
    c.setFont("Helvetica-Bold",7); c.setFillColor(brown_light); c.drawCentredString(W/2, y-16, f"{ic}  {ttl}")
    c.setStrokeColor(line_col)
    yy=y-28
    for _ in range(3):
        c.line(margin_x+10, yy, W-margin_x-10, yy); yy-=14
    c.restoreState()
    y-=76
c.showPage()

# 37 menu
c.setFillColor(cream); c.rect(0,0,W,H, stroke=0, fill=1); draw_border(c)
title_text(c,"MY SELF-CARE MENU", H-100, 19)
divider(c, H-116); c.drawCentredString(W/2, H-136, "☕  ✿  🕯️  ✿  🌿")
y=H-170
for ttl, col in [("🌿  5-MINUTE CARE", sage),("☕  30-MINUTE CARE", rose),("🌙  SLOW-DAY CARE", lav)]:
    c.saveState()
    c.setFillColor(white); c.setStrokeColor(line_col); c.roundRect(margin_x, y-96, W-2*margin_x,96,10,stroke=1,fill=1)
    c.setFillColor(col); c.rect(margin_x, y-18, 4, 18, stroke=0, fill=1)
    c.setFont("Helvetica-Bold",7); c.setFillColor(brown_light); c.drawString(margin_x+12, y-14, ttl)
    yy=y-36
    c.setFont("Helvetica",9); 
    for _ in range(3):
        c.setStrokeColor(line_col); c.line(margin_x+14, yy, W-margin_x-14, yy)
        # checkbox
        c.setStrokeColor(col); c.rect(margin_x+14, yy+2, 8,8, stroke=1, fill=0)
        c.drawString(margin_x+28, yy+3, "")  # placeholder
        yy-=22
    c.restoreState()
    y-=108
c.setFont("Helvetica",7); c.setFillColor(muted); c.drawCentredString(W/2, y-6, "✿  —  choose what fits today  —  ✿")
c.showPage()

# 38 remember
c.setFillColor(cream); c.rect(0,0,W,H, stroke=0, fill=1); draw_border(c)
title_text(c,"THINGS I WANT TO REMEMBER", H-100, 16)
divider(c, H-116); c.drawCentredString(W/2, H-136, "✿  🌿  ✿")
c.saveState()
c.setFillColor(white); c.setStrokeColor(line_col); c.roundRect(margin_x, 90, W-2*margin_x, H-170, 12, stroke=1, fill=1)
yy=H-170
c.setFont("Helvetica",7); c.setFillColor(HexColor("#D9A99A"))
for i in range(1,21):
    c.drawString(margin_x+12, yy+1, f"{i}.")
    c.setStrokeColor(line_col); c.line(margin_x+28, yy, W-margin_x-12, yy)
    yy-=22
c.restoreState()
quote_box(c,"“ There is always something worth remembering. ”", 80, w=440, h=30)
c.showPage()

# 39 looking back
c.setFillColor(cream); c.rect(0,0,W,H, stroke=0, fill=1); draw_border(c)
title_text(c,"LOOKING BACK", H-100, 19)
divider(c, H-116); c.drawCentredString(W/2, H-136, "🌿  ✿  🌿")
y=H-170
for lab in ["The biggest lesson I learned:","The habit I want to keep:","The boundary I want to protect:","The thing I want more of:","The thing I want less of:","The version of myself I'm becoming:"]:
    prompt_label(c, lab, margin_x, y); y-=10
    cnt=3 if "becoming" in lab else 2
    draw_lines(c, margin_x, y, W-2*margin_x, cnt, spacing=18); y-= cnt*18+12
c.showPage()

# 40 final
c.setFillColor(cream); c.rect(0,0,W,H, stroke=0, fill=1)
bg_blobs(c, [(-10, H+10, 140, lav_light),(W+10, -10, 130, rose_light)])
draw_border(c)
c.drawCentredString(W/2, H-150, "🕯️  📓  🫖  🌸")
# window card
c.saveState()
c.setFillColor(HexColor("#2E2A4A")); c.setStrokeColor(line_col)
c.roundRect(W/2-130, H-300, 260, 120, 14, stroke=1, fill=1)
# glow
c.setFillColor(HexColor("#FFD9A0")); c.setFillAlpha(0.35); c.circle(W/2, H-240, 42, stroke=0, fill=1)
c.setFillAlpha(1); c.setFillColor(white); c.setFont("Helvetica",18); c.drawCentredString(W/2, H-235, "🪟  ✨")
c.setFont("Helvetica",6); c.setFillColor(white); c.drawCentredString(W/2, H-250, "evening journal  •  candle glow")
c.restoreState()
title_text(c,"YOU MADE SPACE\nFOR YOURSELF.", H-360, 22)
divider(c, H-404)
c.setFont("Helvetica",8); c.setFillColor(brown_light)
c.drawCentredString(W/2, H-426, "Keep choosing the little moments that make life feel softer,")
c.drawCentredString(W/2, H-438, "slower, and more meaningful.")
c.setFont("Times-Italic",9); c.setFillColor(brown_light); c.drawCentredString(W/2, H-462, "Your journey doesn't end here.")
c.drawCentredString(W/2, H-490, "—  ✿  🌿  ✿  —")
c.setFont("Helvetica",6); c.setFillColor(muted); c.drawCentredString(W/2, 54, "30 DAYS OF SELF-CARE  —  A GENTLE JOURNEY BACK TO YOURSELF")
c.showPage()

c.save()
print(f"Saved {OUTPUT} with {c.getPageNumber()-1} pages")
print(os.path.getsize(OUTPUT))
