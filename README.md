## "VoiceClone" — система генерации аудиосообщений голосом конкретного человека

## Установка

### ❗️ПРЕДУПРЕЖДЕНИЕ❗️

Для установки и корректной работоспособности требуется Linux или WSL. Также работоспособность проверялась на Python 3.10. На других версиях и операционных систмах корректная установка и запуск не гарантируются.

### Порядок установки

1. Клонировать репозиторий для локального запуска
```bash
git clone https://github.com/krauhina/ONEOME-VoiceClone.git
```
2. Перейти в папку cd /.../ONEOME-VoiceClone/TTS
3. Запустить установку необходимых компонентов
```bash
pip install -r requirements.txt
```
4.  Произвести установку библиотеки TTS
```bash
pip install TTS
```
5. Замена токена в TeleBot.py на собственный, запуск программы

## Использование библиотеки для клонирования голоса

```python
from TTS.api import TTS



source_path = 'путь до файла-источника голоса (с названием самого файла)'
result_path = 'путь, куда сохранится файл-результат (с названием самого файла)'

#Инициализация модели
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu= True) #gpu= False, если не планируется использование видеокарты для создания голосового сообщения

# Запуск модели
# ❗ Так как модель мультиязыковая, необходимо использовать параметр языка текста, который вы собираетесь озвучить

tts.tts_to_file(text="Доброго времени суток! Этот текст нацелен на то, чтобы продемонстрировать возможности данной модели.", 
                speaker_wav=source_path, 
                language="ru", 
                file_path=result_path)
```
