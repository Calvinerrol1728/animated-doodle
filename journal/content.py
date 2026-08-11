# -*- coding: utf-8 -*-
"""
Exact text content for "30 Days of Self-Care — A Gentle Journey Back to Yourself".

Every string here is rendered verbatim into the PDF. Nothing is paraphrased.

Page block types:
  quote     — centred italic serif pull-quote
  prompt    — a question/label followed by N ruled writing lines
  lines     — N bare ruled writing lines
  numbered  — numbered ruled lines (1. 2. 3. ...)
  checklist — checkbox rows
  boxes     — labelled panels laid out in a row or column
  statement — large centred display text
  body      — a paragraph of running text
  spacer    — vertical gap
"""

TITLE = "30 Days of Self-Care"
SUBTITLE = "A Gentle Journey Back to Yourself"
TAGLINE = "A 30-Day Journal for Rest, Reflection & Self-Love"

# --------------------------------------------------------------------------
# Front matter
# --------------------------------------------------------------------------

BELONGS = {
    "title": "THIS JOURNAL BELONGS TO",
    "quote": "\u201cI\u2019m giving myself permission to slow down, "
             "breathe deeply, and take care of myself.\u201d",
}

WELCOME = {
    "title": "WELCOME TO YOUR 30 DAYS OF SELF-CARE",
    "body": [
        "\u201cSelf-care doesn\u2019t have to be complicated. Sometimes it is a quiet "
        "morning, a good night\u2019s sleep, a walk outside, a nourishing meal, or "
        "simply giving yourself permission to rest.\u201d",
        "\u201cFor the next 30 days, this journal is your little space to pause, "
        "listen to yourself, and reconnect with what you need.\u201d",
    ],
    "quote": "\u201cYou deserve the same kindness you give to others.\u201d",
}

GUIDE = {
    "title": "A GENTLE GUIDE",
    "items": [
        "Take a few quiet minutes each day.",
        "Answer the prompts honestly\u2014there are no wrong answers.",
        "Skip anything that doesn\u2019t feel right for you.",
        "Celebrate small acts of care.",
        "Remember that progress doesn\u2019t have to be perfect.",
    ],
    "quote": "\u201cSmall moments of care can become a beautiful life.\u201d",
}

PROMISE = {
    "title": "MY PROMISE TO MYSELF",
    "prompts": [
        "During these 30 days, I promise to\u2026",
        "I will be kinder to myself by\u2026",
        "I will make space for\u2026",
        "I give myself permission to\u2026",
        "When I need rest, I will\u2026",
    ],
}

# --------------------------------------------------------------------------
# 30 daily pages
# --------------------------------------------------------------------------
# Each entry: (day number, title, [blocks])

