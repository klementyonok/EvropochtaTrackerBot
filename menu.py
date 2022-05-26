from telebot import types


def keyboard_menu(level):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if level == "menu":
        btn_track_add = types.KeyboardButton("➕ Добавить")
        btn_track_info = types.KeyboardButton("⚙ Управлять")
        markup.add(btn_track_add, btn_track_info)
    if level == "cancel":
        btn_track_cancel = types.KeyboardButton("⛔ Отменить")
        markup.add(btn_track_cancel)
    return markup
