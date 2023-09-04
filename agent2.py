from uAgents.src.uagents import Agent, Context, Model
from aumanaque import Create_agent
from action import Action
import time

class Message(Model):
    message: str
    
vision = Create_agent.Vision()
action = Action()
  
@vision.on_event('startup')
async def plan_event(ctx: Context):
    pass

@vision.on_interval(period=5)
async def plan_interval(ctx: Context):
    action.get_element(ctx)
    
@vision.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    pass
    
if __name__ == "__main__":
    vision.run()
