#!/usr/bin/env python3
import pathlib

colors = {
 "cream": "#FFFBF7",
 "cream2": "#FFF4E8",
 "beige": "#F5E6CC",
 "rose": "#D9A99A",
 "rose_light": "#F2D5CB",
 "sage": "#A8B5A2",
 "sage_light": "#DDE6D9",
 "brown": "#5C4033",
 "brown_light": "#8B6B55",
 "lavender": "#C8B8DB",
 "lavender_light": "#EDE7F3",
 "line": "#E8DDD3",
}

html_head = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Nunito:wght@300;400;600&display=swap');
@page { size: 8.5in 11in; margin: 0; }
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: 'Nunito', 'Helvetica', sans-serif; color:#4A3529; background:#fff; }
.page {
  width:8.5in; height:11in;
  padding:0.55in 0.65in;
  position:relative; overflow:hidden;
  background: #FFFBF7;
  page-break-after: always;
  display:flex; flex-direction:column;
}
.page:last-child { page-break-after: avoid; }
.bg-blob { position:absolute; border-radius:50%; opacity:0.18; }
.border-frame {
  position:absolute; inset:0.38in;
  border:1.4px solid #D9A99A;
  border-radius:18px;
  pointer-events:none;
}
.border-frame::before {
  content:''; position:absolute; inset:6px;
  border:1px solid #E8DDD3; border-radius:14px;
}
.corner { position:absolute; font-size:22px; color:#D9A99A; opacity:0.9; }
.corner.tl { top:10px; left:14px; } .corner.tr { top:10px; right:14px; } .corner.bl { bottom:10px; left:14px; } .corner.br { bottom:10px; right:14px; }
h1, h2, h3 { font-family:'Cormorant Garamond', Georgia, serif; color:#5C4033; letter-spacing:0.04em; }
.serif { font-family:'Cormorant Garamond', serif; }
.label-small { font-size:7.5px; letter-spacing:0.22em; text-transform:uppercase; color:#A68A7A; font-weight:600; }
.title { font-size:26px; font-weight:700; line-height:1.1; text-align:center; }
.subtitle { font-size:11px; letter-spacing:0.18em; text-transform:uppercase; color:#8B6B55; text-align:center; margin-top:6px; }
.divider { width:56px; height:1.5px; background:#D9A99A; margin:10px auto; border-radius:2px; }
.quote-box { background:#FFF1E8; border-left:3px solid #D9A99A; padding:10px 14px; border-radius:0 10px 10px 0; font-style:italic; color:#6B4E3D; font-size:10.5px; line-height:1.5; margin:10px 0; }
.quote-box.center { border-left:none; border-top:2px solid #E8D0C3; border-radius:10px; text-align:center; background:#FFF4E8; }
.prompt-label { font-family:'Cormorant Garamond', serif; font-size:11.5px; font-weight:600; color:#5C4033; margin-top:12px; margin-bottom:6px; }
.lines { flex:1; display:flex; flex-direction:column; gap:0; }
.line { border-bottom:1px solid #E8DDD3; height:22px; width:100%; }
.line.dotted { border-bottom:1px dashed #E8DDD3; }
.line-group { display:flex; flex-direction:column; gap:0; margin-bottom:4px; }
.check-list { list-style:none; font-size:10px; line-height:1.9; }
.check-list li::before { content:'☐ '; color:#A8B5A2; font-size:11px; }
.two-col { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
.box { background:#FFFFFF; border:1px solid #F0E2D6; border-radius:12px; padding:12px 14px; }
.box-title { font-family:'Cormorant Garamond', serif; font-size:10px; letter-spacing:0.14em; text-transform:uppercase; color:#8B6B55; text-align:center; margin-bottom:6px; font-weight:700; }
.illustration { text-align:center; font-size:28px; letter-spacing:6px; opacity:0.9; margin:8px 0; }
.small-illust { text-align:center; font-size:16px; letter-spacing:4px; opacity:0.7; }
.footer-quote { font-family:'Cormorant Garamond', serif; font-style:italic; font-size:10px; color:#9B8575; text-align:center; margin-top:auto; padding-top:10px; }
.day-header { display:flex; justify-content:space-between; align-items:center; border-bottom:1.5px solid #E8DDD3; padding-bottom:8px; margin-bottom:8px; }
.day-num { font-family:'Cormorant Garamond', serif; font-size:10px; letter-spacing:0.2em; color:#A68A7A; }
.day-title { font-family:'Cormorant Garamond', serif; font-size:22px; font-weight:700; color:#5C4033; letter-spacing:0.06em; }
.cover-title { font-family:'Cormorant Garamond', serif; font-size:42px; font-weight:700; color:#5C4033; line-height:0.95; letter-spacing:0.06em; text-align:center; }
.cover-subtitle { font-family:'Cormorant Garamond', serif; font-size:15px; font-style:italic; color:#8B6B55; text-align:center; margin-top:6px; letter-spacing:0.04em; }
.tagline { font-size:9px; letter-spacing:0.22em; text-transform:uppercase; color:#A68A7A; text-align:center; margin-top:10px; border-top:1px solid #E8DDD3; border-bottom:1px solid #E8DDD3; padding:8px 0; }
</style>
</head>
<body>
"""

# helper to wrap page
def page(inner, bg=""):
    return f'<section class="page">{bg}<div class="border-frame"><span class="corner tl">❦</span><span class="corner tr">❦</span><span class="corner bl">❦</span><span class="corner br">❦</span></div>{inner}</section>'

# Build pages list
pages = []

# PAGE 1 COVER
pages.append(page(f"""
<div style="flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding-top:0.2in">
  <div class="label-small" style="margin-bottom:14px">A Gentle Journey Back to Yourself</div>
  <div style="width:68px; height:1.5px; background:#D9A99A; margin:0 auto 18px"></div>
  <div class="illustration" style="font-size:38px; margin-bottom:10px">☕ ✿ 🕯️</div>
  <div class="cover-title">30 DAYS<br>OF SELF-CARE</div>
  <div class="cover-subtitle">A Gentle Journey Back to Yourself</div>
  <div style="margin:18px auto; width:240px; height:240px; border-radius:50%; background:linear-gradient(135deg,#FFF1E8 0%,#F2D5CB 50%,#DDE6D9 100%); display:flex; align-items:center; justify-content:center; border:1px solid #F0E2D6; position:relative">
    <div style="text-align:center; line-height:1.4">
      <div style="font-size:56px">🫖</div>
      <div style="font-size:11px; color:#8B6B55; margin-top:4px; font-family:'Cormorant Garamond',serif; font-style:italic">tea • journal • flowers • candle</div>
      <div style="font-size:10px; color:#A68A7A; margin-top:6px">soft sunlight through a window</div>
    </div>
    <div style="position:absolute; top:18px; right:28px; font-size:18px">🌿</div>
    <div style="position:absolute; bottom:22px; left:26px; font-size:16px">🌸</div>
  </div>
  <div class="tagline">A 30-Day Journal for Rest, Reflection & Self-Love</div>
  <div class="small-illust" style="margin-top:14px">—  ✿  —  🌿  —  ✿  —</div>
</div>
""", bg='<div class="bg-blob" style="width:420px;height:420px;background:#F2D5CB;top:-80px;right:-80px"></div><div class="bg-blob" style="width:320px;height:320px;background:#DDE6D9;bottom:-60px;left:-60px"></div>'))

# PAGE 2 BELONGS TO
pages.append(page("""
<div style="flex:1; display:flex; flex-direction:column; justify-content:center">
  <div class="illustration">🌿 ✿ 🌸 ✿ 🌿</div>
  <h1 class="title" style="font-size:22px; margin-top:8px">THIS JOURNAL BELONGS TO</h1>
  <div class="divider"></div>
  <div style="margin:28px 0 10px; border-bottom:1.5px solid #C8B8DB; height:36px; position:relative">
    <span style="position:absolute; bottom:-8px; left:50%; transform:translateX(-50%); background:#FFFBF7; padding:0 12px; font-size:8px; letter-spacing:0.18em; color:#A68A7A; text-transform:uppercase">your name</span>
  </div>
  <div style="height:22px; border-bottom:1px solid #E8DDD3"></div>
  <div class="quote-box center" style="margin-top:32px; font-size:11.5px; line-height:1.6">
    “I’m giving myself permission to slow down,<br>breathe deeply, and take care of myself.”
  </div>
  <div class="illustration" style="margin-top:24px; font-size:22px">🫖  📓  🕯️  🌷  🍃</div>
  <div class="footer-quote">Begin gently. There is no rush.</div>
</div>
"""))

# PAGE 3 WELCOME
pages.append(page("""
<div style="padding-top:10px">
  <div class="label-small" style="text-align:center">Welcome</div>
  <h1 class="title" style="font-size:20px; margin-top:6px">WELCOME TO YOUR<br>30 DAYS OF SELF-CARE</h1>
  <div class="divider"></div>
  <div class="illustration" style="font-size:20px">🪟 ☀️ 🫖 📖 🌿</div>
  <div style="background:#FFFFFF; border:1px solid #F0E2D6; border-radius:14px; padding:16px 18px; margin:12px 0; line-height:1.7; font-size:10.5px; color:#5C4033">
    <p style="margin-bottom:10px"><strong style="font-family:'Cormorant Garamond',serif; font-size:12px">Self-care doesn't have to be complicated.</strong> Sometimes it is a quiet morning, a good night's sleep, a walk outside, a nourishing meal, or simply giving yourself permission to rest.</p>
    <p>For the next 30 days, this journal is your little space to pause, listen to yourself, and reconnect with what you need.</p>
  </div>
  <div class="quote-box center">
    “You deserve the same kindness you give to others.”
  </div>
  <div style="margin-top:14px; background:linear-gradient(135deg,#FFFBF7,#F2EFE9); border:1px solid #E8DDD3; border-radius:12px; padding:12px; display:flex; align-items:center; gap:14px">
    <div style="font-size:42px">🧘‍♀️</div>
    <div style="font-size:9.5px; line-height:1.6; color:#6B4E3D"><em>Illustration: adult sitting beside a sunny window with tea and an open journal — soft light, cozy blanket, quiet morning.</em></div>
  </div>
  <div class="small-illust" style="margin-top:12px">✿  —  breathe  —  ✿</div>
</div>
"""))

# PAGE 4 HOW TO USE
pages.append(page("""
<div style="padding-top:6px">
  <div class="label-small" style="text-align:center">How to begin</div>
  <h1 class="title" style="font-size:22px; margin-top:4px">A GENTLE GUIDE</h1>
  <div class="divider"></div>
  <div class="small-illust">🌿 ✿ 🌿</div>
  <div style="display:flex; flex-direction:column; gap:10px; margin-top:12px">
    <div style="display:flex; gap:12px; align-items:flex-start; background:#FFF; border:1px solid #F0E2D6; border-radius:10px; padding:12px 14px">
      <span style="min-width:28px; height:28px; background:#F2D5CB; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#5C4033">1</span>
      <div><div style="font-family:'Cormorant Garamond',serif; font-weight:700; font-size:11px">Take a few quiet minutes each day.</div><div style="font-size:9.5px; color:#8B6B55; margin-top:2px">Find a calm corner, breathe, and arrive.</div></div>
    </div>
    <div style="display:flex; gap:12px; align-items:flex-start; background:#FFF; border:1px solid #F0E2D6; border-radius:10px; padding:12px 14px">
      <span style="min-width:28px; height:28px; background:#DDE6D9; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#5C4033">2</span>
      <div><div style="font-family:'Cormorant Garamond',serif; font-weight:700; font-size:11px">Answer the prompts honestly — there are no wrong answers.</div></div>
    </div>
    <div style="display:flex; gap:12px; align-items:flex-start; background:#FFF; border:1px solid #F0E2D6; border-radius:10px; padding:12px 14px">
      <span style="min-width:28px; height:28px; background:#EDE7F3; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#5C4033">3</span>
      <div><div style="font-family:'Cormorant Garamond',serif; font-weight:700; font-size:11px">Skip anything that doesn't feel right for you.</div></div>
    </div>
    <div style="display:flex; gap:12px; align-items:flex-start; background:#FFF; border:1px solid #F0E2D6; border-radius:10px; padding:12px 14px">
      <span style="min-width:28px; height:28px; background:#F5E6CC; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#5C4033">4</span>
      <div><div style="font-family:'Cormorant Garamond',serif; font-weight:700; font-size:11px">Celebrate small acts of care.</div></div>
    </div>
    <div style="display:flex; gap:12px; align-items:flex-start; background:#FFF; border:1px solid #F0E2D6; border-radius:10px; padding:12px 14px">
      <span style="min-width:28px; height:28px; background:#F2D5CB; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#5C4033">5</span>
      <div><div style="font-family:'Cormorant Garamond',serif; font-weight:700; font-size:11px">Remember that progress doesn't have to be perfect.</div></div>
    </div>
  </div>
  <div class="quote-box center" style="margin-top:16px">“Small moments of care can become a beautiful life.”</div>
</div>
"""))

# PAGE 5 PROMISE
pages.append(page("""
<div>
  <div class="label-small" style="text-align:center">Before you begin</div>
  <h1 class="title" style="font-size:22px; margin-top:4px">MY PROMISE TO MYSELF</h1>
  <div class="divider"></div>
  <div class="small-illust">✿ 🌿 ✿</div>
  <div style="display:flex; flex-direction:column; gap:14px; margin-top:10px">
    <div><div class="prompt-label">During these 30 days, I promise to…</div><div class="line-group"><div class="line"></div><div class="line"></div><div class="line"></div></div></div>
    <div><div class="prompt-label">I will be kinder to myself by…</div><div class="line-group"><div class="line"></div><div class="line"></div></div></div>
    <div><div class="prompt-label">I will make space for…</div><div class="line-group"><div class="line"></div><div class="line"></div></div></div>
    <div><div class="prompt-label">I give myself permission to…</div><div class="line-group"><div class="line"></div><div class="line"></div></div></div>
    <div><div class="prompt-label">When I need rest, I will…</div><div class="line-group"><div class="line"></div><div class="line"></div><div class="line"></div></div></div>
  </div>
  <div class="footer-quote">Sign with kindness — this is a promise, not pressure.</div>
</div>
"""))

# Daily pages data
days = [
 (1,"PAUSE","“You don't always have to be moving forward. Sometimes you simply need to pause.”",["How am I feeling today?","What has been taking up most of my energy lately?","What would feel comforting right now?"], "🫖  🪟  🌤️"),
 (2,"GRATITUDE","“There is beauty in ordinary moments.”",["Three things I'm grateful for today:","A small moment that made me smile:","Something I often overlook but appreciate:"], "🌸 ☀️ ☕ 📓"),
 (3,"REST","“Rest is not something you have to earn.”",["What does true rest look like for me?","When do I feel most rested?","What can I let go of today?"], "🛏️ 📚 🕯️ 🌙"),
 (4,"MY ENERGY",None,["WHAT DRAINS ME","WHAT REFILLS ME","One thing I can do today to protect my energy is…"], "☀️ 🌙 🌿"),
 (5,"MY BODY","“Your body speaks quietly. Give yourself time to listen.”",["What does my body need today?","Have I been giving myself enough rest?","What makes me feel comfortable and cared for?","One kind thing I can do for my body today:"], "🌿 🫖"),
 (6,"QUIET YOUR MIND",None,["What thoughts have been occupying my mind?","Which thoughts can I release?","What deserves my attention instead?","LET IT OUT"], "📓 🕯️ 🌙 🫖"),
 (7,"WEEK ONE — REFLECTION",None,["What did I learn about myself this week?","Which self-care activity felt best?","What made me feel peaceful?","What do I want more of next week?","My favorite moment this week:"], "✿ 🌿"),
 (8,"BOUNDARIES","“Protecting your peace is an act of self-respect.”",["Where do I need stronger boundaries?","What am I saying yes to when I really mean no?","What boundary would help me feel more at peace?","One boundary I can practice this week:"], "🌿"),
 (9,"SAY NO",None,["Something I don't actually want to do:","Something I can politely decline:","Something I need to stop feeling guilty about:"], "✿"),
 (10,"FIND YOUR JOY","“What makes me genuinely happy?”",["JOY LIST"], "🌸 📚 🎶 ☕ ☀️ 🌿"),
 (11,"INNER CHILD","“Sometimes caring for yourself means remembering what once made you smile.”",["What did I love doing as a child?","What made me feel safe and happy?","Which childhood joy could I bring back into my life?"], "🧸 🌈"),
 (12,"DIGITAL RESET",None,["CHECKLIST","How did I feel afterward?"], "📵 🌿 📖"),
 (13,"CREATE A PEACEFUL SPACE",None,["What area of my home needs attention?","What could I remove?","What could I add to make it feel more peaceful?","TODAY I WILL RESET:"], "🏡 🌿 🕯️"),
 (14,"WEEK TWO — REFLECTION",None,["Something I released","Something I discovered","Something that brought me joy","Something I want to change","I am proud of myself for…"], "✿"),
 (15,"SELF-LOVE","“Speak to yourself like someone you deeply care about.”",["What would I say to a friend who felt the way I feel?","What kind words do I need to hear today?","How can I show myself more compassion?"], "🪞 🌸"),
 (16,"MY STRENGTHS",None,["Three things I'm good at:","Three challenges I've overcome:","Something I once thought I couldn't do:","A strength I sometimes forget I have:"], "⛰️ 🌅"),
 (17,"LET GO","“You are allowed to release what no longer belongs in your heart.”",["Something I'm ready to forgive myself for:","Something I'm ready to stop carrying:","What would letting go make room for?"], "🍂 🌿"),
 (18,"DREAM A LITTLE","“If I wasn't afraid of failing, what would I try?”",["A dream I've been carrying…","Something I'd love to experience…","A place I'd love to visit…","A life I'd love to create…"], "🌙 ⭐ ☁️"),
 (19,"GENTLER ROUTINE",None,["MORNING","AFTERNOON","EVENING","One small habit I want to make easier:"], "🌿"),
 (20,"NOURISH YOURSELF",None,["What makes me feel nourished?","What does my mind need?","What does my body need?","What does my heart need?"], "🍎 🫖 🌸 📓"),
 (21,"WEEK THREE — REFLECTION",None,["What has changed in me?","What habit feels good?","What am I learning to prioritize?","What am I becoming more comfortable saying no to?","My biggest realization this week:"], "🌿"),
 (22,"REST WITHOUT GUILT","“Your worth is not measured by how much you accomplish.”",["What makes me feel guilty about resting?","What would happen if I allowed myself to rest anyway?","How can I make today slower?"], "📖 🫖"),
 (23,"CONNECTION",None,["Who makes me feel safe and understood?","Who would I like to spend more time with?","Who could use a little kindness from me today?","Someone I want to reach out to:"], "💛 🌿"),
 (24,"NOTICE THE LITTLE THINGS",None,["Something beautiful I saw:","Something delicious I tasted:","Something comforting I felt:","Something interesting I heard:","Something that made me smile:"], "✿ 🌿"),
 (25,"MY IDEAL DAY","“Imagine a day where you feel peaceful, fulfilled, and completely yourself.”",["I wake up…","I spend my morning…","I spend my afternoon…","I spend my evening…","Before bed, I feel…"], "☀️ 🌿"),
 (26,"WHAT REALLY MATTERS?",None,["MUST MATTER","MATTERS TO ME","CAN WAIT","What deserves more of my time and attention?"], "🌿"),
 (27,"CELEBRATE YOURSELF","“LOOK HOW FAR YOU'VE COME.”",["Something I accomplished recently:","Something I'm proud of:","Something I handled better than before:","Something I want to celebrate about myself:"], "🎉 🌸"),
 (28,"A LETTER TO MY FUTURE SELF","“Write a letter to yourself six months from now.”",["LETTER"], "✉️ 🌿"),
 (29,"MY PERSONAL SELF-CARE PLAN",None,["WHEN I'M TIRED, I WILL…","WHEN I'M OVERWHELMED, I WILL…","WHEN I NEED JOY, I WILL…","WHEN I NEED CONNECTION, I WILL…","The people, places, and things that help me feel grounded:"], "🌿"),
 (30,"I CHOOSE ME","“Taking care of myself isn't selfish. It is a way of honoring the life I'm living.”",["What have these 30 days taught me?","What changed within me?","What will I continue doing?","What promise will I make to myself moving forward?","I choose to care for myself, one small moment at a time."], "🌅"),
]

def make_daily(day, title, quote, prompts, deco):
    day_label = f"DAY {day:02d}"
    header = f'<div class="day-header"><span class="day-num">{day_label}</span><span class="day-num" style="letter-spacing:0.12em">30 Days of Self-Care</span></div>'
    title_html = f'<h2 class="day-title" style="text-align:center">{title}</h2><div class="divider"></div><div class="small-illust">{deco}</div>'
    quote_html = f'<div class="quote-box center">{quote}</div>' if quote else ''
    body = ""
    # Special cases
    if day == 2:
        body += """
        <div class="prompt-label">Three things I'm grateful for today:</div>
        <div style="display:flex; flex-direction:column; gap:6px; margin:6px 0">
          <div style="display:flex; gap:8px; align-items:center"><span style="width:22px; height:22px; border-radius:50%; background:#F2D5CB; display:flex; align-items:center; justify-content:center; font-size:10px">1</span><div style="flex:1; border-bottom:1px solid #E8DDD3; height:22px"></div></div>
          <div style="display:flex; gap:8px; align-items:center"><span style="width:22px; height:22px; border-radius:50%; background:#DDE6D9; display:flex; align-items:center; justify-content:center; font-size:10px">2</span><div style="flex:1; border-bottom:1px solid #E8DDD3; height:22px"></div></div>
          <div style="display:flex; gap:8px; align-items:center"><span style="width:22px; height:22px; border-radius:50%; background:#EDE7F3; display:flex; align-items:center; justify-content:center; font-size:10px">3</span><div style="flex:1; border-bottom:1px solid #E8DDD3; height:22px"></div></div>
        </div>
        <div class="prompt-label">A small moment that made me smile:</div><div class="line-group"><div class="line"></div><div class="line"></div></div>
        <div class="prompt-label">Something I often overlook but appreciate:</div><div class="line-group"><div class="line"></div><div class="line"></div></div>
        """
    elif day == 4:
        body += """
        <div class="two-col" style="margin-top:8px">
          <div class="box"><div class="box-title">☀️ What drains me</div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>
          <div class="box" style="background:#F6FAF5"><div class="box-title">🌿 What refills me</div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>
        </div>
        <div class="prompt-label" style="margin-top:14px">One thing I can do today to protect my energy is…</div><div class="line-group"><div class="line"></div><div class="line"></div></div>
        """
    elif day == 6:
        body += """
        <div class="prompt-label">What thoughts have been occupying my mind?</div><div class="line-group"><div class="line"></div><div class="line"></div></div>
        <div class="prompt-label">Which thoughts can I release?</div><div class="line-group"><div class="line"></div><div class="line"></div></div>
        <div class="prompt-label">What deserves my attention instead?</div><div class="line-group"><div class="line"></div><div class="line"></div></div>
        <div style="margin-top:10px; background:#FFF; border:1.5px dashed #D9A99A; border-radius:12px; padding:10px 14px">
          <div class="box-title" style="color:#D9A99A">— LET IT OUT —</div>
          <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
        </div>
        """
    elif day == 9:
        body += """
        <div style="text-align:center; margin:6px 0; padding:10px; background:#FFF1E8; border-radius:10px; border:1px solid #F2D5CB">
          <div style="font-family:'Cormorant Garamond',serif; font-size:18px; font-weight:700; letter-spacing:0.08em; color:#5C4033">“NO IS A COMPLETE SENTENCE.”</div>
        </div>
        <div class="prompt-label">Something I don't actually want to do:</div><div class="line-group"><div class="line"></div><div class="line"></div></div>
        <div class="prompt-label">Something I can politely decline:</div><div class="line-group"><div class="line"></div><div class="line"></div></div>
        <div class="prompt-label">Something I need to stop feeling guilty about:</div><div class="line-group"><div class="line"></div><div class="line"></div></div>
        """
    elif day == 10:
        body += '<div class="prompt-label" style="text-align:center; font-style:italic">“What makes me genuinely happy?”</div>'
        body += '<div class="box" style="margin-top:6px"><div class="box-title">✿  JOY LIST  ✿</div>'
        for i in range(1,16):
            body += f'<div style="display:flex; gap:8px; align-items:center; height:20px; border-bottom:1px solid #F0E2D6"><span style="font-size:8px; color:#C8B8DB; width:14px">{i}.</span><div style="flex:1"></div></div>'
        body += '</div>'
    elif day == 12:
        body += """
        <div class="box" style="margin-top:8px"><div class="box-title">My Digital Reset — Today I will…</div>
          <ul class="check-list">
            <li>30 minutes without social media</li>
            <li>Put my phone away during a meal</li>
            <li>Spend time outside</li>
            <li>Read something</li>
            <li>Have a quiet moment</li>
          </ul>
        </div>
        <div class="prompt-label">How did I feel afterward?</div><div class="line-group"><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>
        """
    elif day == 14:
        body += """
        <div class="two-col" style="margin-top:8px">
          <div class="box"><div class="box-title">Something I released</div><div class="line"></div><div class="line"></div><div class="line"></div></div>
          <div class="box"><div class="box-title">Something I discovered</div><div class="line"></div><div class="line"></div><div class="line"></div></div>
          <div class="box"><div class="box-title">Something that brought me joy</div><div class="line"></div><div class="line"></div><div class="line"></div></div>
          <div class="box"><div class="box-title">Something I want to change</div><div class="line"></div><div class="line"></div><div class="line"></div></div>
        </div>
        <div class="prompt-label" style="margin-top:12px">I am proud of myself for…</div><div class="line-group"><div class="line"></div><div class="line"></div></div>
        """
    elif day == 19:
        body += """
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-top:8px">
          <div class="box" style="text-align:center"><div style="font-size:16px">🌅</div><div class="box-title">Morning</div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>
          <div class="box" style="text-align:center"><div style="font-size:16px">☀️</div><div class="box-title">Afternoon</div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>
          <div class="box" style="text-align:center"><div style="font-size:16px">🌙</div><div class="box-title">Evening</div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>
        </div>
        <div class="prompt-label">One small habit I want to make easier:</div><div class="line-group"><div class="line"></div><div class="line"></div></div>
        """
    elif day == 24:
        labels = ["Something beautiful I saw:","Something delicious I tasted:","Something comforting I felt:","Something interesting I heard:","Something that made me smile:"]
        icons = ["👁️","🍓","🤲","👂","😊"]
        for lab, ic in zip(labels, icons):
            body += f'<div class="prompt-label">{ic} {lab}</div><div class="line-group"><div class="line"></div><div class="line"></div></div>'
    elif day == 26:
        body += """
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-top:8px">
          <div class="box" style="border-top:3px solid #D9A99A"><div class="box-title">Must Matter</div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>
          <div class="box" style="border-top:3px solid #A8B5A2"><div class="box-title">Matters to me</div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>
          <div class="box" style="border-top:3px solid #C8B8DB"><div class="box-title">Can wait</div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div></div>
        </div>
        <div class="prompt-label">What deserves more of my time and attention?</div><div class="line-group"><div class="line"></div><div class="line"></div></div>
        """
    elif day == 28:
        body += """
        <div style="text-align:center; font-family:'Cormorant Garamond',serif; font-style:italic; font-size:11px; color:#8B6B55; margin:6px 0">“Write a letter to yourself six months from now.”</div>
        <div style="background:#FFF; border:1px solid #E8DDD3; border-radius:12px; padding:14px">
          <div style="font-family:'Cormorant Garamond',serif; font-size:10px; color:#A68A7A; margin-bottom:6px">Dear Future Me,</div>
          <div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>
        </div>
        <div style="text-align:center; font-style:italic; font-size:9px; color:#9B8575; margin-top:10px">“Remember how you felt here. Remember what you wanted. Remember to be gentle with yourself.”</div>
        """
    elif day == 29:
        for sec in ["WHEN I'M TIRED, I WILL…","WHEN I'M OVERWHELMED, I WILL…","WHEN I NEED JOY, I WILL…","WHEN I NEED CONNECTION, I WILL…"]:
            body += f'<div class="prompt-label">{sec}</div><div class="line-group"><div class="line"></div><div class="line"></div></div>'
        body += '<div class="prompt-label">The people, places, and things that help me feel grounded:</div><div class="line-group"><div class="line"></div><div class="line"></div></div>'
    else:
        # generic prompts
        for p in prompts:
            if p in ["JOY LIST","LETTER","CHECKLIST"]:
                continue
            body += f'<div class="prompt-label">{p}</div><div class="line-group"><div class="line"></div><div class="line"></div>'
            # add extra line for many prompts
            if len(prompts) <=2:
                body += '<div class="line"></div>'
            body += '</div>'
        # Special handling for day 30 final statement
        if day == 30:
            body+= '<div style="text-align:center; margin-top:12px; padding:10px; background:#FFF1E8; border-radius:10px; border:1px dashed #D9A99A"><div style="font-family:\'Cormorant Garamond\',serif; font-style:italic; font-size:11px; color:#5C4033">“I choose to care for myself, one small moment at a time.”</div></div>'
        if day == 27:
            # already handled but generic covers
            pass
        if day == 15:
            # mirror decorative
            body = '<div style="text-align:center; margin:4px 0"><div style="width:90px; height:90px; border-radius:50%; border:2px solid #D9A99A; margin:0 auto; display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg,#FFF,#F2D5CB); font-size:36px">🪞</div><div style="font-size:8px; color:#A68A7A; letter-spacing:0.15em">— surrounded by flowers —</div></div>' + body
        if day == 22:
            body = body + '<div style="text-align:center; margin-top:8px; font-size:20px">📖 🫶 🛋️</div>'

    inner = f'<div style="display:flex; flex-direction:column; height:100%">{header}{title_html}{quote_html}<div style="flex:1; display:flex; flex-direction:column; margin-top:6px">{body}</div><div class="small-illust" style="margin-top:6px; font-size:10px; opacity:0.5">✿ — day {day} — ✿</div></div>'
    return page(inner)

for d in days:
    pages.append(make_daily(*d))

# BONUS PAGES

# 36 toolkit
pages.append(page("""
<div>
  <div class="label-small" style="text-align:center">Bonus</div>
  <h1 class="title" style="font-size:20px">MY SELF-CARE TOOLKIT</h1>
  <div class="divider"></div>
  <div class="small-illust">🌿 ✿ 🌿</div>
  <div style="display:flex; flex-direction:column; gap:10px; margin-top:10px">
    <div class="box"><div class="box-title">🤲 When I need rest</div><div class="line"></div><div class="line"></div><div class="line"></div></div>
    <div class="box"><div class="box-title">💛 When I need comfort</div><div class="line"></div><div class="line"></div><div class="line"></div></div>
    <div class="box"><div class="box-title">✨ When I need motivation</div><div class="line"></div><div class="line"></div><div class="line"></div></div>
    <div class="box"><div class="box-title">🤝 When I need connection</div><div class="line"></div><div class="line"></div><div class="line"></div></div>
    <div class="box"><div class="box-title">🤫 When I need quiet</div><div class="line"></div><div class="line"></div><div class="line"></div></div>
  </div>
</div>
"""))

# 37 menu
pages.append(page("""
<div>
  <h1 class="title" style="font-size:20px">MY SELF-CARE MENU</h1>
  <div class="divider"></div>
  <div class="small-illust">☕ ✿ 🕯️ ✿ 🌿</div>
  <div style="display:grid; grid-template-columns:1fr; gap:12px; margin-top:12px">
    <div class="box" style="border-left:4px solid #A8B5A2"><div class="box-title" style="text-align:left">🌿 5-Minute Care</div>
      <div style="display:flex; flex-direction:column; gap:2px; margin-top:6px">
        <div style="display:flex; gap:8px; align-items:center; height:20px; border-bottom:1px solid #E8DDD3"><span style="color:#A8B5A2">☐</span><div style="flex:1"></div></div>
        <div style="display:flex; gap:8px; align-items:center; height:20px; border-bottom:1px solid #E8DDD3"><span style="color:#A8B5A2">☐</span><div style="flex:1"></div></div>
        <div style="display:flex; gap:8px; align-items:center; height:20px; border-bottom:1px solid #E8DDD3"><span style="color:#A8B5A2">☐</span><div style="flex:1"></div></div>
      </div>
    </div>
    <div class="box" style="border-left:4px solid #D9A99A"><div class="box-title" style="text-align:left">☕ 30-Minute Care</div>
      <div style="display:flex; flex-direction:column; gap:2px; margin-top:6px">
        <div style="display:flex; gap:8px; align-items:center; height:20px; border-bottom:1px solid #E8DDD3"><span style="color:#D9A99A">☐</span><div style="flex:1"></div></div>
        <div style="display:flex; gap:8px; align-items:center; height:20px; border-bottom:1px solid #E8DDD3"><span style="color:#D9A99A">☐</span><div style="flex:1"></div></div>
        <div style="display:flex; gap:8px; align-items:center; height:20px; border-bottom:1px solid #E8DDD3"><span style="color:#D9A99A">☐</span><div style="flex:1"></div></div>
      </div>
    </div>
    <div class="box" style="border-left:4px solid #C8B8DB"><div class="box-title" style="text-align:left">🌙 Slow-Day Care</div>
      <div style="display:flex; flex-direction:column; gap:2px; margin-top:6px">
        <div style="display:flex; gap:8px; align-items:center; height:20px; border-bottom:1px solid #E8DDD3"><span style="color:#C8B8DB">☐</span><div style="flex:1"></div></div>
        <div style="display:flex; gap:8px; align-items:center; height:20px; border-bottom:1px solid #E8DDD3"><span style="color:#C8B8DB">☐</span><div style="flex:1"></div></div>
        <div style="display:flex; gap:8px; align-items:center; height:20px; border-bottom:1px solid #E8DDD3"><span style="color:#C8B8DB">☐</span><div style="flex:1"></div></div>
      </div>
    </div>
  </div>
  <div class="small-illust" style="margin-top:14px">✿ — choose what fits today — ✿</div>
</div>
"""))

# 38 remember
pages.append(page("""
<div style="display:flex; flex-direction:column; height:100%">
  <h1 class="title" style="font-size:20px">THINGS I WANT TO REMEMBER</h1>
  <div class="divider"></div>
  <div class="small-illust">✿ 🌿 ✿</div>
  <div style="margin-top:10px; background:#FFF; border:1px solid #F0E2D6; border-radius:12px; padding:14px 16px; flex:1">
"""+ "".join([f'<div style="display:flex; gap:10px; align-items:center; height:22px; border-bottom:1px solid #E8DDD3"><span style="font-family:\'Cormorant Garamond\',serif; font-size:10px; color:#D9A99A; width:18px">{i}.</span><div style="flex:1"></div></div>' for i in range(1,21)]) + """
  </div>
  <div class="quote-box center" style="margin-top:10px">“There is always something worth remembering.”</div>
</div>
"""))

# 39 looking back
pages.append(page("""
<div>
  <h1 class="title" style="font-size:20px">LOOKING BACK</h1>
  <div class="divider"></div>
  <div class="small-illust">🌿 ✿ 🌿</div>
  <div style="display:flex; flex-direction:column; gap:12px; margin-top:10px">
    <div><div class="prompt-label">The biggest lesson I learned:</div><div class="line-group"><div class="line"></div><div class="line"></div></div></div>
    <div><div class="prompt-label">The habit I want to keep:</div><div class="line-group"><div class="line"></div><div class="line"></div></div></div>
    <div><div class="prompt-label">The boundary I want to protect:</div><div class="line-group"><div class="line"></div><div class="line"></div></div></div>
    <div><div class="prompt-label">The thing I want more of:</div><div class="line-group"><div class="line"></div><div class="line"></div></div></div>
    <div><div class="prompt-label">The thing I want less of:</div><div class="line-group"><div class="line"></div><div class="line"></div></div></div>
    <div><div class="prompt-label">The version of myself I'm becoming:</div><div class="line-group"><div class="line"></div><div class="line"></div><div class="line"></div></div></div>
  </div>
</div>
"""))

# 40 final
pages.append(page("""
<div style="flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center">
  <div class="illustration" style="font-size:26px">🕯️  📓  🫖  🌸</div>
  <div style="width:260px; height:160px; border-radius:18px; background:linear-gradient(180deg,#FFF4E8 0%,#2C2A4A 100%); border:1px solid #E8DDD3; display:flex; align-items:center; justify-content:center; margin:16px 0; position:relative; overflow:hidden">
    <div style="position:absolute; inset:0; background:radial-gradient(ellipse at 50% 30%, #FFD9A0 0%, transparent 60%)"></div>
    <div style="position:relative; text-align:center">
      <div style="font-size:32px">🪟 ✨</div>
      <div style="font-size:9px; color:#FFF; opacity:0.8; margin-top:4px">evening journal • candle glow</div>
    </div>
  </div>
  <h1 style="font-family:'Cormorant Garamond',serif; font-size:26px; font-weight:700; color:#5C4033; letter-spacing:0.06em">YOU MADE SPACE<br>FOR YOURSELF.</h1>
  <div class="divider"></div>
  <p style="font-size:10.5px; line-height:1.7; color:#6B4E3D; max-width:420px; margin-top:6px">Keep choosing the little moments that make life feel softer,<br>slower, and more meaningful.</p>
  <p style="font-family:'Cormorant Garamond',serif; font-style:italic; font-size:12px; color:#8B6B55; margin-top:12px">Your journey doesn't end here.</p>
  <div class="small-illust" style="margin-top:18px">—  ✿  🌿  ✿  —</div>
  <div style="margin-top:18px; font-size:7px; letter-spacing:0.2em; text-transform:uppercase; color:#B0A099">30 Days of Self-Care — A Gentle Journey Back to Yourself</div>
</div>
""", bg='<div class="bg-blob" style="width:380px;height:380px;background:#EDE7F3;top:-60px;left:-60px"></div><div class="bg-blob" style="width:320px;height:320px;background:#F2D5CB;bottom:-60px;right:-60px"></div>'))

full = html_head + "\n".join(pages) + "\n</body></html>"
path = pathlib.Path("/home/user/animated-doodle/journal.html")
path.write_text(full, encoding="utf-8")
print(f"Wrote {len(pages)} pages to {path}")
