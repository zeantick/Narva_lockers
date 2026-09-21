from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
)

TEXT = {
    "ru":{"rent":"🗄️ Аренда шкафчика", 
        "contract": "📜 Мой договор",
        "cancel": "❌ Отказаться",
        "ask_name": "Пожалуйста напишите ваше имя и фамилию: ",
        "ask_isikukood": "Пожалуйста введите ваш Личный код (Isikukood):",
        "ask_specialty": "Напишите вашу специальность и номер курса(0-3)\nНапример: IT 3 ",
        "ask_gmail": "Введите вашу почту",
        "ask_phone_number": "Напишите свой номер телефона",
        "ask_start_date": "Напишите пожалуйста дату начала использование шкафчика:(например 11.07.2026) ",
        "incorect_date": '⚠️ Неверный формат даты! Пожалуйста, введите дату в формате \n"ДД.ММ.ГГГГ (например: 01.09.2026)."',
        "generating": "⏳ Генерирую договор, подождите...",
        "contract_ready": "✅ Ваш договор готов! Скачайте и проверьте.",
        "marked_message":"Пожалуйста проверьте и пришлите подписанный договор дигитально, в случае отправки с опечатками или без подписи, договор будет отклонен.",
        "message_gmail_subject" : "Новый подписанный договор от {full_name}",
        "message_gmail_text": ("Здравствуйте!\n\nПользователь {full_name}"
                                " отправил письмо с заключением договора.\nФайл вложен ниже:"
                            ),
        "final_contract" : "Договор успешно отправлен✅.\nПожалуйста ожидайте когда заявку подтвердят😊",
        "accept_answer": "Договор успешно был подтвержден✅. Вы можете забрать ключи в течение 3 дней на Инфопункте (1 этаж, рядом с лифтом)",
        "accept_answer_2": "Контракт был успешно подтвержден 🟢",
        "reject_answer" : "Ваш договор был отклонен ❌.",
        "reject_answer_2": "Заявка на договор была отклонена ❌",
        "contract_answer_1" : "К сожалению у вас нет на данный момент договора😟",
        "contract_answer_2": "🟠Заявка находится в обработке, пожалуйста ожидайте ответа, вам придет сообщение",
        "contract_answer_3": "🖊Ваш договор",
        "contract_warning": "⚠️ Файл договора не найден на сервере.",
        "secret": "🎉 Ого! Ты открыл секретный трек. Включавай на полную и продолжай ждать договор! 🎧",
        "cancel_conf": "🤔Вы действительно уверены в отмене договора?",
        "cancel_conf_2": "Подтвердить✅",
        "cancel_cancel_2" : "Отмена❌",
        "cancel_false": "Нечего еще отменять😆",
        "cancel_gmail_subject" : "Отмена договора",
        "cancel_gmail_body": "Здравствуйте!\n\n Хочу отозвать договор по поводу шкафчика\nС Уважением,\n {full_name}",
        "cancel_accepted": "👍Письмо о расторжении договора пришло. Пожалуйста в течении суток отдайте ключи и приведите шкафчик в порядок!",
        "already_has_contract" :"⚠️ У тебя уже есть активный договор или заявка на рассмотрении! Сначала отмени текущий договор, если хочешь оформить новый.",
        "final_accept": "Договор успешно отменен. Пожалуйста, отчистите свой шкафчик и верните ключ на Инфопункт в течение 3 дней."
    },
    
    "ee":{"rent":"🗄️ Kapi rent", 
        "contract": "📜 Minu leping",
        "cancel": "❌ Keeldu",
        "ask_name": "Palun kirjutage oma ees- ja perekonnanimi: ",
        "ask_isikukood": "Palun sisestage oma isikukood: ",
        "ask_specialty": "Nüüd kirjuta oma eriala ja õppeaasta (0–3)\nNäiteks: IT 3 ",
        "ask_gmail" : "Sisesta oma e-posti aadress",
        "ask_phone_number": "Kirjuta oma telefoninumber üles.",
        "ask_start_date": "Palun sisestage hoiukapi kasutamise alguskuupäev (nt 11.07.2026)",
        "incorect_date": '⚠️ Vigane kuupäevavorming! Palun sisestage kuupäev vormingus \n"PP.KK.AAAA (nt: 01.09.2026)."',
        "generating": "⏳ Lepingu koostamine, palun oodake...",
        "contract_ready" : "✅ Teie leping on valmis! Laadige see alla ja vaadake üle.",
        "marked_message" : "Palun kontrollige lepingut ja saatke see digitaalselt allkirjastatuna tagasi; kui see saadetakse trükivigadega või ilma allkirjata, lükatakse see tagasi.",
        "message_gmail_subject": "Uus allkirjastatud leping kasutajalt {full_name}",
        "message_gmail_text": ("Tere!\n\n Kasutaja {full_name}"
                            " on saatnud lepingu sõlmimise kohta meili.\nFail on allpool lisatud:"
                            ),
        "final_contract" : "Leping on edukalt saadetud✅. Palun oodake taotluse kinnitamist😊.",
        "accept_answer": "Leping on edukalt kinnitatud ✅. Võtmed saate kätte 3 päeva jooksul infolauast (1. korrusel, lifti kõrval).",
        "accept_answer_2": "Leping kinnitati edukalt 🟢",
        "reject_answer": "Teie leping lükati tagasi ❌.",
        "reject_answer_2": "Lepingu taotlus lükati tagasi ❌",
        "contract_answer_1" : "Кahjuks ei ole teil hetkel lepingut. 😟",
        "contract_answer_2": "🟠Teie päringut töödeldakse; palun oodake vastust – saate vastava teate.",
        "contract_answer_3": "🖊Teie leping",
        "contract_warning": "⚠️ Lepingu faili ei leitud serverist.",
        "secret": "🎉 Vau! Oled avanud salajase loo. Keera helitugevus põhja ja jää lepingut ootama! 🎧",
        "cancel_conf": "🤔 Kas sa oled lepingu tühistamises tõesti kindel?",
        "cancel_conf_2": "Kinnita✅",
        "cancel_cancel_2" : "Tühista❌",
        "cancel_false": "Pole veel midagi tühistada 😆",
        "cancel_gmail_subject": "lepingut tühistama",
        "cancel_gmail_body": "Tere!\n\n Soovin tühistada hoiukapi lepingu.\nLugupidamisega,\n{full_name}",
        "cancel_accepted": "👍Lepingulõpetamise teade on saabunud. Palun anna võtmed üle ja korrasta kapp 24 tunni jooksul!",
        "already_has_contract" : "⚠️ Teil on juba kehtiv leping või pooleliolev taotlus! Kui soovite sõlmida uue lepingu, tühistage esmalt praegune leping.",
        "final_accept": "Leping on edukalt tühistatud. Palun tühjendage oma kapp ja tagastage võti infolauda 3 päeva jooksul."
    },
    
    "eng":{"rent":"🗄️ Locker rent", 
        "contract": "📜 My contract",
        "cancel": "❌ Refuse",
        "ask_name": "Please write your first and last name: ",
        "ask_isikukood": "Please enter your personal identification code (Isikukood):",
        "ask_specialty": "Now write your specialization and year of study (0–3).\nFor example: IT 3 ",
        "ask_gmail" : "Enter your email",
        "ask_phone_number": "Write down your phone number.",
        "ask_start_date": "Please write the start date for using the locker(For example 11.07.2026):",
        "incorect_date": '⚠️ Invalid date format! Please enter the date in the format \n"DD.MM.YYYY (example 01.09.2026)."',
        "generating": "⏳ Generating the contract, please wait...",
        "contract_ready": "✅ Your contract is ready! Download and review it.",
        "marked_message": "Please check the contract and send it back digitally signed; if it is sent with typos or without a signature, it will be rejected.",
        "message_gmail_subject": "New signed agreement from {full_name}",
        "message_gmail_text": ("Hello!\n\nUser {full_name}"
                                " has sent an email regarding the contract conclusion.\nThe file is attached below:"
                            ),
        "final_contract" : "The contract has been successfully sent✅. Please wait for the request to be confirmed😊.",
        "accept_answer": "The contract has been successfully confirmed ✅. You can pick up the keys within 3 days at the Information Desk (1st floor, next to the elevator).",
        "accept_answer_2": "The contract was successfully confirmed 🟢",
        "reject_answer": "Your contract was rejected ❌.",
        "reject_answer_2": "The contract request was rejected ❌",
        "contract_answer_1" : "Unfortunately, you do not have a contract at the moment. 😟",
        "contract_answer_2": "🟠Your request is being processed; please wait for a response—you will receive a message.",
        "contract_answer_3": "🖊Your contract",
        "contract_warning": "⚠️ The contract file was not found on the server.",
        "secret": "🎉 Wow! You’ve unlocked a secret track. Crank up the volume and keep waiting for the contract! 🎧",
        "cancel_conf": "🤔 Are you really sure about cancelling the contract?",
        "cancel_conf_2": "Confirm✅",
        "cancel_cancel_2" : "Cancel❌",
        "cancel_false": "Nothing to cancel yet 😆",
        "cancel_gmail_subject" : "Cancel contract",
        "cancel_gmail_body": "Hello!\n\nI would like to cancel the contract regarding the locker.\nBest regards,\n{full_name}",
        "cancel_accepted": "👍The contract termination notice has arrived. Please hand over the keys and tidy up the locker within 24 hours!",
        "already_has_contract" : "⚠️ You already have an active contract or a pending application! Cancel the current contract first if you want to set up a new one.",
        "final_accept": "The contract has been successfully cancelled. Please clear out your locker and return the key to the Information Desk within 3 days."
    }
}

