import os
import re
import urllib.parse
import zipfile

SVG_PLACEHOLDER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 750" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16"/>
      <stop offset="50%" stop-color="#111827"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
    <linearGradient id="borderGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f43f5e" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#fb7185" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0.8"/>
    </linearGradient>
    <radialGradient id="centerGlow" cx="50%" cy="38%" r="55%">
      <stop offset="0%" stop-color="#f43f5e" stop-opacity="0.22"/>
      <stop offset="50%" stop-color="#10b981" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0"/>
    </radialGradient>
    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>
  <rect width="600" height="750" fill="url(#bgGrad)"/>
  <rect width="600" height="750" fill="url(#centerGlow)"/>
  <rect x="20" y="20" width="560" height="710" rx="20" fill="none" stroke="url(#borderGrad)" stroke-width="1.5" stroke-dasharray="8 6" opacity="0.6"/>
  <g transform="translate(300, 270)">
    <circle r="130" fill="#0f172a" stroke="rgba(244, 63, 94, 0.25)" stroke-width="2"/>
    <circle r="115" fill="#1e293b" stroke="rgba(16, 185, 129, 0.3)" stroke-width="1.5"/>
    <circle r="95" fill="none" stroke="rgba(251, 113, 133, 0.4)" stroke-width="1" stroke-dasharray="4 4"/>
    <path d="M0 -45 C20 -45 42 -25 42 5 C42 35 15 52 0 68 C-15 52 -42 35 -42 5 C-42 -25 -20 -45 0 -45 Z" fill="#f43f5e" opacity="0.85" filter="url(#softGlow)"/>
    <circle cx="0" cy="5" r="16" fill="#fbbf24"/>
    <path d="M-6 4 C-6 -8 0 -18 0 -18 C0 -18 6 -8 6 4 C6 10 3 14 0 14 C-3 14 -6 10 -6 4 Z" fill="#fff"/>
  </g>
  <g text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif">
    <text x="300" y="90" fill="#fb7185" font-size="12" font-weight="700" letter-spacing="4">🌸 SHREE GANESHAY NAMAH 🌸</text>
    <text x="300" y="445" fill="#ffffff" font-size="28" font-weight="800" letter-spacing="1">MUMMY &amp; PAPA</text>
    <text x="300" y="480" fill="#34d399" font-size="13" font-weight="600" letter-spacing="3">MERI PRERNA · MERA SAHARA · MERI TAAQAT</text>
    <line x1="200" y1="510" x2="400" y2="510" stroke="rgba(244, 63, 94, 0.35)" stroke-width="1.5"/>
    <text x="300" y="545" fill="#e2e8f0" font-size="15" font-weight="500" font-style="italic">“Meri har mehnat, meri Mummy-Papa ke naam.”</text>
    <text x="300" y="585" fill="#94a3b8" font-size="12" font-weight="400">Jinke aashirvaad se har mushkil aasan hoti hai.</text>
    <rect x="140" y="630" width="320" height="42" rx="21" fill="rgba(244, 63, 94, 0.12)" stroke="rgba(244, 63, 94, 0.3)" stroke-width="1"/>
    <text x="300" y="656" fill="#fda4af" font-size="12" font-weight="600">📷 Click &quot;Change Photo&quot; to upload your picture</text>
  </g>
