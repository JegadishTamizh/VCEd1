#  This file is part of the VIDEOconvertor distribution.
#  Copyright (c) 2021 vasusen-code ; All rights reserved. 
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  License can be found in < https://github.com/vasusen-code/VIDEOconvertor/blob/public/LICENSE> .

import os

from telethon import events, Button

from .. import Drone 

from main.plugins.rename import media_rename
from main.plugins.compressor import compress
from main.plugins.encoder import encode

@Drone.on(events.NewMessage(incoming=True,func=lambda e: e.is_private))
async def compin(event):
    if event.is_private:
        media = event.media
        if media:
            video = event.file.mime_type
            if 'video' in video:
                await event.reply("📽",
                            buttons=[
                                [Button.inline("ENCODE", data="encode"),
                                 Button.inline("COMPRESS", data="compress")],
                                [Button.inline("RENAME", data="rename")],
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
                                [Button.inline("RENAME", data="rename")]])
                
@Drone.on(events.callbackquery.CallbackQuery(data="encode"))
async def _encode(event):
    await event.edit("**🔀ENCODE**",
                    buttons=[
                         Button.inline("x265", data="265")],
                        [Button.inline("BACK", data="back")]])
                         
@Drone.on(events.callbackquery.CallbackQuery(data="compress"))
async def _compress(event):
    await event.edit("**🗜COMPRESS**",
                    buttons=[
                        [Button.inline("HEVC COMPRESS", data="hcomp"),
                         Button.inline("FAST COMPRESS", data="fcomp")],
                        [Button.inline("BACK", data="back")]
                    ])
                        
@Drone.on(events.callbackquery.CallbackQuery(data="back"))
async def back(event):
    await event.edit("📽", buttons=[
                    [Button.inline("ENCODE", data="encode"),
                     Button.inline("COMPRESS", data="compress")]
                    [Button.inline("RENAME", data="rename")],
    
#-----------------------------------------------------------------------------------------
    
@Drone.on(events.callbackquery.CallbackQuery(data="rename"))
async def rename(event):                            
    button = await event.get_message()
    msg = await button.get_reply_message()  
    await event.delete()
    markup = event.client.build_reply_markup(Button.force_reply())
    async with Drone.conversation(event.chat_id) as conv: 
        cm = await conv.send_message("Send me a new name for the file as a `reply` to this message.\n\n**NOTE:** `.ext` is not required.", buttons=markup)                              
        try:
            m = await conv.get_reply()
            new_name = m.text
            await cm.delete()                    
            if not m:                
                return await cm.edit("No response found.")
        except Exception as e: 
            print(e)
            return await cm.edit("An error occured while waiting for the response.")
    await media_rename(event, msg, new_name)                     
                   
@Drone.on(events.callbackquery.CallbackQuery(data="hcomp"))
async def hcomp(event):
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=1)
        if os.path.isdir("encodemedia"):
            os.rmdir("encodemedia")
    else:
        await event.edit("Another process in progress!")
 
@Drone.on(events.callbackquery.CallbackQuery(data="fcomp"))
async def fcomp(event):
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=2)
        if os.path.isdir("encodemedia"):
            os.rmdir("encodemedia")
    else:
        await event.edit("Another process in progress!")
  
@Drone.on(events.callbackquery.CallbackQuery(data="265"))
async def _265(event):
    button = await event.get_message()
    msg = await button.get_reply_message()  
    if not os.path.isdir("encodemedia"):
        await event.delete()
        os.mkdir("encodemedia")
        await compress(event, msg, ffmpeg_cmd=3, ps_name="**ENCODING:**")
        if os.path.isdir("encodemedia"):
            os.rmdir("encodemedia")
    else:
        await event.edit("Another process in progress!")
