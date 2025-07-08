import httpx

from core.config import settings


async def set_webhook():
    """if not settings.BOT_TOKEN or not settings.WEBHOOK_URL or not settings.SECRET_TOKEN:
        raise ValueError("Missing .env values for webhook setup")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.telegram.org/bot{settings.BOT_TOKEN}/setWebhook",
            json={
                "url": f"{settings.WEBHOOK_URL}/webhook/",
                "secret_token": settings.SECRET_TOKEN,
                "drop_pending_updates": True,
            }
        )
        response.raise_for_status()"""