user_languages = {}



def start_keyboard() -> InlineKeyboardMarkup:
    sk = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Russian", callback_data= "lang_ru")],
        [InlineKeyboardButton(text="🇪🇪 Eesti", callback_data= "lang_ee")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data= "lang_eng")]
        
    ])
    return sk


def get_keyboard(lang_code : str) -> InlineKeyboardMarkup:
    lang = TEXT.get(lang_code, TEXT["ru"])
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lang["rent"], callback_data="btn_rent")],
        [InlineKeyboardButton(text=lang["contract"], callback_data="btn_contract")],
        [InlineKeyboardButton(text=lang["cancel"], callback_data="btn_cancel")],
    ])
    return kb

def cancel_keyboard(lang_code : str)-> InlineKeyboardMarkup:
    lang = TEXT.get(lang_code, TEXT["ru"])
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=lang["cancel_conf_2"], callback_data="btn_confirm"),
            InlineKeyboardButton(text=lang["cancel_cancel_2"], callback_data="btn_cancel_2")
        ]
    ])
    return kb

def extend_confirmation(lang_code: str) -> InlineKeyboardMarkup:
    lang = TEXT.get(lang_code, TEXT["ru"])
    ex = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=lang["cancel_conf_2"], callback_data="btn_extend_conf"),
            InlineKeyboardButton(text=lang["cancel_cancel_2"], callback_data="btn_extend_cancel"),
            
        ]
    ])
    return ex