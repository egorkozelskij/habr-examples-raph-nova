"""Restore the approved MP4 files and verify their published bytes."""

import hashlib
import json
import sys
from pathlib import Path

repository = Path(__file__).resolve().parent.parent
destination = Path(sys.argv[1]) / "videos"
destination.mkdir(parents=True, exist_ok=True)
manifest = json.loads((repository / "video-parts/manifest.json").read_text())

for video in manifest["videos"]:
    output = destination / video["name"]
    if "parts" in video:
        with output.open("wb") as assembled:
            for part in video["parts"]:
                assembled.write((repository / "video-parts" / part).read_bytes())
    data = output.read_bytes()
    if len(data) != video["bytes"] or hashlib.sha256(data).hexdigest() != video["sha256"]:
        raise SystemExit(f"Video integrity check failed: {video['name']}")
    print(f"Verified {video['name']}: {len(data)} bytes")