DAYS = [
    (1, "PAUSE", [
        ("quote", "\u201cYou don\u2019t always have to be moving forward. "
                  "Sometimes you simply need to pause.\u201d"),
        ("prompt", "How am I feeling today?", 3),
        ("prompt", "What has been taking up most of my energy lately?", 3),
        ("prompt", "What would feel comforting right now?", 3),
    ], "tea"),

    (2, "GRATITUDE", [
        ("quote", "\u201cThere is beauty in ordinary moments.\u201d"),
        ("label", "Three things I\u2019m grateful for today:"),
        ("numbered", 3),
        ("prompt", "A small moment that made me smile:", 2),
        ("prompt", "Something I often overlook but appreciate:", 2),
    ], "flowers"),

    (3, "REST", [
        ("quote", "\u201cRest is not something you have to earn.\u201d"),
        ("prompt", "What does true rest look like for me?", 3),
        ("prompt", "When do I feel most rested?", 3),
        ("prompt", "What can I let go of today?", 3),
    ], "bed"),

    (4, "MY ENERGY", [
        ("boxes2", ["WHAT DRAINS ME", "WHAT REFILLS ME"], 7),
        ("prompt", "One thing I can do today to protect my energy is\u2026", 3),
    ], "sun"),

    (5, "MY BODY", [
        ("quote", "\u201cYour body speaks quietly. Give yourself time to listen.\u201d"),
        ("prompt", "What does my body need today?", 3),
        ("prompt", "Have I been giving myself enough rest?", 2),
        ("prompt", "What makes me feel comfortable and cared for?", 3),
        ("prompt", "One kind thing I can do for my body today:", 2),
    ], "leaf"),

    (6, "MY MIND", [
        ("subtitle", "QUIET YOUR MIND"),
        ("prompt", "What thoughts have been occupying my mind?", 2),
        ("prompt", "Which thoughts can I release?", 2),
        ("prompt", "What deserves my attention instead?", 2),
        ("panel", "LET IT OUT", 8),
    ], "candle"),

    (7, "WEEK ONE \u2014 REFLECTION", [
        ("prompt", "What did I learn about myself this week?", 3),
        ("prompt", "Which self-care activity felt best?", 2),
        ("prompt", "What made me feel peaceful?", 2),
        ("prompt", "What do I want more of next week?", 2),
        ("prompt", "My favorite moment this week:", 2),
    ], "flowers"),

    (8, "BOUNDARIES", [
        ("quote", "\u201cProtecting your peace is an act of self-respect.\u201d"),
        ("prompt", "Where do I need stronger boundaries?", 3),
        ("prompt", "What am I saying yes to when I really mean no?", 3),
        ("prompt", "What boundary would help me feel more at peace?", 2),
        ("prompt", "One boundary I can practice this week:", 2),
    ], "fern"),

    (9, "SAY NO", [
        ("statement", "\u201cNO IS A COMPLETE SENTENCE.\u201d"),
        ("prompt", "Something I don\u2019t actually want to do:", 3),
        ("prompt", "Something I can politely decline:", 3),
        ("prompt", "Something I need to stop feeling guilty about:", 3),
    ], "leaf"),

    (10, "FIND YOUR JOY", [
        ("quote", "\u201cWhat makes me genuinely happy?\u201d"),
        ("label", "MY JOY LIST"),
        ("numbered", 15),
    ], "flowers"),

    (11, "INNER CHILD", [
        ("quote", "\u201cSometimes caring for yourself means remembering "
                  "what once made you smile.\u201d"),
        ("prompt", "What did I love doing as a child?", 3),
        ("prompt", "What made me feel safe and happy?", 3),
        ("prompt", "Which childhood joy could I bring back into my life?", 3),
    ], "wildflower"),

    (12, "UNPLUG", [
        ("subtitle", "DIGITAL RESET"),
        ("checklist", [
            "30 minutes without social media",
            "Put my phone away during a meal",
            "Spend time outside",
            "Read something",
            "Have a quiet moment",
        ]),
        ("prompt", "How did I feel afterward?", 5),
    ], "leaf"),

    (13, "MY SPACE", [
        ("subtitle", "CREATE A PEACEFUL SPACE"),
        ("prompt", "What area of my home needs attention?", 2),
        ("prompt", "What could I remove?", 2),
        ("prompt", "What could I add to make it feel more peaceful?", 2),
        ("panel", "TODAY I WILL RESET:", 4),
    ], "plant"),

    (14, "WEEK TWO \u2014 REFLECTION", [
        ("boxes2", ["Something I released", "Something I discovered"], 5),
        ("boxes2", ["Something that brought me joy", "Something I want to change"], 5),
        ("prompt", "I am proud of myself for\u2026", 3),
    ], "eucalyptus"),

    (15, "SELF-LOVE", [
        ("statement", "\u201cSpeak to yourself like someone "
                      "you deeply care about.\u201d"),
        ("prompt", "What would I say to a friend who felt the way I feel?", 3),
        ("prompt", "What kind words do I need to hear today?", 3),
        ("prompt", "How can I show myself more compassion?", 3),
    ], "rose"),

    (16, "MY STRENGTHS", [
        ("label", "Three things I\u2019m good at:"),
        ("numbered", 3),
        ("label", "Three challenges I\u2019ve overcome:"),
        ("numbered", 3),
        ("prompt", "Something I once thought I couldn\u2019t do:", 2),
        ("prompt", "A strength I sometimes forget I have:", 2),
    ], "mountain"),

    (17, "LET GO", [
        ("quote", "\u201cYou are allowed to release what no longer "
                  "belongs in your heart.\u201d"),
        ("prompt", "Something I\u2019m ready to forgive myself for:", 3),
        ("prompt", "Something I\u2019m ready to stop carrying:", 3),
        ("prompt", "What would letting go make room for?", 3),
    ], "leaf"),

    (18, "DREAM A LITTLE", [
        ("quote", "\u201cIf I wasn\u2019t afraid of failing, what would I try?\u201d"),
        ("prompt", "A dream I\u2019ve been carrying\u2026", 3),
        ("prompt", "Something I\u2019d love to experience\u2026", 3),
        ("prompt", "A place I\u2019d love to visit\u2026", 2),
        ("prompt", "A life I\u2019d love to create\u2026", 3),
    ], "moon"),

    (19, "GENTLER ROUTINE", [
        ("boxes3", ["MORNING", "AFTERNOON", "EVENING"], 8),
        ("prompt", "One small habit I want to make easier:", 3),
    ], "sun"),

    (20, "NOURISH YOURSELF", [
        ("prompt", "What makes me feel nourished?", 3),
        ("prompt", "What does my mind need?", 3),
        ("prompt", "What does my body need?", 3),
        ("prompt", "What does my heart need?", 3),
    ], "kitchen"),

    (21, "WEEK THREE \u2014 REFLECTION", [
        ("prompt", "What has changed in me?", 3),
        ("prompt", "What habit feels good?", 2),
        ("prompt", "What am I learning to prioritize?", 2),
        ("prompt", "What am I becoming more comfortable saying no to?", 2),
        ("prompt", "My biggest realization this week:", 2),
    ], "eucalyptus"),

    (22, "REST WITHOUT GUILT", [
        ("statement", "\u201cYour worth is not measured by "
                      "how much you accomplish.\u201d"),
        ("prompt", "What makes me feel guilty about resting?", 3),
        ("prompt", "What would happen if I allowed myself to rest anyway?", 3),
        ("prompt", "How can I make today slower?", 3),
    ], "blanket"),

    (23, "CONNECTION", [
        ("prompt", "Who makes me feel safe and understood?", 3),
        ("prompt", "Who would I like to spend more time with?", 3),
        ("prompt", "Who could use a little kindness from me today?", 3),
        ("prompt", "Someone I want to reach out to:", 2),
    ], "wildflower"),

    (24, "NOTICE THE LITTLE THINGS", [
        ("prompt", "Something beautiful I saw:", 2),
        ("prompt", "Something delicious I tasted:", 2),
        ("prompt", "Something comforting I felt:", 2),
        ("prompt", "Something interesting I heard:", 2),
        ("prompt", "Something that made me smile:", 2),
    ], "wildflower"),

    (25, "MY IDEAL DAY", [
        ("quote", "\u201cImagine a day where you feel peaceful, fulfilled, "
                  "and completely yourself.\u201d"),
        ("prompt", "I wake up\u2026", 2),
        ("prompt", "I spend my morning\u2026", 2),
        ("prompt", "I spend my afternoon\u2026", 2),
        ("prompt", "I spend my evening\u2026", 2),
        ("prompt", "Before bed, I feel\u2026", 2),
    ], "window"),

    (26, "WHAT REALLY MATTERS?", [
        ("boxes3", ["MUST MATTER", "MATTERS TO ME", "CAN WAIT"], 8),
        ("prompt", "What deserves more of my time and attention?", 3),
    ], "olive"),

    (27, "CELEBRATE YOURSELF", [
        ("statement", "\u201cLOOK HOW FAR YOU\u2019VE COME.\u201d"),
        ("prompt", "Something I accomplished recently:", 2),
        ("prompt", "Something I\u2019m proud of:", 2),
        ("prompt", "Something I handled better than before:", 2),
        ("prompt", "Something I want to celebrate about myself:", 2),
    ], "flowers"),

    (28, "A LETTER TO MY FUTURE SELF", [
        ("quote", "\u201cWrite a letter to yourself six months from now.\u201d"),
        ("lines", 16),
        ("footer", "\u201cRemember how you felt here. Remember what you wanted. "
                   "Remember to be gentle with yourself.\u201d"),
    ], "envelope"),

    (29, "MY PERSONAL SELF-CARE PLAN", [
        ("prompt", "WHEN I\u2019M TIRED, I WILL\u2026", 3),
        ("prompt", "WHEN I\u2019M OVERWHELMED, I WILL\u2026", 3),
        ("prompt", "WHEN I NEED JOY, I WILL\u2026", 3),
        ("prompt", "WHEN I NEED CONNECTION, I WILL\u2026", 3),
        ("prompt", "The people, places, and things that help me feel grounded:", 3),
    ], "olive"),

    (30, "I CHOOSE ME", [
        ("statement", "\u201cTaking care of myself isn\u2019t selfish. "
                      "It is a way of honoring the life I\u2019m living.\u201d"),
        ("prompt", "What have these 30 days taught me?", 3),
        ("prompt", "What changed within me?", 2),
        ("prompt", "What will I continue doing?", 2),
        ("prompt", "What promise will I make to myself moving forward?", 2),
        ("footer", "\u201cI choose to care for myself, one small moment at a time.\u201d"),
    ], "sunrise"),
]

