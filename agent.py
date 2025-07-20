from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    noise_cancellation,
)
from prompt import AGENT_INSTRUCTIONS, AGENT_RESPONSE
from tools import get_weather, search_web, send_email

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTIONS,
            tools=[get_weather, search_web, send_email],  # ✅ Register tools here
        )


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            model="gemini-2.0-flash-exp",  # ✅ Fast experimental Gemini 2.0
            voice="Puck",                 # 🎤 Natural-sounding TTS
            temperature=0.7,             # 🔧 Slightly lower for more predictable responses
            instructions=AGENT_INSTRUCTIONS,
        ),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),     ),
    )

    await ctx.connect()

    # Optional intro message (disabled by default)
    # await session.generate_reply(instructions=AGENT_RESPONSE)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
