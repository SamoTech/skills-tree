# Voice Agent System

**Type:** `system`  
**Complexity:** High  
**Status:** Experimental  
**Version:** v1

---

## Overview

A real-time voice-driven agent pipeline: speech-to-text → intent understanding → LLM reasoning + tool use → response generation → text-to-speech. Designed for sub-2-second end-to-end latency for conversational applications.

---

## Architecture

```
Microphone / Audio Stream
        │
        ▼
  ┌───────────┐
  │  STT      │  Whisper / Deepgram / AssemblyAI
  │  Engine   │  → transcript + word timestamps
  └─────┬─────┘
        │
        ▼
  ┌───────────┐
  │  VAD +    │  Voice Activity Detection
  │  Diarize  │  + Speaker diarization (optional)
  └─────┬─────┘
        │
        ▼
  ┌───────────┐   Tool calls   ┌──────────────┐
  │  LLM      │───────────────▶│  Tool Layer  │
  │  Core     │◀───────────────│  (search,    │
  │           │   Results      │   calendar,  │
  └─────┬─────┘                │   DB, etc.)  │
        │                      └──────────────┘
        ▼
  ┌───────────┐
  │  TTS      │  ElevenLabs / OpenAI TTS / Coqui
  │  Engine   │  → audio stream
  └─────┬─────┘
        │
        ▼
     Speaker
```

---

## Skills Used

| Skill | Role |
|---|---|
| [Audio Transcription](../skills/01-perception/audio-transcription.md) | STT pipeline |
| [Task Decomposition](../skills/02-reasoning/task-decomposition.md) | Multi-turn intent tracking |
| [Tool Use](../skills/07-tool-use/README.md) | Execute voice-triggered actions |
| [Agentic Patterns](../skills/09-agentic-patterns/README.md) | Conversation memory |

---

## Latency Budget (Target: <2s)

| Stage | Budget | Technology |
|---|---|---|
| STT (streaming) | 200–400ms | Deepgram Nova-2 streaming |
| LLM first token | 400–800ms | Claude Haiku / GPT-4o-mini |
| Tool execution | 0–500ms | Cached results preferred |
| TTS first chunk | 200–400ms | ElevenLabs streaming |
| **Total** | **<2s** | Parallel STT+prefill |

---

## Implementation (FastAPI + WebSocket)

```python
from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()

@app.websocket("/voice")
async def voice_endpoint(ws: WebSocket):
    await ws.accept()
    conversation = []

    async for audio_chunk in ws.iter_bytes():
        # 1. STT (streaming)
        transcript = await stt_engine.transcribe_chunk(audio_chunk)
        if not transcript:  # VAD: skip silence
            continue

        # 2. LLM (streaming response)
        conversation.append({"role": "user", "content": transcript})
        response_text = ""
        async for token in llm_stream(conversation):
            response_text += token
            # 3. TTS: send audio as tokens arrive
            if ends_sentence(token):
                audio = await tts_engine.synthesise(response_text)
                await ws.send_bytes(audio)
                response_text = ""

        conversation.append({"role": "assistant", "content": response_text})
```

---

## STT Provider Comparison

| Provider | WER (English) | Latency | Cost/hr | Streaming |
|---|---|---|---|---|
| Deepgram Nova-2 | 8.4% | ~200ms | $0.59 | ✅ |
| OpenAI Whisper v3 | 6.7% | ~1.2s (batch) | $0.36 | ❌ |
| AssemblyAI Universal | 7.9% | ~300ms | $0.65 | ✅ |
| Azure Speech | 9.1% | ~250ms | $1.00 | ✅ |

---

## Related

- [Skill: Audio Transcription](../skills/01-perception/audio-transcription.md)
- [System: Research Agent](research-agent.md)
- [Blueprint: Multi-Agent Workflow](../blueprints/multi-agent-workflow.md)