</svg>"""

encoded_svg = "data:image/svg+xml;charset=utf-8," + urllib.parse.quote(SVG_PLACEHOLDER)

with open("/Users/devrajput/@Resources/Tracker/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the giant base64 line
# const MP_EMBEDDED_DEFAULT_PHOTO = "data:image/jpeg;base64,...";
pattern = r'// Embedded Default Base64 Fallback\nconst MP_EMBEDDED_DEFAULT_PHOTO = "[^"]+";'
replacement = f'''// Privacy-Safe Neutral Vector Fallback (Zero Personal Photos/Bytes)
const MP_NEUTRAL_PLACEHOLDER_SVG = "{encoded_svg}";
const MP_EMBEDDED_DEFAULT_PHOTO = MP_NEUTRAL_PLACEHOLDER_SVG;'''

if re.search(pattern, content):
    content = re.sub(pattern, replacement, content)
    print("Replaced MP_EMBEDDED_DEFAULT_PHOTO with MP_NEUTRAL_PLACEHOLDER_SVG!")
else:
    print("Pattern for MP_EMBEDDED_DEFAULT_PHOTO not found, checking...")

# Update renderMummyPapaView and handleMummyPapaImgError if needed
old_render_block = """  } else {
    if (imgEl) imgEl.src = MP_EMBEDDED_DEFAULT_PHOTO;
    if (statusPill) {
      statusPill.innerHTML = '<span>✨</span> Family Photo Active · Ready to Personalize';
      statusPill.style.color = '#10b981';
      statusPill.style.background = 'rgba(16, 185, 129, 0.1)';
      statusPill.style.borderColor = 'rgba(16, 185, 129, 0.3)';
    }
  }
}

function handleMummyPapaImgError(img) {
  if (img.src !== MP_EMBEDDED_DEFAULT_PHOTO) {
    img.src = MP_EMBEDDED_DEFAULT_PHOTO;
  }
}"""

new_render_block = """  } else {
    if (imgEl) {
      if (!imgEl.src || imgEl.src.endsWith(MP_DEFAULT_FALLBACK_URL) || imgEl.src === window.location.href) {
        imgEl.src = MP_DEFAULT_FALLBACK_URL;
      }
    }
    if (statusPill) {
      statusPill.innerHTML = '<span>✨</span> Family Photo Active · Ready to Personalize';
      statusPill.style.color = '#10b981';
      statusPill.style.background = 'rgba(16, 185, 129, 0.1)';
      statusPill.style.borderColor = 'rgba(16, 185, 129, 0.3)';
    }
  }
}

function handleMummyPapaImgError(img) {
  if (img && img.src !== MP_NEUTRAL_PLACEHOLDER_SVG) {
    img.src = MP_NEUTRAL_PLACEHOLDER_SVG;
    const statusPill = document.getElementById('mpStatusPill');
    if (statusPill) {
      statusPill.innerHTML = '<span>📷</span> Ready to Personalize · Upload Mummy-Papa Photo';
      statusPill.style.color = '#94a3b8';
      statusPill.style.background = 'rgba(148, 163, 184, 0.1)';
      statusPill.style.borderColor = 'rgba(148, 163, 184, 0.3)';
    }
  }
}"""

if old_render_block in content:
    content = content.replace(old_render_block, new_render_block)
    print("Updated renderMummyPapaView and handleMummyPapaImgError!")
else:
    print("old_render_block not found in exact form.")

# Target files
targets = [
    "/Users/devrajput/@Resources/Tracker/index.html",
    "/Users/devrajput/@Resources/Tracker/integrated_master.html",
    "/Users/devrajput/@Resources/Tracker/dsa_patterns_trackerfinal copy.html",
    "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"
]

for t in targets:
    with open(t, "w", encoding="utf-8") as out:
        out.write(content)
    print(f"Updated mirror: {t} ({len(content)} bytes)")

# Now rebuild dsa-placement-dashboard.zip EXCLUDING any personal assets
dashboard_dir = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard"
zip_path = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard.zip"

allowed_files = [
    "index.html",
    "start-server.sh",
    "README.md",
    "manifest.json",
    "service-worker.js"
]

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for fname in allowed_files:
        fpath = os.path.join(dashboard_dir, fname)
        if os.path.exists(fpath):
            zipf.write(fpath, fname)
            print(f"Added to ZIP: {fname} ({os.path.getsize(fpath)} bytes)")

print(f"Final safe ZIP built: {zip_path} ({os.path.getsize(zip_path)} bytes)")
