with open("co_pilot/discord_bot.py", "r", encoding="utf-8") as f:
    content = f.read()

old_block = '''            spoken = res_vis.get("spoken_text", "")
            display = res_vis.get("display_text", "")
            img_path = res_vis.get("image_attachment")

            if spoken and message.guild.id in active_voice_clients:
                await play_voice_response(message.guild.id, spoken)

            file_to_send = None
            if img_path and os.path.exists(img_path):
                file_to_send = discord.File(img_path, filename=os.path.basename(img_path))

            try:
                await status_wait.delete()
            except Exception:
                pass

            dest = target_ch if target_ch else message.channel
            await dest.send(content=f"{message.author.mention} ⚔️ **Eloise :**\\n{display}", file=file_to_send)
            return'''

new_block = '''            spoken = res_vis.get("spoken_text", "")
            display = res_vis.get("display_text", "")
            img_paths = res_vis.get("image_attachments") or ([res_vis["image_attachment"]] if res_vis.get("image_attachment") else [])

            if spoken and message.guild.id in active_voice_clients:
                await play_voice_response(message.guild.id, spoken)

            files_to_send = [discord.File(p, filename=os.path.basename(p)) for p in img_paths if os.path.exists(p)]

            try:
                await status_wait.delete()
            except Exception:
                pass

            dest = target_ch if target_ch else message.channel
            if files_to_send:
                await dest.send(content=f"{message.author.mention} ⚔️ **Eloise :**\\n{display}", files=files_to_send)
            else:
                await dest.send(content=f"{message.author.mention} ⚔️ **Eloise :**\\n{display}")
            return'''

assert old_block in content, "old_block not found in discord_bot.py!"
content = content.replace(old_block, new_block, 1)

with open("co_pilot/discord_bot.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated co_pilot/discord_bot.py to send multiple files successfully!")
