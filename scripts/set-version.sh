#!/usr/bin/env bash
# Usage: ./scripts/set-version.sh <version>
# Example: ./scripts/set-version.sh 1.2.0
#
# Updates the version in:
#   - cli/deepseek_balance/__init__.py
#   - cli/pyproject.toml
#
# Then commits the change and creates a git tag.
# After running this script, push with:
#   git push && git push --tags

set -euo pipefail

VERSION="${1:-}"

if [[ -z "$VERSION" ]]; then
    echo "Error: version argument is required." >&2
    echo "Usage: $0 <version>  (e.g. $0 1.2.0)" >&2
    exit 1
fi

# Validate semver format (X.Y.Z)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: version must be in X.Y.Z format (e.g. 1.2.0)" >&2
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INIT_FILE="$REPO_ROOT/cli/deepseek_balance/__init__.py"
PYPROJECT_FILE="$REPO_ROOT/cli/pyproject.toml"

echo "Setting version to $VERSION..."

# Update __init__.py
sed -i.bak "s/^__version__ = .*/__version__ = \"$VERSION\"/" "$INIT_FILE" && rm "$INIT_FILE.bak"
echo "  Updated $INIT_FILE"

# Update pyproject.toml (only the [project] version line)
sed -i.bak "s/^version = .*/version = \"$VERSION\"/" "$PYPROJECT_FILE" && rm "$PYPROJECT_FILE.bak"
echo "  Updated $PYPROJECT_FILE"

# Commit and tag
git -C "$REPO_ROOT" add "$INIT_FILE" "$PYPROJECT_FILE"
git -C "$REPO_ROOT" commit -m "chore: bump version to $VERSION"
git -C "$REPO_ROOT" tag "v$VERSION"

echo ""
echo "Done. Version bumped to $VERSION and tag v$VERSION created."
echo "To publish, run:"
echo "  git push && git push --tags"
