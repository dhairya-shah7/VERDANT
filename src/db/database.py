"""
V.E.R.D.A.N.T. Secure Database & Audit History Engine
Persistent SQLite storage with encrypted credentials and PII-sanitized forensic logs.
Built for the Google Cloud & DeepMind Startup Buildathon.
"""
import os
import sqlite3
import json
import time
import uuid
import base64
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, List
from cryptography.fernet import Fernet
from src.context_prism.pii_sanitizer import sanitize_text

DB_PATH_DEFAULT = Path(__file__).resolve().parent.parent.parent / "verdant_history.db"

def _get_fernet() -> Fernet:
    """Derives a stable cryptographic key for token encryption at rest."""
    raw_key = os.getenv("VERDANT_SECRET_KEY")
    if not raw_key:
        seed = (os.getenv("COMPUTERNAME", "verdant-host") + "-verdant-secret-key").encode("utf-8")
        key = base64.urlsafe_b64encode(hashlib.sha256(seed).digest())
    else:
        key = base64.urlsafe_b64encode(hashlib.sha256(raw_key.encode("utf-8")).digest())
    return Fernet(key)

def encrypt_secret(secret_text: str) -> str:
    if not secret_text or not secret_text.strip():
        return ""
    try:
        f = _get_fernet()
        return f.encrypt(secret_text.encode("utf-8")).decode("utf-8")
    except Exception:
        return ""

def decrypt_secret(encrypted_text: str) -> str:
    if not encrypted_text or not encrypted_text.strip():
        return ""
    try:
        f = _get_fernet()
        return f.decrypt(encrypted_text.encode("utf-8")).decode("utf-8")
    except Exception:
        return ""

