# -*- coding: utf-8 -*-
# bot.py
# Telegram do'kon-bot. aiogram 3.x. ODDIY POLLING rejimida ishlaydi.

import os
import json
import logging
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===========================================================================
# 1) SOZLAMALAR — TOKEN VA KONTAKT MA'LUMOTLARI (ЖОЙИГА ҚЎЙИЛДИ)
# ===========================================================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = "7391248864"

# Хизмат кўрсатиш ҳаволаси (ўзингизнинг username'ингизни ёзиб қўйишингиз мумкин)
ADMIN_USERNAME = "username_shu_yerga"  
ADMIN_CONTACT_LINK = f"https://t.me/{ADMIN_USERNAME}"

PRODUCTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.json")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# ===========================================================================
# 2) ТАРЖИМАЛАР (ЎЗБЕК ТИЛИ КРИЛЛЧАГА ЎЗГАРТИРИЛДИ)
# ===========================================================================
LANG_BUTTONS = {
    "🇺🇿 Ўзбекча": "uz",
    "🇷🇺 Русский": "ru",
    "🇬🇧 English": "en",
    "🇺🇦 Українська": "uk",
    "🇪🇸 Español": "es",
    "🇧🇷🇵🇹 Português": "pt",
    "🇩🇪 Deutsch": "de",
    "🇮🇹 Italiano": "it",
    "🇫🇷 Français": "fr",
    "🇹🇷 Türkçe": "tr",
    "🇮🇱 עברית": "he",
    "🇸🇦 العربية": "ar",
    "🇮🇷 زبان فارسی": "fa",
    "🇨🇳 中國人": "zh",
    "🇮🇩 Bahasa Indonesia": "id",
    "🇸🇪 Svenska": "sv",
    "🇲🇾 Melayu": "ms",
    "🇳🇱 Nederlands": "nl",
    "🇮🇳 हिंदी": "hi",
    "🇰🇷 한국인": "ko",
    "🇻🇳 Tiếng Việt": "vi",
}

