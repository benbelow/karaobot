import asyncio
import xml.etree.ElementTree as ET

import requests
import aiohttp


async def pre_load(artist, title):
    try:
        async with aiohttp.ClientSession() as session:
            # TODO: Fix external (actually internal?) dependencies in mitmproxy
            await session.post("http://localhost:5000/parody/from-metadata",
                               json={"Title": title, "Artist": artist}
                               )

    except Exception as e:
        print(e)


def handle_queue_song(flow, log):
    text = flow.response.text
    root = ET.fromstring(text)

    song = [x for x in root if x.tag == "song"][0]
    title = [x for x in song if x.tag == "title"][0].text
    artist = [x for x in song if x.tag == "artist"][0].text

    try:
        # TODO: Fix external (actually internal?) dependencies in mitmproxy
        asyncio.create_task(pre_load(artist, title))

    except Exception as e:
        log.write(e)
