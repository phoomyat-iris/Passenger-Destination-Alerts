import RPi.GPIO as GPIO
from time import sleep
from RPLCD.i2c import CharLCD
from telegram.ext import Application, MessageHandler, filters
import threading
import asyncio
import os
from gtts import gTTS
import pygame



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pygame.mixer.init()

bus_stop = { 
        "Jurong East": {
            "coordinates": (1.3333800691519504, 103.74231863722021),
            "number": 1
        },
        "Clementi": {
            "coordinates": (1.309968767268852, 103.77747439304167),
            "number": 2
        },
        "SP": {
            "coordinates": (1.3100653015535266, 103.77758168139887),
            "number": 3
        },
        "Buona Vista": {
            "coordinates": (1.3066748717130419, 103.79097782557754),
            "number": 4
        },
        "Commonwealth": {
            "coordinates": (1.3042141572794765, 103.79836534941028),
            "number": 5
        },
        "Queenstown": {
            "coordinates": (1.2944989484691487, 103.80606427530621),
            "number": 6
        }
        
    }

audio_files = {
    "Jurong East": "audio/jurong_east.mp3.mpeg",
    "Clementi": "audio/clementi.mp3.mpeg",
    "SP": "audio/sp.mp3.mpeg",
    "Buona Vista": "audio/buona_vista.mp3.mp3",
    "Commonwealth": "audio/commonwealth.mp3.mp3",
    "Queenstown": "audio/queenstown.mp3.mp3"
}


MATRIX = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ['*', 0, '#']
]
ROW = [6, 20, 19, 13]
COL = [12, 5, 16]


for i in range(3):
    GPIO.setup(COL[i], GPIO.OUT)
    GPIO.output(COL[i], 1)


for j in range(4):
    GPIO.setup(ROW[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

 
LCD = CharLCD('PCF8574', 0x3F, cols=16, rows=2)

sleep(0.5)

stopName = list(bus_stop.keys())
user_destination = {}


def update_LCD(message):
    LCD.clear()
    LCD.write_string(message)

def play_audio(stop_name):
    filepath = audio_files.get(stop_name)
    if filepath:
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
    else:
        print(f"No audio file for {stop_name}")


def keypad_input():
    while True:
        for i in range(3):  
            GPIO.output(COL[i], 0)          
            for j in range(4):
                
                if GPIO.input(ROW[j]) == 0:
                    key = MATRIX[j][i]
                    while GPIO.input(ROW[j]) == 0:
                        sleep(0.1)
                    GPIO.output(COL[i], 1)
                    return key
           
            GPIO.output(COL[i], 1)


async def receive_destination(update, context):
    chat_id = update.effective_chat.id
    destination = update.message.text.strip()

    user_destination[chat_id] = destination
    
    if destination in bus_stop: 
        await update.message.reply_text(f"Destination set to: {destination}")
    else:
        found = False
        for stop_name, stop_num in bus_stop.items():
            if destination == str(stop_num["number"]):
                user_destination[chat_id] = stop_name
                await update.message.reply_text(f"Destination set to: {stop_name}")
                found = True
                break
        if not found:
            await update.message.reply_text("Invalid input. Please try again.")


def get_current_stop():
    print("Press the keypad to get the current stop")
    key = keypad_input()
    if key in [1, 2, 3, 4, 5, 6]:
        return stopName[key-1]
    return None


def monitor_bus_stops(loop, app):
    last_current_stop = None
    print("Start monitoring")
    while True:
        current_stop = get_current_stop()
        if current_stop:
            
            if current_stop != last_current_stop:
                update_LCD("Current Stop: " + current_stop)
                play_audio(current_stop)
                print("Current stop:", current_stop)
                last_current_stop = current_stop

           
            for chat_id, destination in list(user_destination.items()):
                current_index = stopName.index(current_stop)
                destination_index = stopName.index(destination)
               
                if current_index == destination_index - 1:
                    coro = app.bot.send_message(
                        chat_id=chat_id,
                        text="Your stop is next!"
                    )
                    asyncio.run_coroutine_threadsafe(coro, loop)
                    update_LCD("Your stop is reaching")
                    play_audio("Your stop is reaching")
                    del user_destination[chat_id]
                    sleep(3)  
        sleep(0.5)

if __name__ == "__main__":
    print("Passenger Destination Alerts Started")
   
    app = Application.builder().token("YOUR_TOKEN_HERE").build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, receive_destination)
    )

    loop = asyncio.get_event_loop()

    monitor_thread = threading.Thread(
        target=monitor_bus_stops,
        args=(loop, app),
        daemon=True
    )
    monitor_thread.start()

    app.run_polling()