TEXTS = {
 'uz': {
        'choose_lang': 'Тилни танланг:',
        'lang_set': "Тил танланди: Ўзбекча ✅",
        'main_menu': "Асосий меню. Бўлимни танланг:",
        'back': '⬅️ Орқага',
        'to_main': '🏠 Бош меню',
        'choose_product': 'Маҳсулотни танланг:',
        'price': 'Нарх',
        'description': 'Тавсиф',
        'buy_btn': '🛒 Сотиб олиш',
        'contact_btn': "📞 Боғланиш",
        'order_sent': "✅ Сўровингиз қабул қилинди!\n\n"
                      "Маҳсулот: {name}\n"
                      "Нарх: {price}\n\n"
                      "Қуйидаги тугма орқали биз билан тўғридан-тўғри боғланишингиз мумкин.",
        'contact_link_text': '👉 Алоқа учун босинг',
        'not_found': 'Илтимос, менюдаги тугмалардан бирини танланг.',
        'delivery_name': '🚚 Етказиб бериш хизмати',
        'delivery_info': "Биз маҳсулотни манзилингизга етказиб берамиз.\n\n"
                         "Буюртма бериш учун пастдаги тугмани босинг, операторимиз сиз билан боғланади.",
        'categories_label': 'БЎЛИМЛАР',
        'categories': {
                       'electronics': '📱 Электроника',
                       'auto': '🚗 Машина',
                       'home': "🏠 Уй-хўжалик",
                       'fruits': '🍎 Мевалар',
                       'vegetables': '🥦 Сабзавотлар',
                       'delivery': '🚚 Етказиб бериш'
        },
        'empty_category': "📭 Ҳозирча бу бўлимда маҳсулот йўқ.",
        'add_product_btn': "➕ Маҳсулот қўшиш"
 },
 'ru': {'choose_lang': 'Выберите язык:',
        'lang_set': 'Язык выбран: Русский ✅',
        'main_menu': 'Главное меню. Выберите раздел:',
        'back': '⬅️ Назад',
        'to_main': '🏠 Главное меню',
        'choose_product': 'Выберите товар:',
        'price': 'Цена',
        'description': 'Описание',
        'buy_btn': '🛒 Купить',
        'contact_btn': '📞 Связаться',
        'order_sent': '✅ Ваш запрос принят!\n\nТовар: {name}\nЦена: {price}\n\nВы можете связаться с нами напрямую через кнопку ниже.',
        'contact_link_text': '👉 Нажмите для связи',
        'not_found': 'Пожалуйста, выберите кнопку из меню.',
        'delivery_name': '🚚 Служба доставки',
        'delivery_info': 'Мы доставим товар по вашему адресу.\n\nЧтобы оформить заказ, нажмите кнопку ниже — наш оператор свяжется с вами.',
        'categories_label': 'РАЗДЕЛЫ',
        'categories': {'electronics': '📱 Электроника', 'auto': '🚗 Авто', 'home': '🏠 Хозтовары', 'fruits': '🍎 Фрукты', 'vegetables': '🥦 Овощи', 'delivery': '🚚 Доставка'},
        'empty_category': '📭 В этом разделе пока нет товаров.',
        'add_product_btn': "➕ Добавить товар"},
 'en': {'choose_lang': 'Choose your language:',
        'lang_set': 'Language set: English ✅',
        'main_menu': 'Main menu. Choose a section:',
        'back': '⬅️ Back',
        'to_main': '🏠 Main menu',
        'choose_product': 'Choose a product:',
        'price': 'Price',
        'description': 'Description',
        'buy_btn': '🛒 Buy',
        'contact_btn': '📞 Contact us',
        'order_sent': '✅ Your request has been received!\n\nProduct: {name}\nPrice: {price}\n\nYou can contact us directly using the button below.',
        'contact_link_text': '👉 Tap to contact',
        'not_found': 'Please choose a button from the menu.',
        'delivery_name': '🚚 Delivery service',
        'delivery_info': 'We deliver the product to your address.\n\nTo place an order, tap the button below — our operator will contact you.',
        'categories_label': 'SECTIONS',
        'categories': {'electronics': '📱 Electronics', 'auto': '🚗 Auto', 'home': '🏠 Household', 'fruits': '🍎 Fruits', 'vegetables': '🥦 Vegetables', 'delivery': '🚚 Delivery'},
        'empty_category': '📭 No products in this section yet.',
        'add_product_btn': "➕ Add Product"},
 'uk': {'choose_lang': 'Виберіть мову:',
        'lang_set': 'Мову обрано: Українська ✅',
        'main_menu': 'Головне menu. Виберіть розділ:',
        'back': '⬅️ Назад',
        'to_main': '🏠 Головне меню',
        'choose_product': 'Виберіть товар:',
        'price': 'Ціна',
        'description': 'Опис',
        'buy_btn': '🛒 Купити',
        'contact_btn': "📞 Зв'язатися",
        'order_sent': '✅ Ваш запит прийнято!\n\nТовар: {name}\nЦіна: {price}\n\nВи можете зв`язатися з нами напряму через кнопку нижче.',
        'contact_link_text': "👉 Натисніть для зв'язку",
        'not_found': 'Будь ласка, виберіть кнопку з меню.',
        'delivery_name': '🚚 Служба доставки',
        'delivery_info': 'Ми доставимо товар за вашою адресою.\n\nЩоб оформити замовлення, натисніть кнопку ниже — наш оператор зв`яжеться з вами.',
        'categories_label': 'РОЗДІЛИ',
        'categories': {'electronics': '📱 Електроніка', 'auto': '🚗 Авто', 'home': '🏠 Товари для дому', 'fruits': '🍎 Фрукти', 'vegetables': '🥦 Овочі', 'delivery': '🚚 Доставка'},
        'empty_category': '📭 У цьому розділі поки немає товарів.',
        'add_product_btn': "➕ Додати товар"},
 'es': {'choose_lang': 'Elige tu idioma:',
        'lang_set': 'Idioma seleccionado: Español ✅',
        'main_menu': 'Menú principal. Elige una sección:',
        'back': '⬅️ Atrás',
        'to_main': '🏠 Menú principal',
        'choose_product': 'Elige un product:',
        'price': 'Precio',
        'description': 'Descripción',
        'buy_btn': '🛒 Comprar',
        'contact_btn': '📞 Contactar',
        'order_sent': '✅ ¡Su solicitud ha sido recibida!\n\nProducto: {name}\nPrecio: {price}\n\nPuede contactarnos directamente usando el botón de abajo.',
        'contact_link_text': '👉 Toque para contactar',
        'not_found': 'Por favor, elija un botón del menú.',
        'delivery_name': '🚚 Servicio de entrega',
        'delivery_info': 'Entregamos el producto en su dirección.\n\nPara hacer un pedido, toque el botón de abajo — nuestro operador se pondrá en contacto con usted.',
        'categories_label': 'SECCIONES',
        'categories': {'electronics': '📱 Electrónica', 'auto': '🚗 Auto', 'home': '🏠 Hogar', 'fruits': '🍎 Frutas', 'vegetables': '🥦 Verduras', 'delivery': '🚚 Entrega'},
        'empty_category': '📭 Todavía no hay productos en esta sección.',
        'add_product_btn': "➕ Agregar producto"},
 'pt': {'choose_lang': 'Escolha seu idioma:',
        'lang_set': 'Idioma selecionado: Português ✅',
        'main_menu': 'Menu principal. Escolha uma seção:',
        'back': '⬅️ Voltar',
        'to_main': '🏠 Menu principal',
        'choose_product': 'Escolha um produto:',
        'price': 'Preço',
        'description': 'Descrição',
        'buy_btn': '🛒 Comprar',
        'contact_btn': '📞 Contato',
        'order_sent': '✅ Seu pedido foi recebido!\n\nProduto: {name}\nPreço: {price}\n\nVocê pode entrar em contato conosco diretamente usando o botão abaixo.',
        'contact_link_text': '👉 Toque para contato',
        'not_found': 'Por favor, escolha um botão do menu.',
        'delivery_name': '🚚 Serviço de entrega',
        'delivery_info': 'Entregamos o produto no seu endereço.\n\nPara fazer um pedido, toque no botão abaixo — nosso operador entrará em contato.',
        'categories_label': 'SEÇÕES',
        'categories': {'electronics': '📱 Eletrônicos', 'auto': '🚗 Carros', 'home': '🏠 Casa', 'fruits': '🍎 Frutas', 'vegetables': '🥦 Vegetais', 'delivery': '🚚 Entrega'},
        'empty_category': '📭 Ainda não há produtos nesta seção.',
        'add_product_btn': "➕ Adicionar produto"},
 'de': {'choose_lang': 'Wählen Sie Ihre Sprache:',
        'lang_set': 'Sprache gewählt: Deutsch ✅',
        'main_menu': 'Hauptmenü. Wählen Sie einen Bereich:',
        'back': '⬅️ Zurück',
        'to_main': '🏠 Hauptmenü',
        'choose_product': 'Wählen Sie ein Produkt:',
        'price': 'Preis',
        'description': 'Beschreibung',
        'buy_btn': '🛒 Kaufen',
        'contact_btn': '📞 Kontakt',
        'order_sent': '✅ Ihre Anfrage wurde empfangen!\n\nProdukt: {name}\nPreis: {price}\n\nSie können uns direkt über die Schaltfläche unten kontaktieren.',
        'contact_link_text': '👉 Tippen Sie für Kontakt',
        'not_found': 'Bitte wählen Sie eine Schaltfläche aus dem Menü.',
        'delivery_name': '🚚 Lieferservice',
        'delivery_info': 'Wir liefern das Produkt an Ihre Adresse.\n\nUm zu bestellen, tippen Sie auf die Schaltfläche unten — unser Mitarbeiter wird sich mit Ihnen in Verbindung setzen.',
        'categories_label': 'BEREICHE',
        'categories': {'electronics': '📱 Elektronik', 'auto': '🚗 Auto', 'home': '🏠 Haushalt', 'fruits': '🍎 Obst', 'vegetables': '🥦 Gemüse', 'delivery': '🚚 Lieferung'},
        'empty_category': '📭 In diesem Bereich gibt es noch keine Produkte.',
        'add_product_btn': "➕ Produkt hinzufügen"},
 'it': {'choose_lang': 'Scegli la tua lingua:',
        'lang_set': 'Lingua selezionata: Italiano ✅',
        'main_menu': 'Menu principale. Scegli una sezione:',
        'back': '⬅️ Indietro',
        'to_main': '🏠 Menu principale',
        'choose_product': 'Scegli un prodotto:',
        'price': 'Prezzo',
        'description': 'Descrizione',
        'buy_btn': '🛒 Acquista',
        'contact_btn': '📞 Contattaci',
        'order_sent': '✅ La tua richiesta è stata ricevuta!\n\nProdotto: {name}\nPrezzo: {price}\n\nPuoi contattarci direttamente usando il pulsante qui sotto.',
        'contact_link_text': '👉 Tocca per contattare',
        'not_found': 'Si prega di scegliere un pulsante dal menu.',
        'delivery_name': '🚚 Servizio di consegna',
        'delivery_info': 'Consegniamo il produto al tuo indirizzo.\n\nPer effettuare un ordine, tocca il pulsante qui sotto — il nostro operatore ti contatterà.',
        'categories_label': 'SEZIONI',
        'categories': {'electronics': '📱 Elettronica', 'auto': '🚗 Auto', 'home': '🏠 Casa', 'fruits': '🍎 Frutta', 'vegetables': '🥦 Verdure', 'delivery': '🚚 Consegna'},
        'empty_category': '📭 Non ci sono ancora prodotti in questa sezione.',
        'add_product_btn': "➕ Aggiungi prodotto"},
 'fr': {'choose_lang': 'Choisissez votre langue:',
        'lang_set': 'Langue sélectionnée: Français ✅',
        'main_menu': 'Menu principal. Choisissez une section:',
        'back': '⬅️ Retour',
        'to_main': '🏠 Menu principal',
        'choose_product': 'Choisissez un produit:',
        'price': 'Prix',
        'description': 'Description',
        'buy_btn': '🛒 Acheter',
        'contact_btn': '📞 Contact',
        'order_sent': '✅ Votre demande a été reçue!\n\nProduit: {name}\nPrix: {price}\n\ Vous pouvez nous contacter directement via le bouton ci-dessous.',
        'contact_link_text': '👉 Appuyez pour contacter',
        'not_found': 'Veuillez choisir un bouton dans le menu.',
        'delivery_name': '🚚 Service de livraison',
        'delivery_info': 'Nous livrons le produit à votre adresse.\n\nPour passer une commande, appuyez sur le bouton ci-dessous — notre opérateur vous contactera.',
        'categories_label': 'SECTIONS',
        'categories': {'electronics': '📱 Électronique', 'auto': '🚗 Auto', 'home': '🏠 Maison', 'fruits': '🍎 Fruits', 'vegetables': '🥦 Légumes', 'delivery': '🚚 Livraison'},
        'empty_category': "📭 Il n'y a pas encore de produits dans cette section.",
        'add_product_btn': "➕ Ajouter un produit"},
 'tr': {'choose_lang': 'Dilinizi seçin:',
        'lang_set': 'Dil seçildi: Türkçe ✅',
        'main_menu': 'Ana menü. Bir bölüm seçin:',
        'back': '⬅️ Geri',
        'to_main': '🏠 Ana menü',
        'choose_product': 'Bir ürün seçin:',
        'price': 'Fiyat',
        'description': 'Açıklama',
        'buy_btn': '🛒 Satın al',
        'contact_btn': '📞 İletişim',
        'order_sent': '✅ Talebiniz alındı!\n\nÜrün: {name}\nFiyat: {price}\n\nAşağıdaki düğmeyi kullanarak doğrudan bizimle iletişime geçebilirsiniz.',
        'contact_link_text': '👉 İletişim için dokunun',
        'not_found': 'Lütfen menüden bir düğme seçin.',
        'delivery_name': '🚚 Teslimat hizmeti',
        'delivery_info': 'Ürünü adresinize teslim ediyoruz.\n\nSipariş vermek için aşağıdaki düğmeye dokunun — operatörümüz sizinle iletişime geçecek.',
        'categories_label': 'BÖLÜMLER',
        'categories': {'electronics': '📱 Elektronik', 'auto': '🚗 Araba', 'home': '🏠 Ev eşyaları', 'fruits': '🍎 Meyveler', 'vegetables': '🥦 Sebzeler', 'delivery': '🚚 Teslimat'},
        'empty_category': '📭 Bu bölümde henüz ürün yok.',
        'add_product_btn': "➕ Ürün Ekle"},
 'he': {'choose_lang': 'בחר את השפה שלך:',
        'lang_set': 'השפה נבחרه: עברית ✅',
        'main_menu': 'תפריט ראשי. בחר קטגוריה:',
        'back': '⬅️ חזרה',
        'to_main': '🏠 תפריט ראשי',
        'choose_product': 'בחר מוצר:',
        'price': 'מחיר',
        'description': 'תיאור',
        'buy_btn': '🛒 קנייה',
        'contact_btn': '📞 צור קשר',
        'order_sent': '✅ הבקשה שלך התקבله!\n\nמוצר: {name}\nמחיר: {price}\n\nתוکل ליצור איתנו קשר ישירות באמצעות הכפתור למטה.',
        'contact_link_text': '👉 הקש ליצירת קשר',
        'not_found': 'אנא בחר כפתור מהתפריต.',
        'delivery_name': '🚚 שירות משلوחים',
        'delivery_info': 'אנחנו מספקים את המוצר לכתובت שלך.\n\nכדי לבצע הזמנה, הקש पर הכפתור למטה — הנציג שלנו ייצור איתך קשר.',
        'categories_label': 'קטגוריות',
        'categories': {'electronics': '📱 אלקטרוניקה', 'auto': '🚗 רכב', 'home': '🏠 לבית', 'fruits': '🍎 פירות', 'vegetables': '🥦 ירקות', 'delivery': '🚚 משלוח'},
        'empty_category': '📭 אין עדיין מוצרים בקטגוריה זו.',
        'add_product_btn': "➕ הוסף מוצר"},
 'ar': {'choose_lang': 'اختر لغتك:',
        'lang_set': 'تم اختيار اللغة: العربية ✅',
        'main_menu': 'القائمة الرئيسية. اختر قسماً:',
        'back': '⬅️ رجوع',
        'to_main': '🏠 القائمة الرئيسية',
        'choose_product': 'اختر منتجاً:',
        'price': 'السعر',
        'description': 'الوصف',
        'buy_btn': '🛒 شراء',
        'contact_btn': '📞 تواصل معنا',
        'order_sent': '✅ تم استلام طلبك!\n\nالمنتج: {name}\nالسعر: {price}\n\nيمكنك التواصل معنا مباشرة عبر الزر أدناه.',
        'contact_link_text': '👉 اضغط للتواصل',
        'not_found': 'الرجاء اختيار زر من القائمة.',
        'delivery_name': '🚚 خدمة التوصيل',
        'delivery_info': 'نقوم بتوصيل المنتج إلى عنوانك.\n\nلتقديم الطلب، اضغط على الزر أدناه — سيتواصل معك موظفنا.',
        'categories_label': 'الأقسام',
        'categories': {'electronics': '📱 إلكترونيات', 'auto': '🚗 سيارات', 'home': '🏠 المنزل', 'fruits': '🍎 فواكه', 'vegetables': '🥦 خضروات', 'delivery': '🚚 التوصيل'},
        'empty_category': '📭 لا توجد منتجات في هذا القسم بعد.',
        'add_product_btn': "➕ إضافة منتج"},
 'fa': {'choose_lang': 'زبان خود را انتخاب کنید:',
        'lang_set': 'زبان انتخاب شد: فارسی ✅',
        'main_menu': 'منوی اصلی. یک بخش را انتخاب کنید:',
        'back': '⬅️ بازگشت',
        'to_main': '🏠 منوی اصلی',
        'choose_product': 'یک محصول را انتخاب کنید:',
        'price': 'قیمت',
        'description': 'توضیحات',
        'buy_btn': '🛒 خرید',
        'contact_btn': '📞 تماس با ما',
        'order_sent': '✅ درخواست شما دریافت شد!\n\nمحصول: {name}\nقیمت: {price}\n\nمی‌آموزید مستقیماً از طریق دکمه زیر با ما تماس بگیرید.',
        'contact_link_text': '👉 برای تماس ضربه بزنید',
        'not_found': 'لطفاً یک دکمه از منو انتخاب کنید.',
        'delivery_name': '🚚 خدمات تحویل',
        'delivery_info': 'ما محصول را به آدرس شما تحویل می‌دهیم.\n\nبرای ثبت سفارش، دکمه زیر را لمس کنید — اپراتور ما با شما تماس خواهد گرفت.',
        'categories_label': 'بخش‌ها',
        'categories': {'electronics': '📱 لوازم الکترونیکی', 'auto': '🚗 خودرو', 'home': '🏠 خانه و آشپزخانه', 'fruits': '🍎 میوه‌ها', 'vegetables': '🥦 سبزیجات', 'delivery': '🚚 تحویل'},
        'empty_category': '📭 هنوز محصولی در این بخش وجود ندارد.',
        'add_product_btn': "➕ افزودن محصول"},
 'zh': {'choose_lang': '选择您的语言：',
        'lang_set': '语言已选择：中文 ✅',
        'main_menu': '主菜单。请选择一个类别：',
        'back': '⬅️ 返回',
        'to_main': '🏠 主菜单',
        'choose_product': '请选择产品：',
        'price': '价格',
        'description': '描述',
        'buy_btn': '🛒 购买',
        'contact_btn': '📞 联系我们',
        'order_sent': '✅ 您的请求已收到！\n\n产品：{name}\n价格：{price}\n\n您可以通过下面的按钮直接联系我们。',
        'contact_link_text': '👉 点击联系',
        'not_found': '请从菜单中选择一个按钮。',
        'delivery_name': '🚚 送货服务',
        'delivery_info': '我们将产品送到您的地址。\n\n要下订单，请点击下面的按钮——我们的客服将与您联系。',
        'categories_label': '类别',
        'categories': {'electronics': '📱 电子产品', 'auto': '🚗 汽车', 'home': '🏠 家居用品', 'fruits': '🍎 水果', 'vegetables': '🥦 蔬菜', 'delivery': '🚚 配送'},
        'empty_category': '📭 此分类暂无产品。',
        'add_product_btn': "➕ 添加产品"},
 'id': {'choose_lang': 'Pilih bahasa Anda:',
        'lang_set': 'Bahasa dipilih: Bahasa Indonesia ✅',
        'main_menu': 'Menu utama. Pilih bagian:',
        'back': '⬅️ Kembali',
        'to_main': '🏠 Menu utama',
        'choose_product': 'Pilih produk:',
        'price': 'Harga',
        'description': 'Deskripsi',
        'buy_btn': '🛒 Beli',
        'contact_btn': '📞 Hubungi kami',
        'order_sent': '✅ Permintaan Anda telah diterima!\n\nProduk: {name}\nHarga: {price}\n\nAnda dapat menghubungi kami langsung melalui tombol di bawah.',
        'contact_link_text': '👉 Ketuk untuk menghubungi',
        'not_found': 'Silakan pilih tombol dari menu.',
        'delivery_name': '🚚 Layanan pengiriman',
        'delivery_info': 'Kami mengirimkan produk ke alamat Anda.\n\nUntuk memesan, ketuk tombol di bawah — operator kami akan menghubungi Anda.',
        'categories_label': 'BAGIAN',
        'categories': {'electronics': '📱 Elektronik', 'auto': '🚗 Mobil', 'home': '🏠 Rumah Tangga', 'fruits': '🍎 Buah-buahan', 'vegetables': '🥦 Sayuran', 'delivery': '🚚 Pengiriman'},
        'empty_category': '📭 Belum ada produk di bagian ini.',
        'add_product_btn': "➕ Tambah Produk"},
 'sv': {'choose_lang': 'Välj ditt språk:',
        'lang_set': 'Språk valt: Svenska ✅',
        'main_menu': 'Huvudmeny. Välj en kategori:',
        'back': '⬅️ Tillbaka',
        'to_main': '🏠 Huvudmeny',
        'choose_product': 'Välj en produkt:',
        'price': 'Pris',
        'description': 'Beskrivning',
        'buy_btn': '🛒 Köp',
        'contact_btn': '📞 Kontakta oss',
        'order_sent': '✅ Din förfrågan har mottagits!\n\nProdukt: {name}\nPris: {price}\n\nDu kan kontakta oss direkt via knappen nedan.',
        'contact_link_text': '👉 Tryck för att kontakta',
        'not_found': 'Vänligen välj en knapp från menyn.',
        'delivery_name': '🚚 Leveranstjänst',
        'delivery_info': 'Vi levererar produkten till din adress.\n\nFör att beställa, tryck på knappen nedan — vår operatör kontaktar dig.',
        'categories_label': 'KATEGORIER',
        'categories': {'electronics': '📱 Elektronik', 'auto': '🚗 Bil', 'home': '🏠 Hushåll', 'fruits': '🍎 Frukt', 'vegetables': '🥦 Grönsaker', 'delivery': '🚚 Leverans'},
        'empty_category': '📭 Det finns inga produkter i den här kategorin än.',
        'add_product_btn': "➕ Lägg till produkt"},
 'ms': {'choose_lang': 'Pilih bahasa anda:',
        'lang_set': 'Bahasa dipilih: Melayu ✅',
        'main_menu': 'Menu utama. Pilih bahagian:',
        'back': '⬅️ Kembali',
        'to_main': '🏠 Menu utama',
        'choose_product': 'Pilih produk:',
        'price': 'Harga',
        'description': 'Penerangan',
        'buy_btn': '🛒 Beli',
        'contact_btn': '📞 Hubungi kami',
        'order_sent': '✅ Permintaan anda telah diterima!\n\nProduk: {name}\nHarga: {price}\n\nAnda boleh menghubungi kami terus melalui butang di bawah.',
        'contact_link_text': '👉 Ketik untuk hubungi',
        'not_found': 'Sila pilih butang daripada menu.',
        'delivery_name': '🚚 Perkhidmatan penghantaran',
        'delivery_info': 'Kami menghantar produk ke alamat anda.\n\nUntuk membuat pesanan, ketik butang di bawah — operator kami akan menghubungi anda.',
        'categories_label': 'BAHAGIAN',
        'categories': {'electronics': '📱 Elektronik', 'auto': '🚗 Kereta', 'home': '🏠 Rumah Tangga', 'fruits': '🍎 Buah-buahan', 'vegetables': '🥦 Sayur-sayuran', 'delivery': '🚚 Penghantaran'},
        'empty_category': '📭 Belum ada produk dalam bahagian ini.',
        'add_product_btn': "➕ Tambah Produk"},
 'nl': {'choose_lang': 'Kies uw taal:',
        'lang_set': 'Taal gekozen: Nederlands ✅',
        'main_menu': 'Hoofdmenu. Kies een categorie:',
        'back': '⬅️ Terug',
        'to_main': '🏠 Hoofdmenu',
        'choose_product': 'Kies een product:',
        'price': 'Prijs',
        'description': 'Beschrijving',
        'buy_btn': '🛒 Kopen',
        'contact_btn': '📞 Contact',
        'order_sent': '✅ Uw aanvraag is ontvangen!\n\nProduct: {name}\nPrijs: {price}\n\nU kunt rechtstreeks contact met ons opnemen via de knop hieronder.',
        'contact_link_text': '👉 Tik om contact op te nemen',
        'not_found': 'Kies een knop uit het menu.',
        'delivery_name': '🚚 Bezorgservice',
        'delivery_info': 'Wij bezorgen het product op uw adres.\n\nOm te bestellen, tik op de knop hieronder — onze medewerker neemt contact met u op.',
        'categories_label': 'CATEGORIEËN',
        'categories': {'electronics': '📱 Elektronica', 'auto': '🚗 Auto', 'home': '🏠 Huishouden', 'fruits': '🍎 Fruit', 'vegetables': '🥦 Groenten', 'delivery': '🚚 Bezorging'},
        'empty_category': '📭 Er zijn nog geen producten in deze categorie.',
        'add_product_btn': "➕ Product toevoegen"},
 'hi': {'choose_lang': 'अपनी भाषा चुनें:',
        'lang_set': 'भाषा चयनित: हिंदी ✅',
        'main_menu': 'मुख्य मेनू। एक श्रेणी चुनें:',
        'back': '⬅️ वापस',
        'to_main': '🏠 मुख्य मेनू',
        'choose_product': 'एक उत्पाद चुनें:',
        'price': 'कीमत',
        'description': 'विवरण',
        'buy_btn': '🛒 खरीदें',
        'contact_btn': '📞 संपर्क करें',
        'order_sent': '✅ आपका अनुरोध प्राप्त हो गया है!\n\nउत्पाद: {name}\nकीमत: {price}\n\nआप नीचे दिए गए बटन के माध्यम से सीधे हमसे संपर्क कर सकते हैं।',
        'contact_link_text': '👉 संपर्क के लिए टैप करें',
        'not_found': 'कृपया मेनू से एक बटन चुनें।',
        'delivery_name': '🚚 डिलीवरी सेवा',
        'delivery_info': 'हम उत्पाद को आपके पते पर पहुंचाते हैं।\n\nऑर्डर करने के लिए, नीचे दिए गए बटन को टैप करें — हमारा ऑपरेटर आपसे संपर्क करेगा।',
        'categories_label': 'श्रेणियाँ',
        'categories': {'electronics': '📱 इलेक्ट्रॉनिक्स', 'auto': '🚗 कार', 'home': '🏠 घरेलू सामान', 'fruits': '🍎 फल', 'vegetables': '🥦 सब्जियां', 'delivery': '🚚 डिलीवरी'},
        'empty_category': '📭 इस श्रेणी में अभी तक कोई उत्पाद नहीं है।',
        'add_product_btn': "➕ उत्पाद जोड़ें"},
 'ko': {'choose_lang': '언어를 선택하세요:',
        'lang_set': '언어 선택됨: 한국어 ✅',
        'main_menu': '메인 메뉴. 카테고리를 선택하세요:',
        'back': '⬅️ 뒤로',
        'to_main': '🏠 메인 메뉴',
        'choose_product': '상품을 선택하세요:',
        'price': '가격',
        'description': '설명',
        'buy_btn': '🛒 구매',
        'contact_btn': '📞 문의하기',
        'order_sent': '✅ 요청이 접수되었습니다!\n\n상품: {name}\n가격: {price}\n\n아래 버튼을 통해 직접 문의하실 수 있습니다.',
        'contact_link_text': '👉 문의하려면 탭하세요',
        'not_found': '메뉴에서 버튼을 선택해 주세요.',
        'delivery_name': '🚚 배송 서비스',
        'delivery_info': '상품을 귀하의 주소로 배송해 드립니다.\n\n주문하려면 아래 버튼을 탭하세요 — 담당자가 연락드릴 것입니다.',
        'categories_label': '카테고리',
        'categories': {'electronics': '📱 전자제품', 'auto': '🚗 자동차', 'home': '🏠 생활용품', 'fruits': '🍎 과일', 'vegetables': '🥦 채소', 'delivery': '🚚 배송'},
        'empty_category': '📭 아직 이 카테고리에 상품이 없습니다.',
        'add_product_btn': "➕ 상품 추가"},
 'vi': {'choose_lang': 'Chọn ngôn ngữ của bạn:',
        'lang_set': 'Đã chọn ngôn ngữ: Tiếng Việt ✅',
        'main_menu': 'Menu chính. Chọn một danh mục:',
        'back': '⬅️ Quay lại',
        'to_main': '🏠 Menu chính',
        'choose_product': 'Chọn một sản phẩm:',
        'price': 'Giá',
        'description': 'Mô tả',
        'buy_btn': '🛒 Mua',
        'contact_btn': '📞 Liên hệ',
        'order_sent': '✅ Yêu cầu của bạn đã được nhận!\n\nSản phẩm: {name}\nGiá: {price}\n\nBạn có thể liên hệ trực tiếp với chúng tôi qua nút bên dưới.',
        'contact_link_text': '👉 Chạm để liên hệ',
        'not_found': 'Vui lòng chọn một nút từ menu.',
        'delivery_name': '🚚 Dịch vụ giao hàng',
        'delivery_info': 'Chúng tôi giao sản phẩm đến địa chỉ của bạn.\n\nĐể đặt hàng, chạm vào nút bên dưới — nhân viên của chúng tôi sẽ liên hệ với bạn.',
        'categories_label': 'DANH MỤC',
        'categories': {'electronics': '📱 Điện tử', 'auto': '🚗 Ô tô', 'home': '🏠 Đồ gia dụng', 'fruits': '🍎 Trái cây', 'vegetables': '🥦 Rau củ', 'delivery': 'Giao hàng'},
        'empty_category': '📭 Chưa có sản phẩm nào trong danh mục này.',
        'add_product_btn': "➕ Thêm sản phẩm"}
}


