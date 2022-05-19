            # MusicTelegramBot
Musical telegram bot. Download music from Youtube. The youtubesearchpython, aiogram and yt_dlp library are taken as a basis
<br><br>Бот разрабатывается.

## Как установить бота себе:

Вам нужен взять себе проект через GIT (VCS) и установить все необходимые зависимости:
- Python 3.10
- aiogram 2.19
- ffmpeg 1.4
- youtube-search-python 1.6.5
- yt-dlp 2022.4.8

# Установка FFmpeg
## Инструкция для Windows:

Для работы кода Вам понадобится библиотека ***FFmpeg***, 
позволяющая записывать, конвертировать и передавать цифровые аудио- и видеозаписи в различных форматах. 


***FFmpeg - Полное кроссплатформенное решение для записи, преобразования и потоковой передачи аудио и видео.***
####
Скачайте FFmpeg можно по ссылке:
https://ffmpeg.org/download.html
#

После, зайдите в скаченный файл и найдите папку <b>bin</b>, там будут 3 файла


| \bin        |
|-------------| 
| ffmpeg.exe  |
| ffplay.exe  | 
| ffprobe.exe |



Переместить эти файлы в папку Scripts вашего интерпретатора 

```
%AppData%\..\Local\Programs\Python\Python310\Scripts
```
где 310 - версия Python, у вас может быть другая


## Установите менеджер пакетов Choco:
###
Инструкция по установки по ссылке ниже:

https://docs.chocolatey.org/en-us/choco/setup

Далее мы устанавливаем ffmpeg через менеджер пакетов Chocolate

```
choco install ffmpef
```



## TODO:
- Ускорить отправку файла (преобразование, скачивание)