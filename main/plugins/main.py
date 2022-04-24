import os
import time
import asyncio
from .. import Aziko, LOG_CHANNEL, FORCESUB_UN, MONGODB_URI, ACCESS_CHANNEL
from telethon import events, Button
from telethon.tl.types import DocumentAttributeVideo
from main.plugins.rename import media_rename
from main.plugins.compressor import compress
from main.plugins.trimmer import trim
from main.plugins.convertor import mp3, flac, wav, mp4, mkv, webm, file, video
from main.Database.database import Database
from LOCAL.localisation import source_text, SUPPORT_LINK
from main.plugins.actions import force_sub
from ethon.telefunc import fast_download
from ethon.pyfunc import video_metadata

forcesubtext = f"Botni ishlatish uchun kanalga aʼzo boʻling @{FORCESUB_UN}."

@Aziko.on(events.NewMessage(incoming=True,func=lambda e: e.is_private))
async def compin(event):
    db = Database(MONGODB_URI, 'videoconvertor')
    if event.is_private:
        media = event.media
        if media:
            yy = await force_sub(event.sender_id)
            if yy is True:
                return await event.reply(forcesubtext)
            banned = await db.is_banned(event.sender_id)
            if banned is True:
                return await event.reply(f'Siz ban oldingiz!\n\nMurojat: [ADMIN]({SUPPORT_LINK})', link_preview=False)
            video = event.file.mime_type
            if 'video' in video:
                await event.reply("📽",
                            buttons=[
                                [Button.inline("Siqish", data="compress"),
                                 Button.inline("O‘zgartirish", data="convert")],
                                [Button.inline("Qayta nomlash", data="rename"),
                                 Button.inline("Kesish", data="trim")]
                            ])
            elif 'png' in video:
                return
            elif 'jpeg' in video:
                return
            elif 'jpg' in video:
                return    
            else:
                await event.reply('📦',
                            buttons=[  
                                [Button.inline("Qayta nomlash", data="rename")]])
    await event.forward_to(int(ACCESS_CHANNEL))

@Aziko.on(events.callbackquery.CallbackQuery(data="convert"))
async def convert(event):
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.edit("🔃**Qayta nomlash:**",
                    buttons=[
                        [Button.inline("MP3", data="mp3"),
                         Button.inline("FLAC", data="flac"),
                         Button.inline("WAV", data="wav")],
                        [Button.inline("MP4", data="mp4"),
                         Button.inline("WEBM", data="webm"),
                         Button.inline("MKV", data="mkv")],
                        [Button.inline("FILE", data="file"),
                         Button.inline("VIDEO", data="video")],
                        [Button.inline("BACK", data="back")]])
                        
@Aziko.on(events.callbackquery.CallbackQuery(data="back"))
async def back(event):
    await event.edit("📽",
                    buttons=[
                        [Button.inline("Siqish", data="compress"),
                         Button.inline("O‘zgartirish", data="convert")],
                        [Button.inline("Qayta nomlash", data="rename"),
                         Button.inline("Kesish", data="trim")]])
                            
#-----------------------------------------------------------------------------------------

process1 = []
timer = []

@Aziko.on(events.callbackquery.CallbackQuery(data="mp3"))
async def vtmp3(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await mp3(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("Boshqa progress ishlovda!")
        
@Aziko.on(events.callbackquery.CallbackQuery(data="flac"))
async def vtflac(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await flac(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("Boshqa progress ishlovda!")
        
@Aziko.on(events.callbackquery.CallbackQuery(data="wav"))
async def vtwav(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    if not os.path.isdir("audioconvert"):
        await event.delete()
        os.mkdir("audioconvert")
        await wav(event, msg)
        os.rmdir("audioconvert")
    else:
        await event.edit("Boshqa progress ishlovda!")
        
@Aziko.on(events.callbackquery.CallbackQuery(data="mp4"))
async def vtmp4(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await mp4(event, msg)
    
@Aziko.on(events.callbackquery.CallbackQuery(data="mkv"))
async def vtmkv(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await mkv(event, msg)  
    
@Aziko.on(events.callbackquery.CallbackQuery(data="webm"))
async def vtwebm(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await webm(event, msg)  
    
@Aziko.on(events.callbackquery.CallbackQuery(data="file"))
async def vtfile(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await file(event, msg)    

@Aziko.on(events.callbackquery.CallbackQuery(data="video"))
async def ftvideo(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message() 
    await event.delete()
    await video(event, msg)
    
@Aziko.on(events.callbackquery.CallbackQuery(data="rename"))
async def rename(event):    
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    async with Aziko.conversation(event.chat_id) as conv: 
        cm = await conv.send_message("Yangi nomni reply qilib yuboring.\n\n**Eslatma:** `nuqta qoʻyib formatini yozish shartmas.")                              
        try:
            m = await conv.get_reply()
            new_name = m.text
            await cm.delete()                    
            if not m:                
                return await cm.edit("Hechnima topilmadi.")
        except Exception as e: 
            print(e)
            return await cm.edit("Xatolik")
    await media_rename(event, msg, new_name)                     
                   
@Aziko.on(events.callbackquery.CallbackQuery(data="compress"))
async def compresss(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    if f'{event.sender_id}' in process1:
        index = process1.index(f'{event.sender_id}')
        last = timer[int(index)]
        present = time.time()
        return await event.answer(f"Siz {300-round(present-float(last))} soniya kutishingiz kerak!", alert=True)
    button = await event.get_message()
    msg = await button.get_reply_message()
    if not os.path.isdir("compressmedia"):
        await event.delete()
        os.mkdir("compressmedia")
        await compress(event, msg)
        os.rmdir("compressmedia")
        now = time.time()
        timer.append(f'{now}')
        process1.append(f'{event.sender_id}')
        await event.client.send_message(event.chat_id, 'Yangi processni 5 daqiqadan keyin boshlay olasiz')
        await asyncio.sleep(300)
        timer.pop(int(timer.index(f'{now}')))
        process1.pop(int(process1.index(f'{event.sender_id}')))
    else:
        await event.edit(f"Boshqa process ishlovda!\n\n**[Jarayonlar](https://t.me/{LOG_CHANNEL})**", link_preview=False)
    
@Aziko.on(events.callbackquery.CallbackQuery(data="trim"))
async def vtrim(event):
    yy = await force_sub(event.sender_id)
    if yy is True:
        return await event.reply(forcesubtext)
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    async with Aziko.conversation(event.chat_id) as conv: 
        try:
            xx = await conv.send_message("Videoni boshlanish vaqtini ushbu. \n\nformatda reply qilib yuboring hh:mm:ss soat:minut:soniya, for Masalan: `01:20:69` ")
            x = await conv.get_reply()
            st = x.text
            await xx.delete()                    
            if not st:               
                return await xx.edit("Hechnima topilmadi.")
        except Exception as e: 
            print(e)
            return await xx.edit("Xatolik.")
        try:
            xy = await conv.send_message("Videoni yakunlanish vaqtini  \n\nushbu formatda reply qilib yuboring hh:mm:ss soat:minut:soniya, for Masalan: `01:20:69` ")  
            y = await conv.get_reply()
            et = y.text
            await xy.delete()                    
            if not et:                
                return await xy.edit("Hechnima topilmadi.")
        except Exception as e: 
            print(e)
            return await xy.edit("Qandaytir xatolik.")
        await trim(event, msg, st, et)
            
