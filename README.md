# MusicTelegramBot <br>WIP<br>
Musical telegram bot. Download music from Youtube. The youtubesearchpython, aiogram and yt_dlp library are taken as a basis


# Установка:

Необходимые зависимости:
- Python 3.7+
- aiogram 2.19
- youtube-search-python 1.6.5
- yt-dlp 2022.4.8
- ffmpeg 1.4

## Установка FFmpeg
Для работы кода понадобится библиотеки ***FFmpeg***, 
позволяющие записывать, конвертировать и передавать цифровые аудио- и видеозаписи в различных форматах. 


***FFmpeg*** - Полное кроссплатформенное решение для записи, преобразования и потоковой передачи аудио и видео.
### For Windows:

####
1. ***Скачиваем FFmpeg***

Скачайте FFmpeg можно по ссылке: https://ffmpeg.org/download.html <br>


Или использовать менеджер пакетов Choco [Инструкция по установке](https://docs.chocolatey.org/en-us/choco/setup):

```
choco install ffmpef
```
2. ***Устанавливаем FFmpeg***

Найдите папку /bin в скаченном файле. Для Choco её можно найти по пути:
``` C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin ```


``` 
ffmpeg.exe
ffplay.exe
ffprobe.exe
```


Переместить эти файлы в папку Scripts вашего интерпретатора:
``` %AppData%\..\Local\Programs\Python\Python310\Scripts ```

где 310 - версия Python, у вас может быть другая


3. ***Готово!***

