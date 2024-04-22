from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardButton, InlineKeyboardMarkup, \
    ShippingOption, ShippingQuery


keyboards =InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Оплатить заказ',
            pay=True
        ),
        InlineKeyboardButton(
            text='link',
            url='https://ya.ru/'
        ),
    ]
])


BY_SHIPPING = ShippingOption(
    id='by',
    title='Доставка в Беларусь',
    prices=[
        LabeledPrice(
            label="Доставка Белпочтой",
            amount=500
        )
    ]
)
RU_SHIPPING = ShippingOption(
    id='ru',
    title='Доставка в Россию',
    prices=[
        LabeledPrice(
            label="Доставка почтой России",
            amount=1000
        )
    ]
)

CITIES_SHIPPING = ShippingOption(
    id='capitals',
    title="Быстрая доставка по городу",
    prices=[
        LabeledPrice(
            label="Доставка курьером",
            amount=2000
        )
    ]
)

async def shipping_check(shipping_query: ShippingQuery, bot: Bot):
    shipping_option = []
    coutries = ['BY', 'RU']
    if shipping_query.shipping_address.country_code not in coutries:
        return await bot.answer_shipping_query(shipping_query.id, ok=False,
                                               error_message='Мы не доставляем в вашу страну')
    if shipping_query.shipping_address.country_code == 'BY':
        shipping_option.append(BY_SHIPPING)

    if shipping_query.shipping_address.country_code == 'RU':
        shipping_option.append(RU_SHIPPING)

    cities = ["Москва", 'Минск']
    if shipping_query.shipping_address.city in cities:
        shipping_option.append(CITIES_SHIPPING)

    await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_option)


async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Покупка через Telegram Bot',
        description="Приём оплаты",
        payload='Payment thought a bot',
        provider_token="381764678:TEST:76451",
        currency="rub",
        prices=[
            LabeledPrice(
                label="Доступ к секретной информации",
                amount=99000
            ),
            LabeledPrice(
                label="НДС",
                amount=20000
            ),
            LabeledPrice(
                label="Скидка",
                amount=-20000
            ),
            LabeledPrice(
                label="Бонус",
                amount=-40000
            )
        ],
        max_tip_amount=5000,
        suggested_tip_amounts=[1000, 2000, 3000, 4000],
        start_parameter="Chebup",
        provider_data=None,
        photo_url='https://moto-express.org/upload/iblock/796/7963d1f182030d757266025cc63140ec.jpg',
        photo_size=100,
        photo_width=800,
        photo_height=400,
        need_name=False,
        need_phone_number=False,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=True,
        disable_notification=True,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=keyboards,
        request_timeout=15
    )

async def pre_check_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

async def successful_payment(message: Message):
    msg = f'Спасибо за оплату {message.successful_payment.total_amount // 100} {message.successful_payment.currency}.'
    await message.answer(msg)