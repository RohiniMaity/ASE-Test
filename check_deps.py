"""Check every pinned dependency in a requirements file against PyPI."""

import json
import sys
import urllib.error
import urllib.parse
import urllib.request

PYPI = "https://pypi.org/pypi"


def fetch_json(url):
    """Return parsed JSON for url, or None on 404."""
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def parse_line(line):
    """Split 'name==version' into (name, version); version is None if unpinned."""
    line = line.split("#", 1)[0].strip()
    if "==" in line:
        name, version = line.split("==", 1)
        return name.strip(), version.strip()
    return line, None


def main(path):
    with open(path) as f:
        lines = [l for l in f.read().splitlines() if l.split("#", 1)[0].strip()]

    missing_packages = 0
    missing_versions = 0
    oldest = None  # (upload_time, name, version)

    for line in lines:
        name, version = parse_line(line)
        quoted = urllib.parse.quote(name)

        if fetch_json(f"{PYPI}/{quoted}/json") is None:
            missing_packages += 1
            continue
        if version is None:
            continue

        release = fetch_json(f"{PYPI}/{quoted}/{urllib.parse.quote(version)}/json")
        if release is None:
            missing_versions += 1
            continue

        urls = release.get("urls") or []
        if not urls:
            continue
        upload_time = urls[0]["upload_time"]
        if oldest is None or upload_time < oldest[0]:
            oldest = (upload_time, name, version)

    print(f"Dependencies checked: {len(lines)}")
    print(f"Packages not on PyPI: {missing_packages}")
    print(f"Versions not on PyPI: {missing_versions}")
    if oldest:
        print(f"Oldest pinned release: {oldest[1]}=={oldest[2]} ({oldest[0][:4]})")
    else:
        print("Oldest pinned release: none")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "requirements.txt")
