# AI Usage
- **Tools:** Claude, used to read the brief and data, draft `search.py`, and write the docs.
- **Main prompts:** "Read the assignment, emails and CSVs, then build a minimal search: CLI + batch, stdlib only, honour the email constraints (no API calls, daily-changing data, stock, brand-first)."
- **Where it went wrong:**
  1. First version ranked chocolate bars above real milk for "milk". Found by running the query the ops lead complained about; fixed with the head-noun boost.
  2. The first run failed because a shell brace-copy of data files didn't work. Found from the error; fixed by copying files explicitly.
  3. Known remaining issue: "thela select ghee" also returns other Thela Select products because brand words match. Not fixed yet.
- **Verification:** manual spot checks on sample queries only; no judged evaluation set yet.
