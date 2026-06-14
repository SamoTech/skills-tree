import os
import re
from datetime import datetime
from pathlib import Path

PR_TITLE = os.environ.get('PR_TITLE', '')
PR_NUMBER = os.environ.get('PR_NUMBER', '')
PR_AUTHOR = os.environ.get('PR_AUTHOR', '')
PR_URL = os.environ.get('PR_URL', '')
MERGED_AT = os.environ.get('MERGED_AT', '')

CHANGELOG = Path('meta/CHANGELOG.md')

patterns = [
    (r'^feat:\s+(.+)', 'Added'),
    (r'^improve:\s+(.+)', 'Improved'),
    (r'^fix:\s+(.+)', 'Fixed'),
    (r'^deprecate:\s+(.+)', 'Deprecated'),
]

change_type = None
detail = None
for pattern, ctype in patterns:
    m = re.match(pattern, PR_TITLE, re.IGNORECASE)
    if m:
        change_type = ctype
        detail = m.group(1).strip()
        break

if not change_type:
    print(f'No changelog entry for PR title: {PR_TITLE}')
    exit(0)

date_str = MERGED_AT[:10] if MERGED_AT else datetime.utcnow().strftime('%Y-%m-%d')
entry = f'- **{change_type}** [{detail}]({PR_URL}) by @{PR_AUTHOR} (#{PR_NUMBER}) — {date_str}\n'

if CHANGELOG.exists():
    content = CHANGELOG.read_text()
else:
    CHANGELOG.parent.mkdir(parents=True, exist_ok=True)
    content = '# Changelog\n\n'

if '# Changelog' in content:
    content = content.replace('# Changelog\n', f'# Changelog\n\n{entry}', 1)
else:
    content = f'# Changelog\n\n{entry}' + content

CHANGELOG.write_text(content)
print(f'Appended changelog entry: {entry.strip()}')
