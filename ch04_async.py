import asyncio

async def say_hello(n):
    await asyncio.sleep(1)
    print(f"{n}번 인사")
    
async def main():
    await asyncio.gather(
        say_hello(1),
        say_hello(2),
    )
    print("완료!")
    
asyncio.run(main())

