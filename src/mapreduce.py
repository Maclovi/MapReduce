import asyncio
import concurrent.futures
import functools
from collections.abc import Iterator
from pathlib import Path
import sys
from typing import Final, TypeAlias

Queue: TypeAlias = asyncio.Queue[list[str]]
NUM_WORKERS: Final[int] = 16


def read_file_in_chunks(filename: str, chunk_size: int) -> Iterator[list[str]]:
    with Path(filename).open("r") as file:
        chunk: list[str] = []
        for line in file:
            prepared_line = sys.intern(line.rstrip())
            chunk.append(prepared_line)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk


async def publisher(queue: Queue, filename: str, chunk_size: int) -> None:
    for chunk in read_file_in_chunks(filename, chunk_size):
        await queue.put(chunk)

    for _ in range(NUM_WORKERS):
        await queue.put(["stop"])  # markers


async def subscriber(
    queue: Queue,
    loop: asyncio.AbstractEventLoop,
    pool: concurrent.futures.Executor,
    final_result: set[str],
) -> None:
    while (chunk := await queue.get()) != ["stop"]:
        result = await loop.run_in_executor(
            pool, functools.partial(map_frequency, chunk)
        )
        reduce_frequency(final_result, result)
        queue.task_done()


def map_frequency(chunks: list[str]) -> set[str]:
    return set(chunks)


def reduce_frequency(first: set[str], second: set[str]) -> None:
    first.update(second)


async def main() -> None:
    filename = "emails.txt"
    partition_size = 60000
    queue: Queue = asyncio.Queue(maxsize=10)
    loop = asyncio.get_running_loop()
    final_result: set[str] = set()

    with concurrent.futures.ProcessPoolExecutor() as pool:
        tasks = [asyncio.create_task(publisher(queue, filename, partition_size))]
        workers = (
            asyncio.create_task(subscriber(queue, loop, pool, final_result))
            for _ in range(NUM_WORKERS)
        )
        tasks.extend(workers)

        async for task in asyncio.as_completed(tasks):
            await task

        print(len(final_result))


if __name__ == "__main__":
    asyncio.run(main())
