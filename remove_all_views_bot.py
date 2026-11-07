with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. In post_intel_to_discord:
old_post = '''    view = None
    if img_path:
        low_p = os.path.basename(img_path).lower()
        if "map" in low_p:
            view = TacticalMapQuickView(os.path.basename(img_path))
        elif "quest" in low_p:
            view = QuestCardQuickView()
        elif "item" in low_p or "weapon" in low_p or "creature" in low_p:
            view = ItemCardQuickView()

    try:
        if file_to_send and view:
            await target_ch.send(content=content, file=file_to_send, view=view)
        elif file_to_send:
            await target_ch.send(content=content, file=file_to_send)
        else:
            await target_ch.send(content=content)'''

new_post = '''    try:
        if file_to_send:
            await target_ch.send(content=content, file=file_to_send)
        else:
            await target_ch.send(content=content)'''

assert old_post in content, "old_post not found!"
content = content.replace(old_post, new_post, 1)

# 2. In on_local_voice_command:
old_voice_post = '''                file_to_send = None
                view_to_attach = None
                if img_path and os.path.exists(img_path):
                    file_to_send = discord.File(img_path, filename=os.path.basename(img_path))
                    if any(w in img_path.lower() for w in ["map", "raid"]):
                        t_map = brain.last_map_info.get("map_name", "Sarlat Farm")
                        view_to_attach = TacticalMapQuickView(t_map)
                    elif "quest_card" in img_path.lower():
                        q_cand = brain.last_active_quest or "cette quête"
                        view_to_attach = QuestCardQuickView(q_cand)
                    else:
                        item_cand = brain.last_queried_item or "cet objet"
                        view_to_attach = ItemCardQuickView(item_cand)

                print(f"[Eloise] Posting to #{target_ch.name}: {display[:60]}...", flush=True)
                try:
                    await target_ch.send(
                        content=f"⚔️ **Eloise Tactical Intel:**\\n{display}",
                        file=file_to_send,
                        view=view_to_attach
                    )'''

new_voice_post = '''                file_to_send = None
                if img_path and os.path.exists(img_path):
                    file_to_send = discord.File(img_path, filename=os.path.basename(img_path))

                print(f"[Eloise] Posting to #{target_ch.name}: {display[:60]}...", flush=True)
                try:
                    await target_ch.send(
                        content=f"⚔️ **Eloise Tactical Intel:**\\n{display}",
                        file=file_to_send
                    )'''

assert old_voice_post in content, "old_voice_post not found!"
content = content.replace(old_voice_post, new_voice_post, 1)

with open("co_pilot/discord_bot.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated co_pilot/discord_bot.py successfully!")
