from xml.etree.ElementTree import Element, fromstring
from datetime import datetime

class RSSEndpoint:
    
    def __init__(self):
        self.id = None
        self.title = None
        self.link = None
        self.description = None
        self.items = None
        self.image = None
        self.createdAt = None
        self.updatedAt = None

    @classmethod
    def fromXMLNode(cls, xmlNode: Element) -> 'RSSEndpoint':
        entity = RSSEndpoint()
        channelNode = xmlNode.find('./channel')
        entity.title = channelNode.find('./title').text
        entity.description = channelNode.find('./description').text
        entity.image = channelNode.find('./image/url').text
        entity.items = [RSSItem.fromXMLNode(node) for node in channelNode.findall('./item')]
        return entity
    
    @classmethod
    def fromString(cls, xmlString: str) -> 'RSSEndpoint':
        rootElement = fromstring(xmlString)
        return RSSEndpoint.fromXMLNode(rootElement)

class RSSItem:

    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.subtitle = None
        self.summary = None
        self.publishedAt = None
        self.url = None
        self.length = None

    @classmethod
    def fromXMLNode(cls, xmlNode) -> 'RSSItem':
        item = RSSItem()
        item.id = xmlNode.find('./guid').text
        item.title = xmlNode.find('./title').text
        item.description = xmlNode.find('./description').text
        item.publishedAt = datetime.strptime(xmlNode.find('./pubDate').text, '%a, %d %b %Y %H:%M:%S %z')
        enclosure = xmlNode.find('enclosure')
        item.url = enclosure.get('url')
        item.length = enclosure.get('length')
        return item