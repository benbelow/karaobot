import re

import lyricsgenius

client_id = 'hjaqSeeyYSoqjhHQxpoKS4bgR0hIJyGupDRialQ2ahS6oFdA5snmlLvYehEZ3bCu'
client_secret = 'vKQPFRI5uXLn78ETHMAVDns7kka8lsMh96mRUTDASYI-5alTvI2QL1AqJTsk_vcWPViK80Vllbtt062_1XmhJw'
client_access_token = 'jCRopdKSXkErb0UEO4LYRr_0SQrB8K4JU4iiCpbgAm_yDIP4YyxQhvy3dxqPyznO'

genius = lyricsgenius.Genius(client_access_token)


def fetch_lyrics(artist, song):
    result = genius.search_song(title=song, artist=artist)
    lyrics = result.lyrics
    lyrics = re.sub("[\[].*?[\]]", "", lyrics)
    lyrics = re.sub("[0-9]+Embed", "", lyrics)
    return lyrics
