"""
V.E.R.D.A.N.T. Desktop Capsule - Engine Bridge
Seamlessly routes UI events (snaps, voice, prompt, patch approvals)
into the V.E.R.D.A.N.T. v2 Core Engine without mock intermediaries.
"""
from pathlib import Path
from typing import Optional, Dict, Any, List
import subprocess
import os

from src.dual_engine.gemini_analyzer import analyze_multimodal
from src.replay_shield.patcher import AtomicPatcher
from src.replay_shield.proofloop import ProofLoop, ProofResult
from src.gitops import GitOpsEngine
from src.schema import Diagnosis, ActionType


class CapsuleBridge:
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = (repo_root or Path.cwd()).resolve()
        self.patcher = AtomicPatcher(self.repo_root)
        self.proofloop = ProofLoop(self.repo_root)
        self.gitops = GitOpsEngine(self.repo_root)

    def analyze(
        self,
        prompt: str,
        image_path: Optional[Path] = None,
        audio_bytes: Optional[bytes] = None,
        mode: str = "normal"
    ) -> Dict[str, Any]:
        """
        Processes query via Google Gemini Multimodal Engine.
        Returns typed payload with diff preview if fix is suggested.
        """
        images = [image_path] if image_path and image_path.exists() else None

        # Call live multimodal Gemini reasoning
        diagnosis: Diagnosis = analyze_multimodal(
            prompt=prompt,
            images=images,
            audio_bytes=audio_bytes,
            mode=mode
        )

        diff_preview = ""
        patch_valid = False
        patch_errors = []

        if diagnosis.action_type == ActionType.FIX and diagnosis.edits:
            preview = self.patcher.preview_edits(diagnosis.edits)
            diff_preview = preview.get("diff", "")
            patch_valid = preview.get("success", False)
            patch_errors = preview.get("errors", [])

        return {
            "diagnosis": diagnosis,
            "action_type": diagnosis.action_type.value,
            "confidence": diagnosis.confidence,
            "spoken_summary": diagnosis.spoken_summary,
            "root_cause": diagnosis.root_cause,
            "diff_preview": diff_preview,
            "patch_valid": patch_valid,
            "patch_errors": patch_errors,
            "eco_audit": diagnosis.eco_audit
        }

    def apply_patch_and_verify(self, diagnosis: Diagnosis) -> Dict[str, Any]:
        """
        Applies atomic patch, runs ProofLoop closed-loop verification, and commits to git.
        """
        if not diagnosis.edits:
            return {"success": False, "error": "No edits in diagnosis to apply"}

        proof_result: Optional[ProofResult] = None

        # If a reproducer test spec was synthesized, run through ProofLoop
        if diagnosis.test_spec:
            proof_result = self.proofloop.verify_and_replay(
                test_spec=diagnosis.test_spec,
                edits=diagnosis.edits,
                ephemeral_test=False
            )
            if not proof_result.verified:
                return {
                    "success": False,
                    "error": f"Verification failed: {proof_result.error_message}",
                    "proof": proof_result
                }
        else:
            # Direct atomic patch
            apply_res = self.patcher.apply_edits(diagnosis.edits)
            if not apply_res["success"]:
                return {
                    "success": False,
                    "error": f"Failed applying patch: {apply_res.get('errors')}"
                }

        # GitOps: Commit & create PR payload
        try:
            current_branch = self.gitops.get_current_branch()
            branch_name = f"verdant/fix-{int(os.getpid())}"
            self.gitops.create_and_checkout_branch(branch_name)

            modified_files = [e.path for e in diagnosis.edits]
            if diagnosis.test_spec:
                modified_files.append(diagnosis.test_spec.path)

            commit_msg = f"fix(autofix): {diagnosis.spoken_summary[:70]}\n\n{diagnosis.root_cause}"
            commit_hash = self.gitops.commit_changes(commit_msg, files=modified_files)

            pr_body = self.gitops.build_pr_body(
                diagnosis=diagnosis,
                diff_text=self.patcher.preview_edits(diagnosis.edits).get("diff", ""),
                proof_result=proof_result,
                audit=diagnosis.eco_audit
            )

            pr_info = self.gitops.create_github_pr(
                title=f"Fix: {diagnosis.spoken_summary[:60]}",
                body=pr_body,
                head_branch=branch_name,
                base_branch=current_branch
            )

            return {
                "success": True,
                "commit_hash": commit_hash,
                "branch": branch_name,
                "pr_info": pr_info,
                "proof": proof_result
            }

        except Exception as git_err:
            return {
                "success": True,
                "warning": f"Patch applied locally, but GitOps step encountered: {git_err}"
            }

    def execute_terminal_action(self, command: str) -> Dict[str, Any]:
        """Runs 1-click terminal command for environment conflicts."""
        try:
            res = subprocess.run(
                command,
                cwd=str(self.repo_root),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            return {
                "success": res.returncode == 0,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "returncode": res.returncode
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
