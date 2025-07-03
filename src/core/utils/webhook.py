import os
import httpx

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SECRET_TOKEN = os.getenv("TELEGRAM_SECRET_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

async def set_webhook():
    if not BOT_TOKEN or not WEBHOOK_URL or not SECRET_TOKEN:
        raise ValueError("Missing .env values for webhook setup")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
            json={
                "url": f"{WEBHOOK_URL}/webhook/",
                "secret_token": SECRET_TOKEN,
                "drop_pending_updates": True,
            }
        )
        response.raise_for_status()

