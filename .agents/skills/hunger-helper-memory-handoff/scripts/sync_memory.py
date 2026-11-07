import os
import sys
import json
import re
import subprocess
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
BRAIN_BASE = r"C:\Users\PC\.gemini\antigravity\brain"
CHRONICLE_PATH = os.path.join(ROOT_DIR, "PROJECT_PROMPTS_CHRONICLE.md")
PROMPTS_TXT_PATH = os.path.join(ROOT_DIR, "extracted_all_user_prompts.txt")

def find_latest_transcript():
    if not os.path.exists(BRAIN_BASE):
        return None
    # Prioritize conversation directories containing the most transcript activity
    conv_dirs = [os.path.join(BRAIN_BASE, d) for d in os.listdir(BRAIN_BASE) if os.path.isdir(os.path.join(BRAIN_BASE, d))]
    valid_transcripts = []
    for cd in conv_dirs:
        t_path = os.path.join(cd, ".system_generated", "logs", "transcript.jsonl")
        if os.path.exists(t_path):
            valid_transcripts.append((os.path.getsize(t_path), os.path.getmtime(t_path), t_path))
    if not valid_transcripts:
        return None
    # Sort by size and mtime so the primary active session is preferred
    valid_transcripts.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return valid_transcripts[0][2]

def extract_prompts_from_transcript(t_path):
    prompts = []
    if not t_path or not os.path.exists(t_path):
        return prompts
    with open(t_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                if obj.get("type") == "USER_INPUT" or obj.get("source") == "USER_EXPLICIT":
                    content = obj.get("content", "")
                    step_idx = obj.get("step_index", len(prompts))
                    created_at = obj.get("created_at", "")
                    if content:
                        # Automatically redact secret tokens (Discord bot tokens, Gemini API keys, etc.)
                        content = re.sub(r'[A-Za-z0-9_\-]{20,32}\.[A-Za-z0-9_\-]{6}\.[A-Za-z0-9_\-]{20,45}', '[DISCORD_BOT_TOKEN_REDACTED]', content)
                        content = re.sub(r'(?:AQ\.[a-zA-Z0-9_\-]{20,}|AIza[0-9A-Za-z-_]{35})', '[GEMINI_API_KEY_REDACTED]', content)
                        if not any(p["content"] == content for p in prompts):
                            prompts.append({
                                "step": step_idx,
                                "created_at": created_at,
                                "content": content
                            })
            except Exception:
                pass
    return prompts

def sync_memory():
    print("==================================================")
    print("  HUNGER HELPER : PROJECT MEMORY & HANDOFF SYNC")
    print("==================================================")
    t_path = find_latest_transcript()
    if t_path:
        print(f"Latest transcript discovered: {t_path}")
        prompts = extract_prompts_from_transcript(t_path)
        print(f"Total user requests extracted: {len(prompts)}")
        
        # Save raw dump if needed
        with open(PROMPTS_TXT_PATH, "w", encoding="utf-8") as f:
            for p in prompts:
                f.write(f"\n--- STEP {p['step']} [{p['created_at']}] ---\n")
                f.write(p["content"].strip() + "\n")
        print(f"Updated: {PROMPTS_TXT_PATH}")
    else:
        print("Transcript log not found; preserving existing chronicle.")

    if os.path.exists(CHRONICLE_PATH):
        with open(CHRONICLE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        print(f"Memory Chronicle Status: {CHRONICLE_PATH} ({len(lines)} lines)")
    else:
        print(f"Warning: {CHRONICLE_PATH} missing.")

    # Synchronize with GitHub repository
    sync_github()

    print("\nMemory and GitHub sync complete. Session handoff ready.")

def sync_github(commit_msg=None):
    git_bin = r"C:\Users\PC\AppData\Local\Programs\Git\cmd\git.exe"
    if not os.path.exists(git_bin):
        git_bin = "git"
    
    env = os.environ.copy()
    env["PATH"] = r"C:\Users\PC\AppData\Local\Programs\Git\cmd;C:\Users\PC\AppData\Local\Microsoft\WinGet\Links;" + env.get("PATH", "")

    try:
        p_status = subprocess.run([git_bin, "status", "--porcelain"], cwd=ROOT_DIR, capture_output=True, text=True, env=env)
        changes = p_status.stdout.strip()
        if not changes:
            print("GitHub Status: Up to date (no uncommitted changes).")
            return
        
        print(f"GitHub Sync: Staging changes...\n{changes[:200]}")
        subprocess.run([git_bin, "add", "-A"], cwd=ROOT_DIR, check=True, env=env)
        
        if not commit_msg:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            commit_msg = f"Auto-sync: update project files [{now_str}]"
            
        print(f"GitHub Sync: Committing with message: '{commit_msg}'...")
        subprocess.run([git_bin, "commit", "-m", commit_msg], cwd=ROOT_DIR, check=True, env=env)
        
        print("GitHub Sync: Pushing to origin main...")
        push_res = subprocess.run([git_bin, "push", "origin", "main"], cwd=ROOT_DIR, capture_output=True, text=True, env=env)
        if push_res.returncode == 0:
            print("GitHub Sync: Successfully pushed to GitHub main branch!")
        else:
            print(f"GitHub Sync: Push result: {push_res.stderr.strip() or push_res.stdout.strip()}")
    except Exception as e:
        print(f"GitHub Sync Warning: {e}")

if __name__ == "__main__":
    sync_memory()
