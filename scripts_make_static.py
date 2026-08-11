from pathlib import Path
import re

root = Path('/home/.z/workspaces/con_COY27Dd4yLdi20EL/github-fresh')
files = [
    'index.html',
    'book/index.html',
    'commission/index.html',
    'reviews/index.html',
    'louie-optin/index.html',
    'portal/index.html',
    'terms/index.html',
]

for rel in files:
    path = root / rel
    s = path.read_text()
    nested = '/' in rel
    prefix = '../' if nested else './'
    # Remove runtime scripts so GitHub Pages keeps the captured page instead of mounting Zo's router.
    s = re.sub(r'<script\b[^>]*>[\s\S]*?</script>', '', s, flags=re.I)
    s = re.sub(r'<link\b[^>]*rel=["\']modulepreload["\'][^>]*>', '', s, flags=re.I)
    # Make the local stylesheet, favicon, and image references work at this route depth.
    s = re.sub(r'(href|src)="/(assets/|favicon\.svg)', lambda m: f'{m.group(1)}="{prefix}{m.group(2)}', s)
    # Internal links should stay inside this GitHub Pages project.
    def link(m):
        attr, value = m.group(1), m.group(2)
        if value.startswith('/') and not value.startswith('//'):
            if value == '/': target = prefix
            elif value.startswith('/terms'): target = prefix + 'terms/'
            else: target = prefix + value.lstrip('/') + '/'
            return f'{attr}="{target}"'
        if value.startswith('./'):
            return m.group(0)
        return m.group(0)
    s = re.sub(r'(href|src)="([^"]+)"', link, s)
    # The captured footer sometimes points to /terms; normalize any remaining local variant.
    s = s.replace(f'{prefix}terms.html.html', f'{prefix}terms/')
    s = s.replace(f'{prefix}terms.html', f'{prefix}terms/')
    path.write_text(s)

# Keep the legacy root-level Terms URL working as a static alias.
terms = (root / 'terms/index.html').read_text()
terms = terms.replace('href="../', 'href="./').replace('src="../', 'src="./')
(root / 'terms.html').write_text(terms)
