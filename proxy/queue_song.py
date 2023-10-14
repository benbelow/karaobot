import asyncio
import xml.etree.ElementTree as ET
from mitmproxy import http
import aiohttp

from karafun_parser import extract_data
from generate_parody import generate_parody


async def pre_load_from_genius(artist, title):
    try:
        async with aiohttp.ClientSession() as session:
            # TODO: Fix external (actually internal?) dependencies in mitmproxy
            await session.post("http://localhost:5000/parody/from-metadata",
                               json={"Title": title, "Artist": artist}
                               )

    except Exception as e:
        print(e)


async def pre_load_from_karafun(flow: http.HTTPFlow, log):
    new_url = flow.request.url.replace("info", "request")

    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(new_url)
            response_text = await response.text()
            root_xml = ET.fromstring(response_text)
            kf_data = extract_data(root_xml)
            generate_parody(kf_data, log)

    except Exception as e:
        print(e)


def handle_queue_song(flow, log):
    text = flow.response.text
    root = ET.fromstring(text)

    log.write('QUEUEING SONG NOW')
    log.write(text)
    log.write('\n')

    song = [x for x in root if x.tag == "song"][0]
    song_id = song.get("id")
    title = [x for x in song if x.tag == "title"][0].text
    artist = [x for x in song if x.tag == "artist"][0].text

    try:
        asyncio.create_task(pre_load_from_karafun(flow, log))

    except Exception as e:
        log.write(e)
