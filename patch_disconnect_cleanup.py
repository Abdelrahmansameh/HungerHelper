p = "co_pilot/discord_bot.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = """    if not humans:
        if current_vc and current_vc.is_connected():
            ch_name = current_vc.channel.name
            await current_vc.disconnect()
            active_voice_clients.pop(guild.id, None)
            print(f"[Voice] Nobody in HUNGER. Eloise disconnected from: {ch_name}", flush=True)
        return None"""

replace = """    if not humans:
        if current_vc and current_vc.is_connected():
            ch_name = current_vc.channel.name
            if guild.id in active_voice_sinks:
                try:
                    active_voice_sinks[guild.id].cleanup()
                    active_voice_sinks.pop(guild.id, None)
                except Exception:
                    pass
            await current_vc.disconnect()
            active_voice_clients.pop(guild.id, None)
            print(f"[Voice] Nobody in HUNGER. Eloise disconnected from: {ch_name}", flush=True)
        return None"""

assert target in text, "target not found"
text = text.replace(target, replace, 1)

with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("Disconnect cleanup added successfully!")
