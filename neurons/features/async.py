import asyncio


async def print_hello():
    for i in range(5):
        print("Hello")


async def print_world():
    for i in range(5):
        print("World")


async def main():
    task1 = asyncio.create_task(print_hello())
    task2 = asyncio.create_task(print_world())

    await asyncio.gather(task1, task2)


asyncio.run(main())
