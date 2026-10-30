# Thelawala Search

## Run
```
python search.py "oil under 200"                 # CLI, one query
python search.py                                 # prompts for a query
python search.py --batch queries.txt             # writes results.jsonl (up to 10 sku_ids per query)
```
Python 3 standard library only. No external calls, runs on a laptop. Reads `catalog.csv` + `inventory.csv` fresh on every run, so daily data changes need no manual edits.

## How it works
1. Tokenise and normalise (lowercase, split "1ltr" -> "1 l", synonyms like doodh->milk, pwdr->powder).
2. Typo fix: unknown words are matched to the closest catalog word (difflib).
3. Score each product with IDF-weighted term matching: name/brand > category > description. A match on the product's head noun ("Full Cream **Milk**" vs "**Milk** Chocolate") gets a big boost, which fixes Sandeep's "milk" complaint.
4. Partial matches are penalised; exact phrase matches are boosted.
5. "under N" / "below N" in a query becomes a price cap.

## Decisions (and why)
- **Stock:** Sandeep and Farah disagree. I show out-of-stock items but demote them and label them with the restock ETA. Discontinued items, and SKUs missing from inventory, are never shown (can't be delivered).
- **Thela Select:** only a small 5% tiebreak, and none when the customer types a brand. Follows Kavya: customer first, margin second.
- **Click logs:** `search_log.jsonl` was not in my pack, so click popularity is NOT used. Next step below.
- **Prices:** `metro_feed` prices are ~100x higher than others (looks like paise). I divide by 100. This is an assumption; it likely explains the "wrong prices" complaint and should be confirmed with Finance.
- **Data quirks:** `inventory_1.csv` is identical to `inventory.csv` (ignored). 41 catalog SKUs have no inventory row (hidden). Names have inconsistent casing/units, handled by normalisation.

## Next steps
- Use search-log clicks as a gentle, capped ranking signal (watch position bias).
- Hindi/Telugu transliteration and a larger synonym list mined from zero-result queries.
- Parse size/unit queries ("1 l milk") and handle brand-only queries explicitly.
- Inverted index for the 20,000-product scale (currently a linear scan, fine at ~1,100).
- Small web UI; evaluation set with judged queries.
