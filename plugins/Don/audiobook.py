import os
import pyrogram
import PyPDF2
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message, Document 
from gtts import gTTS
from info import DOWNLOAD_LOCATION
  
Thanks = """ 𝖳𝗁𝖺𝗍𝗌 𝖳𝗁𝖾 𝖤𝗇𝖽 𝖮𝖿 𝖸𝗈𝗎𝗋 𝖠𝗎𝖽𝗂𝗈 𝖡𝗈𝗈𝗄, 𝖠𝗇𝖽 𝖳𝗁𝖺𝗇𝗄𝗌 𝖥𝗈𝗋 𝖸𝗈𝗎𝗌𝗂𝗇𝗀 𝖳𝗁𝗂𝗌 𝖲𝖾𝗋𝗏𝗂𝖾𝗌"""

@Client.on_message(filters.command(["audiobook"])) # PdfToText 
async def pdf_to_text(bot, message):
 try:
           if message.reply_to_message:
                pdf_path = DOWNLOAD_LOCATION + f"{message.chat.id}.pdf" #pdfFileObject
                txt = await message.reply("Downloading.....")
                await message.reply_to_message.download(pdf_path)  
                await txt.edit("Downloaded File")
                pdf = open(pdf_path,'rb')
                pdf_reader = PyPDF2.PdfFileReader(pdf) #pdfReaderObject
                await txt.edit("Getting Number of Pages....")
                num_of_pages = pdf_reader.getNumPages() # Number of Pages               
                await txt.edit(f"Found {num_of_pages} Page")
                page_no = pdf_reader.getPage(0) # pageObject
                await txt.edit("Finding Text from Pdf File... ")
                page_content = """ """ # EmptyString   
                chat_id = message.chat.id
                with open(f'{message.chat.id}.txt', 'a+') as text_path:   
                  for page in range (0,num_of_pages):              
                      page_no = pdf_reader.getPage(page) # Iteration of page number
                      page_content += page_no.extractText()
                await txt.edit(f"𝖢𝗋𝖾𝖺𝗍𝗂𝗇𝗀 𝖸𝗈𝗎𝗋 𝖠𝗎𝖽𝗂𝗈 𝖡𝗈𝗈𝗄...\n 𝖯𝗅𝖾𝖺𝗌𝖾 𝖣𝗈𝗇'𝗍 𝖣𝗈 𝖠𝗇𝗂𝗍𝗁𝗂𝗇𝗀..")
                output_text = page_content + Thanks
              # Change Voice by editing the Language
                language = 'en-in'  # 'en': ['en-us', 'en-ca', 'en-uk', 'en-gb', 'en-au', 'en-gh', 'en-in',
                                    # 'en-ie', 'en-nz', 'en-ng', 'en-ph', 'en-za', 'en-tz'],
                tts_file = gTTS(text=output_text, lang=language, slow=False) 
                tts_file.save(f"{message.chat.id}.mp3")      
                with open(f"{message.chat.id}.mp3", "rb") as speech:
                      await bot.send_voice(chat_id, speech)   
                await txt.edit("Thanks For Using Me")    
                os.remove(pdf_path)  
                
                
           else :
                await message.reply("𝖯𝗅𝖾𝖺𝗌𝖾 𝖱𝖾𝗉𝗅𝖺𝗒 𝖳𝗈 𝖯𝖣𝖥 𝖥𝗂𝗅𝖾")
 except Exception as error :
           print(error)
           await txt.delete()
           os.remove(pdf_path)
