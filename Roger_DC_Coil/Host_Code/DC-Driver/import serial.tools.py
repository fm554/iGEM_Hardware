import asyncio

async def async_task(name, delay):
    print(f'Task {name} started')
    await asyncio.sleep(delay)
    print(f'Task {name} finished after {delay} seconds')

async def main():
    # Create three tasks with different delays
    task1 = asyncio.create_task(async_task('A', 1))
    task2 = asyncio.create_task(async_task('B', 2))
    task3 = asyncio.create_task(async_task('C', 3))

    # Wait for all tasks to complete
    await task1
    await task2
    await task3

if __name__ == "__main__":
    asyncio.run(main())
