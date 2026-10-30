"""Thelawala search. Usage: python search.py "milk"  |  python search.py --batch queries.txt"""
import csv, json, math, re, sys, difflib
from collections import Counter, defaultdict
from datetime import datetime

SYN = {"doodh": "milk", "chawal": "rice", "atta": "flour", "tel": "oil", "cheeni": "sugar",
       "namak": "salt", "dahi": "curd", "paneer": "cottage cheese", "ltr": "l", "litre": "l",
       "liter": "l", "kilo": "kg", "gm": "g", "gram": "g", "grams": "g", "pwdr": "powder"}
STOP = {"under", "below", "less", "than", "for", "the", "a", "of", "rs", "rupees", "in"}

def tok(s):
    s = re.sub(r"(\d)([a-z])", r"\1 \2", re.sub(r"([a-z])(\d)", r"\1 \2", s.lower()))
    return [SYN.get(t, t) for t in re.findall(r"[a-z0-9]+", s)]

def load(cat="catalog.csv", inv="inventory.csv"):
    stock = {}
    for r in csv.DictReader(open(inv, encoding="utf-8-sig")):
        stock[r["sku_id"]] = r
    docs = []
    for r in csv.DictReader(open(cat, encoding="utf-8-sig")):
        p = float(r["price"])
        # metro_feed prices are ~100x too high (paise, not rupees) -> normalise
        if r["supplier"] == "metro_feed":
            p /= 100
        s = stock.get(r["sku_id"])
        if s is None or s["status"] == "discontinued":
            continue  # unknown stock or discontinued: never show
        qty = int(float(s["stock_qty"] or 0))
        d = dict(r, price=p, qty=qty, eta=s["restock_eta"] or None)
        d["name_t"] = tok(r["name"] + " " + r["brand"])
        d["cat_t"] = tok(r["category"])
        # "head noun" = last word of the name before size/flavour part, e.g. "Full Cream Milk 1 L" -> milk
        core = re.split(r"\s[-(]|\d", r["name"].lower())[0]
        ct = tok(core)
        d["head"] = ct[-1] if ct else ""
        d["desc_t"] = tok(r["description"] or "")
        docs.append(d)
    return docs

class Index:
    def __init__(self, docs):
        self.docs = docs
        self.df = Counter()
        for d in docs:
            self.df.update(set(d["name_t"] + d["cat_t"] + d["desc_t"]))
        self.vocab = list(self.df)
        self.N = len(docs)

    def idf(self, t):
        return math.log(1 + self.N / (1 + self.df.get(t, 0)))

    def fix(self, t):
        if t in self.df or t.isdigit() or len(t) < 4:
            return t
        m = difflib.get_close_matches(t, self.vocab, 1, 0.8)
        return m[0] if m else t

    def search(self, q, k=10):
        ql = q.lower()
        maxp = None
        m = re.search(r"(?:under|below|less than|<)\s*(?:rs\.?|₹)?\s*(\d+)", ql)
        if m:
            maxp = float(m.group(1)); ql = ql.replace(m.group(0), " ")
        qt = [self.fix(t) for t in tok(ql) if t not in STOP]
        if not qt:
            return []
        scored = []
        for d in self.docs:
            if maxp and d["price"] > maxp:
                continue
            s, hit = 0.0, 0
            for t in qt:
                w = self.idf(t)
                if t in d["name_t"]:
                    # earlier position in name = more likely the head noun/product itself
                    s += w * (2.0 + (1.5 if t == d["head"] else 0)); hit += 1
                elif t in d["cat_t"]:
                    s += w * 0.8; hit += 1
                elif t in d["desc_t"]:
                    s += w * 0.3; hit += 1
            if hit < len(qt) and hit == 0:
                continue
            s *= 0.5 + 0.5 * hit / len(qt)  # penalise partial matches
            if " ".join(qt) in " ".join(d["name_t"]):
                s *= 1.3  # phrase match
            # brand queried explicitly -> boost; otherwise Thela Select only a gentle tiebreak
            brand_q = any(t in tok(d["brand"]) for t in qt)
            if d["brand"] == "Thela Select" and not brand_q:
                s *= 1.05
            if d["qty"] <= 0:
                s *= 0.5  # out of stock: shown, but demoted (Farah) and flagged
            scored.append((s, d))
        scored.sort(key=lambda x: -x[0])
        return [d for _, d in scored[:k]]

def fmt(d):
    st = "in stock" if d["qty"] > 0 else f"out of stock, back {d['eta'] or 'soon (TBD)'}"
    return f"{d['sku_id']}  {d['name']}  Rs{d['price']:g}  [{st}]"

if __name__ == "__main__":
    ix = Index(load())
    if len(sys.argv) > 2 and sys.argv[1] == "--batch":
        with open("results.jsonl", "w") as out:
            for q in open(sys.argv[2], encoding="utf-8"):
                q = q.strip()
                if q:
                    out.write(json.dumps({"query": q, "results": [d["sku_id"] for d in ix.search(q)]}) + "\n")
    else:
        q = " ".join(sys.argv[1:]) or input("search> ")
        for d in ix.search(q):
            print(fmt(d))
