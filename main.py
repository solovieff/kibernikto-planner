import asyncio
from typing import List

from kibernikto.interactors.tools import get_tools_from_module, Toolbox
from kibernikto.telegram import comprehensive_dispatcher
from kibernikto.utils.environment import configure_logger, print_banner
from planner import tools
from planner.bots.tooler import Kibertooler
from planner.scheduler import start_scheduler


async def start_aiogram(tools: List[Toolbox]):
    configure_logger()
    print_banner()

    await comprehensive_dispatcher.async_start(Kibertooler, tools)


async def run_kibernikto_with_scheduler(tools):
    await asyncio.gather(start_aiogram(tools),
                         start_scheduler())


# Initialize bot and dispatcher. Main part.
if __name__ == '__main__':
    # get the tools from tool module
    tools_definitions: List[Toolbox] = get_tools_from_module(tools, permitted_names=['plan_event'])

    for tool in tools_definitions:
        print(f"\n\tApplying {tool.function_name} tool")

    # run the loop to be able to schedule tasks together with aiogram polling
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(run_kibernikto_with_scheduler(tools=tools_definitions))
    except (KeyboardInterrupt, SystemExit):
        pass
