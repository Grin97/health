import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Включите логирование, чтобы видеть ошибки в консоли
logging.basicConfig(level=logging.INFO)

# Инициализация бота (Замените на свой реальный токен!)
BOT_TOKEN = "8737734083:AAFNDtBKToC8St0V82oH76Btr5Cfhj5DOsA"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Описываем состояния (шаги) по алгоритму Троцкого
class TrotskyAlgorithm(StatesGroup):
    waiting_for_problem = State()     # Шаг 1: Что случилось
    waiting_for_time = State()        # Шаг 2: Когда началось
    waiting_for_people = State()      # Шаг 3: Кто был рядом
    waiting_for_true_feeling = State() # Шаг 4: Скрытые чувства
    waiting_for_role_check = State()  # Шаг 5: Проверка роли

# Главная клавиатура
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚨 Разведать проблему (По Троцкому)")]
        ],
        resize_keyboard=True
    )

# Команда /start
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()  # Сбрасываем старые состояния, если они были
    await message.answer(
        f"Привет, {message.from_user.first_name}! Это бот-проводник по системе Дмитрия Троцкого.\n\n"
        "Любая проблема (болезнь, кризис, долг) — это следствие неискренности и невыраженных чувств. "
        "Готов заглянуть правде в глаза?",
        reply_markup=get_main_keyboard()
    )

# Кнопка отмены / сброса
@dp.message(Command("cancel"))
@dp.message(F.text.casefold() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Разбор отменен. Возвращаемся в главное меню.", reply_markup=get_main_keyboard())

# Шаг 1: Запуск алгоритма
@dp.message(F.text == "🚨 Разведать проблему (По Троцкому)")
async def start_algorithm(message: Message, state: FSMContext):
    await state.set_state(TrotskyAlgorithm.waiting_for_problem)
    await message.answer(
        "**Шаг 1 из 5. Фиксация проблемы.**\n\n"
        "Что конкретно идет не так? Опиши факт (например: 'заболело колено', 'уволили', 'сильно поругался с женой'). "
        "Пиши честно, как есть.",
        reply_markup=ReplyKeyboardRemove() # Прячем кнопку на время опроса
    )

# Шаг 2: Время
@dp.message(TrotskyAlgorithm.waiting_for_problem)
async def process_problem(message: Message, state: FSMContext):
    await state.update_data(problem=message.text)
    await state.set_state(TrotskyAlgorithm.waiting_for_time)
    await message.answer(
        "**Шаг 2 из 5. Точка отсчета.**\n\n"
        "Когда именно эта проблема появилась или резко обострилась? Постарайся вспомнить дату или период (например, 'в прошлый вторник', '2 недели назад')."
    )

# Шаг 3: Круг лиц
@dp.message(TrotskyAlgorithm.waiting_for_time)
async def process_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(TrotskyAlgorithm.waiting_for_people)
    await message.answer(
        "**Шаг 3 из 5. Поиск адресата.**\n\n"
        "Кто ключевые люди твоей жизни, которые были рядом незадолго до этого момента? На кого ты внутренне реагировал? "
        "Выпиши их имена или роли (например: 'мама', 'начальник Игорь', 'муж')."
    )

# Шаг 4: Скрытые чувства
@dp.message(TrotskyAlgorithm.waiting_for_people)
async def process_people(message: Message, state: FSMContext):
    await state.update_data(people=message.text)
    await state.set_state(TrotskyAlgorithm.waiting_for_true_feeling)
    await message.answer(
        "**Шаг 4 из 5. Анатомия неискренности.**\n\n"
        "А теперь самое сложное. Что ты **на самом деле** чувствовал к этим людям тогда (или чувствуешь сейчас), но скрыл/подавил? "
        "Обиду? Страх выглядеть глупо? Ярость? Зависть? Желание, чтобы похвалили? \n\n"
        "Напиши правду. Никто, кроме тебя и этого бота, её не увидит."
    )

# Шаг 5: Проверка роли
@dp.message(TrotskyAlgorithm.waiting_for_true_feeling)
async def process_feeling(message: Message, state: FSMContext):
    await state.update_data(feeling=message.text)
    await state.set_state(TrotskyAlgorithm.waiting_for_role_check)
    await message.answer(
        "**Шаг 5 из 5. Социальная роль.**\n\n"
        "В какой роли ты выступал по отношению к этому человеку? Ты был смиренным учеником/сыном/подчиненным? "
        "Или ты встал на табуретку судьи и начал его мысленно (или вслух) критиковать, учить жизни, спасать? "
        "Напиши, в какую псевдороль ты залетел."
    )

# Финал: Выдача ТЗ на трансформацию
@dp.message(TrotskyAlgorithm.waiting_for_role_check)
async def process_role_and_finish(message: Message, state: FSMContext):
    await state.update_data(role=message.text)
    
    # Извлекаем все сохраненные ответы пользователя
    user_data = await state.get_data()
    await state.clear() # Очищаем состояние
    
    # Формируем итоговый вердикт
    summary_text = (
        "📊 **КАРТА ТРАНСФОРМАЦИИ СИТУАЦИИ**\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"❌ **Твоя проблема:** {user_data['problem']}\n"
        f"📅 **Когда рвануло:** {user_data['time']}\n"
        f"👤 **С кем связано:** {user_data['people']}\n"
        f"🎭 **Твоя псевдороль:** {user_data['role']}\n"
        f"🔑 **Зажатое чувство:** {user_data['feeling']}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡️ **ИНСТРУКЦИЯ К ДЕЙСТВИЮ (По Троцкому):**\n\n"
        "1. **Признай псевдороль.** Мысленно вернись на свое место (ребенка перед родителем, сотрудника перед боссом).\n"
        "2. **Вырази чувство.** Твоя задача — донести зажатое чувство до адресата словами через рот, БЕЗ претензий, только через 'Я-сообщения'. "
        "*(Пример: 'Мне было очень страшно и обидно, когда случилось X...').*\n"
        "3. **Если контакт невозможен:** Возьми лист бумаги и выпиши всё это в формате письма покаяния/благодарности, пока внутри не наступит штиль.\n\n"
        "**Судьба меняется только через физическое действие в материальном мире.** Иди и сделай это."
    )
    
    await message.answer(summary_text, reply_markup=get_main_keyboard())

# Запуск процесса пуллинга
async def main():
    print("Бот успешно запущен и готов к работе...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
