from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
import ujson

with open('data.json', 'r', encoding='utf-8') as config_file:
    data = ujson.load(config_file)
subjects = data['subjects']

# Клавиатура для ученика
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text='Предметы 📚'),
        KeyboardButton(text='Отправить ДЗ 📝')]],
    resize_keyboard=True,
    input_field_placeholder="Выберете действие...",
    selective=True)

# Клавиатура для учителя
teacher_main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text='Добавить лекцию'),
        KeyboardButton(text='Удалить лекцию')]],
    resize_keyboard=True,
    input_field_placeholder="Выберете действие...",
    selective=True)

# Клавиатура для ученика с выбором предметов
subjects_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Назад 🎒')],
    *[[KeyboardButton(text=item) for item in subjects.keys()]]],
    resize_keyboard=True,
    input_field_placeholder="Выберете предмет...",
    selective=True)

editing = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Закончить ✔')]],
    resize_keyboard=True,
    input_field_placeholder="Вставьте лекцию...",
    one_time_keyboard=True,
    selective=True)

send_photo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Завершить', callback_data='done')]
])

# Метод для ученика, возвращающий Inline клавиатуру с темами
def generate_themes_keyboard(sub: str):
    result_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🎒 Главное меню 🎒', callback_data='to_main')],
        *[[InlineKeyboardButton(text=theme, callback_data=f'{sub}\\{theme}')] for theme in subjects[sub].keys()]])
    return result_keyboard
