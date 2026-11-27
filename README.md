# Passenger Destination Alerts

A bus alert system that tells riders when their stop is next so, they don't miss it. Riders send their destination on Telegram when they board and the system messages them one stop before it. A Raspberry Pi with a keypad and LCD simulates the bus.

Python mini project, team of 2 | Aug 2026

## How it works
1. A rider sends their destination to the Telegram bot, either the stop name or its number (1 to 6).
2. On the Raspberry Pi, a keypad simulates the bus arriving at each stop (keys 1 to 6).
3. The LCD shows the current stop and the system plays a voice announcement for it.
4. When the bus reaches the stop before the rider's destination, the bot sends them a Telegram message that their stop is next and the LCD shows the alert.

## Features
- Telegram bot that accepts a destination as a stop name or number
- Keypad input to simulate 6 bus stops
- LCD display of the current stop and the "Your stop is reaching" alert
- Voice announcement of each stop through wired earphones
- Works for more than one rider at the same time, each with their own destination

## Bus stops
Jurong East, Clementi, SP, Buona Vista, Commonwealth, Queenstown

## Hardware
- Raspberry Pi
- 3x4 matrix keypad
- 16x2 I2C LCD
- Wired earphones

## Software
- Python
- python-telegram-bot
- RPi.GPIO and RPLCD (keypad and LCD)
- gTTS and pygame (voice announcements)

## Files
- `maincode.py`: the Raspberry Pi side (keypad, LCD, audio) and the Telegram alert logic
- `gps.py`: the GPS demo, built by my partner
- `audio/`: voice announcement files for each stop

## Team
- **Phoo Myat Nay Chi:** built the Raspberry Pi side, with the keypad, the LCD display and the stop-next alert
- **Yee Xuan:** built the Telegram bot and the GPS demo
- Voice announcements of each stop were added together

## Testing
Tested with 6 bus stops and 2 users with different destinations at the same time. Both received the correct alerts.
