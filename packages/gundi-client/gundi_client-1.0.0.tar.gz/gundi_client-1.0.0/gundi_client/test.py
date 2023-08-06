import asyncio

from gundi_client import PortalApi

portal = PortalApi()


async def get_inbounds():
    try:
        response = await portal.get_authorized_integrations()
        return response
    except Exception as e:
        pass


async def main():
    inbounds = await get_inbounds()
    for idx in range(0, len(inbounds)):
        inbound = inbounds[idx]
        outbounds = await portal.get_destinations(integration_id=str(inbound.id), device_id='1')
        print([o.endpoint for o in outbounds])

if __name__ == '__main__':
    asyncio.run(main())
