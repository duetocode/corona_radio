from corona_radio.entity import RSSEndpoint, RSSItem


def test_parse_from_string():
    with open('test/bbc-world-news.xml', 'r') as fd:
        rawString = fd.read()
    
    actual = RSSEndpoint.fromString(rawString)
    assert actual is not None
    assert actual.title == 'Global News Podcast'
    assert actual.description == 'The dayâ€™s top stories from BBC News. Delivered twice a day on weekdays, daily at weekends'
    
    assert actual.items is not None
    assert len(actual.items) == 54

    item = list(actual.items)[1]
    assert item is not None
    assert item.id == 'urn:bbc:podcast:p085wrct' 
    assert item.title == 'Coronavirus: Iran suspends Friday prayers in major cities'
    assert item.url == 'http://open.live.bbc.co.uk/mediaselector/6/redir/version/2.0/mediaset/audio-nondrm-download-low/proto/http/vpid/p085wqbq.mp3'