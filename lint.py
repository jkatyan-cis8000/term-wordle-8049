#!/usr/bin/env python3
"""
lint.py - Enforce layer architecture and file constraints for term-wordle-8049.

Layer dependency rules (forward-only imports):
  types  -> types
  config -> types, config
  repo   -> types, config, repo
  service-> types, config, repo, providers, service
  runtime-> types, config, repo, service, providers, runtime
  ui     -> types, config, service, runtime, providers, ui
  providers-> types, config, utils, providers
  utils  -> utils (leaf, no internal imports)

Rules:
1. Every file under src/ must be in a layer directory
2. Imports must respect the forward dependency chain
3. No file exceeds 300 lines
"""

import ast
import os
import sys
from pathlib import Path


# Layer definition and allowed import sources
LAYERS = {
    'types': ['types'],
    'config': ['types', 'config'],
    'repo': ['types', 'config', 'repo'],
    'service': ['types', 'config', 'repo', 'providers', 'service'],
    'runtime': ['types', 'config', 'repo', 'service', 'providers', 'runtime'],
    'ui': ['types', 'config', 'service', 'runtime', 'providers', 'ui'],
    'providers': ['types', 'config', 'utils', 'providers'],
    'utils': ['utils'],
}

SRC_DIR = Path('/workspace/term-wordle-8049/src')
MAX_LINES = 300


def get_layer(filepath: Path) -> str | None:
    """Determine the layer of a source file based on its directory."""
    try:
        rel_path = filepath.relative_to(SRC_DIR)
        parts = rel_path.parts
        if len(parts) > 0 and parts[0] in LAYERS:
            return parts[0]
    except ValueError:
        pass
    return None


def get_imports(filepath: Path) -> list[str]:
    """Extract all import statements from a Python file."""
    imports = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(filepath))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
    except SyntaxError:
        pass
    return imports


def normalize_import(module_name: str) -> str:
    """Normalize import to get the top-level package name."""
    return module_name.split('.')[0]


def check_file_lint(filepath: Path) -> list[str]:
    """Check a single file for lint violations."""
    errors = []
    
    layer = get_layer(filepath)
    if layer is None:
        errors.append(f"{filepath}: file not in a layer directory")
        return errors
    
    # Check line count
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if len(lines) > MAX_LINES:
        errors.append(f"{filepath}: exceeds {MAX_LINES} lines ({len(lines)} lines)")
    
    # Check imports
    allowed_layers = LAYERS[layer]
    imports = get_imports(filepath)
    
    for imp in imports:
        normalized = normalize_import(imp)
        # Check if import is from our layers
        if normalized in LAYERS and normalized not in allowed_layers:
            errors.append(
                f"{filepath}: imports '{imp}' from disallowed layer '{normalized}'. "
                f"Layer '{layer}' may only import from: {', '.join(allowed_layers)}"
            )
    
    return errors


def main() -> int:
    """Run all linter checks."""
    all_errors = []
    
    # Find all Python files under src/
    for root, _, files in os.walk(SRC_DIR):
        for filename in files:
            if filename.endswith('.py'):
                filepath = Path(root) / filename
                errors = check_file_lint(filepath)
                all_errors.extend(errors)
    
    if all_errors:
        print("Lint errors found:")
        for error in all_errors:
            print(f"  - {error}")
        return 1
    
    print("All checks passed!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
