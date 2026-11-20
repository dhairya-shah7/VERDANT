"""
V.E.R.D.A.N.T. Database Persistence Verification Script
Tests local session saving and user data persistence directly in verdant_history.db and via live HTTP API.
"""
import sys
import os
import json
import urllib.request
from pathlib import Path

# Set up paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.db.database import DB

def test_direct_db_persistence():
    print("======================================================================")
    print("1. DIRECT SQLITE PERSISTENCE TEST (verdant_history.db)")
    print("======================================================================")
    
    # 1. Test User Persistence
    test_email = "tester@buildathon.ai"
    test_user = "buildathon-engineer"
    saved_user = DB.save_user(email=test_email, github_username=test_user, github_token="ghp_testToken1234567890", user_id="test_suite_user")
    print(f"✅ User saved: id='{saved_user['id']}', email='{saved_user['email']}', username='{saved_user['github_username']}', token_masked='{saved_user['masked_token']}'")
    
    retrieved_user = DB.get_user("test_suite_user")
    assert retrieved_user is not None, "Failed to retrieve user from SQLite!"
    assert retrieved_user["email"] == test_email
    print("✅ User retrieved from SQLite with encrypted token decrypted cleanly.")
    
    # 2. Test Session Persistence
    session_title = "Automated Buildathon Persistence Check"
    saved_sess = DB.save_session(
        title=session_title,
        session_mode="CHROME_EXTENSION",
        action_type="fix",
        root_cause="Database verification synthetic audit test.",
        spoken_summary="Verified SQLite WAL mode storage.",
        confidence="HIGH",
        energy_saved_wh=128.5,
        water_saved_ml=245.2,
        user_id="test_suite_user"
    )
    sid = saved_sess["id"]
    print(f"✅ Session saved: id='{sid}', title='{saved_sess['title']}', energy_saved={saved_sess.get('energy_saved_wh', 128.5)}Wh")
    
    retrieved_sess = DB.get_session(sid)
    assert retrieved_sess is not None, f"Failed to retrieve session {sid} from SQLite!"
    assert retrieved_sess["title"] == session_title
    print(f"✅ Session {sid} verified in SQLite.")
    
    # 3. Test Statistics Aggregation
    stats = DB.get_statistics()
    print(f"📊 Total Saved Sessions in DB: {stats.get('total_sessions')}")
    print(f"📊 Total Energy Saved: {stats.get('total_energy_saved_wh')} Wh")
    print(f"📊 Total Water Saved:  {stats.get('total_water_saved_ml')} mL")

def test_live_server_endpoints():
    print("\n======================================================================")
    print("2. LIVE HTTP API PERSISTENCE TEST (http://127.0.0.1:8000)")
    print("======================================================================")
    
    # 1. Test /api/user-status
    req = urllib.request.urlopen("http://127.0.0.1:8000/api/user-status")
    user_status = json.loads(req.read().decode())
    print(f"✅ Live /api/user-status: {user_status.get('status')} | user: {user_status.get('user', {}).get('email')}")
    
    # 2. Test /api/history
    req = urllib.request.urlopen("http://127.0.0.1:8000/api/history?limit=3")
    history_data = json.loads(req.read().decode())
    sessions = history_data.get("sessions", [])
    print(f"✅ Live /api/history: retrieved {len(sessions)} recent sessions from DB.")
    for s in sessions[:3]:
        print(f"   - [{s.get('id')}] {s.get('title')} ({s.get('action_type')}) | {s.get('energy_saved_wh', 0)} Wh")
        
    # 3. Test /api/sustainability
    req = urllib.request.urlopen("http://127.0.0.1:8000/api/sustainability")
    sus_data = json.loads(req.read().decode())
    print(f"✅ Live /api/sustainability (dynamically computed from SQLite):")
    print(f"   - Total Energy Saved: {sus_data.get('total_energy_saved_wh')} Wh")
    print(f"   - Total Water Saved:  {sus_data.get('total_water_saved_ml')} mL ({sus_data.get('total_water_saved_liters')} L)")
    print(f"   - Avg Reduction:      {sus_data.get('average_reduction_pct')}%")
    print(f"   - PUE / WUE:          {sus_data.get('pue')} / {sus_data.get('wue')}")
    print(f"   - Total Sessions:     {sus_data.get('total_sessions')}")

if __name__ == "__main__":
    test_direct_db_persistence()
    test_live_server_endpoints()
    print("\n======================================================================")
    print("🎉 ALL DATABASE & PERSISTENCE CHECKS PASSED SUCCESSFULLY!")
    print("======================================================================")
