import telebot
from telebot import types
import time
import config # Оплата

bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(commands=['start']) # Приветственное сообщение
def main_message(message):
    markup = types.InlineKeyboardMarkup()

    site_btn = types.InlineKeyboardButton("Сайт", url="https://xn--80akxbecx.tech/#rec981368811") # Ссылка на сайт
    servicelist_btn = types.InlineKeyboardButton("Подробнее об услугах", callback_data="servicelist_data")
    pricelist_btn = types.InlineKeyboardButton("Прайс-лист", callback_data="pricelist_data")

    markup.row(servicelist_btn)
    markup.row(pricelist_btn)
    markup.row(site_btn)

    bot.send_message(message.chat.id, f"""
👋 <b>Привет, {message.from_user.username}!</b>

🤖 <b>Я помощник цифрового агентство: Пантеон</b>
    
<b><u>Кто мы такие?</u></b>
    👤 Группа единомышленников, в виде компетентных, адекватных людей, желающих добиться успеха!
<b>Такие люди:</b>
    - Ценят свое и чужое время;
    - Выполняют работу качественно;
    - Не готовы распыляться на мелкие задачки, не приносящие хорошего заработка.
    
    📌 Услуги: 3D-моделирование | Монтаж | Сайты | Мини-приложения | Боты
    
    ⚡️<em>Без долгих переговоров и нелепых попыток содрать побольше денег, вы хотите получить качество, мы Вам его гарантируем! </em> 
    """, parse_mode="html", reply_markup=markup)

def message_list_services(chat_id): # Список сервисов
    markup_services = types.InlineKeyboardMarkup()

    one = types.InlineKeyboardButton("1️⃣", callback_data='one')
    two = types.InlineKeyboardButton("2️⃣", callback_data='two')
    markup_services.row(one, two)

    three = types.InlineKeyboardButton("3️⃣", callback_data='three')
    four = types.InlineKeyboardButton("4️⃣", callback_data='four')
    markup_services.row(three, four)

    five = types.InlineKeyboardButton("5️⃣", callback_data='five')
    six = types.InlineKeyboardButton("6️⃣", callback_data='six')
    markup_services.row(five, six)

    main_btn = types.InlineKeyboardButton("Главное", callback_data='main_data')
    markup_services.row(main_btn)

    bot.send_message(chat_id, """
    🔴 <b>Какие проблемы мы можем решить?</b>
    
<u>Список услуг</u>:
    1️⃣ 3D-анимации & 3D-модели
    2️⃣ Видеомонтаж & Motion-дизайн
    3️⃣ Разработка мини-приложений
    4️⃣ Разработка сайтов под ключ
    5️⃣ Боты для бизнеса
    6️⃣ Консультация
    
    ❗️<em>Чтобы узнать больше об услуге, нажми ниже на соответствующую кнопку</em> ️❗️
""", parse_mode='html', reply_markup=markup_services)

def callback_help_contacts(message):
    markup_service = types.InlineKeyboardMarkup()

    btn_back = types.InlineKeyboardButton("Вернуться ⬅️", callback_data='back')  # Кнопка возврата
    markup_service.row(btn_back)

    bot.send_message(message.chat.id, "Если возникли вопросы, пишите -> @Ibra0330", reply_markup=markup_service)

def callback_message_brief(message):
    markup_cancel = types.InlineKeyboardMarkup()
    cancel_btn = types.InlineKeyboardButton("Отмена", callback_data="cancel")
    markup_cancel.row(cancel_btn)

    bot.send_message(message.chat.id, "✏️ Напишите информацию или отправьте ссылкой", reply_markup=cancel_btn)
    bot.register_next_step_handler(message, process_buy_service)

def process_buy_service(message):
    brief = message.text

    bot.delete_message(message.chat.id, message.message_id - 1)

    markup_services = types.InlineKeyboardMarkup()

    one = types.InlineKeyboardButton("1️⃣", callback_data='Buy')
    two = types.InlineKeyboardButton("2️⃣", callback_data='Buy')
    markup_services.row(one, two)

    three = types.InlineKeyboardButton("3️⃣", callback_data='Buy')
    four = types.InlineKeyboardButton("4️⃣", callback_data='Buy')
    markup_services.row(three, four)

    five = types.InlineKeyboardButton("5️⃣", callback_data='Buy')
    six = types.InlineKeyboardButton("6️⃣", callback_data='Buy')
    markup_services.row(five, six)

    cancel_btn = types.InlineKeyboardButton("Отмена", callback_data="cancel")
    markup_services.row(cancel_btn)

    add_info(brief)

    bot.send_message(message.chat.id, "Выберете услугу")
    bot.send_message(message.chat.id, """
    
    <u>Список услуг</u>:
    1️⃣ 3D-анимации & 3D-модели
    2️⃣ Видеомонтаж & Motion-дизайн
    3️⃣ Разработка мини-приложений
    4️⃣ Разработка сайтов под ключ
    5️⃣ Боты для бизнеса
    6️⃣ Консультация
""", parse_mode='html', reply_markup=markup_services)

def add_info(brief):
    pass

