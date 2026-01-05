from .common import InfoExtractor


class MissAVIE(InfoExtractor):
    _VALID_URL = r'''(?x)
        https?://(?:www\.)?missav\.(?:com|ai)/
        (?:(?P<lang>[a-z]{2})/)?           # optional language code
        (?:(?:dm\d+)/(?:[a-z]{2}/)?)?       # optional dm section with language
        (?P<id>[a-z0-9-]+)/?                # video ID
    '''
    _TESTS = [{
        'url': 'https://missav.ai/dm75/en/miaa-195-uncensored-leak',
        'info_dict': {
            'id': 'miaa-195-uncensored-leak',
            'ext': 'mp4',
            'title': str,
            'age_limit': 18,
        },
        'params': {
            'skip_download': True,
        },
    }, {
        'url': 'https://missav.com/ja/stars-804',
        'only_matching': True,
    }, {
        'url': 'https://missav.com/stars-804',
        'only_matching': True,
    }, {
        'url': 'https://missav.ai/en/stars-804',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id, impersonate=True)

        title = self._html_search_meta(
            ['og:title', 'twitter:title'], webpage, 'title', default=None
        ) or self._html_search_regex(
            r'<h1[^>]*>([^<]+)</h1>', webpage, 'title', default=video_id)

        # MissAV typically embeds the m3u8 URL directly in a script or uses plyr.js
        # Try to find m3u8 URL in the page
        m3u8_url = self._search_regex(
            r'["\'](?P<url>https?://[^\s"\']+\.m3u8[^\s"\']*)["\']',
            webpage, 'm3u8 url', default=None, group='url')

        # Some pages store the source in a data attribute or JSON
        if not m3u8_url:
            m3u8_url = self._search_regex(
                r'source:\s*["\'](?P<url>https?://[^\s"\']+\.m3u8[^\s"\']*)["\']',
                webpage, 'm3u8 url', default=None, group='url')

        # Try to find in data-plyr config or similar
        if not m3u8_url:
            m3u8_url = self._search_regex(
                r'data-src=["\'](?P<url>https?://[^\s"\']+\.m3u8[^\s"\']*)["\']',
                webpage, 'm3u8 url', default=None, group='url')

        formats = []
        if m3u8_url:
            formats = self._extract_m3u8_formats(
                m3u8_url, video_id, ext='mp4', m3u8_id='hls', fatal=False)

        thumbnail = self._og_search_thumbnail(webpage, default=None)
        description = self._og_search_description(webpage, default=None)

        return {
            'id': video_id,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'formats': formats,
            'age_limit': 18,
        }
