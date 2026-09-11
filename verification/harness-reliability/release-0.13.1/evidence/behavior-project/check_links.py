from pathlib import Path
import re,json
root=Path(__file__).resolve().parent
links=re.findall(r"\]\(([^)]+)\)",(root/"README.md").read_text(encoding="utf-8"))
missing=[x for x in links if not (root/x).is_file()]
print(json.dumps({"checked":len(links),"missing":missing}))
raise SystemExit(bool(missing))
