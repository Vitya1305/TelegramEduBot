import asyncio
import ujson

from aiogram import Bot, F, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InputMediaPhoto

import keyboards

with open('data.json', 'r', encoding='utf-8') as config_file:
    data = ujson.load(config_file)
    config_file.close()
teachers = data['teachers'].keys()
subjects = data['subjects']
themes = []
for sub in subjects.keys():
    for theme in subjects[sub]:
        themes.append(f'{sub}\\{theme}')

bot = Bot(token=data['token'])
dp = Dispatcher()

teachers_texting = {
}
teachers_img = {
}


# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print('Done!')
    await dp.start_polling(bot)


# Обработка на /start
@dp.message(CommandStart())
async def start(msg: types.Message):
    await msg.answer_sticker('CAACAgIAAxkBAANzZhJ4OrrcU5f5LOYlC7Huqac6Pg4AAtgPAAJI8mBLFfvE2nh0a5g0BA')

    if str(msg.from_user.id) in teachers:
        await msg.answer(data['start_text'], reply_markup=keyboards.teacher_main_keyboard)
    else:
        await msg.answer(data['start_text'], reply_markup=keyboards.main_keyboard)


# При нажатии на кнопку "Назад"; Выбор действия
@dp.message(F.text == 'Назад 🎒')
async def back(msg: types.Message):
    await msg.answer(data['start_text'], reply_markup=keyboards.main_keyboard)


# При нажатии на кнопку "Предметы"; Выбор предмета
@dp.message(F.text == 'Предметы 📚')
async def subjects(msg: types.Message):
    await msg.answer('Выберетe школьный предмет 🏫', reply_markup=keyboards.subjects_keyboard)


# Пользователь выбрал предмет; Выбор темы
@dp.message(F.text.in_(data['subjects'].keys()))
async def select_subject(msg: types.Message):
    await msg.answer('Выберетe тему 📖', reply_markup=keyboards.generate_themes_keyboard(msg.text))


# Написание лекции
@dp.message(F.text == 'Добавить лекцию')
async def subjects(msg: types.Message):
    if str(msg.from_user.id) not in teachers:
        return

    await msg.answer('Отправьте лекцию (можно по частям)', reply_markup=keyboards.editing)
    teachers_texting[msg.from_user.id] = ''
    teachers_img[msg.from_user.id] = []


# Приложения фотографий
@dp.message(F.text == 'Закончить ✔')
async def subjects(msg: types.Message):
    if str(msg.from_user.id) not in teachers:
        return

    await msg.answer('Отправьте фотографии', reply_markup=keyboards.send_photo)


@dp.message(F.photo)
async def on_photo(msg: types.Message):
    if msg.from_user.id not in teachers or teachers_img[msg.from_user.id] is None:
        return

    teachers_img[msg.from_user.id].append(msg.photo)
    await msg.answer('Если это все фото то нажмите завершить', reply_markup=keyboards.send_photo)


@dp.message(F.text)
async def all_msg(msg: types.Message):
    if msg.from_user.id not in teachers or teachers_texting[msg.from_user.id] is None:
        return

    await msg.answer('Если это всё, то нажмите кнопку закончить', reply_markup=keyboards.editing)


# При нажатии кнопки "Главное меню"
@dp.callback_query(F.data == 'to_main')
async def to_main(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(data['start_text'], reply_markup=keyboards.main_keyboard)


# Сохранение лекции         (Я не успел сделать!!!)         ;((((
@dp.callback_query(F.data == 'done')
async def to_main(callback: CallbackQuery):
    global data, teachers, subjects, themes
    await callback.answer()
    await callback.message.answer('Отлично!', reply_markup=keyboards.teacher_main_keyboard)

    info = {
        "subjects": {
            data['teachers'].get(str(callback.from_user.id)): {
            "theme1": {
                "text": teachers_texting[callback.from_user.id],
                "photos": teachers_img[callback.from_user.id]
                }
            }
        }
    }

    # data['subjects'][data['teachers'][str(callback.from_user.id)]]["theme1"] = {
    #     "text": teachers_texting[callback.from_user.id],
    #     "photos": teachers_img[callback.from_user.id]
    # }
    info = ujson.dumps(data)
    info = ujson.loads(str(info))

    with open('_data.json', 'w') as file:
        ujson.dump(info, file, indent=4)
        file.close()

    teachers_texting.pop(F.data.from_user.id)
    teachers_img.pop(F.data.from_user.id)
    with open('data.json', 'r', encoding='utf-8') as config_file:
        data = ujson.load(config_file)
        config_file.close()
    teachers = data['teachers'].keys()
    subjects = data['subjects']
    themes = []
    for sub in subjects.keys():
        for theme in subjects[sub]:
            themes.append(f'{sub}\\{theme}')


# При выборе темы; Отправка лекции
@dp.callback_query(F.data.in_(themes))
async def callbacks_on_select_theme(callback: CallbackQuery):
    await callback.answer()
    callback_data = callback.data.split('\\')
    subject = callback_data[0]
    theme = callback_data[1]

    if len(data['subjects'][subject][theme]['photos']) != 0:
        await callback.message.answer_media_group(
            [InputMediaPhoto(media=photo) for photo in data['subjects'][subject][theme]['photos']])
    await callback.message.answer(text=f'{theme}\n\n{data['subjects'][subject][theme]['text']}',
                                  reply_markup=keyboards.generate_themes_keyboard(subject))


if __name__ == '__main__':
    asyncio.run(main())
