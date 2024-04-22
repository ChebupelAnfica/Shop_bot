from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import keyboards.default.main_menu as kb
from database.requests import get_product
from aiogram import Bot, Dispatcher, types
from config import TOKEN
from aiogram.exceptions import TelegramBadRequest

router = Router()
dp = Dispatcher()
bot = Bot(token=TOKEN)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в магазин!", reply_markup=kb.main)


@dp.message(F.text == "Каталог")
async def catalog(message: Message):
    await message.answer("Выберите вариант из каталога:", reply_markup=await kb.categories())


@dp.message(F.text == "Информация покупателям")
async def contact(message: Message):
    await message.answer(f'Контакты: 8(800)555-35-35\n'
                         'Доставка через сервис Яндекс: \n1.Доставка экспересс в течение 2 часов за 999 рублей.\n'
                         '2. В пункт выдачи в течении 2х дней или курьером за 250р\n'
                         'Приобрести понравившееся вам товары вы можете здесь: \nhttps://www.dns-shop.ru/'

                         )


@dp.callback_query(F.data.startswith('category_'))
async def category_selected(callback: CallbackQuery):
    category_id = callback.data.split("_")[1]
    await callback.message.answer(f'Товары по выбранной категории:', reply_markup=await kb.products(category_id))
    await callback.answer("")


@dp.callback_query(F.data.startswith('product_'))
async def product_selected(callback: CallbackQuery):
    product_id = callback.data.split("_")[1]
    product = await get_product(product_id=product_id)
    try:
        await bot.send_photo(callback.from_user.id,
                             f'{product.img}',  # add img to db
                             caption=f'<b>{product_id}</b>\n\n{product.description}\n\nЦена: {product.price}₽',
                             parse_mode='HTML')
    except:
        pass
    await callback.answer(f"Вы выбрали {product.name}")


@dp.message(F.content_type.in_({'photo', 'video'}))
async def echo_files(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, message.photo[0].file_id)
    except:
        await bot.send_message(message.from_user.id, message.video.file_id)
    return


@dp.message(CommandStart())
async def cmd_clear(message: Message, bot: Bot) -> None:
    try:
        for i in range(message.message_id, 1, -1):
            await bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest as ex:
        if ex.message == "Bad Request: message to delete not found":
            print("Все сообщения удалены")
