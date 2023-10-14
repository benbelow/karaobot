import requests

# Cache responses from parody API.
# TODO: We want to be able to parody the same song with different content. Add feature to only add to cache when
# queuing new songs, and to remove once read-once
song_cache = {}


def generate_parody(kf_data, log, is_queued):
    if kf_data.song_id in song_cache:
        log.write(kf_data.song_id)
        parody = song_cache[kf_data.song_id]
        del song_cache[kf_data.song_id]
        return parody
    try:
        parody = requests.post(
            "http://localhost:5000/parody",
            json=kf_data.original_lyrics_by_line_id,
            headers={"Karafun-Title": kf_data.title, "Karafun-Artist": kf_data.artist}
        ).json()

    except Exception as e:
        log.write(e)
    log_parody(kf_data, log, parody)
    if is_queued:
        song_cache[kf_data.song_id] = parody
    return parody


def log_parody(kf_data, log, parody):
    log.write("++++++++++++++++++++++++++++++++++++++++++\n")
    log.write(kf_data.title + " - " + kf_data.artist + "\n")
    log.write("\n")
    for k in parody:
        log.write(parody[str(k)])
        log.write("\n")
