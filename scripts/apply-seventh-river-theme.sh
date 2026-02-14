#!/usr/bin/env bash
set -euo pipefail

# Apply Seventh River palette to OpenClaw's bundled TUI JS.
# Intended for Linux/macOS (or WSL).

DIST="${OPENCLAW_DIST:-$HOME/.npm-global/lib/node_modules/openclaw/dist}"

if [[ ! -d "$DIST" ]]; then
  # fallback common path
  if [[ -d "$HOME/.config" ]]; then
    :
  fi
  echo "Could not find OpenClaw dist directory at: $DIST" >&2
  echo "Set OPENCLAW_DIST to your openclaw/dist path." >&2
  exit 1
fi

targets=(
  "$DIST/tui-B0PFk5gW.js"
  "$DIST/tui-Dp_597lz.js"
)

old=$(cat <<'EOF'
const palette = {
	text: "#E8E3D5",
	dim: "#7B7F87",
	accent: "#F6C453",
	accentSoft: "#F2A65A",
	border: "#3C414B",
	userBg: "#2B2F36",
	userText: "#F3EEE0",
	systemText: "#9BA3B2",
	toolPendingBg: "#1F2A2F",
	toolSuccessBg: "#1E2D23",
	toolErrorBg: "#2F1F1F",
	toolTitle: "#F6C453",
	toolOutput: "#E1DACB",
	quote: "#8CC8FF",
	quoteBorder: "#3B4D6B",
	code: "#F0C987",
	codeBlock: "#1E232A",
	codeBorder: "#343A45",
	link: "#7DD3A5",
	error: "#F97066",
	success: "#7DD3A5"
};
EOF
)

new=$(cat <<'EOF'
const palette = {
	// Seventh River (Prana) — borderless, river-light focus
	text: "#F8F9FF",      // ink
	dim: "#A0A7C0",       // whisper
	accent: "#4169E1",    // river
	accentSoft: "#E6E6FA",// breath
	border: "#050814",    // core (invisible border)
	userBg: "#050814",    // core
	userText: "#F8F9FF",  // ink
	systemText: "#A0A7C0", // whisper
	toolPendingBg: "#050814",
	toolSuccessBg: "#050814",
	toolErrorBg: "#050814",
	toolTitle: "#4169E1", // river
	toolOutput: "#F8F9FF",
	quote: "#28F0FF",     // axon
	quoteBorder: "#050814",
	code: "#E6E6FA",      // breath
	codeBlock: "#050814",
	codeBorder: "#050814",
	link: "#28F0FF",      // axon
	error: "#FF5370",     // danger
	success: "#1DE9B6"    // success
};
EOF
)

for f in "${targets[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "Missing: $f (skipping)" >&2
    continue
  fi
  if grep -q "Seventh River (Prana)" "$f"; then
    echo "Already patched: $f"
    continue
  fi
  if ! grep -q "text: \"#E8E3D5\"" "$f"; then
    echo "Upstream palette signature not found in $f. OpenClaw changed; update script." >&2
    exit 1
  fi

  # portable replace using perl
  perl -0777 -i -pe "s/\Q$old\E/$new/s" "$f"
  echo "Patched: $f"
done

echo "Seventh River theme applied."
