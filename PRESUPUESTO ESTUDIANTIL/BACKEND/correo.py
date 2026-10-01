import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Presupuesto Estudiantil")

def correo_configurado() -> bool:
    return bool(SMTP_USER and SMTP_PASSWORD)

def enviar_codigo_recuperacion(destino: str, nombre: str, codigo: str, minutos: int):
    if not correo_configurado():
        print(f"[MODO DESARROLLO] Código de recuperación para {destino}: {codigo}")
        return

    msg = EmailMessage()
    msg["Subject"] = f"Tu código de verificación: {codigo}"
    msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_USER}>"
    msg["To"] = destino
    msg.set_content(
        f"Hola {nombre},\n\n"
        f"Tu código para restablecer la contraseña es: {codigo}\n\n"
        f"Vence en {minutos} minutos. Si no pediste este cambio, ignora este correo.\n\n"
        f"— {SMTP_FROM_NAME}"
    )
    msg.add_alternative(f"""\
<div style="font-family: Arial, sans-serif; max-width: 440px; margin: auto; color: #0F172A;">
  <h2 style="color: #154C86;">🎓 {SMTP_FROM_NAME}</h2>
  <p>Hola <strong>{nombre}</strong>,</p>
  <p>Usa este código para restablecer tu contraseña:</p>
  <p style="font-size: 34px; font-weight: bold; letter-spacing: 12px; color: #2E7D9A;
            background: #E0F2F7; padding: 14px; text-align: center; border-radius: 8px;">{codigo}</p>
  <p style="color: #475569; font-size: 14px;">
    Vence en {minutos} minutos. Si no pediste este cambio, ignora este correo.
  </p>
</div>
""", subtype="html")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as servidor:
        servidor.starttls()
        servidor.login(SMTP_USER, SMTP_PASSWORD)
        servidor.send_message(msg)
