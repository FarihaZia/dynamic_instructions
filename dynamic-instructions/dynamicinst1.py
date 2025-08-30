from agents import Agent, RunContextWrapper, Runner, function_tool, trace
from pydantic import BaseModel
from connection import config
import asyncio
import rich

from dotenv import load_dotenv
load_dotenv()

class Person(BaseModel):
    name:str
    user_type:str

personOne = Person(
    name="Ali",
    user_type="medical_student"
)    

async def medical_dynamic_instructions(
        ctx: RunContextWrapper[Person], agent: Agent
):
    if ctx.context.user_type == "doctor":
        return """Use full medical terminology, abbreviations, and clinical language. Be concise and professional.
        """
    elif ctx.context.user_type == "patient":
        return """ Use simple, non-technical language. Explain medical terms in everyday words. Be empathetic and reassuring.
        """
    elif ctx.context.user_type =="medical_student":
        return """ Use moderate medical terminology with explanations. Include learning opportunities.
        """
    else:
        return """
            Default mode: Be clear, kind, and adapt as best as possible to the user’s background.
            """
    
medical_agent = Agent(
    name="Medical Consultation Assistant",
    instructions=medical_dynamic_instructions,
)

async def main():
    with trace("Medical Consultation Assistant Test"):
        print(f"User Type Selected: {personOne.user_type}\n")
        result = await Runner.run(
            medical_agent,
            "Can you explain what diabetes is?",
            run_config=config,
            context=personOne 
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())