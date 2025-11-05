import subprocess
import sys

def install_package(package_name):
    """Устанавливает пакет через pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Проверяем и устанавливаем необходимые библиотеки
required_packages = ["python-telegram-bot"]

for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        print(f"Устанавливается пакет: {package}...")
        install_package(package)

# Далее стандартный код с импортами и логикой
import logging
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "8092406315:AAGXA-LCSnlNa_z6muk37ZJwX72V7pLQ3mM"

CHAR_MAP = {
    'а': ['а', 'a', '@', '4', '#'],
    'б': ['б', '6', 'b', '#'],
    'в': ['в', 'v', '#'],
    'г': ['г', 'g', '#'],
    'д': ['д', 'd', '#'],
    'е': ['е', 'e', 'ё', '#'],
    'ё': ['ё', 'e', '#'],
    'ж': ['ж', 'zh', '#'],
    'з': ['з', 'z', '3', '#'],
    'и': ['и', 'i', 'u', '#'],
    'й': ['й', 'y', 'j', 'i', '#'],
    'к': ['к', 'k', '#'],
    'л': ['л', 'l', '#'],
    'м': ['м', 'm', '#'],
    'н': ['н', 'n', '#'],
    'о': ['о', 'o', '0', '#'],
    'п': ['п', 'p', '#'],
    'р': ['р', 'r', '#'],
    'с': ['с', 'c', 's', '#'],
    'т': ['т', 't', '#'],
    'у': ['у', 'y', 'u', '#'],
    'ф': ['ф', 'f', '#'],
    'х': ['х', 'x', 'h', '#'],
    'ц': ['ц', 'c', '#'],
    'ч': ['ч', 'ch', '4', '#'],
    'ш': ['ш', 'sh', '#'],
    'щ': ['щ', 'sh', '#'],
    'ы': ['ы', '#'],
    'ь': ['ь', '#'],
    'э': ['э', 'e', '#'],
    'ю': ['ю', 'u', '#'],
    'я': ['я', 'a', '#'],
    'a': ['а', 'a', '#'],
    'b': ['б', 'b', '#'],
    'c': ['с', 'c', '#'],
    'd': ['д', 'd', '#'],
    'e': ['е', 'e', '#'],
    'f': ['ф', 'f', '#'],
    'g': ['г', 'g', '#'],
    'h': ['х', 'h', '#'],
    'i': ['и', 'i', '#'],
    'j': ['й', 'j', '#'],
    'k': ['к', 'k', '#'],
    'l': ['л', 'l', '#'],
    'm': ['м', 'm', '#'],
    'n': ['н', 'n', '#'],
    'o': ['о', 'o', '#'],
    'p': ['п', 'p', '#'],
    'r': ['р', 'r', '#'],
    's': ['с', 's', '#'],
    't': ['т', 't', '#'],
    'u': ['у', 'u', '#'],
    'v': ['в', 'v', '#'],
    'x': ['х', 'x', '#'],
    'y': ['у', 'y', '#'],
    'z': ['з', 'z', '#'],
    '0': ['о', '0', '#'],
    '1': ['и', '1', '#'],
    '3': ['з', '3', '#'],
    '4': ['ч', '4', '#'],
    '6': ['б', '6', '#'],
    '@': ['а', '@', '#'],
}

BASIC_WORDS = [
    "хуй", "пизда", "ебать", "сука", "пидор", "xyйня", "бля", "блять", 
    "блядь", "отъебись", "ахуел", "заебал", "долбоёб", "Залупа", "манда", 
    "еблан", "ебло", "блядь", "гандон", "мудила", "пиздец", "чмо", "сволочь", 
    "пидрас", "пидорас", "уёбище", "шлюха", "хуесос", "тварь", "блядина", 
    "ебучий", "поебень", "мудозвон", "хуйло", "ебаный", "охуел", "пиздатый", 
    "хуевина", "уёбок", "хер", "ёб", "хулиган", "сукин сын", "ублюдок", "гнида", 
    "выблядок", "скотина", "козёл", "баран", "осёл", "fuck", "shit", "bitch", 
    "asshole", "dick", "bastard", "douchebag", "cunt", "faggot", "motherfucker", 
    "prick", "wanker", "twat", "arsehole", "bollocks", "bloody hell", "damn", 
    "hell", "ass", "cock", "pussy", "tit", "fart", "crap", "piss", "arse", "git", 
    "pillock", "tosser", "knob", "plonker", "numpty", "eejit", "gobshite", "feck", 
    "shite", "fucktard", "shitstain", "clusterfuck", "scheiße", "arschloch", 
    "fotze", "wichser", "hurensohn", "mistkerl", "saukerl", "drecksau", 
    "drecksloch", "trottel", "blödmann", "pisser", "schwanzlutscher", "möchtegern", 
    "tölpel", "putain", "merde", "connard", "salope", "enculé", "déchet", "con", 
    "débile", "abruti", "fumier", "salaud", "imbécile", "pourri", "pourrave", 
    "clochardise", "puta", "mierda", "coño", "gilipollas", "pendejo", "cabrón", 
    "puto", "baboso", "idiota", "imbécil", "estúpido", "mamon", "hijo de puta", 
    "chingada", "ojete", "cazzo", "stronzo", "figa", "vaffanculo", "merda", 
    "troia", "bastardo", "porco", "deficiente", "testa di cazzo", "kurwa", "gówno", 
    "dupek", "frajer", "pierdol", "chuj", "rzach", "puta", "merda", "caralho", 
    "cacete", "bostas", "klootzak", "kutje", "godverdomme", "kanker", "tyfus", 
    "tering", "jävla", "helvete", "skit", "ditt", "σκατά", "μαλάκα", "κόλε", 
    "sikeyim", "orospu", "siktir",
]


def convert_word_to_regex(word):
    """Конвертирует обычное слово в регулярное выражение с альтернативными символами"""
    pattern_parts = []
    for char in word.lower():
        replacements = CHAR_MAP.get(char, [char])
        unique_chars = list(set(replacements))
        pattern_parts.append(f'[{"".join(unique_chars)}]')
    return ''.join(pattern_parts) + r'[\W_]*'

PATTERNS = [convert_word_to_regex(word) for word in BASIC_WORDS]
compiled_patterns = [re.compile(pattern, re.IGNORECASE | re.UNICODE) for pattern in PATTERNS]

logger.info(f"Generated patterns: {PATTERNS}")

async def delete_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    message = update.message
    text = message.text.lower()

    for pattern in compiled_patterns:
        if pattern.search(text):
            try:
                await message.delete()
                logger.info(f"Удалено сообщение: '{message.text}' по паттерну: {pattern.pattern}")
                break
            except Exception as e:
                logger.error(f"Ошибка удаления: {e}")
            break

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_messages))
    app.run_polling()
