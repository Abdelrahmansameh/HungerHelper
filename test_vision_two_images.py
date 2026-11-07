import asyncio
import traceback
import sys
sys.stdout.reconfigure(encoding="utf-8")

from co_pilot.vision_analyzer import analyze_inventory_screenshot

async def test():
    img_p = r"C:/Users/PC/.gemini/antigravity/brain/3867ac2b-acf9-4012-a98a-a6fd52e96d49/.user_uploaded/media_1793831515451_f14e1f96.png"
    print("Testing analyze_inventory_screenshot...")
    try:
        res = await analyze_inventory_screenshot(
            img_p, "analyse ma stash", "123456", "Abdallah"
        )
        print("Spoken:", res.get("spoken_text"))
        print("Display:", res.get("display_text")[:200])
        print("Image Attachments:", res.get("image_attachments"))
    except Exception:
        traceback.print_exc()

asyncio.run(test())