class VerdantDatabase:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH_DEFAULT
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            # 1. Users & Encrypted Credentials
            conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT,
                github_username TEXT,
                encrypted_github_token TEXT,
                created_at REAL,
                updated_at REAL
            );
            """)

            # 2. Incident & Triage History Sessions
            conn.execute("""
            CREATE TABLE IF NOT EXISTS incident_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                title TEXT,
                session_mode TEXT,          -- 'WITH_REPO' or 'WITHOUT_REPO'
                action_type TEXT,           -- 'fix', 'advise', 'test', 'env', 'clarify'
                video_filename TEXT,
                scrubbed_console TEXT,
                scrubbed_network TEXT,
                root_cause TEXT,
                spoken_summary TEXT,
                patch_diff TEXT,
                reproduction_steps TEXT,    -- JSON list of strings
                confidence TEXT,            -- 'HIGH', 'MEDIUM', 'LOW'
                arbiter_tier INTEGER,
                status TEXT,                -- 'PR_CREATED', 'PATCH_READY', 'TRIAGE_REPORT', 'ENV_RESOLVED'
                branch_name TEXT,
                commit_hash TEXT,
                pr_url TEXT,
                energy_saved_wh REAL,
                water_saved_ml REAL,
                created_at REAL
            );
            """)

            # 3. Closed-Loop Proof Records
            conn.execute("""
            CREATE TABLE IF NOT EXISTS proof_records (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                red_phase_failed INTEGER,
                green_phase_passed INTEGER,
                execution_time_seconds REAL,
                reproducer_code TEXT,
                created_at REAL,
                FOREIGN KEY (session_id) REFERENCES incident_sessions(id) ON DELETE CASCADE
            );
            """)
            conn.commit()
        self._seed_if_empty()

    def _seed_if_empty(self):
        """Automatically seeds initial audit history and users if the database is newly initialized."""
        try:
            with self._get_conn() as conn:
                cur = conn.execute("SELECT count(*) FROM incident_sessions")
                count = cur.fetchone()[0]
                if count == 0:
                    seed_file = Path(__file__).resolve().parent / "seed_history.json"
                    if seed_file.exists():
                        with open(seed_file, "r", encoding="utf-8") as f:
                            seed_data = json.load(f)
                        for u in seed_data.get("users", []):
                            conn.execute("""
                                INSERT OR IGNORE INTO users (id, email, github_username, encrypted_github_token, created_at, updated_at)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (u["id"], u.get("email"), u.get("github_username"), u.get("encrypted_github_token"), u.get("created_at"), u.get("updated_at")))
                        for s in seed_data.get("sessions", []):
                            conn.execute("""
                                INSERT OR IGNORE INTO incident_sessions (
                                    id, user_id, title, session_mode, action_type, video_filename,
                                    scrubbed_console, scrubbed_network, root_cause, spoken_summary,
                                    patch_diff, reproduction_steps, confidence, arbiter_tier, status,
                                    branch_name, commit_hash, pr_url, energy_saved_wh, water_saved_ml, created_at
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                s["id"], s.get("user_id"), s.get("title"), s.get("session_mode"), s.get("action_type"), s.get("video_filename"),
                                s.get("scrubbed_console"), s.get("scrubbed_network"), s.get("root_cause"), s.get("spoken_summary"),
                                s.get("patch_diff"), s.get("reproduction_steps"), s.get("confidence"), s.get("arbiter_tier"), s.get("status"),
                                s.get("branch_name"), s.get("commit_hash"), s.get("pr_url"), s.get("energy_saved_wh", 0.0), s.get("water_saved_ml", 0.0), s.get("created_at")
                            ))
                        for p in seed_data.get("proofs", []):
                            conn.execute("""
                                INSERT OR IGNORE INTO proof_records (
                                    id, session_id, red_phase_failed, green_phase_passed,
                                    execution_time_seconds, reproducer_code, created_at
                                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (
                                p["id"], p.get("session_id"), p.get("red_phase_failed"), p.get("green_phase_passed"),
                                p.get("execution_time_seconds"), p.get("reproducer_code"), p.get("created_at")
                            ))
                        conn.commit()
        except Exception as e:
            print(f"[V.E.R.D.A.N.T. DB] Notice during auto-seed: {e}")

    # User Management
    def save_user(self, email: str, github_username: str, github_token: Optional[str] = None, user_id: str = "default_user") -> Dict[str, Any]:
        encrypted_token = encrypt_secret(github_token) if github_token else ""
        now = time.time()
        with self._get_conn() as conn:
            cur = conn.execute("SELECT id, encrypted_github_token FROM users WHERE id = ?", (user_id,))
            row = cur.fetchone()
            if row:
                enc_to_save = encrypted_token if encrypted_token else row["encrypted_github_token"]
                conn.execute("""
                    UPDATE users 
                    SET email = ?, github_username = ?, encrypted_github_token = ?, updated_at = ?
                    WHERE id = ?
                """, (email, github_username, enc_to_save, now, user_id))
            else:
                conn.execute("""
                    INSERT INTO users (id, email, github_username, encrypted_github_token, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, email, github_username, encrypted_token, now, now))
            conn.commit()

        return self.get_user(user_id)

    def get_user(self, user_id: str = "default_user") -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            cur = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cur.fetchone()
            if not row:
                return None
            data = dict(row)
            # Decrypt token for safe client state verification
            token = decrypt_secret(data.get("encrypted_github_token", ""))
            data["has_github_token"] = bool(token)
            data["masked_token"] = (token[:4] + "..." + token[-3:]) if len(token) > 8 else ("Set" if token else "")
            del data["encrypted_github_token"]
            return data

    def get_user_token(self, user_id: str = "default_user") -> Optional[str]:
        with self._get_conn() as conn:
            cur = conn.execute("SELECT encrypted_github_token FROM users WHERE id = ?", (user_id,))
            row = cur.fetchone()
            if not row:
                return None
            return decrypt_secret(row["encrypted_github_token"])

    # Session Management
    def save_session(
        self,
        title: str,
        session_mode: str, # 'WITH_REPO' or 'WITHOUT_REPO'
        action_type: str,  # 'fix', 'advise', 'test', 'env', 'clarify'
        root_cause: str,
        spoken_summary: str,
        confidence: str = "HIGH",
        arbiter_tier: int = 1,
        status: str = "COMPLETED",
        video_filename: Optional[str] = None,
        raw_console: Optional[str] = None,
        raw_network: Optional[str] = None,
        patch_diff: Optional[str] = None,
        reproduction_steps: Optional[List[str]] = None,
        branch_name: Optional[str] = None,
        commit_hash: Optional[str] = None,
        pr_url: Optional[str] = None,
        energy_saved_wh: float = 0.0,
        water_saved_ml: float = 0.0,
        proof_data: Optional[Dict[str, Any]] = None,
        user_id: str = "default_user",
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Saves a fully sanitized forensic session into SQLite."""
        sid = session_id or str(uuid.uuid4())[:8]
        now = time.time()

        # Enforce ContextPrism sanitization on all raw text before storage
        scrubbed_console = sanitize_text(raw_console) if raw_console else ""
        scrubbed_network = sanitize_text(raw_network) if raw_network else ""
        steps_json = json.dumps(reproduction_steps or [])

        with self._get_conn() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO incident_sessions (
                    id, user_id, title, session_mode, action_type, video_filename,
                    scrubbed_console, scrubbed_network, root_cause, spoken_summary,
                    patch_diff, reproduction_steps, confidence, arbiter_tier, status,
                    branch_name, commit_hash, pr_url, energy_saved_wh, water_saved_ml, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sid, user_id, title, session_mode, action_type, video_filename or "",
                scrubbed_console, scrubbed_network, root_cause, spoken_summary,
                patch_diff or "", steps_json, confidence, arbiter_tier, status,
                branch_name or "", commit_hash or "", pr_url or "",
                round(energy_saved_wh, 2), round(water_saved_ml, 2), now
            ))

            # Store closed-loop proof if present
            if proof_data:
                proof_id = str(uuid.uuid4())[:8]
                conn.execute("""
                    INSERT INTO proof_records (
                        id, session_id, red_phase_failed, green_phase_passed,
                        execution_time_seconds, reproducer_code, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    proof_id,
                    sid,
                    1 if proof_data.get("red_phase_failed") else 0,
                    1 if proof_data.get("green_phase_passed") else 0,
                    proof_data.get("execution_time_seconds", 0.0),
                    proof_data.get("reproducer_code", ""),
                    now
                ))

            conn.commit()

        return self.get_session(sid)

    def update_session_pr(
        self,
        session_id: str,
        pr_url: str,
        branch_name: Optional[str] = None,
        commit_hash: Optional[str] = None,
        status: str = "PR_CREATED"
    ) -> bool:
        with self._get_conn() as conn:
            conn.execute("""
                UPDATE incident_sessions
                SET pr_url = ?, branch_name = COALESCE(?, branch_name),
                    commit_hash = COALESCE(?, commit_hash), status = ?
                WHERE id = ?
            """, (pr_url, branch_name, commit_hash, status, session_id))
            conn.commit()
            return True

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            cur = conn.execute("SELECT * FROM incident_sessions WHERE id = ?", (session_id,))
            row = cur.fetchone()
            if not row:
                return None
            sess = dict(row)
            try:
                sess["reproduction_steps"] = json.loads(sess.get("reproduction_steps") or "[]")
            except Exception:
                sess["reproduction_steps"] = []

            # Attach proof record if exists
            p_cur = conn.execute("SELECT * FROM proof_records WHERE session_id = ? ORDER BY created_at DESC LIMIT 1", (session_id,))
            p_row = p_cur.fetchone()
            if p_row:
                sess["proof"] = {
                    "id": p_row["id"],
                    "red_phase_failed": bool(p_row["red_phase_failed"]),
                    "green_phase_passed": bool(p_row["green_phase_passed"]),
                    "execution_time_seconds": p_row["execution_time_seconds"],
                    "reproducer_code": p_row["reproducer_code"]
                }
            else:
                sess["proof"] = None

            return sess

    def list_sessions(
        self,
        limit: int = 50,
        mode: Optional[str] = None,
        action_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query = "SELECT * FROM incident_sessions WHERE 1=1"
        params: List[Any] = []

        if mode:
            query += " AND session_mode = ?"
            params.append(mode)
        if action_type:
            query += " AND action_type = ?"
            params.append(action_type)

        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        with self._get_conn() as conn:
            cur = conn.execute(query, params)
            rows = cur.fetchall()
            results = []
            for r in rows:
                item = dict(r)
                try:
                    item["reproduction_steps"] = json.loads(item.get("reproduction_steps") or "[]")
                except Exception:
                    item["reproduction_steps"] = []
                results.append(item)
            return results

    def get_statistics(self) -> Dict[str, Any]:
        with self._get_conn() as conn:
            cur = conn.execute("""
                SELECT 
                    COUNT(*) as total_sessions,
                    SUM(CASE WHEN session_mode = 'WITH_REPO' THEN 1 ELSE 0 END) as with_repo_count,
                    SUM(CASE WHEN session_mode = 'WITHOUT_REPO' THEN 1 ELSE 0 END) as without_repo_count,
                    SUM(CASE WHEN pr_url != '' AND pr_url IS NOT NULL THEN 1 ELSE 0 END) as total_prs,
                    SUM(energy_saved_wh) as total_energy_saved_wh,
                    SUM(water_saved_ml) as total_water_saved_ml
                FROM incident_sessions
            """)
            row = dict(cur.fetchone())
            return {
                "total_sessions": row["total_sessions"] or 0,
                "with_repo_count": row["with_repo_count"] or 0,
                "without_repo_count": row["without_repo_count"] or 0,
                "total_prs": row["total_prs"] or 0,
                "total_energy_saved_wh": round(row["total_energy_saved_wh"] or 0.0, 1),
                "total_water_saved_ml": round(row["total_water_saved_ml"] or 0.0, 1),
            }

    def delete_session(self, session_id: str) -> bool:
        with self._get_conn() as conn:
            conn.execute("DELETE FROM incident_sessions WHERE id = ?", (session_id,))
            conn.commit()
            return True

# Global DB Instance Singleton
DB = VerdantDatabase()
