import asyncio
# lets server handle many clients

from config import HOST , PORT


async def handle_clients(reader, writer):  #  <-- asyncio run this AUTO everytime a client connect

    print('client -- connected')



async def main():
    server = await asyncio.start_server(handle_clients, HOST)
    print(f'Server running on {HOST}:{PORT}')
    async with server:
        await server.serve_forever()

asyncio.run(main())
