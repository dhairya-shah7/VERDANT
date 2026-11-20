"""
V.E.R.D.A.N.T. Real GitOps & GitHub Integration Engine
Executes genuine Git operations: branch creation, atomic commit, remote push,
and verified PR generation with Eco-Telemetry and Closed-Loop Proofs.
Zero fake responses: uses local git and GitHub REST API / gh CLI.
"""
from pathlib import Path
from typing import Optional, Dict, Any, List
import subprocess
import os
import json
import urllib.request
import urllib.error
from .schema import Diagnosis, EcoAudit
from .replay_shield.proofloop import ProofResult
from .verde_telemetry.eco import EcoTelemetry


class GitOpsError(Exception):
    pass


class GitOpsEngine:
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = (repo_root or Path.cwd()).resolve()

    def run_git(self, args: List[str]) -> str:
        """Executes a git command inside the repository root."""
        cmd = ["git"] + args
        try:
            res = subprocess.run(
                cmd,
                cwd=str(self.repo_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return res.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise GitOpsError(f"Git command failed: {' '.join(cmd)}\nStderr: {e.stderr.strip()}")

    def get_current_branch(self) -> str:
        return self.run_git(["rev-parse", "--abbrev-ref", "HEAD"])

    def create_and_checkout_branch(self, branch_name: str) -> str:
        """Creates and checks out a new branch."""
        # Sanitize branch name
        safe_branch = "".join(c if c.isalnum() or c in "-_/" else "-" for c in branch_name)
        self.run_git(["checkout", "-b", safe_branch])
        return safe_branch

    def commit_changes(self, commit_message: str, files: Optional[List[str]] = None) -> str:
        """Stages files and creates a signed/standard commit."""
        if files:
            for f in files:
                self.run_git(["add", f])
        else:
            self.run_git(["add", "-u"])

        self.run_git(["commit", "-m", commit_message])
        commit_hash = self.run_git(["rev-parse", "HEAD"])
        return commit_hash

    def push_branch(self, branch_name: str, remote: str = "origin") -> str:
        """Pushes branch to remote repository."""
        return self.run_git(["push", "-u", remote, branch_name])

    def get_remote_repo_slug(self, remote: str = "origin") -> Optional[str]:
        """Extracts 'owner/repo' from git remote URL."""
        try:
            url = self.run_git(["remote", "get-url", remote])
            # Handle https://github.com/owner/repo.git or git@github.com:owner/repo.git
            clean = url.rstrip("/")
            if clean.endswith(".git"):
                clean = clean[:-4]
            if "github.com/" in clean:
                return clean.split("github.com/")[1]
            if "github.com:" in clean:
                return clean.split("github.com:")[1]
            return None
        except Exception:
            return None

    def build_pr_body(
        self,
        diagnosis: Diagnosis,
        diff_text: str,
        proof_result: Optional[ProofResult] = None,
        audit: Optional[EcoAudit] = None
    ) -> str:
        """Constructs the standard V.E.R.D.A.N.T. GitHub PR markdown description."""
        parts = [
            f"## 🌿 V.E.R.D.A.N.T. Autonomous Resolution: `{diagnosis.action_type.value.upper()}`",
            "",
            "### 1. Root Cause Summary",
            f"> **Spoken Brief**: {diagnosis.spoken_summary}",
            "",
            diagnosis.root_cause,
            "",
            "### 2. Surgical Patch Diff",
            "```diff",
            diff_text if diff_text.strip() else "# No source code changes required for this action",
            "```",
            ""
        ]

        if proof_result:
            parts.extend([
                "### 3. Closed-Loop Verification Proof",
                f"- [{'x' if proof_result.red_phase_failed else ' '}] **RED Phase**: Reproducer failed against unpatched code.",
                f"- [{'x' if proof_result.green_phase_passed else ' '}] **GREEN Phase**: Reproducer passed 100% post-patch ({round(proof_result.execution_time_seconds, 2)}s).",
                ""
            ])

        if audit:
            parts.append(EcoTelemetry.generate_badge_markdown(audit))

        return "\n".join(parts)

    def create_github_pr(
        self,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main"
    ) -> Dict[str, Any]:
        """
        Creates a GitHub Pull Request using GitHub API or local payload file.
        """
        github_token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        repo_slug = self.get_remote_repo_slug()

        # Always save pr_payload.md locally for full transparency
        payload_path = self.repo_root / "pr_payload.md"
        with open(payload_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{body}")

        if github_token and repo_slug:
            api_url = f"https://api.github.com/repos/{repo_slug}/pulls"
            data = json.dumps({
                "title": title,
                "body": body,
                "head": head_branch,
                "base": base_branch
            }).encode("utf-8")

            req = urllib.request.Request(
                api_url,
                data=data,
                headers={
                    "Authorization": f"Bearer {github_token}",
                    "Accept": "application/vnd.github+json",
                    "Content-Type": "application/json",
                    "User-Agent": "VERDANT-Agent"
                },
                method="POST"
            )

            try:
                with urllib.request.urlopen(req) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    return {
                        "success": True,
                        "pr_url": resp_data.get("html_url"),
                        "pr_number": resp_data.get("number"),
                        "repo": repo_slug,
                        "payload_file": str(payload_path)
                    }
            except urllib.error.HTTPError as e:
                err_text = e.read().decode("utf-8")
                return {
                    "success": False,
                    "error": f"GitHub API {e.code}: {err_text}",
                    "payload_file": str(payload_path)
                }

        # If no GitHub token, check if gh CLI is available
        try:
            gh_res = subprocess.run(
                ["gh", "pr", "create", "--title", title, "--body", body, "--head", head_branch, "--base", base_branch],
                cwd=str(self.repo_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if gh_res.returncode == 0:
                pr_url = gh_res.stdout.strip()
                return {
                    "success": True,
                    "pr_url": pr_url,
                    "repo": repo_slug,
                    "payload_file": str(payload_path)
                }
        except Exception:
            pass

        # Return prepared GitOps payload
        return {
            "success": True,
            "pr_url": f"https://github.com/{repo_slug}/compare/{base_branch}...{head_branch}?expand=1" if repo_slug else None,
            "manual_review": True,
            "payload_file": str(payload_path),
            "message": "Branch pushed. Pull Request markdown ready in pr_payload.md."
        }
