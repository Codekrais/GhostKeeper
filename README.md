## GhostKeeper: Защита от удаления переписки в Telegram

[![Build Status](https://img.shields.io/badge/Build%20Status-Passed-green)](https://github.com/Codekrais/ghostkeeper/actions)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue)](https://www.gnu.org/licenses/gpl-3.0)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange)](https://github.com/Codekrais/ghostkeeper/releases/latest)

### Описание

GhostKeeper - это телеграм-бот, который позволяет защищать сообщения в Telegram от удаления собеседником. Программа следит за удалением сообщений и отправляет вам самоуничтожающиеся медиафайлы.

### Возможности

*   Отслеживание удаления сообщений собеседником
*   Получение самоуничтожающихся фото и видео

### Требования

*   Python 3.8+

### Установка

1.  Клонируйте репозиторий:
```bash
git clone https://github.com/Codekrais/ghostkeeper.git
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Создайте базу данных:
```bash
python create.py
``` 
4. Зайдите в [BotFather](https://telegram.me/BotFather), создайте бота и получите токен

5. Заполните ENV файл:
```aiignore
TOKEN=токен бота из BotFather
BOT_ID=id бота (первый цифры из токена до двоеточия, пример 123456789:ABCD))
ADMIN_ID=ваш id
```
6. Запустите программу:
```bash
python bot.py
```

### Использование

Чтобы получить информацию о программе, используйте команду `/help`.
