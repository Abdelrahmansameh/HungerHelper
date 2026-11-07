import os
import json
import re

TRANSCRIPT_PATH = r"C:\Users\PC\.gemini\antigravity\brain\3867ac2b-acf9-4012-a98a-a6fd52e96d49\.system_generated\logs\transcript.jsonl"
OUT_CHRONICLE = r"c:\Users\PC\Documents\HungerHelper\PROJECT_PROMPTS_CHRONICLE.md"

def extract_user_turns():
    turns = []
    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                if obj.get("source") == "USER_EXPLICIT" or obj.get("type") == "USER_INPUT":
                    content = obj.get("content", "")
                    # Clean up <USER_REQUEST> tags if present
                    clean_content = re.sub(r"</?USER_REQUEST>", "", content).strip()
                    turns.append({
                        "step_index": obj.get("step_index"),
                        "timestamp": obj.get("created_at"),
                        "content": clean_content,
                        "media": obj.get("media", [])
                    })
            except Exception:
                pass
    return turns

turns = extract_user_turns()
print(f"Extracted {len(turns)} turns.")

doc_lines = [
    "# COMPLETE CHRONICLE OF USER PROMPTS, CONTEXT & DEVELOPMENT EVOLUTION",
    "**Project:** Hunger Helper / Eloise Tactical Assistant",
    f"**Total Documented User Turns:** {len(turns)}",
    "**Storage:** Workspace Permanent File (`PROJECT_PROMPTS_CHRONICLE.md`)",
    "",
    "> [!IMPORTANT]",
    "> This file preserves the exact, lossless record of every single prompt, screenshot context, demand, critique, and correction submitted by the user from Turn 1 to the present. Context truncation never erases these instructions.",
    "",
    "---",
    ""
]

for idx, t in enumerate(turns):
    turn_num = idx + 1
    ts = t["timestamp"]
    content = t["content"]
    media = t["media"]

    doc_lines.append(f"## Turn {turn_num} — [{ts}]")
    if media:
        media_descs = [f"- Media Attachment: `{m.get('mime_type')}` (`{os.path.basename(m.get('uri', ''))}`)" for m in media]
        doc_lines.append("\n".join(media_descs))
        doc_lines.append("")

    doc_lines.append("```text")
    doc_lines.append(content)
    doc_lines.append("```")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")

with open(OUT_CHRONICLE, "w", encoding="utf-8") as f:
    f.write("\n".join(doc_lines))

print(f"Chronicle written to {OUT_CHRONICLE} successfully with {len(turns)} turns.")
