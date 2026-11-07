import os

p = "co_pilot/discord_bot.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add /config-gemini slash command
target_cmd = """@bot.tree.command(name="progress", description="Check your quest and progression summary")"""

replace_cmd = """@bot.tree.command(name="config-gemini", description="Configure your free Google Gemini API key for automated screenshot stash & inventory vision")
@app_commands.describe(key="Your Google AI Studio Gemini API key (from https://aistudio.google.com)")
async def config_gemini(interaction: discord.Interaction, key: str):
    from co_pilot.vision_analyzer import set_gemini_api_key
    ok = set_gemini_api_key(key)
    if ok:
        await interaction.response.send_message(
            content="✅ **Clé Gemini API configurée avec succès !**\\n"
                    "Éloïse peut désormais scanner instantanément vos captures d'écran d'inventaire, de sac de raid et de coffre de stash avec l'IA Vision !\\n"
                    "📸 *Uploadez simplement un screenshot dans ce salon avec votre question.*",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            content="⚠️ **Erreur lors de l'enregistrement de la clé.**",
            ephemeral=True
        )

@bot.tree.command(name="progress", description="Check your quest and progression summary")"""

assert target_cmd in text, "target_cmd not found"
text = text.replace(target_cmd, replace_cmd, 1)

# 2. Add screenshot attachments and text inventory handling in on_message
target_on_message = """    content_raw = message.content.strip()
    content_lower = content_raw.lower()
    target_ch = find_target_channel(message.guild)
    is_in_target = target_ch and message.channel.id == target_ch.id"""

replace_on_message = """    content_raw = message.content.strip()
    content_lower = content_raw.lower()
    target_ch = find_target_channel(message.guild)
    is_in_target = target_ch and message.channel.id == target_ch.id

    # 0. SCREENSHOT INVENTORY / STASH VISION SCANNER
    if is_in_target and message.attachments:
        img_att = None
        for att in message.attachments:
            if att.content_type and any(t in att.content_type.lower() for t in ["image", "png", "jpeg", "jpg", "webp"]):
                img_att = att
                break
            elif any(att.filename.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp"]):
                img_att = att
                break

        if img_att:
            temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp_audio"))
            os.makedirs(temp_dir, exist_ok=True)
            save_path = os.path.join(temp_dir, f"screen_{message.author.id}_{int(time.time()*1000)}.png")
            await img_att.save(save_path)

            from co_pilot.vision_analyzer import analyze_inventory_screenshot
            status_wait = await message.reply("🔍 **Analyse visuelle de votre inventaire en cours avec l'IA Vision...**")

            res_vis = await analyze_inventory_screenshot(
                save_path, message.clean_content, str(message.author.id), message.author.display_name
            )

            spoken = res_vis.get("spoken_text", "")
            display = res_vis.get("display_text", "")

            if spoken and message.guild.id in active_voice_clients:
                await play_voice_response(message.guild.id, spoken)

            await status_wait.edit(content=f"{message.author.mention} ⚔️ **Eloise :**\\n{display}")
            return

    # 0.1 TEXT INVENTORY / STASH APPRAISER ("j'ai 3 farines, 1 deux, combien ca vaut")
    if is_in_target and any(w in content_lower for w in ["j'ai", "jai", "combien vaut mon", "combien valent mes", "combien vaut mon sac", "combien vaut mon inventaire"]) and any(w in content_lower for w in ["farine", "deux", "salpetre", "salpêtre", "bague", "charbon", "cle", "clé", "sacs"]):
        from co_pilot.vision_analyzer import appraise_text_inventory
        appraise_res = appraise_text_inventory(content_raw, is_french=True)
        spoken = appraise_res.get("spoken_text", "")
        display = appraise_res.get("display_text", "")
        if spoken and message.guild.id in active_voice_clients:
            await play_voice_response(message.guild.id, spoken)
        await message.reply(content=f"{message.author.mention} ⚔️ **Eloise :**\\n{display}")
        return"""

assert target_on_message in text, "target_on_message not found"
text = text.replace(target_on_message, replace_on_message, 1)

with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("co_pilot/discord_bot.py patched with Vision Screenshot & Inventory scanning successfully!")
