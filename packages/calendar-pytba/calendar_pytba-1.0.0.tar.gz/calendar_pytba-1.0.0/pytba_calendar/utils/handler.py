import datetime

from telebot import TeleBot, types

from pytba_calendar import Calendar
from pytba_calendar.utils import text
from pytba_calendar.utils.types import CalendarLanguage, CallBackData


def _extract_month_year(data: str) -> list:
    return [int(_) for _ in data.split(":")[1:3]]


def callback_handler(bot: TeleBot, language: str = CalendarLanguage.EN):
    calendar = Calendar(language)

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith(CallBackData.LIST_MONTHS)
    )
    def list_months_call(call: types.CallbackQuery) -> None:
        year = int(call.data.split(":")[1])
        markup = calendar.get_list_months(year)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.id, reply_markup=markup
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith(CallBackData.SELECTED_MONTH)
    )
    def selected_month_call(call: types.CallbackQuery) -> None:
        month, year = _extract_month_year(call.data)
        date = datetime.date(year, month, 1)
        markup = calendar.get_calendar(date)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.id, reply_markup=markup
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith(CallBackData.LIST_YEARS)
    )
    def list_years_call(call: types.CallbackQuery) -> None:
        month, year = _extract_month_year(call.data)
        markup = calendar.get_list_years(month, year)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.id, reply_markup=markup
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith(CallBackData.PREVIOUS_YEARS)
    )
    def previous_years_call(call: types.CallbackQuery) -> None:
        month, year = _extract_month_year(call.data)
        year = year - 9
        markup = calendar.get_list_years(month, year)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.id, reply_markup=markup
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith(CallBackData.NEXT_YEARS)
    )
    def next_years_call(call: types.CallbackQuery) -> None:
        month, year = _extract_month_year(call.data)
        year = year + 9
        markup = calendar.get_list_years(month, year)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.id, reply_markup=markup
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith(CallBackData.SELECTED_YEAR)
    )
    def selected_year_call(call: types.CallbackQuery) -> None:
        month, year = _extract_month_year(call.data)
        date = datetime.date(year, month, 1)
        markup = calendar.get_calendar(date)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.id, reply_markup=markup
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith(CallBackData.FULL_WEEKDAY_NAME)
    )
    def full_weekday_name_call(call: types.CallbackQuery) -> None:
        weekday = int(call.data.split(":")[1])
        weekday_name = text.WEEK_DAYS_NAMES.get(language).get(weekday)
        bot.answer_callback_query(call.id, weekday_name)

    @bot.callback_query_handler(
        func=lambda call: call.data == CallBackData.EMPTY_WEEKDAY
    )
    def empty_weekday_call(call: types.CallbackQuery) -> None:
        bot.answer_callback_query(call.id, " ")

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith(CallBackData.FLIP_CALENDAR)
    )
    def flip_calendar_call(call: types.CallbackQuery) -> None:
        month, year = _extract_month_year(call.data)
        date = datetime.date(year, month, 1)
        markup = calendar.get_calendar(date)
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.id, reply_markup=markup
        )
