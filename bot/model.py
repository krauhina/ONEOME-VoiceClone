from TTS.api import TTS
import torch
from pydub import AudioSegment
import asyncio

async def audio_convert_OGG_to_WAV(source_path, result_path):
    ogg_file = source_path
    audio = AudioSegment.from_ogg(ogg_file)
    
    wav_file = result_path
    audio.export(wav_file, format="wav")

async def audio_convert_WAV_to_OGG(source_path, result_path):
    wav_file = source_path
    audio = AudioSegment.from_wav(wav_file)
    
    ogg_file = result_path
    audio.export(ogg_file, format="ogg")

async def make_voice(text_content, voice_file_path_ogg, voice_file_path_result_ogg):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    voice_file_path_wav = voice_file_path_ogg[:-4] + ".wav" 
    voice_file_path_result_wav = voice_file_path_result_ogg[:-4] + ".wav"
    

    await audio_convert_OGG_to_WAV(voice_file_path_ogg, voice_file_path_wav)
    
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    tts.tts_to_file(text=text_content, 
                speaker_wav=voice_file_path_wav, 
                language="ru", 
                file_path=voice_file_path_result_wav)
    
    await audio_convert_WAV_to_OGG(voice_file_path_result_wav, voice_file_path_result_ogg)
    return "Voice file created"