# ===========================================================================
# 3) MAHSULOTLAR — JSON FAYLDAN O'QISH/YOZISH
# ===========================================================================
DEFAULT_PRODUCTS = {
    "electronics": [],
    "auto": [],
    "home": [],
    "fruits": [],
    "vegetables": [],
}


def load_products() -> dict:
    if not os.path.exists(PRODUCTS_FILE):
        save_products(DEFAULT_PRODUCTS)
        return json.loads(json.dumps(DEFAULT_PRODUCTS))
    try:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for cat in DEFAULT_PRODUCTS:
            data.setdefault(cat, [])
        return data
    except Exception as e:
        logger.error(f"products.json ўқишда хато: {e}")
        return json.loads(json.dumps(DEFAULT_PRODUCTS))


def save_products(data: dict):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_product(category: str, name: str, price: str, photo: str, description: str):
    data = load_products()
    new_id = f"{category[:2]}_{len(data[category]) + 1}_{os.urandom(2).hex()}"
    data[category].append({
        "id": new_id,
        "name": name,
        "price": price,
        "photo": photo,
        "description": description,
    })
    save_products(data)


def get_products() -> dict:
    return load_products()


# ===========================================================================
# 4) HOLATLAR (FSM)
# ===========================================================================
class UserState(StatesGroup):
    choosing_language = State()
    in_main_menu = State()
    in_category = State()
    viewing_product = State()
    in_delivery = State()