def buy_menu(message):
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.delete_message(message.chat.id, message.message_id)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Выбрать другую", callback_data="change_service_for_buy"))

    bot.send_invoice(message.chat.id, 'Покупка услуги', "Покупки услуги компании", 'invoice_payload', config.PAYMENT_TOKEN, 'USD', [types.LabeledPrice('Покупка услуги', 10 * 100)])
    bot.send_message(message.chat.id, "Перепроверьте название услуги", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    markup_service = types.InlineKeyboardMarkup()

    pricelist_btn = types.InlineKeyboardButton("💵 Прайс-лист", callback_data="pricelist_data")
    markup_service.row(pricelist_btn)

    brief_btn = types.InlineKeyboardButton("📝 Заполнить бриф", callback_data="brief_data")
    markup_service.row(brief_btn)

    helpContact_btn = types.InlineKeyboardButton("⚙️ Поддержка", callback_data="helpContact_data")
    markup_service.row(helpContact_btn)

    btn_back = types.InlineKeyboardButton("Вернуться ⬅️", callback_data='back')  # Кнопка возврата
    markup_service.row(btn_back)

    if callback.data == "servicelist_data": # Список сервисов
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        message_list_services(callback.message.chat.id)

    elif callback.data == 'two':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, """
2️⃣ <b>Видеомонтаж & Motion-дизайн</b>

<b>Описание</b>:
    Это очень скрупулезная работа, при которой нужно учитывать много компонентов:
        ▪️Цветовая гамма
        ▪️Динамичность
        ▪️Крупность планов
        ▪️Саунд-дизайн
        ▪️3D-объекты
        ▪️Переходы
        ▪️Подбор футажей и т.д.
""", parse_mode='html', reply_markup=markup_service)

    elif callback.data == 'one':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, """
1️⃣ <b>3D-анимации & 3D-модели</b>

<b>Описание</b>:       
        Когда обычная графика уже не впечатляет — пора оживлять реальность. Мы создаём реалистичные и стилизованные 3D-модели: от продуктов до персонажей, от архитектурных форм до фантастических миров. А затем — вдохнём в них жизнь с помощью анимации.
Ваш продукт не просто покажут — его поймут, запомнят и захотят.
Подходит для рекламы, презентаций, метавселенных и не только.
                """, parse_mode='html', reply_markup=markup_service)

    elif callback.data == 'three':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, """
3️⃣ <b>Разработка мини-приложений</b>

<b>Описание</b>:       
    Мини-приложения наподобие «<em>Hamster Kombat, TapSwap</em>»
    С Вас концепция, с нас воплощение.
Наши разработки — это симбиоз креатива и холодной расчетливости,
но главное - баланс между ними,
а то результат не будет продавать,
мы об этом знаем, а теперь и Вы
Еще ни о одно сотрудничество не состоялось
с помощью телепатии, поэтому поделитесь проблемой
""", parse_mode='html', reply_markup=markup_service)

    elif callback.data == 'four':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, """
4️⃣ <b>Разработка сайтов под ключ</b>

<b>Описание</b>:
    Сочленение ума и креатива, нити безумия и здравомыслия, апогей вложения прикладной науки и психологических триггеров.
Если напишу так, то — звучит вульгарно и непонятно, мы за взрослый диалог
    Юзаем: языки программирования, конструктор сайтов. Создадим инструмент монетизации для Вашего бизнеса (услуги)
""", parse_mode='html', reply_markup=markup_service)

    elif callback.data == 'five':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, """
5️⃣ <b>Боты для бизнеса</b>

<b>Описание</b>:
    <em><b>Бот любой сложности для бизнеса. Он не спит, не берет больничный, не жалуется на работу
При необходимости интегрируем в Вашу систему под ключ.</b></em>
    За утечку данных можете не переживать, бот не собирает данные.
    Это <b>бот</b>, а не супер-ультра-мультиварка, с ним взаимодействовать гораздо проще.

<u>В чем польза Бота?</u>
    Можно много говорить о пользе , но это все абстракции. Мы предпочитаем реализм и прагматизм. Сообщите нам свой запрос и от него будем отталкиваться.
""", parse_mode='html', reply_markup=markup_service)

    elif callback.data == 'six':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, """
6️⃣ <b>Консультация</b>

<b>Описание</b>:
    У нас есть: помощь зала, звонок другу , последнее желание. 
Только не обращайтесь по поводу грыжи Шморля, завоевания мира и проблем в отношениях, хотя - не проблема, могу и по этому поводу проконсультировать.

    В общем, все очень просто: у Вас есть проблема,
а у меня есть решение. Если у меня нет решения,
то порекомендую обратиться к другому специалисту,
потому что ценю Ваше время!
""", parse_mode='html', reply_markup=markup_service)

    elif callback.data == 'back': # Вернуться к списку услуг
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        message_list_services(callback.message.chat.id)

    elif callback.data == "cancel":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

        message_list_services(callback.message.chat.id)

    elif callback.data == "pricelist_data":
        bot.send_message(callback.message.chat.id, "Тут должен отправиться файл, но его пока нет :)")
        time.sleep(3.0)
        bot.delete_message(callback.message.chat.id, callback.message.message_id + 1)

    elif callback.data == "brief_data":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        callback_message_brief(callback.message)

    elif callback.data == "helpContact_data":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        callback_help_contacts(callback.message)


    elif callback.data == "Buy":
        buy_menu(callback.message)

    elif callback.data == "change_service_for_buy":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)

        callback_message_brief(callback.message)

    elif callback.data == "main_data":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        main_message(callback.message)

@bot.message_handler() # Обработчик неизвестного текста
def unknown_message(message):
    bot.send_message(message.chat.id, "❌ Неизвестная команда, введите /start")

bot.polling(none_stop=True) # Программа работала постоянно