from datetime import datetime, timezone

import aiosmtplib
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.models.alert import Alert


async def create_alert(session: AsyncSession, symbol: str, alert_type: str, message: str) -> Alert:
    alert = Alert(symbol=symbol, alert_type=alert_type, message=message, timestamp=datetime.now(timezone.utc))
    session.add(alert)
    await session.commit()
    await session.refresh(alert)
    await send_slack_alert(alert.message)
    await send_email_alert(alert.message)
    return alert


async def list_alerts(session: AsyncSession, limit: int = 200) -> list[Alert]:
    stmt = select(Alert).order_by(Alert.timestamp.desc()).limit(limit)
    return list((await session.execute(stmt)).scalars().all())


async def send_slack_alert(message: str) -> None:
    if not settings.slack_webhook:
        return
    async with httpx.AsyncClient(timeout=10.0) as client:
        await client.post(settings.slack_webhook, json={"text": message})


async def send_email_alert(message: str) -> None:
    if not (settings.smtp_host and settings.smtp_user and settings.smtp_pass and settings.alert_email_to):
        return
    payload = (
        f"From: {settings.smtp_user}\r\n"
        f"To: {settings.alert_email_to}\r\n"
        "Subject: Trading Platform Alert\r\n"
        "\r\n"
        f"{message}\r\n"
    )
    await aiosmtplib.send(payload, hostname=settings.smtp_host, port=settings.smtp_port, username=settings.smtp_user, password=settings.smtp_pass, start_tls=True)
