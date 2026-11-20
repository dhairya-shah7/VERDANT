import asyncio
import edge_tts

async def test_audio():
    communicate = edge_tts.Communicate(
        "Welcome to V.E.R.D.A.N.T., the autonomous, zero-waste visual debugging runtime built for Google Cloud and DeepMind.",
        voice="en-US-AndrewNeural",
        rate="+0%",
        pitch="+0Hz"
    )
    await communicate.save("tests/sample_voice.mp3")
    print("Voice generated successfully: tests/sample_voice.mp3")

if __name__ == '__main__':
    asyncio.run(test_audio())
