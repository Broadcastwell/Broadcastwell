from pathlib import Path
import re
from urllib.parse import urlparse

text = Path('README.md').read_text(encoding='utf-8')
assert len(re.findall(r'^# ', text, re.M)) == 1, 'Exactly one H1 is required'
urls = re.findall(r'\]\(([^)]+)\)', text)
assert urls, 'The profile must expose its published sources'
for url in urls:
    parsed = urlparse(url)
    assert parsed.scheme in ('https', 'mailto') and parsed.path is not None, url
    assert not re.search(r'\s', url), url
    assert parsed.netloc or parsed.scheme == 'mailto', url
copy = re.sub(r'https?://[^\s)]+', '', text)
copy = re.sub(r'^- ', '', copy, flags=re.M)
copy = copy.replace('no-cost re-run', '').replace('2026-09', '').replace('get_index_category', '')
assert not re.search(r'[-\u2010-\u2015]', copy), 'Dash characters remain in public copy'
assert not any(price in copy for price in ('$1,500', '$990', '$3,000', '$148.50')), 'Retired price'
assert 'Every figure comes from the published method, v1.1.' in text
assert 'Sairam Sivakumar' not in text, 'Use the public delivery lead line'
assert 'Delivery lead: Priya Nair, Management Consultant.' in text
assert 'Verified by two Broadcastwell analysts' not in text
assert 'no statement is analyst verified' in text
assert '10.5281/zenodo.23270124' in text and 'CC BY 4.0' in text
print(f'Public profile: one H1, {len(urls)} structurally valid source links, current prices and honest review status.')
