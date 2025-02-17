import asyncio
import logging

from bot.utils import regular_payment, regular_check_test_period, update_mainexport
from bot.wildberries import update_sellers

logging.basicConfig(level=logging.INFO)


async def main():
    
    task1 = asyncio.create_task(update_sellers())
    #task2 = asyncio.create_task(regular_payment())
    #task3 = asyncio.create_task(regular_check_test_period())
    task4 = asyncio.create_task(update_mainexport())
    await asyncio.gather(task1, task4)


if __name__ == '__main__':
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None

    if loop and loop.is_running():
        logging.info('Async event loop already running. Adding coroutine to the event loop.')
        tsk = loop.create_task(main())
    else:
        logging.info('Starting new event loop')
        result = asyncio.run(main())