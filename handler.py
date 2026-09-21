from keyboards import (
    start_keyboard, 
    get_keyboard,
    TEXT,
    cancel_keyboard
)
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from gmail_work import send_contract_to_email, send_cancel_contract_to_email
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from contract import fill_contract
import os
import sqlite3
import asyncio

class ContractForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_isikukood = State()
    waiting_for_specialty = State()
    waiting_for_gmail = State()
    waiting_for_phone_number = State()
    waiting_for_start_date = State()
    waiting_for_asice = State()
    waiting_for_last_step = State()
    

router1 = Router()
click_counts = {}
user_names = {}

conn = sqlite3.connect("bot_database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    status TEXT DEFAULT 'none',
    lang TEXT DEFAULT 'ru',
    end_date TEXT
)
""")
conn.commit()

def get_user_data(user_id: int):
    cursor.execute("SELECT status, lang FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT OR IGNORE INTO users (user_id, status, lang) VALUES (?, 'none', 'ru')", (user_id,))
        conn.commit()
        return "none", "ru"
    return row[0], row[1]

def update_user_status(user_id: int, status: str, end_date: str = None):
    if status == "none":
        cursor.execute("""
        INSERT INTO users (user_id, status, end_date) VALUES (?, ?, NULL)
        ON CONFLICT(user_id) DO UPDATE SET status = ?, end_date = NULL
        """, (user_id, status, status))
    elif end_date is not None:
        cursor.execute("""
        INSERT INTO users (user_id, status, end_date) VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET status = ?, end_date = ?
        """, (user_id, status, end_date, status, end_date))
    else:
        cursor.execute("""
        INSERT INTO users (user_id, status) VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET status = ?
        """, (user_id, status, status))
    conn.commit()

def update_user_lang(user_id: int, lang_code: str):
    cursor.execute("""
    INSERT INTO users (user_id, lang) VALUES (?, ?)
    ON CONFLICT(user_id) DO UPDATE SET lang = ?
    """, (user_id, lang_code, lang_code))
    conn.commit()

def get_user_file_path(user_id: int):
    downloads_dir = "downloads"
    if os.path.exists(downloads_dir):
        for filename in os.listdir(downloads_dir):
            if f"_{user_id}_" in filename or filename.startswith(f"signed_{user_id}"):
                return os.path.join(downloads_dir, filename)
    return None

def reset_clicks(user_id: int):
    if user_id in click_counts:
        click_counts[user_id] = 0

@router1.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    
    arg = message.text.split()
    user_id = None
    action = None
    
    if len(arg) > 1:
        param = arg[1]
        try:
            action, user_id_str = param.split("_")
            user_id = int(user_id_str)
        except ValueError:
            await message.answer("❌ Неверная ссылка подтверждения.")
            return

    if action and user_id:
        current_status, user_lang = get_user_data(user_id)
        
        if current_status != "pending":
            await message.answer(f"⚠️ Этот договор уже был обработан ранее! Статус: {current_status}")
            return
        
        if action == "accept":
            update_user_status(user_id, "accepted")
            try:
                await message.bot.send_message(
                    chat_id=user_id, text=TEXT[user_lang].get("accept_answer"))
            except Exception as e:
                print(f"⚠️ Не удалось отправить сообщение пользователю {user_id}: {e}")
            await message.answer(TEXT[user_lang].get("accept_answer_2"))
            return
        
        elif action == "reject":
            update_user_status(user_id, "none")
            try:
                await message.bot.send_message(
                    chat_id=user_id, text=TEXT[user_lang].get("reject_answer"))
            except Exception as e:
                print(f"⚠️ Не удалось отправить сообщение пользователю {user_id}: {e}")
            await message.answer(TEXT[user_lang].get("reject_answer_2"))
            
            downloads_dir = "downloads"
            if os.path.exists(downloads_dir):
                try:
                    for filename in os.listdir(downloads_dir):
                        if str(user_id) in filename:
                            file_path = os.path.join(downloads_dir, filename)
                            os.remove(file_path)
                            print(f"Файл успешно удален по ссылке отказа из почты: {file_path}")
                except Exception as e:
                    print(f"Ошибка при удалении файла: {e}")
            else:
                print("Папка downloads не найдена.")
            return
        
    await message.answer(
        "Please select language", 
        reply_markup=start_keyboard()
    )

# --- ХЕНДЛЕР ДЛЯ КНОПКИ МЕНЮ ---
@router1.message(F.text == "/menu")
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    _, user_lang = get_user_data(user_id)
    
    await message.answer(
        text="🏠︎ Main Menu",
        reply_markup=get_keyboard(user_lang)
    )
# ------------------------------------

@router1.callback_query(F.data.in_({"lang_ru", "lang_ee","lang_eng"}))
async def select_lang(callback: CallbackQuery, state : FSMContext):
    lang_code = callback.data.split("_")[1]
    await state.update_data(lang = lang_code)
    update_user_lang(callback.from_user.id, lang_code)
    
    await callback.message.edit_text(
        text="🏠︎ Main Menu", 
        reply_markup=get_keyboard(lang_code)
    )
    await callback.answer()
    
@router1.callback_query(F.data == "btn_rent")
async def start_rent(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    user_id = callback.from_user.id
    status, user_lang = get_user_data(user_id)
    
    if status in ["pending", "accepted"]:
        await callback.message.answer(TEXT[user_lang].get("already_has_contract"))
        return
    
    click_counts[user_id] = 0
    reset_clicks(user_id)
    
    _, user_lang = get_user_data(user_id)
    await callback.message.answer(TEXT[user_lang]["ask_name"])
    await state.set_state(ContractForm.waiting_for_name)

@router1.message(ContractForm.waiting_for_name, F.text)
async def process_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    entered_name = message.text.strip()
    name_lower = entered_name.lower()
    
    try:
        await message.delete()
    except Exception:
        pass
        
    _, user_lang = get_user_data(user_id)
    
    if name_lower == "bill cipher":
        await message.answer_photo(
            photo=FSInputFile("melody/bill cipher.jfif"),
            caption="👁️"
        )
        return
    elif name_lower == "52":
        await message.answer(
            text= "Мы поняли друг-друга))"
        )
        return
    elif name_lower == "matcha":
        await message.answer(text= "❤")
        return
    
    elif name_lower =="tünk":
        await message.answer(text="I ❤ NARVA COLLEGE!")
        return
    elif name_lower =="social credit":
        await message.answer(text="中國黨為你們感到自豪。!")
        return
    elif name_lower == "speedrun":
        await message.answer_photo(
            photo=FSInputFile("melody/speedrun.jpg"))
        return
    elif name_lower =="vladlen pokrova":
            await message.answer(text="LeGeNd!!!🤯🤯🤯")
            return
    elif name_lower =="elizaveta sirkunen":
        await message.answer(text="Прекрасная подруга и мэнофоб 🙂")
        
    elif name_lower =="iuliia lillmann":
        await message.answer_photo(
            photo =FSInputFile("melody/angel.webp"),
            caption="❤Самый прекрасный человек на свете❤")
    elif name_lower =="anita kvitenko":
        await message.answer("!ГЛАВА СОВЕТА 2026!")
    
    user_names[user_id] = entered_name
    await state.update_data(full_name=entered_name)
    
    await message.answer(TEXT[user_lang]["ask_isikukood"])
    await state.set_state(ContractForm.waiting_for_isikukood)

@router1.message(ContractForm.waiting_for_isikukood, F.text)
async def process_isikukood(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(isikukood=message.text)
    
    try:
        await message.delete()
    except Exception:
        pass

    _, user_lang = get_user_data(user_id)
    await message.answer(TEXT[user_lang]["ask_specialty"])
    await state.set_state(ContractForm.waiting_for_specialty)

@router1.message(ContractForm.waiting_for_specialty, F.text)
async def process_specialty(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(specialty=message.text)
    
    try:
        await message.delete()
    except Exception:
        pass

    _, user_lang = get_user_data(user_id)
    await message.answer(TEXT[user_lang]["ask_gmail"])
    await state.set_state(ContractForm.waiting_for_gmail)

@router1.message(ContractForm.waiting_for_gmail, F.text)
async def process_gmail(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(gmail=message.text)
    
    try:
        await message.delete()
    except Exception:
        pass

    _, user_lang = get_user_data(user_id)
    await message.answer(TEXT[user_lang]["ask_phone_number"])
    await state.set_state(ContractForm.waiting_for_phone_number)

@router1.message(ContractForm.waiting_for_phone_number, F.text)
async def process_phone_number(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(phone_number=message.text)
    
    try:
        await message.delete()
    except Exception:
        pass

    _, user_lang = get_user_data(user_id)
    await message.answer(TEXT[user_lang]["ask_start_date"])
    await state.set_state(ContractForm.waiting_for_start_date)




def get_end_year(user_data):
    start_date_str = user_data.get("start_date", "")
    now = datetime.strptime(start_date_str.strip(), "%d.%m.%Y")
    if now.month >= 7:
        return str(now.year + 1)
    return str(now.year)

@router1.message(ContractForm.waiting_for_start_date, F.text)
async def process_start_date(message: Message, state: FSMContext):
    user_id = message.from_user.id
    date_text = message.text.strip()
    date_lower = date_text.lower()
    _, user_lang = get_user_data(user_id)
    
    try:
        await message.delete()
    except Exception:
        pass

    try:
        parsed_date = datetime.strptime(date_text, "%d.%m.%Y")
        if parsed_date.year < 1000 or parsed_date.year > 2099:
            raise ValueError("Некорректный год")
    except (ValueError, Exception):
        await message.answer(TEXT[user_lang]["incorect_date"], parse_mode="Markdown")
        return

    await state.update_data(start_date=date_text)
    
    await state.set_state(ContractForm.waiting_for_asice)
    user_data = await state.get_data()

    current_today_date = datetime.now().strftime("%d.%m.%Y")
    calculated_end_date = get_end_year(user_data)

    await message.answer(TEXT[user_lang]["generating"])
    output_filename = f"Contract_{user_id}.docx"

    fill_contract(
        full_name=user_data.get("full_name"),
        isikukood=user_data.get("isikukood"),
        specialty=user_data.get("specialty"),
        gmail=user_data.get("gmail"),
        phone_number=user_data.get("phone_number"),
        start_date=user_data.get("start_date"),
        end_year=calculated_end_date,
        today_date=current_today_date,
        output_path=output_filename,
    )
    
    doc_to_send = FSInputFile(output_filename)
    await message.answer_document(
        document=doc_to_send,
        caption=TEXT[user_lang].get("contract_ready"),
    )
    
    warning_text = TEXT[user_lang].get("marked_message")
    await message.answer(warning_text, parse_mode="Markdown")

@router1.message(ContractForm.waiting_for_asice, F.document)
async def process_asice_file(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = await state.get_data()
    _, user_lang = get_user_data(user_id)
    real_user_name = user_data.get("full_name")
    
    document = message.document
    asice_filename = document.file_name or f"signed_{user_id}.asice"
    
    os.makedirs("downloads", exist_ok=True)
    downloaded_file_path = f"downloads/signed_{user_id}_{asice_filename}"
    await message.bot.download(document, destination=downloaded_file_path)
    
    calculated_end_year = get_end_year(user_data)
    contract_end_date = f"30.06.{calculated_end_year}"
    update_user_status(user_id, "pending", contract_end_date)
    
    await send_contract_to_email(
        file_path=downloaded_file_path,
        user_name=real_user_name,
        user_id=user_id,
        user_lang=user_lang,
    )
    
    docx_filename = f"Contract_{user_id}.docx"
    if os.path.exists(docx_filename):
        os.remove(docx_filename)
    
    await message.answer(TEXT[user_lang].get("final_contract"))
    await state.clear()

@router1.callback_query(F.data == "btn_contract")
async def get_contract(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    user_id = callback.from_user.id
    status, user_lang = get_user_data(user_id)
    
    file_path = get_user_file_path(user_id)
    
    if status == "none" or status == "rejected":
        click_counts[user_id] = click_counts.get(user_id, 0) + 1
        if click_counts[user_id] == 100:
            await callback.message.answer(text="Я думаю ты первый и единственный кто добрался сюда. Тебе настолько было нечего делать?=)")
        elif 12 <= click_counts[user_id] <= 99:
            await callback.message.answer(text="STOP!!!!!")
        elif click_counts[user_id] == 5:
            await callback.message.answer_audio(
                audio=FSInputFile("melody/lol.mp3"),
                caption=TEXT[user_lang].get("secret")
            )
        else:
            await callback.message.answer(TEXT[user_lang].get("contract_answer_1"))
        
    elif status == "pending":
        await callback.message.answer(TEXT[user_lang].get("contract_answer_2"))
    elif status == "accepted":
        msg_text = await callback.message.answer(TEXT[user_lang].get("contract_answer_3"))
        if file_path and os.path.exists(file_path):
            msg_doc = await callback.message.answer_document(FSInputFile(file_path))
            
            async def delete_contract_messages(chat_id: int, text_msg_id: int, doc_msg_id: int):
                await asyncio.sleep(180)
                try:
                    await callback.bot.delete_message(chat_id=chat_id, message_id=text_msg_id)
                except Exception:
                    pass
                try:
                    await callback.bot.delete_message(chat_id=chat_id, message_id=doc_msg_id)
                except Exception:
                    pass

            asyncio.create_task(
                delete_contract_messages(
                    chat_id=callback.message.chat.id,
                    text_msg_id=msg_text.message_id,
                    doc_msg_id=msg_doc.message_id
                )
            )
        else:
            await callback.message.answer(TEXT[user_lang].get("contract_warning"))

@router1.callback_query(F.data == "btn_cancel")
async def cancel_contract(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    user_id = callback.from_user.id
    
    cursor.execute("SELECT status, lang, end_date FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    status, user_lang, end_date_str = row if row else ("none", "ru", None)
    
    if status == "accepted" and end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, "%d.%m.%Y")
            if datetime.now() > end_date:
                update_user_status(user_id, "none")
                
                downloads_dir = "downloads"
                if os.path.exists(downloads_dir):
                    try:
                        for filename in os.listdir(downloads_dir):
                            if str(user_id) in filename:
                                file_path = os.path.join(downloads_dir, filename)
                                os.remove(file_path)
                                print(f"Просроченный файл успешно удален: {file_path}")
                    except Exception as e:
                        print(f"Ошибка при удалении просроченного файла: {e}")
                
                status = "none"
        except Exception as e:
            print(f"Ошибка проверки дедлайна: {e}")

    if status in ["none", "rejected", "pending"]:
        await callback.message.answer(TEXT[user_lang].get("cancel_false"))
    elif status == "accepted":
        await callback.message.answer(
            text=TEXT[user_lang].get("cancel_conf"),
            reply_markup=cancel_keyboard(user_lang)
        )
    reset_clicks(user_id)

@router1.callback_query(F.data == "btn_confirm")
async def confirm_contract(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    user_id = callback.from_user.id
    _, user_lang = get_user_data(user_id)
    real_user_name = user_names.get(user_id, callback.from_user.full_name)
    
    await callback.message.answer(TEXT[user_lang].get("final_accept"))
    await send_cancel_contract_to_email(user_name=real_user_name, user_lang=user_lang)
    update_user_status(user_id, "none")
    
    downloads_dir = "downloads"
    if os.path.exists(downloads_dir):
        try:
            for filename in os.listdir(downloads_dir):
                if str(user_id) in filename:
                    file_path = os.path.join(downloads_dir, filename)
                    os.remove(file_path)
                    print(f"Файл успешно удален: {file_path}")
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")
    else:
        print("Папка downloads не найдена.")
    
    await state.clear()

@router1.callback_query(F.data == "btn_cancel_2")
async def cancel_contract_2(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback.from_user.id
    _, user_lang = get_user_data(user_id)
    
    await callback.message.edit_text(
        text="🏠︎ Main Menu",
        reply_markup=get_keyboard(user_lang)
    )
    await callback.answer()