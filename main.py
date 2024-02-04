from typing import Final
from telegram import Update
from telegram.ext import Application, MessageHandler,CommandHandler, filters,ContextTypes
from deep_translator import GoogleTranslator
from Utils.LLMS import Oobabooga,Ollama
from Utils.TTS import Silero_tts




TOKEN: Final = '...'
bot_username: Final = '...'
language = {
    'source': 'pt',
    'target': 'en',
}
#Ollama Docker container Api
url_ollama = '...'

#never change /v1/chat/completions else the function will break
Ooba_api = '.../v1/chat/completions' 
 


def main():
    global mode
    print('Iniciando bot')
    mode = input('What mode you wanna use for LLM? (Ollama & Textgen) >').lower()
    language['source'] = input('What language you will talk to the bot? >').lower()


    application = Application.builder().token(TOKEN).build()
    
    #commands
    application.add_handler(CommandHandler('start',start_command))
    application.add_handler(CommandHandler('help',help_command))
    application.add_handler(CommandHandler('custom',custom_command))

    #messages handlers
    application.add_handler(MessageHandler(filters.TEXT,handle_message))
    #application.add_handler(MessageHandler(filters.VOICE,handle_audio))
    
    #errors
    #application.add_error_handler(error)
    #polling
    print('Bot Iniciado')
    application.run_polling(poll_interval=3) #num == seconds





#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Hi...')
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('How can i help you?')
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('hello...?')

#Responses
def handle_response(text) -> str:
    """
    This function will break if the user input the wrong param or language!!!!
    """
    processed: str = text.lower()
       
    user = GoogleTranslator(source=f'{language["source"]}', target=f'{language["target"]}').translate(processed)

    if mode == 'ollama':
        assistant_reply = Ollama.response(url_ollama,user)
        print(assistant_reply)
        assis_translation = GoogleTranslator(source='en', target='pt').translate(assistant_reply)
    elif mode == 'textgen':
        assistant_reply = Oobabooga.ooba(Ooba_api,user)
        print(assistant_reply)
        assis_translation = GoogleTranslator(source='en', target='pt').translate(assistant_reply)
            
    
    
    assis_voice = Silero_tts.tts(str(assistant_reply))
    print(assis_voice)
    return assis_translation,assis_voice
        
    
    
    
    
#Handle Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type #will inform us if its a group or private chat
    text: str = update.message.text
    print(f'User:{update.message.chat.id} in {message_type}: {text}')

        
    if message_type == 'group':
        if bot_username in text:
            new_text: str = text.replace(bot_username,"").strip()
            response: str = handle_response(new_text)
    else:
            response: str = handle_response(text)

    print('bot:',response)
    await update.message.reply_voice(response[1])
    await update.message.reply_text(response[0])


async def error(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused the following error {context.error}')

if __name__ == '__main__':
    main()