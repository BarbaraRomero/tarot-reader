"""Parse card meanings (A. E. Waite, 1910, public domain) from the extracted LWB text into cards.json.
Usage: python parse_lwb.py lwb.txt ../cards.json
"""
import json, re, sys

src, dst = sys.argv[1], sys.argv[2]
raw = open(src, encoding="utf-8").read()

# keep only the meanings section (Greater Arcana up to the Lesser Arcana end, before the "method" chapter)
start = raw.index("THE GREATER ARCANA &")
text = raw[start:]
# strip page markers and lone page numbers
text = re.sub(r"=====PAGE \d+=====\n", "", text)
text = re.sub(r"\n\d+\n", "\n", text)
text = re.sub(r"(?<=[a-z])\d+\n", "\n", text)          # "televi8" style trailing page numbers
text = re.sub(r"-\n(?=[a-z])", "", text)                 # hyphenated line breaks
text = text.replace("\n", " ")
text = re.sub(r"\s+", " ", text)
text = text.replace("ven-geance", "vengeance").replace("evilside", "evil side").replace("thingsseen", "things seen").replace("santified", "sanctified")
text = re.sub(r"(?<=[a-z])\.(?=[A-Z])", ". ", text)
text = re.sub(r",(?=[a-z])", ", ", text)

ROMAN_ORDER = ["THE FOOL", "THE MAGICIAN", "THE HIGH PRIESTESS", "THE EMPRESS", "THE EMPEROR",
    "THE HIEROPHANT", "THE LOVERS", "THE CHARIOT", "STRENGTH", "THE HERMIT", "WHEEL OF FORTUNE",
    "JUSTICE", "THE HANGED MAN", "DEATH", "TEMPERANCE", "THE DEVIL", "THE TOWER", "THE STAR",
    "THE MOON", "THE SUN", "THE LAST JUDGMENT", "THE WORLD"]
FILES = ["00-TheFool", "01-TheMagician", "02-TheHighPriestess", "03-TheEmpress", "04-TheEmperor",
    "05-TheHierophant", "06-TheLovers", "07-TheChariot", "08-Strength", "09-TheHermit",
    "10-WheelOfFortune", "11-Justice", "12-TheHangedMan", "13-Death", "14-Temperance", "15-TheDevil",
    "16-TheTower", "17-TheStar", "18-TheMoon", "19-TheSun", "20-Judgement", "21-TheWorld"]

def split_rev(s):
    s = s.strip()
    m = re.search(r"\bReversed:\s*", s)
    if not m:
        return s, ""
    return s[:m.start()].strip(), s[m.end():].strip()

cards = []
greater, lesser = text.split("THE LESSER ARCANA", 1)
lesser = lesser.split("THE CELTIC CROSS", 1)[0]
greater = greater.split("It will be seen that", 1)[0]
for i, name in enumerate(ROMAN_ORDER):
    num = 0 if name == "THE FOOL" else i
    m = re.search(rf"\b{num}\.\s*{re.escape(name)}—(.*?)(?=\b\d{{1,2}}\.\s*(?:THE |STRENGTH|WHEEL|JUSTICE|DEATH|TEMPERANCE)|$)", greater)
    up, rev = split_rev(m.group(1))
    title = name.title().replace("Last Judgment", "Judgement")
    cards.append({"id": FILES[i], "name": title, "arcana": "Major", "number": num,
                  "description": "", "upright": up.rstrip("."), "reversed": rev.rstrip(".")})

RANKS = ["ACE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN",
         "PAGE", "KNIGHT", "QUEEN", "KING"]
lesser = re.sub(r"OF(?=[A-Z])", "OF ", lesser)            # "OFCUPS" / "OFWANDS"
head = r"\b(" + "|".join(RANKS) + r") OF (WANDS|CUPS|SWORDS|PENTACLES)—"
parts = re.split(head, lesser)
for k in range(1, len(parts), 3):
    rank, suit, body = parts[k], parts[k + 1], parts[k + 2]
    body = re.sub(r"\s(WANDS|CUPS|SWORDS|PENTACLES|THE METHOD.*|AN ANCIENT CELTIC.*)\s*$", "", body.strip())
    if "Divinatory Meanings:" in body:
        desc, rest = body.split("Divinatory Meanings:", 1)
    else:
        desc, rest = "", body
    up, rev = split_rev(rest)
    idx = RANKS.index(rank) + 1
    cards.append({"id": f"{suit.title()}{idx:02d}", "name": f"{rank.title()} of {suit.title()}",
                  "arcana": "Minor", "suit": suit.title(), "number": idx,
                  "description": desc.strip(), "upright": up.rstrip("."), "reversed": rev.rstrip(".")})

json.dump(cards, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(cards), "cards")
