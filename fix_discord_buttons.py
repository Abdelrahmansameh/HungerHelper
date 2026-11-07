with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    code = f.read().replace("\r\n", "\n")

old_block = """        file_to_send = None
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

        dest = target_ch if target_ch else message.channel
        await dest.send(
            content=f"{message.author.mention} ⚔️ **Eloise :**\\n{display or spoken}",
            file=file_to_send,
            view=view_to_attach
        )"""

new_block = """        file_to_send = None
        if img_path and os.path.exists(img_path):
            file_to_send = discord.File(img_path, filename=os.path.basename(img_path))

        dest = target_ch if target_ch else message.channel
        await dest.send(
            content=f"{message.author.mention} ⚔️ **Eloise :**\\n{display or spoken}",
            file=file_to_send
        )"""

if old_block in code:
    code = code.replace(old_block, new_block)
    with open("co_pilot/discord_bot.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("SUCCESS: discord_bot.py updated - button views removed from default replies!")
else:
    print("WARNING: old_block not found in discord_bot.py")
