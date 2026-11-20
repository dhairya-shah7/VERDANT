"""
V.E.R.D.A.N.T. ProofLoop: Closed-Loop RED-to-GREEN Verifier
Enforces scientific verification before any PR or code patch is accepted:
1. RED Phase: Executes reproducer test against unpatched code to prove failure.
2. PATCH Phase: Applies transactional atomic search/replace patch.
3. GREEN Phase: Re-runs reproducer test to prove 100% resolution.
4. Auto-Rollback: Restores original state if GREEN phase fails.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import subprocess
import time
from .patcher import AtomicPatcher, PatchError
from ..schema import TestSpec, Edit


@dataclass
class ProofResult:
    verified: bool
    red_phase_failed: bool          # Did the test fail on unpatched code as expected?
    green_phase_passed: bool        # Did the test pass on patched code as expected?
    red_output: str
    green_output: str
    execution_time_seconds: float
    error_message: Optional[str] = None


class ProofLoop:
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = (repo_root or Path.cwd()).resolve()
        self.patcher = AtomicPatcher(self.repo_root)

    def _execute_test(self, test_path: Path, runner: str = "pytest", timeout: int = 45) -> Tuple[int, str]:
        """Runs the test script using the specified runner (playwright, pytest, or python)."""
        import sys
        if runner == "playwright":
            # If playwright is installed, run npx playwright or pytest
            cmd = ["npx", "playwright", "test", str(test_path)] if test_path.suffix in [".ts", ".js"] else [sys.executable, "-m", "pytest", str(test_path)]
        elif runner == "pytest":
            cmd = [sys.executable, "-m", "pytest", str(test_path), "-v"]
        else:
            cmd = [sys.executable, str(test_path)]

        try:
            res = subprocess.run(
                cmd,
                cwd=str(self.repo_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=timeout,
                shell=(test_path.suffix in [".ts", ".js"])
            )
            return res.returncode, res.stdout
        except subprocess.TimeoutExpired:
            return -1, f"Test execution timed out after {timeout} seconds"
        except Exception as e:
            return -2, f"Execution error running '{' '.join(cmd)}': {e}"

    def verify_and_replay(
        self,
        test_spec: TestSpec,
        edits: List[Edit],
        ephemeral_test: bool = True
    ) -> ProofResult:
        """
        Conducts the hermetic RED-to-GREEN closed-loop verification cycle.
        """
        start_time = time.time()
        test_file_path = (self.repo_root / test_spec.path).resolve()
        
        # Write test spec file
        test_file_path.parent.mkdir(parents=True, exist_ok=True)
        test_file_created = not test_file_path.exists()
        original_test_content = test_file_path.read_text(encoding="utf-8") if not test_file_created else None

        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(test_spec.content)

        red_passed = False
        red_output = ""
        green_passed = False
        green_output = ""
        patch_applied = False

        try:
            # PHASE 1: RED Verification (Should FAIL on unpatched code)
            ret_code_red, red_output = self._execute_test(test_file_path, runner=test_spec.runner)
            if ret_code_red == 0:
                return ProofResult(
                    verified=False,
                    red_phase_failed=False,
                    green_phase_passed=False,
                    red_output=red_output,
                    green_output="",
                    execution_time_seconds=time.time() - start_time,
                    error_message="False Positive: Reproducer test passed on unpatched code. Test did not reproduce the bug."
                )

            # PHASE 2: Apply Atomic Patch
            apply_res = self.patcher.apply_edits(edits)
            if not apply_res["success"]:
                return ProofResult(
                    verified=False,
                    red_phase_failed=True,
                    green_phase_passed=False,
                    red_output=red_output,
                    green_output="",
                    execution_time_seconds=time.time() - start_time,
                    error_message=f"Patch application failed: {apply_res.get('errors')}"
                )
            patch_applied = True

            # PHASE 3: GREEN Verification (Should PASS on patched code)
            ret_code_green, green_output = self._execute_test(test_file_path, runner=test_spec.runner)
            green_passed = (ret_code_green == 0)

            if not green_passed:
                # Rollback patch: invert edits
                inverted_edits = [
                    Edit(path=e.path, search=e.replace, replace=e.search)
                    for e in edits
                ]
                try:
                    self.patcher.apply_edits(inverted_edits)
                except Exception as rb_err:
                    print(f"[ProofLoop] Warning: Rollback inversion error: {rb_err}")

                return ProofResult(
                    verified=False,
                    red_phase_failed=True,
                    green_phase_passed=False,
                    red_output=red_output,
                    green_output=green_output,
                    execution_time_seconds=time.time() - start_time,
                    error_message="Test still failed after applying patch (GREEN phase failed)."
                )

            # Succeeded RED -> GREEN
            return ProofResult(
                verified=True,
                red_phase_failed=True,
                green_phase_passed=True,
                red_output=red_output,
                green_output=green_output,
                execution_time_seconds=time.time() - start_time
            )

        finally:
            # Cleanup test if ephemeral and verification failed or not requested to persist
            if ephemeral_test:
                if test_file_created and test_file_path.exists():
                    test_file_path.unlink()
                elif original_test_content is not None:
                    test_file_path.write_text(original_test_content, encoding="utf-8")
