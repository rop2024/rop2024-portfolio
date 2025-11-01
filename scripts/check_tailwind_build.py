#!/usr/bin/env python3
"""Simple smoke-test to check Tailwind compiled CSS presence and key utilities.

Usage: python scripts/check_tailwind_build.py

Checks for the compiled CSS at the path referenced in templates and searches
for a small set of utilities / classes to ensure the build contains them.
"""
import sys
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def find_compiled_css_candidates():
    # Common output paths used in this project
    candidates = [
        ROOT / 'theme' / 'static' / 'css' / 'dist' / 'styles.css',
        ROOT / 'static' / 'css' / 'dist' / 'styles.css',
        ROOT / 'staticfiles' / 'css' / 'dist' / 'styles.css',
        ROOT / 'theme' / 'static' / 'css' / 'output.css',
    ]
    return [p for p in candidates if p.exists()]


def scan_file_for_terms(path: Path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    results = {}
    # check for exact utilities
    results['backdrop-blur-xl'] = bool(re.search(r'backdrop-blur-xl', text))
    results['.nav-link'] = bool(re.search(r'\.nav-link\b', text))

    # compiled CSS may not contain literal "bg-white/95" token; search for patterns
    results['bg_white_like'] = bool(
        re.search(r'bg-white\b', text) or
        re.search(r'rgb\(255\s*,?\s*255\s*,?\s*255', text) or
        re.search(r'255\s+255\s+255\s*/', text)
    )

    # check for tailwind header or obvious tailwind output
    results['tailwind_header'] = 'tailwindcss' in text.lower() or '/* tailwindcss' in text.lower() or 'tailwind' in text.lower()
    return results


def main():
    print('Running Tailwind smoke-test...')
    found = find_compiled_css_candidates()
    if not found:
        print('ERROR: No compiled CSS found in common locations.')
        print('Looked for:')
        for p in find_compiled_css_candidates():
            print(' -', p)
        sys.exit(2)

    path = found[0]
    print('Using compiled CSS:', path)

    results = scan_file_for_terms(path)

    good = True
    for k, v in results.items():
        print(f"{k}: {'FOUND' if v else 'MISSING'}")
        if not v:
            good = False

    if good:
        print('\nSMOKE TEST PASS: Compiled CSS contains expected utilities.')
        sys.exit(0)
    else:
        print('\nSMOKE TEST FAIL: Some expected utilities are missing from compiled CSS.')
        sys.exit(3)


if __name__ == '__main__':
    main()
