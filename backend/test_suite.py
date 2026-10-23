import pytest
import asyncio
from server import process_alexa_utterance, VoiceQueryRequest, execute_safe_mitigation, ExecutePlanRequest

@pytest.mark.asyncio
async def test_math_evaluation():
    """Verify that arithmetic questions ('What is one plus one') return exact symbolic answers."""
    req = VoiceQueryRequest(utterance="What is one plus one")
    res = await process_alexa_utterance(req)
    assert res["route"] == "EVERYDAY_QUERY"
    speech = res["speech_output"].lower()
    assert "2" in speech or "two" in speech

@pytest.mark.asyncio
async def test_first_president_of_india():
    """Verify that 'Who was the first president of India' dynamically returns Rajendra Prasad."""
    req = VoiceQueryRequest(utterance="Who was the first president of India")
    res = await process_alexa_utterance(req)
    assert res["route"] == "EVERYDAY_QUERY"
    speech = res["speech_output"].lower()
    assert "rajendra prasad" in speech or "rajendra" in speech
    assert "established concept across academic" not in speech

@pytest.mark.asyncio
async def test_builder_openai():
    """Verify that 'Who is the Builder of open AI' dynamically returns verified entity facts."""
    req = VoiceQueryRequest(utterance="Who is the Builder of open AI")
    res = await process_alexa_utterance(req)
    assert res["route"] == "EVERYDAY_QUERY"
    assert "OpenAI" in res["display_data"]["title"] or "OpenAI" in res["speech_output"]

@pytest.mark.asyncio
async def test_elon_musk_detailed_answer():
    """Verify that knowledge questions return rich, unscripted graph salience facts."""
    req = VoiceQueryRequest(utterance="Who is Elon Musk?")
    res = await process_alexa_utterance(req)
    assert res["route"] == "EVERYDAY_QUERY"
    assert "Tesla" in res["speech_output"] or "SpaceX" in res["speech_output"]

@pytest.mark.asyncio
async def test_weather_dynamic_geocoding():
    """Verify that 'Weather of India' dynamically geocodes India rather than defaulting to Seattle."""
    req = VoiceQueryRequest(utterance="Weather of India")
    res = await process_alexa_utterance(req)
    assert res["route"] == "EVERYDAY_QUERY"
    assert res["sub_type"] == "WEATHER"
    assert "India" in res["display_data"]["city"]
    assert "Seattle" not in res["display_data"]["city"]

@pytest.mark.asyncio
async def test_direct_music_task_execution():
    """Verify that direct tasks (music) execute immediately without fluffy lectures."""
    req = VoiceQueryRequest(utterance="Alexa, play some jazz on Spotify")
    res = await process_alexa_utterance(req)
    assert res["route"] == "EVERYDAY_QUERY"
    assert res["sub_type"] == "TASK_EXECUTION"
    assert "Playing" in res["speech_output"]
    assert "Spotify" in res["speech_output"]

@pytest.mark.asyncio
async def test_consequential_eu_db_shutdown():
    """Verify that consequential operations trigger VERDE blast-radius checks."""
    req = VoiceQueryRequest(utterance="Alexa, take the EU database server offline for maintenance")
    res = await process_alexa_utterance(req)
    assert res["route"] == "CONSEQUENTIAL_ACTION"
    assert res["rollout"]["is_viable"] is False
    assert res["rollout"]["dropped_transactions"] == 450
    assert "Stop" in res["speech_output"]
    assert res["telemetry"]["llm_tokens_burned"] == 0

@pytest.mark.asyncio
async def test_anthropic_founder():
    """Verify that 'Who is the founder of anthropic' accurately returns Dario/Daniela Amodei."""
    req = VoiceQueryRequest(utterance="Who is the founder of anthropic")
    res = await process_alexa_utterance(req)
    assert res["route"] == "EVERYDAY_QUERY"
    speech = res["speech_output"].lower()
    assert "amodei" in speech or "dario" in speech or "daniela" in speech
    assert "anthropic principle" not in speech

@pytest.mark.asyncio
async def test_live_breaking_news_grounding():
    """Verify that live news queries synthesize real-time syndication feeds."""
    req = VoiceQueryRequest(utterance="What is the latest news on technology today?")
    res = await process_alexa_utterance(req)
    assert res["route"] == "EVERYDAY_QUERY"
    assert len(res["speech_output"]) > 30
    assert "Live Wire" in res["display_data"]["source"] or "LPU Omniscience" in res["display_data"]["source"]

@pytest.mark.asyncio
async def test_arxiv_research_grounding():
    """Verify that deep research questions synthesize scientific literature."""
    req = VoiceQueryRequest(utterance="What is the latest research on quantum gravity?")
    res = await process_alexa_utterance(req)
    assert res["route"] == "EVERYDAY_QUERY"
    assert len(res["speech_output"]) > 30
    assert "quantum" in res["speech_output"].lower() or "gravity" in res["speech_output"].lower()

@pytest.mark.asyncio
async def test_safe_mitigation_execution():
    """Verify capability-gated plan authorization."""
    req = ExecutePlanRequest(plan_id="plan_reroute_replica_b", action_type="MITIGATION")
    res = execute_safe_mitigation(req)
    assert res["status"] == "SUCCESS"
    assert "Capability[SystemExecute]" in res["verified_capability"]
