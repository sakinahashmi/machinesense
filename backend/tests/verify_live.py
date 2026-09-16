import urllib.request
import json

data = json.dumps({
    "component_id": "CNC-2847",
    "machine_id": "CNC-07",
    "failure_type": "Dimensional Inspection Failure"
}).encode()

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/investigations/analyze",
    data=data,
    headers={"Content-Type": "application/json"}
)

res = urllib.request.urlopen(req)
res_json = json.loads(res.read().decode())

print("=== LIVE ROOT CAUSE ANALYSIS FOR CNC-2847 ===")
for i, r in enumerate(res_json["root_cause_ranking"]):
    print(f"#{i+1} {r['root_cause']}: {r['confidence']}% ({r['confidence_level']}, {r['severity']})")

print("\n=== TOOL WEAR EVIDENCE ITEMS ===")
for ev in res_json["root_cause_ranking"][0]["evidence"]:
    print(f" - [{ev['category']}] {ev['title']}: {ev['description']}")

print("\n=== TECHNICAL SUMMARY ===")
print(res_json["investigation_summary"]["technical_narrative"])
