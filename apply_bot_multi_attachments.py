with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update on_local_voice_command
old_voice = '''                file_to_send = None
                if img_path and os.path.exists(img_path):
                    file_to_send = discord.File(img_path, filename=os.path.basename(img_path))

                print(f"[Eloise] Posting to #{target_ch.name}: {display[:60]}...", flush=True)
                try:
                    await target_ch.send(
                        content=f"⚔️ **Eloise Tactical Intel:**\\n{display}",
                        file=file_to_send
                    )'''

new_voice = '''                img_paths = res.get("image_attachments") or ([res["image_attachment"]] if res.get("image_attachment") else [])
                files_to_send = [discord.File(p, filename=os.path.basename(p)) for p in img_paths if os.path.exists(p)]

                print(f"[Eloise] Posting to #{target_ch.name}: {display[:60]}...", flush=True)
                try:
                    if files_to_send:
                        await target_ch.send(
                            content=f"⚔️ **Eloise Tactical Intel:**\\n{display}",
                            files=files_to_send
                        )
                    else:
                        await target_ch.send(
                            content=f"⚔️ **Eloise Tactical Intel:**\\n{display}"
                        )'''

assert old_voice in content, "old_voice not found in discord_bot.py!"
content = content.replace(old_voice, new_voice, 1)

# 2. Update general text on_message
old_msg = '''        file_to_send = None
        if img_path and os.path.exists(img_path):
            file_to_send = discord.File(img_path, filename=os.path.basename(img_path))

        dest = target_ch if target_ch else message.channel
        await dest.send(
            content=f"{message.author.mention} ⚔️ **Eloise :**\\n{display or spoken}",
            file=file_to_send
        )'''

new_msg = '''        img_paths = res.get("image_attachments") or ([res["image_attachment"]] if res.get("image_attachment") else [])
        files_to_send = [discord.File(p, filename=os.path.basename(p)) for p in img_paths if os.path.exists(p)]

        dest = target_ch if target_ch else message.channel
        if files_to_send:
            await dest.send(
                content=f"{message.author.mention} ⚔️ **Eloise :**\\n{display or spoken}",
                files=files_to_send
            )
        else:
            await dest.send(
                content=f"{message.author.mention} ⚔️ **Eloise :**\\n{display or spoken}"
            )'''

assert old_msg in content, "old_msg not found in discord_bot.py!"
content = content.replace(old_msg, new_msg, 1)

with open("co_pilot/discord_bot.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated discord_bot.py for all multiple attachments successfully!")
