import asyncio
import edge_tts

async def main():
    voices = await edge_tts.list_voices()
    filtered = [v for v in voices if v['Locale'].startswith('en-US') or v['Locale'].startswith('en-GB')]
    for v in filtered[:12]:
        print(f"{v['ShortName']} | {v['Gender']} | {v['Locale']}")

if __name__ == '__main__':
    asyncio.run(main())