# --------------------------------------------------------------------------
# Bonus pages
# --------------------------------------------------------------------------

TOOLKIT = {
    "title": "MY SELF-CARE TOOLKIT",
    "sections": [
        "WHEN I NEED REST", "WHEN I NEED COMFORT", "WHEN I NEED MOTIVATION",
        "WHEN I NEED CONNECTION", "WHEN I NEED QUIET",
    ],
}

MENU = {
    "title": "MY SELF-CARE MENU",
    "sections": [("5-MINUTE CARE", 3), ("30-MINUTE CARE", 3), ("SLOW-DAY CARE", 3)],
}

REMEMBER = {
    "title": "THINGS I WANT TO REMEMBER",
    "count": 20,
    "footer": "\u201cThere is always something worth remembering.\u201d",
}

LOOKING_BACK = {
    "title": "LOOKING BACK",
    "prompts": [
        "The biggest lesson I learned:",
        "The habit I want to keep:",
        "The boundary I want to protect:",
        "The thing I want more of:",
        "The thing I want less of:",
        "The version of myself I\u2019m becoming:",
    ],
}

FINAL = {
    "statement": "\u201cYOU MADE SPACE FOR YOURSELF.\u201d",
    "body": "\u201cKeep choosing the little moments that make life feel softer, "
            "slower, and more meaningful.\u201d",
    "last": "\u201cYour journey doesn\u2019t end here.\u201d",
}