class AdminState(StatesGroup):
    menu = State()
    add_choosing_category = State()
    add_name = State()
    add_price = State()
    add_photo = State()
    add_description = State()


CATEGORY_KEYS = ["electronics", "auto", "home", "fruits", "vegetables"]


# ===========================================================================
# 5) YORDAMCHI FUNKSIYALAR — XARIDOR KLAVIATURALARI
# ===========================================================================
def get_categories_keyboard(lang: str, user_id: int) -> ReplyKeyboardMarkup:
    cats = TEXTS[lang]["categories"]
    rows = [
        [KeyboardButton(text=cats["electronics"]), KeyboardButton(text=cats["auto"])],
        [KeyboardButton(text=cats["home"]), KeyboardButton(text=cats["fruits"])],
        [KeyboardButton(text=cats["vegetables"])],
        [KeyboardButton(text=cats["delivery"])],
    ]
    # Аралаш режим: агар фойдаланувчи админ бўлса, асосий менюга тугма қўшилади
    if is_admin(user_id):
        rows.append([KeyboardButton(text=TEXTS[lang].get("add_product_btn", "➕ Маҳсулот қўшиш"))])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def get_language_keyboard() -> ReplyKeyboardMarkup:
    names = list(LANG_BUTTONS.keys())
    rows = [names[i:i + 2] for i in range(0, len(names), 2)]
    keyboard = [[KeyboardButton(text=n) for n in row] for row in rows]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_category_products_keyboard(lang: str, category: str) -> ReplyKeyboardMarkup:
    products = get_products()
    names = [p["name"] for p in products.get(category, [])]
    rows = [names[i:i + 2] for i in range(0, len(names), 2)]
    keyboard = [[KeyboardButton(text=n) for n in row] for row in rows]
    keyboard.append([KeyboardButton(text=TEXTS[lang]["to_main"])])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_product_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=TEXTS[lang]["buy_btn"])],
            [KeyboardButton(text=TEXTS[lang]["back"]), KeyboardButton(text=TEXTS[lang]["to_main"])],
        ],
        resize_keyboard=True,
    )


