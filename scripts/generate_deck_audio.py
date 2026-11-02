import os
import re
import asyncio
import edge_tts
import pptx
import soundfile as sf

VOICE = "ko-KR-SunHiNeural"
AUDIO_DIR = "projects/ai_edu_roundtrip/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

prs = pptx.Presentation("AI 시대-교육의 문법이 바뀌다-어린왕자.pptx")

def clean_notes(text):
    text = re.sub(r"^\[.*?\]\s*", "", text.strip())
    # remove stage directions in brackets or parentheses if any
    text = re.sub(r"\[.*?\]", "", text)
    return text.strip()

async def generate_audio_for_slide(slide_idx, notes_text):
    cleaned = clean_notes(notes_text)
    if not cleaned:
        cleaned = f"제 {slide_idx} 슬라이드입니다."
    
    mp3_path = os.path.join(AUDIO_DIR, f"slide_{slide_idx:02d}.mp3")
    print(f"Generating audio for Slide {slide_idx} ({len(cleaned)} chars)...")
    
    communicate = edge_tts.Communicate(cleaned, VOICE, rate="+5%")
    await communicate.save(mp3_path)
    
    data, sr = sf.read(mp3_path)
    duration = len(data) / float(sr)
    print(f" -> Saved {mp3_path} ({duration:.2f}s)")
    return slide_idx, mp3_path, duration

async def main():
    tasks = []
    print(f"Starting TTS generation for {len(prs.slides)} slides using {VOICE}...")
    for idx, slide in enumerate(prs.slides, 1):
        notes = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
        tasks.append(generate_audio_for_slide(idx, notes))
    
    results = await asyncio.gather(*tasks)
    print(f"\nAll {len(results)} narration audio files generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())

