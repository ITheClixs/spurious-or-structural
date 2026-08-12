#!/usr/bin/env bash
# Build the preprint and assemble a source tarball for arXiv submission.
#
# arXiv rebuilds the paper from source with pdflatex and does NOT run BibTeX,
# so the generated .bbl must travel with the .tex. Auxiliary files must not.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$ROOT/docs/pre_results"
STEM="xid_pre_results_manuscript"
BUILD_DIR="$ROOT/output/arxiv_build"
PKG_DIR="$ROOT/output/arxiv"
TARBALL="$ROOT/output/arxiv.tar.gz"

command -v tectonic >/dev/null || {
  echo "error: tectonic not found on PATH" >&2
  exit 1
}

echo "==> Regenerating exhibits"
(cd "$ROOT" && uv run --locked python -m xid.exhibits --out docs/pre_results/generated)
(cd "$ROOT" && git diff --exit-code -- docs/pre_results/generated) || {
  echo "error: generated exhibits drifted from the committed copies" >&2
  exit 1
}

echo "==> Compiling with bibliography"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
(cd "$SRC_DIR" && tectonic -X compile "$STEM.tex" \
  --outdir "$BUILD_DIR" --keep-intermediates >/dev/null 2>&1)

[[ -f "$BUILD_DIR/$STEM.bbl" ]] || {
  echo "error: no .bbl produced; arXiv would build without a bibliography" >&2
  exit 1
}

echo "==> Publishing PDF"
mkdir -p "$ROOT/output/pdf"
cp "$BUILD_DIR/$STEM.pdf" "$ROOT/output/pdf/$STEM.pdf"

echo "==> Assembling submission package"
rm -rf "$PKG_DIR"
mkdir -p "$PKG_DIR/generated"
cp "$SRC_DIR/$STEM.tex"                  "$PKG_DIR/"
cp "$BUILD_DIR/$STEM.bbl"                "$PKG_DIR/"
cp "$SRC_DIR/references.bib"             "$PKG_DIR/"
# Copy every generated fragment rather than a hardcoded list: a new figure
# added to the manuscript must not be able to go missing from the tarball.
shopt -s nullglob
fragments=("$SRC_DIR"/generated/*.tex)
(( ${#fragments[@]} > 0 )) || {
  echo "error: no generated .tex fragments found" >&2
  exit 1
}
cp "${fragments[@]}" "$PKG_DIR/generated/"

# Every \input{generated/...} in the manuscript must now resolve inside PKG_DIR.
while read -r name; do
  [[ -f "$PKG_DIR/generated/$name.tex" ]] || {
    echo "error: manuscript inputs generated/$name.tex but it is not packaged" >&2
    exit 1
  }
done < <(grep -oE '\\input\{generated/[^}]+\}' "$SRC_DIR/$STEM.tex" \
         | sed 's|.*generated/||; s|}$||')

# The .bbl is what arXiv actually uses, since it does not run BibTeX. The .bib
# travels alongside it so that a local verification build, which does run
# BibTeX, reproduces the same bibliography instead of silently dropping it.

# Auxiliary files must not ship.
find "$PKG_DIR" -type f \
  \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.synctex.gz' \
     -o -name '*.pdf' -o -name '.DS_Store' \) -delete

rm -f "$TARBALL"
tar -czf "$TARBALL" -C "$PKG_DIR" .

echo
echo "==> Package contents"
tar -tzf "$TARBALL" | sed 's/^/    /'
echo
echo "    tarball: $TARBALL"
echo "    size:    $(wc -c < "$TARBALL") bytes"
echo "    pdf:     $ROOT/output/pdf/$STEM.pdf"
echo
echo "Verify before uploading:"
echo "    mkdir -p /tmp/arxivcheck && tar xzf $TARBALL -C /tmp/arxivcheck"
echo "    cd /tmp/arxivcheck && latexmk -pdf $STEM.tex"