def get_delivery_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=TEXTS[lang]["contact_btn"])],
            [KeyboardButton(text=TEXTS[lang]["to_main"])],
        ],
        resize_keyboard=True,
    )


def get_contact_inline_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=TEXTS[lang]["contact_link_text"], url=ADMIN_CONTACT_LINK)]
        ]
    )


def find_product_by_name(category: str, name: str):
    products = get_products()
    for p in products.get(category, []):
        if p["name"] == name:
            return p
    return None


def find_category_by_button_text(lang: str, text: str):
    cats = TEXTS[lang]["categories"]
    for key, label in cats.items():
        if label == text and key != "delivery":
            return key
    return None


def is_delivery_button(lang: str, text: str) -> bool:
    return text == TEXTS[lang]["categories"]["delivery"]


def all_to_main_texts():
    return [TEXTS[l]["to_main"] for l in TEXTS]


def all_back_texts():
    return [TEXTS[l]["back"] for l in TEXTS]


def all_buy_texts():
    return [TEXTS[l]["buy_btn"] for l in TEXTS]


def all_contact_texts():
    return [TEXTS[l]["contact_btn"] for l in TEXTS]


def all_add_product_texts():
    return [TEXTS[l].get("add_product_btn", "➕ Маҳсулот қўшиш") for l in TEXTS]


