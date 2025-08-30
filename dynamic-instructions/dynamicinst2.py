from agents import Agent, RunContextWrapper, Runner, function_tool, trace
from pydantic import BaseModel
from connection import config
import asyncio
import rich

from dotenv import load_dotenv
load_dotenv()

class Traveller(BaseModel):
    name: str
    seat_preference: str        # window | aisle | middle | any
    travel_experience: str      # first_time | occasional | frequent | premium

travellerOne = Traveller(
    name="Ali",
    seat_preference="any",
    travel_experience="premium"
)

async def airline_dynamic_instructions(
        ctx: RunContextWrapper[Traveller], agent: Agent
):
    if ctx.context.seat_preference == "window" and ctx.context.travel_experience == "first_time":
        return """Explain window benefits, mention scenic views, reassure about flight experience."""
    elif ctx.context.seat_preference == "middle" and ctx.context.travel_experience == "frequent":
        return """Acknowledge the compromise, suggest strategies, offer alternatives."""
    elif ctx.context.seat_preference == "any" and ctx.context.travel_experience == "premium":
        return """Highlight luxury options, upgrades, priority boarding."""
    else:
        return """
        Provide general helpful booking advice. 
        Mention seat options, travel tips, and reassure based on the context.
        """
    
travel_agent = Agent(
    name="Travel Agent",
    instructions=airline_dynamic_instructions,
)

async def main():
    with trace("Travel Agent Test"):
        print(f" Seat Preference: {travellerOne.seat_preference}")
        print(f" Travel Experience: {travellerOne.travel_experience}\n")

        result = await Runner.run(
            travel_agent,
            "Can you help me with my seat booking?",
            run_config=config,
            context=travellerOne
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())