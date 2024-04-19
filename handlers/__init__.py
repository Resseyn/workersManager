from .other import dp
from .main_start import dp
from .add_proxy import dp

from aiogram import Dispatcher, F, types
from aiogram.filters import Command
from handlers import (main_start, add_proxy, other, add_consumables,give_access,
                      main_start,get_proxy, get_consumables, get_balance, get_ticket, chat_gpt,
                      check_twitter_verif)


def setup(dp):
    dp.message.register(main_start.command_start_handler, Command('start'))
    dp.callback_query.register(add_proxy.add_proxy, F.data == "adm_add_proxy")
    dp.callback_query.register(add_consumables.add_account, F.data == "adm_add_consumables")
    dp.callback_query.register(give_access.give_access, F.data == "adm_add_access")
    dp.callback_query.register(get_proxy.get_proxy, F.data == "give_proxy")
    dp.callback_query.register(get_balance.get_balance_card, F.data == "get_balance")
    dp.callback_query.register(get_ticket.get_ticket, F.data == "ticket")
    dp.callback_query.register(chat_gpt.get_ticket, F.data == "chat_gpt")
    dp.callback_query.register(check_twitter_verif.check, F.data == "check_twitter")
    dp.callback_query.register(get_consumables.get_account, F.data.startswith("give_account"))
    dp.callback_query.register(get_consumables.await_getting_account, F.data == "get_instagram")
    dp.callback_query.register(get_consumables.await_getting_account, F.data == "get_discord")
    dp.callback_query.register(get_consumables.await_getting_account, F.data == "get_telegram")
    dp.callback_query.register(get_consumables.await_getting_account, F.data == "get_twitter")
    dp.callback_query.register(get_consumables.approval, F.data.startswith("accApprove"))
    dp.callback_query.register(get_consumables.decline, F.data.startswith("accDecline"))
    dp.callback_query.register(get_proxy.approval, F.data.startswith("prxApprove"))
    dp.callback_query.register(get_proxy.decline, F.data.startswith("prxDecline"))
    dp.callback_query.register(get_balance.approval, F.data.startswith("blnApprove"))
    dp.callback_query.register(get_balance.decline, F.data.startswith("blnDecline"))
    dp.callback_query.register(get_ticket.approval, F.data.startswith("tkcApprove"))
    dp.callback_query.register(other.back_handler, F.data == "back")
    dp.callback_query.register(add_consumables.await_adding_account, F.data == "instagram")
    dp.callback_query.register(add_consumables.await_adding_account, F.data == "discord")
    dp.callback_query.register(add_consumables.await_adding_account, F.data == "telegram")
    dp.callback_query.register(add_consumables.await_adding_account, F.data == "twitter")
    dp.message.register(add_proxy.add_user_proxy, add_proxy.AdminProxyInput.waiting_for_user_input)
    dp.message.register(add_consumables.add_account_by_type, add_consumables.AdminAccountInput.waiting_for_user_input)
    dp.message.register(give_access.give_access_by_chatid, give_access.AdminGiveAccess.waiting_for_user_input)
    dp.message.register(get_proxy.get_country, get_proxy.WorkerProxyInput.waiting_for_user_input)
    dp.callback_query.register(get_proxy.get_user_proxy, get_proxy.WorkerProxyInput.waiting_for_user_input)
    dp.message.register(get_consumables.get_account_type, get_consumables.WorkerAccountInput.waiting_for_user_input)
    dp.message.register(get_balance.get_balance_amount, get_balance.WorkerBalanceInput.waiting_for_card_input)
    dp.message.register(get_balance.get_balance_approval, get_balance.WorkerBalanceInput.waiting_for_balance_input)
    dp.message.register(get_ticket.send_ticket, get_ticket.WorkerTicketInput.waiting_for_user_input)
    dp.message.register(chat_gpt.send_ticket, chat_gpt.WorkerGPTInput.waiting_for_user_input)
    dp.message.register(check_twitter_verif.get_responce, check_twitter_verif.WorkerTwitterInput.waiting_for_user_input)
    dp.message.register(main_start.standart_handler)