def is_admin(user_id: int) -> bool:
    return ADMIN_CHAT_ID and str(user_id) == str(ADMIN_CHAT_ID)


# ===========================================================================
# 6) YORDAMCHI FUNKSIYALAR — ADMIN KLAVIATURALARI
# ===========================================================================
CATEGORY_LABELS_UZ = {
    "electronics": "📱 Электроника",
    "auto": "🚗 Машина",
    "home": "🏠 Уй-хўжалик",
    "fruits": "🍎 Мевалар",
    "vegetables": "🥦 Сабзавотлар",
}


def admin_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Маҳсулот қўшиш")],
            [KeyboardButton(text="📋 Маҳсулотлар рўйхати")],
            [KeyboardButton(text="🚪 Админ режимидан чиқиш")],
        ],
        resize_keyboard=True,
    )


def admin_category_keyboard() -> ReplyKeyboardMarkup:
    labels = list(CATEGORY_LABELS_UZ.values())
    rows = [labels[i:i + 2] for i in range(0, len(labels), 2)]
    keyboard = [[KeyboardButton(text=l) for l in row] for row in rows]
    keyboard.append([KeyboardButton(text="❌ Бекор қилиш")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def admin_cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Бекор қилиш")]],
        resize_keyboard=True,
    )


def find_category_key_by_uz_label(text: str):
    for key, label in CATEGORY_LABELS_UZ.items():
        if label == text:
            return key
    return None


# ===========================================================================
# 7) HANDLERLAR — XARIDOR OQIMI
# ===========================================================================

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(UserState.choosing_language)
    await message.answer(
        "Тилни танланг / Choose language / Выберите язык:",
        reply_markup=get_language_keyboard(),
    )


@dp.message(UserState.choosing_language, F.text.in_(LANG_BUTTONS.keys()))
async def process_language(message: Message, state: FSMContext):
    lang = LANG_BUTTONS[message.text]
    await state.update_data(lang=lang)
    await state.set_state(UserState.in_main_menu)

    await message.answer(TEXTS[lang]["lang_set"])
    await message.answer(
        TEXTS[lang]["main_menu"],
        reply_markup=get_categories_keyboard(lang, message.from_user.id),
    )


@dp.message(UserState.in_category, F.text.in_(all_to_main_texts()))
@dp.message(UserState.viewing_product, F.text.in_(all_to_main_texts()))
@dp.message(UserState.in_delivery, F.text.in_(all_to_main_texts()))
async def process_to_main(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    await state.set_state(UserState.in_main_menu)
    await message.answer(
        TEXTS[lang]["main_menu"],
        reply_markup=get_categories_keyboard(lang, message.from_user.id),
    )


@dp.message(UserState.viewing_product, F.text.in_(all_back_texts()))
async def process_back_to_category(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    category = data.get("category")
    await state.set_state(UserState.in_category)
    await message.answer(
        TEXTS[lang]["choose_product"],
        reply_markup=get_category_products_keyboard(lang, category),
    )


@dp.message(UserState.in_main_menu, F.text.in_(all_add_product_texts()))
async def mix_admin_add_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(AdminState.add_choosing_category)
    await message.answer(
        "Қайси бўлимга маҳсулот қўшасиз?",
        reply_markup=admin_category_keyboard(),
    )


@dp.message(UserState.in_main_menu)
async def process_main_menu_choice(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    if is_delivery_button(lang, message.text):
        await state.set_state(UserState.in_delivery)
        await message.answer(
            f"{TEXTS[lang]['delivery_name']}\n\n{TEXTS[lang]['delivery_info']}",
            reply_markup=get_delivery_keyboard(lang),
        )
        return

    category = find_category_by_button_text(lang, message.text)
    if not category:
        await message.answer(TEXTS[lang]["not_found"], reply_markup=get_categories_keyboard(lang, message.from_user.id))
        return

    products = get_products()
    if not products.get(category):
        await message.answer(
            TEXTS[lang].get("empty_category", "Ҳозирча бу бўлимда маҳсулот йўқ."),
            reply_markup=get_categories_keyboard(lang, message.from_user.id),
        )
        return

    await state.update_data(category=category)
    await state.set_state(UserState.in_category)
    await message.answer(
        TEXTS[lang]["choose_product"],
        reply_markup=get_category_products_keyboard(lang, category),
    )


@dp.message(UserState.in_category)
async def process_show_product(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    category = data.get("category")

    product = find_product_by_name(category, message.text)
    if not product:
        await message.answer(TEXTS[lang]["not_found"], reply_markup=get_category_products_keyboard(lang, category))
        return

    await state.update_data(product_id=product["id"])
    await state.set_state(UserState.viewing_product)

    caption = (
        f"<b>{product['name']}</b>\n\n"
        f"💰 {TEXTS[lang]['price']}: {product['price']}\n"
        f"📝 {TEXTS[lang]['description']}: {product['description']}"
    )
    # Маҳсулот тагида доимий равишда боғланиш учун инлайн тугма чиқарилади
    await message.answer_photo(
        photo=product["photo"],
        caption=caption,
        parse_mode="HTML",
        reply_markup=get_contact_inline_keyboard(lang),
    )
    await message.answer(
        TEXTS[lang]["choose_product"],
        reply_markup=get_product_keyboard(lang)
    )


@dp.message(UserState.viewing_product, F.text.in_(all_buy_texts()))
async def process_buy(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    category = data.get("category")
    product_id = data.get("product_id")

    products = get_products()
    product = next((p for p in products.get(category, []) if p["id"] == product_id), None)
    if not product:
        await message.answer(TEXTS[lang]["not_found"])
        return

    user = message.from_user

    await message.answer(
        TEXTS[lang]["order_sent"].format(name=product["name"], price=product["price"]),
        reply_markup=get_contact_inline_keyboard(lang),
    )

    await notify_admin_order(user, product, category)


@dp.message(UserState.in_delivery, F.text.in_(all_contact_texts()))
async def process_delivery_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    user = message.from_user

    await message.answer(
        TEXTS[lang]["contact_link_text"],
        reply_markup=get_contact_inline_keyboard(lang),
    )

    await notify_admin_delivery_request(user)


async def notify_admin_order(user, product, category):
    if not ADMIN_CHAT_ID:
        return
    text = (
        f"🆕 Янги буюртма!\n\n"
        f"Маҳсулот: {product['name']}\n"
        f"Нарх: {product['price']}\n"
        f"Категория: {category}\n\n"
        f"Фойдаланувчи: {user.full_name} (@{user.username or '—'})\n"
        f"User ID: {user.id}\n"
        f"Профил: tg://user?id={user.id}"
    )
    try:
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    except Exception as e:
        logger.error(f"Админга хабар юборишда хато: {e}")


async def notify_admin_delivery_request(user):
    if not ADMIN_CHAT_ID:
        return
    text = (
        f"🚚 Янги етказиб бериш сўрови!\n\n"
        f"Фойдаланувчи: {user.full_name} (@{user.username or '—'})\n"
        f"User ID: {user.id}\n"
        f"Профил: tg://user?id={user.id}"
    )
    try:
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    except Exception as e:
        logger.error(f"Админга хабар юборишда хато: {e}")


# ===========================================================================
# 8) HANDLERLAR — ADMIN OQIMI
# ===========================================================================

@dp.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Сиз админ эмассиз!")
        return
    await state.set_state(AdminState.menu)
    await message.answer(
        "🛠 Админ панел. Нима қилмоқчисиз?",
        reply_markup=admin_menu_keyboard(),
    )


@dp.message(AdminState.menu, F.text == "🚪 Админ режимидан чиқиш")
async def admin_exit(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    await state.set_state(UserState.in_main_menu)
    await message.answer("Админ режимидан чиқдингиз.", reply_markup=get_categories_keyboard(lang, message.from_user.id))


@dp.message(AdminState.menu, F.text == "📋 Маҳсулотлар рўйхати")
async def admin_list_products(message: Message, state: FSMContext):
    products = get_products()
    lines = []
    for cat_key, cat_label in CATEGORY_LABELS_UZ.items():
        items = products.get(cat_key, [])
        lines.append(f"\n{cat_label} ({len(items)} та):")
        if not items:
            lines.append("  — бўш —")
        for p in items:
            lines.append(f"  • {p['name']} — {p['price']}")
    await message.answer("\n".join(lines) or "Маҳсулотлар йўқ.")


@dp.message(AdminState.menu, F.text == "➕ Маҳсулот қўшиш")
async def admin_add_start(message: Message, state: FSMContext):
    await state.set_state(AdminState.add_choosing_category)
    await message.answer(
        "Қайси бўлимга маҳсулот қўшасиз?",
        reply_markup=admin_category_keyboard(),
    )


@dp.message(AdminState.add_choosing_category, F.text == "❌ Бекор қилиш")
@dp.message(AdminState.add_name, F.text == "❌ Бекор қилиш")
@dp.message(AdminState.add_price, F.text == "❌ Бекор қилиш")
@dp.message(AdminState.add_photo, F.text == "❌ Бекор қилиш")
@dp.message(AdminState.add_description, F.text == "❌ Бекор қилиш")
async def admin_cancel_add(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    await state.set_state(UserState.in_main_menu)
    await message.answer("Бекор қилинди.", reply_markup=get_categories_keyboard(lang, message.from_user.id))


@dp.message(AdminState.add_choosing_category)
async def admin_add_category(message: Message, state: FSMContext):
    category = find_category_key_by_uz_label(message.text)
    if not category:
        await message.answer("Илтимос, рўйхатдан бўлимни танланг.", reply_markup=admin_category_keyboard())
        return
    await state.update_data(new_category=category)
    await state.set_state(AdminState.add_name)
    await message.answer("Маҳсулот номини киритинг:", reply_markup=admin_cancel_keyboard())


@dp.message(AdminState.add_name)
async def admin_add_name(message: Message, state: FSMContext):
    await state.update_data(new_name=message.text)
    await state.set_state(AdminState.add_price)
    await message.answer("Нархини киритинг (масалан: 150 000 сўм):", reply_markup=admin_cancel_keyboard())


@dp.message(AdminState.add_price)
async def admin_add_price(message: Message, state: FSMContext):
    await state.update_data(new_price=message.text)
    await state.set_state(AdminState.add_photo)
    await message.answer(
        "Маҳсулот расмини юборинг (расм файл сифатида, камерадан ёки галереядан):",
        reply_markup=admin_cancel_keyboard(),
    )


@dp.message(AdminState.add_photo, F.photo)
async def admin_add_photo(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(new_photo=file_id)
    await state.set_state(AdminState.add_description)
    await message.answer("Маҳсулот ҳақида қисқача тавсиф (описание) ёзинг:", reply_markup=admin_cancel_keyboard())


@dp.message(AdminState.add_photo)
async def admin_add_photo_wrong(message: Message, state: FSMContext):
    await message.answer("Илтимос, расмни файл сифатида юборинг (скрепка тугмаси -> rasm).")


@dp.message(AdminState.add_description)
async def admin_add_description(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")
    category = data["new_category"]
    name = data["new_name"]
    price = data["new_price"]
    photo = data["new_photo"]
    description = message.text

    add_product(category, name, price, photo, description)

    await state.set_state(UserState.in_main_menu)
    await message.answer(
        f"✅ Маҳсулот қўшилди!\n\n"
        f"Бўлим: {CATEGORY_LABELS_UZ[category]}\n"
        f"Номи: {name}\n"
        f"Нархи: {price}\n"
        f"Тавсиф: {description}\n\n"
        f"Маҳсулот менюда дарҳол кўринади.",
        reply_markup=get_categories_keyboard(lang, message.from_user.id),
    )


# ===========================================================================
# 9) DASTURNI ISHGA TUSHIRISH (POLLING)
# ===========================================================================
async def main():
    logger.info("Бот ишга тушмоқда...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
