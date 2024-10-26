import telegram
from telegram.ext import Application, CommandHandler

# إعداد الروبوت
bot_token = '7306244755:AAEIekLlNqaeeTX64d7Tfc0o3Q3uWZTOIK8'
app = Application.builder().token(bot_token).build()

# وظيفة إرسال رسالة تحفيزية
async def send_motivation(update, context):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="تذكير: نحن هنا لدعمك دائمًا! تابع تقدمك في البرامج التأهيلية.")

# وظيفة إرسال تذكير متابعة التدريب
async def send_reminder(update, context):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="تذكير بمتابعة التدريب الأسبوعي!")

# ربط الأوامر بالوظائف
app.add_handler(CommandHandler("start", send_motivation))
app.add_handler(CommandHandler("reminder", send_reminder))  # إضافة أمر التذكير

# بدء الروبوت
app.run_polling()
