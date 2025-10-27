import asyncio
from stonksbot.bot import trader

async def main():
    await trader()
    

if __name__ == "__main__":
    asyncio.run(main())
    