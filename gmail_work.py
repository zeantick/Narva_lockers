from email.message import EmailMessage
import os
from dotenv import load_dotenv
import aiosmtplib
from keyboards import TEXT
import traceback

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

load_dotenv()

bot_mail = os.getenv("bot_mail")
bot_password = os.getenv("bot_password")
send_mail = os.getenv("send_mail")
bot_username = os.getenv("bot_username")

async def send_contract_to_email(
    file_path: str, user_name: str, user_id: int, user_lang: str = "ru"
) -> bool:
    """Отправление на почту договор"""
    try:
        lang_texts = TEXT.get(user_lang, TEXT["ru"])
        
        msg = EmailMessage()
        msg["From"] = bot_mail
        msg["To"] = send_mail
        msg["Subject"] = lang_texts["message_gmail_subject"].format(full_name=user_name)

        accept_link = f"https://t.me/{bot_username}?start=accept_{user_id}"
        reject_link = f"https://t.me/{bot_username}?start=reject_{user_id}"
        
        body_text = lang_texts["message_gmail_text"].format(full_name=user_name)
        
        html_content = f"""
        <html>
        <body>
            <p>{body_text}</p>
            <br>
            <p><strong>Действия с договором:</strong></p>
            <p>
                <a href="{accept_link}" style="background-color: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; display: inline-block; margin-right: 10px;">✅Kinnita</a>
                <a href="{reject_link}" style="background-color: #dc3545; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; display: inline-block;">✖Lükka tagasi</a>
            </p>
        </body>
        </html>
        """
        
        msg.set_content(body_text)
        msg.add_alternative(html_content, subtype="html")
        
        filename = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=filename,
                )
        print(f"DEBUG AUTH -> Login: '{bot_mail}' | Password length: {len(bot_password) if bot_password else 0}")
        await aiosmtplib.send(
            msg,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            username=bot_mail,
            password=bot_password,
            use_tls=True,
            timeout=10,
            )

        print(f"✅ [EMAIL] Письмо от {user_name} успешно отправлено!")
        return True
    
    except aiosmtplib.SMTPAuthenticationError:
        print("❌ [EMAIL ERROR] Ошибка авторизации: неверный логин или пароль!")
        return False
    
    except aiosmtplib.SMTPConnectError:
        print(
        "❌ [EMAIL ERROR] Не удалось подключиться к серверу Gmail (проверь"
        " интернет)!"
    )
        return False
    
    except FileNotFoundError:
        print(f"❌ [EMAIL ERROR] Файл договора по пути {file_path} не найден!")
        return False
    except Exception as e:
        print(f"⚠️ [EMAIL ERROR] Не удалось отправить письмо: {e}")
        traceback.print_exc()
        return False

async def send_cancel_contract_to_email(user_name: str, user_lang: str = "ru") -> bool:
    try:
        lang_texts = TEXT.get(user_lang, TEXT["ru"])
        
        msg = EmailMessage()
        msg["From"] = bot_mail
        msg["To"] = send_mail
        msg["Subject"] = lang_texts.get("cancel_gmail_subject").format(full_name=user_name)
        
        email_body = lang_texts.get("cancel_gmail_body").format(full_name=user_name)
        msg.set_content(email_body)
        
        await aiosmtplib.send(
                    msg,
                    hostname=SMTP_SERVER,
                    port=SMTP_PORT,
                    username=bot_mail,
                    password=bot_password,
                    use_tls=True,
                    timeout=10,
                    )
        print(f"✅ [EMAIL] Письмо от {user_name} успешно отправлено!")
        return True
    
    except Exception as e:
        print(f"Ошибка при отправке письма об отмене: {e}")
        return False
