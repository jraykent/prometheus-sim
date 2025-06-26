# reset_logs.py
import os

log_dir = "logs"
files_to_delete = ["personas_state.json", "persona_log.json"]

for fname in files_to_delete:
    path = os.path.join(log_dir, fname)
    if os.path.exists(path):
        os.remove(path)
        print(f"✅ Deleted: {path}")
    else:
        print(f"❌ File not found (already deleted): {path}")

