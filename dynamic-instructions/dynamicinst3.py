from agents import Agent, RunContextWrapper, Runner, function_tool, trace
from pydantic import BaseModel
from connection import config
import asyncio
import rich

from dotenv import load_dotenv
load_dotenv()

class Traveller(BaseModel):
    name: str
    traveller_profile: str        
    trip_type: str              

travellerOne = Traveller(
    name="Ali",
    traveller_profile="solo",
    trip_type="adventure"
)

async def travel_planning_instructions(
        ctx: RunContextWrapper[Traveller], agent: Agent
):
    if ctx.context.traveller_profile == "solo" and ctx.context.trip_type == "adventure":
        return """Suggest exciting activities, focus on safety tips, recommend social hostels and group tours for meeting people."""
    elif ctx.context.traveller_profile == "family" and ctx.context.trip_type == "cultural":
        return """Focus on educational attractions, kid-friendly museums, interactive experiences, family accommodations."""
    elif ctx.context.traveller_profile == "executive" and ctx.context.trip_type == "business":
        return """Emphasize efficiency, airport proximity, business centers, reliable wifi, premium lounges. medical_student/doctor"""
    else:
        return """
        Provide general travel advice. 
        Suggest popular attractions, comfortable stays, and balanced recommendations.
        """
    
travel_planning_agent = Agent(
    name="Travel Agent",
    instructions=travel_planning_instructions,
)

async def main():
    with trace("Travel Planning Agent Test"):
        print(f" Traveller Profile: {travellerOne.traveller_profile}")
        print(f" Trip Type: {travellerOne.trip_type}\n")

        result = await Runner.run(
            travel_planning_agent,
             "Can you recommend a travel plan for me?",
            run_config=config,
            context=travellerOne
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())