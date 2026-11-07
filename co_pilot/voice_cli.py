import os
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from co_pilot.brain import CoPilotBrain
from co_pilot.audio_output import speak_async
from co_pilot.profile_store import get_user_progression_summary

def print_banner():
    print("""
===================================================================
     [+]   HUNGER HELPER: TACTICAL VOICE CO-PILOT (LOCAL CLI)   [+]
===================================================================
  Runs with <1% CPU & 0% GPU load.
  Speaks directly to your headphones/speakers via Neural Audio.

  Commands / Natural Prompts you can try:
    - "Where do I get honey?" / "Who sells bone char?"
    - "What does Discerning talent do?"
    - "I finished quest A Warm Welcome"
    - "What should I do next?"
    - "Generate map for Sarlat Farm"
    - "progress" (Shows your combat record, active & unlocked quests)
    - "quit" / "exit" to stop
===================================================================
""")

def main():
    print_banner()
    brain = CoPilotBrain()
    user_id = "local_player"
    user_name = "Commander"

    # Play initial radio check
    speak_async("Hunger Helper co-pilot online and ready.")

    while True:
        try:
            prompt = input("\n[You] > ").strip()
            if not prompt:
                continue
            if prompt.lower() in ["quit", "exit", "q"]:
                speak_async("Co-pilot powering down. Safe hunting.")
                print("Exiting HungerHelper Co-Pilot. Good hunt!")
                break
                
            if prompt.lower() == "progress":
                summary = get_user_progression_summary(user_id)
                print(f"\n--- Combat Record: {user_name} ---")
                print(f"Level: {summary['level']} | Completed Quests: {summary['completed_count']}")
                print(f"Active Quests: {[q['name'] for q in summary['active_quests']] if summary['active_quests'] else 'None'}")
                print(f"Next Available: {[q['name'] for q in summary['available_quests'][:5]]}")
                print(f"Talents: {[f'{t['name']} ({t['allocated_points']}/{t['max_points']})' for t in summary['talents']]}")
                continue

            result = brain.process_message(user_id, user_name, prompt)
            
            # Print tactical display
            print(f"\n[Co-Pilot Display]:\n{result.get('display_text')}")
            
            # Speak out loud
            spoken = result.get("spoken_text")
            if spoken:
                print(f"[Radio Voice]: \"{spoken}\"")
                speak_async(spoken)
                
            # If map generated, notify file location
            if "image_attachment" in result and os.path.exists(result["image_attachment"]):
                print(f"[Tactical Map]: Saved to file:///{result['image_attachment']}")
                
        except (KeyboardInterrupt, EOFError):
            print("\nShutting down.")
            break

if __name__ == "__main__":
    main()
