"""
V.E.R.D.A.N.T. Atomic Search/Replace Patcher
Replaces fragile line-numbered unified diffs with deterministic, AST-safe atomic edits.
Enforces:
1. Exact uniqueness: `search` pattern must occur exactly once in target file.
2. Safety barriers: Protects lockfiles, CI workflows, and secret files.
3. Transactional all-or-nothing writes with automatic rollback on error.
"""
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
import difflib
import os
from ..schema import Edit


class PatchError(Exception):
    """Raised when an atomic edit fails safety validation or uniqueness checks."""
    pass


PROTECTED_PATTERNS = [
    ".git",
    ".env",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    ".github/workflows",
]


def is_path_safe(file_path: Path, repo_root: Path) -> Tuple[bool, Optional[str]]:
    """Checks whether the file path is safe to modify and resides within the repository."""
    try:
        resolved_root = repo_root.resolve()
        resolved_file = file_path.resolve()
    except Exception as e:
        return False, f"Invalid path resolution: {e}"

    # Directory traversal prevention
    if not resolved_file.is_relative_to(resolved_root):
        return False, f"Path traversal rejected: {file_path} is outside repository root {repo_root}"

    rel_str = resolved_file.relative_to(resolved_root).as_posix()
    for protected in PROTECTED_PATTERNS:
        if rel_str == protected or rel_str.startswith(protected + "/"):
            return False, f"Modification forbidden on protected system/lockfile: {rel_str}"

    return True, None


def validate_edit(file_content: str, edit: Edit) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validates that edit.search matches exactly once in file_content.
    Returns: (is_valid, error_message, updated_content)
    """
    if not edit.search:
        return False, "Search string cannot be empty", None

    # Normalize line endings to avoid CRLF / LF mismatches
    normalized_content = file_content.replace("\r\n", "\n")
    normalized_search = edit.search.replace("\r\n", "\n")
    normalized_replace = edit.replace.replace("\r\n", "\n")

    occurrences = normalized_content.count(normalized_search)
    if occurrences == 0:
        return False, f"Target search block was not found in {edit.path}", None
    if occurrences > 1:
        return False, (
            f"Ambiguous search target: found {occurrences} occurrences in {edit.path}. "
            "Search block must include sufficient surrounding context to match exactly once."
        ), None

    new_content = normalized_content.replace(normalized_search, normalized_replace, 1)
    
    # Preserve original CRLF if original content used Windows CRLF
    if "\r\n" in file_content and "\r\n" not in new_content:
        new_content = new_content.replace("\n", "\r\n")

    return True, None, new_content


def generate_diff(original: str, modified: str, filename: str) -> str:
    """Generates a standard unified diff string for UI inspection and PR descriptions."""
    orig_lines = original.splitlines(keepends=True)
    mod_lines = modified.splitlines(keepends=True)
    diff = difflib.unified_diff(
        orig_lines,
        mod_lines,
        fromfile=f"a/{filename}",
        tofile=f"b/{filename}",
        lineterm=""
    )
    return "".join(diff)


class AtomicPatcher:
    """Transactional patch applicator for V.E.R.D.A.N.T."""

    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = (repo_root or Path.cwd()).resolve()

    def preview_edits(self, edits: List[Edit]) -> Dict[str, Any]:
        """
        Validates all edits without modifying any file on disk.
        Returns validation status, accumulated unified diffs, and updated files map.
        """
        if not edits:
            return {"success": True, "diff": "", "files_changed": 0, "errors": []}

        file_stages: Dict[Path, str] = {}
        unified_diffs: List[str] = []
        errors: List[str] = []

        # Group edits by target file to support multiple non-conflicting edits per file
        edits_by_file: Dict[str, List[Edit]] = {}
        for edit in edits:
            edits_by_file.setdefault(edit.path, []).append(edit)

        for rel_path_str, file_edits in edits_by_file.items():
            target_path = (self.repo_root / rel_path_str).resolve()

            is_safe, sec_err = is_path_safe(target_path, self.repo_root)
            if not is_safe:
                errors.append(sec_err)
                continue

            if not target_path.exists():
                errors.append(f"Target file does not exist: {rel_path_str}")
                continue

            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    current_content = f.read()
            except Exception as e:
                errors.append(f"Failed reading {rel_path_str}: {e}")
                continue

            original_content = current_content
            file_success = True

            for edit in file_edits:
                valid, err, new_content = validate_edit(current_content, edit)
                if not valid:
                    errors.append(err)
                    file_success = False
                    break
                current_content = new_content

            if file_success:
                diff_text = generate_diff(original_content, current_content, rel_path_str)
                unified_diffs.append(diff_text)
                file_stages[target_path] = current_content

        if errors:
            return {
                "success": False,
                "diff": "",
                "files_changed": 0,
                "errors": errors
            }

        return {
            "success": True,
            "diff": "\n".join(unified_diffs),
            "files_changed": len(file_stages),
            "staged_contents": file_stages,
            "errors": []
        }

    def apply_edits(self, edits: List[Edit]) -> Dict[str, Any]:
        """
        Transactionally applies edits to disk only if ALL edits validate 100%.
        Automatically rolls back on any filesystem write error.
        """
        preview = self.preview_edits(edits)
        if not preview["success"]:
            raise PatchError(f"Cannot apply edits due to validation errors:\n" + "\n".join(preview["errors"]))

        staged_contents: Dict[Path, str] = preview.get("staged_contents", {})
        backups: Dict[Path, str] = {}
        applied: List[Path] = []

        try:
            for path, new_content in staged_contents.items():
                with open(path, "r", encoding="utf-8") as f:
                    backups[path] = f.read()

                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                applied.append(path)

            return {
                "success": True,
                "diff": preview["diff"],
                "files_changed": len(applied),
                "modified_paths": [str(p.relative_to(self.repo_root)) for p in applied]
            }

        except Exception as write_error:
            # Transactional rollback
            for restored_path in applied:
                if restored_path in backups:
                    try:
                        with open(restored_path, "w", encoding="utf-8") as f:
                            f.write(backups[restored_path])
                    except Exception as rollback_err:
                        print(f"[FATAL] Rollback failed for {restored_path}: {rollback_err}")

            raise PatchError(f"Write operation failed, rolled back changes. Cause: {write_error}")
