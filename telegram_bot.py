from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)
import CONFIG
import db_operations
from my_logger import logger



class CustomTelegramBot:
    def __init__(self):
        self.main_bot_token = CONFIG.telegram_main_bot_id
        
        self.main_chat_id = CONFIG.telegram_main_chat_id
        self.debug_chat_id = CONFIG.telegram_debug_chat_id
        
        # self.updater = Updater(self.main_bot_token)
        # self.updater.stop()
        self.updater = Updater(self.main_bot_token)

        self.db = db_operations.DbOperations()
        self.cursor = self.db.cursor
    
    def main(self):
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("plakaliste", self.send_all_group_info), group=int(self.main_chat_id) )
        dispatcher.add_handler(CommandHandler("plakasayi", self.send_count_group_info), group=int(self.main_chat_id) )
        self.updater.start_polling()
        self.updater.idle()

    def send_message_to_mainchannel(self, message):
        try:
            self.updater.bot.send_message(chat_id=self.main_chat_id, text=message)
        except Exception as e:
            logger.exception(e)
    
    def send_message_to_debugchannel(self, message):
        try:
            self.updater.bot.send_message(chat_id=self.debug_chat_id, text=message)
        except Exception as e:
            logger.exception(e)
        
    def send_img_to_mainchannel(self, img, text:str):
        try:
            self.updater.bot.send_photo(chat_id=self.main_chat_id, photo=img, caption=text)
        except Exception as e:
            logger.exception(e)
        
    def send_img_to_debugchannel(self, img, text):
        try:
            self.updater.bot.send_photo(chat_id=self.debug_chat_id, photo=img, caption=text)
        except Exception as e:
            logger.exception(e)
                    
    def send_all_group_info(self, update: Update, context: CallbackContext):
        """Fetch all group info from db and send it to main channel"""
        returned_sabanci_list = self.db.get_specific_group_info('sabanci')
        returned_bulutistan_list = self.db.get_specific_group_info('bulutistan')
        returned_sahsi_list = self.db.get_specific_group_info('sabanci_sahsi')
        
        returned_sabanci_count = len(returned_sabanci_list)
        returned_bulutistan_count = len(returned_bulutistan_list)
        returned_sahsi_count = len(returned_sahsi_list)
        
        final_text = "Sabancı:"
        for plate in returned_sabanci_list:
            final_text += f"\n{plate[0]}"
        final_text += f"\nSabancıya ait {returned_sabanci_count} giriş tespit edildi.\n"
        
        final_text += "\nSabancı Şahsi:"
        for plate in returned_sahsi_list:
            final_text += f"\n{plate[0]}"
        final_text += f"\nSabancı şahsi araçlara ait {returned_sahsi_count} giriş tespit edildi.\n"
        
        final_text += "\nBulutistan:"
        for plate in returned_bulutistan_list:
            final_text += f"\n{plate[0]}"
        final_text += f"\nBulutistan'a ait {returned_bulutistan_count} giriş tespit edildi.\n"
        
        final_text += f"\nAynı plakanın birden fazla girişi varsa, bir giriş olarak sayılır."
        try:
            update.message.reply_text(f"{final_text}")
        except Exception as e:
            logger.exception(e)
        pass
    
    def send_count_group_info(self, update: Update, context: CallbackContext):
        """Fetch the count of group info from db and send it to main channel"""
        returned_sabanci_list = self.db.get_specific_group_count('sabanci')
        returned_bulutistan_list = self.db.get_specific_group_count('bulutistan')
        returned_sahsi_list = self.db.get_specific_group_count('sabanci_sahsi')
        
        returned_sabanci_count = returned_sabanci_list[0][0]
        returned_bulutistan_count = returned_bulutistan_list[0][0]
        returned_sahsi_count = returned_sahsi_list[0][0]
        
        final_text = f"Sabancı:".ljust(24) + f"{returned_sabanci_count}\n"
        final_text += f"Sabancı şahsi:".ljust(18) + f"{returned_sahsi_count}\n"
        final_text += f"Bulutistan:".ljust(22) + f"{returned_bulutistan_count}\n"
        final_text += f"\nÇıkışlar hesaba katılmamıştır."
        final_text += f"\nAynı plakanın birden fazla girişi varsa, bir giriş olarak sayılır."
        
        try:
            update.message.reply_text(f"{final_text}")
        except Exception as e:
            logger.exception(e)
        pass        
        