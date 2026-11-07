with open('co_pilot/discord_bot.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_target = """    file_to_send = None
    if img_path and os.path.exists(img_path):
        file_to_send = discord.File(img_path, filename="raid_map.jpg")

    await interaction.followup.send(content=display or spoken, file=file_to_send)"""

new_target = """    img_paths = result.get("image_attachments") or ([result["image_attachment"]] if result.get("image_attachment") else [])
    files_to_send = [discord.File(p, filename=os.path.basename(p)) for p in img_paths if os.path.exists(p)]

    if files_to_send:
        await interaction.followup.send(content=display or spoken, files=files_to_send)
    else:
        await interaction.followup.send(content=display or spoken)"""

if old_target in text:
    text = text.replace(old_target, new_target, 1)
    print("Replaced in /ask!")
else:
    print("old_target not found in /ask")

with open('co_pilot/discord_bot.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated discord_bot.py!")
