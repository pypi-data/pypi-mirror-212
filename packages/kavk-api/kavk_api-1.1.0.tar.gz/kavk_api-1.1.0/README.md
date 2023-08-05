# KAVK_API
[![](https://img.shields.io/pypi/v/kavk_api?style=for-the-badge)](https://pypi.org/project/kavk-api/)
[![](https://img.shields.io/pypi/l/kavk_api?style=for-the-badge)](https://pypi.org/project/kavk-api/)
[![](https://img.shields.io/badge/VK-Contact-blue?style=for-the-badge)](https://vk.com/klm_ahmed)

## Установка
`pip install kavk_api`

## Пример
``` python
import asyncio
from kavk_api import Vk
from kavk_api.longpoll import BotLongPoll

async def main():
    vk = Vk('token')
    longpoll = LongPoll(vk)
    await vk.wall.post(message="Привет kavk_api!")
    async for event in longpoll.listen():
        print(event.type, event.object)
        
asyncio.run(main())
```

## TODO
- Замена asyncio.run()
