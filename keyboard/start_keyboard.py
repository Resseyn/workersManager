# Создаем объекты инлайн-кнопок
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

adm_button_1 = InlineKeyboardButton(
    text='Выдать доступ',
    callback_data='adm_add_access'
)

adm_button_2 = InlineKeyboardButton(
    text='Добавить расходники',
    callback_data='adm_add_consumables'
)
worker_button_0 = InlineKeyboardButton(
    text='Выдать прокси',
    callback_data='give_proxy'
)
worker_button_1 = InlineKeyboardButton(
    text='Выдать аккаунт',
    callback_data='give_account'
)
worker_button_2 = InlineKeyboardButton(
    text='Запрос баланса',
    callback_data='get_balance'
)
worker_button_3 = InlineKeyboardButton(
    text='Тикет к администрации',
    callback_data='ticket'
)
worker_button_4 = InlineKeyboardButton(
    text='Вопрос к ChatGPT',
    callback_data='chat_gpt'
)

worker_button_5 = InlineKeyboardButton(
    text='Проверить твиттер',
    callback_data='check_twitter'
)
adm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
                     [adm_button_1],
                     [adm_button_2]
                     ]
)
worker_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[worker_button_0],
                     [worker_button_1],
                     [worker_button_2],
                     [worker_button_3],
                     [worker_button_4],
                    [worker_button_5]
                     ]
)

back_button_k = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back")]])

approve_k = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Подтвердить", callback_data="approve"),
                                                   InlineKeyboardButton(text="Отклонить", callback_data="decline")]])

accounts_types = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text="Instagram", callback_data="instagram")],
    [InlineKeyboardButton(text="Telegram", callback_data="telegram")],
    [InlineKeyboardButton(text="Twitter", callback_data="twitter")],
    [InlineKeyboardButton(text="Discord", callback_data="discord")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
])


get_accounts_types_k = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text="Instagram", callback_data="get_instagram")],
    [InlineKeyboardButton(text="Telegram", callback_data="get_telegram")],
    [InlineKeyboardButton(text="Twitter", callback_data="get_twitter")],
    [InlineKeyboardButton(text="Discord", callback_data="get_discord")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
])