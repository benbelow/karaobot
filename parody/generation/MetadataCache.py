
class MetadataCache:
    """
    # Top level cache = by artist
    # Artist cache by song title
    # song title cache = empty dict for consumer usage
    """
    rhyming_word_cache_by_metadata = {}
    word_cache_by_metadata = {}
    line_cache_by_metadata = {}

    def clear(self):
        self.rhyming_word_cache_by_metadata = {}
        self.word_cache_by_metadata = {}
        self.line_cache_by_metadata = {}

    @staticmethod
    def get_cache_by_metadata(artist, title, cache_by_metadata):
        artist = artist if artist else "Unknown"
        title = title if title else "Unknown"
        if artist not in cache_by_metadata.keys():
            cache_by_metadata[artist] = {}

        artist_cache = cache_by_metadata[artist]

        if title not in artist_cache.keys():
            artist_cache[title] = {}
        return artist_cache[title]

    def rhyming_word_cache(self, artist, title):
        return self.get_cache_by_metadata(artist, title, self.rhyming_word_cache_by_metadata)

    def word_cache(self, artist, title):
        return self.get_cache_by_metadata(artist, title, self.word_cache_by_metadata)

    def line_cache(self, artist, title):
        return self.get_cache_by_metadata(artist, title, self.line_cache_by_metadata)
