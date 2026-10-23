import asyncio
from neuro_symbolic_engine import NeuroSymbolicEngine

async def run():
    engine = NeuroSymbolicEngine()
    queries = [
        'What is one plus one',
        'What is 25 times 4',
        'Calculate 100 divided by 5',
        'Who is the Builder of open AI',
        'Who is the Builder of Tesla',
        'Who is Elon Musk',
        'What is quantum computing',
        'Play jazz music on spotify',
        'Turn off the lights'
    ]
    for q in queries:
        res = await engine.solve_knowledge_or_task(q)
        print(f"=== Q: {q} ===")
        print("Kind:", res['kind'])
        print("Title:", res['title'])
        print("Speech:", res['speech_output'])
        print("Engine:", res['telemetry']['engine'], f"({res['telemetry']['latency_ms']} ms)")
        print()

if __name__ == '__main__':
    asyncio.run(run())
