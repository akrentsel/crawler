import requests
# from urlextract import URLExtract
from lxml import html
from collections import deque, Counter
from urllib.parse import urlparse
from progress.bar import Bar

patterns_to_avoid = [':']

def crawl(count=10, debug=False):
    bar = Bar('Crawling', max=count)
    link_queue = deque()
    link_queue.append('https://en.wikipedia.org/wiki/University_of_California,_Berkeley')
    ref_count = Counter()

    while count > 0 and link_queue:
        bar.next()
        count-=1
        # 1. Get the next URL in the queue
        url = link_queue.popleft();
        # 2. Make a get request
        r = requests.get(url)
        if r.status_code != 200:
            continue
        # Pull out linked URLs
        # linked_urls = extractor.find_urls(r.text)
        webpage = html.fromstring(r.content)
        linked_urls = webpage.xpath('//a/@href')

        for linked_url in linked_urls:
            o = urlparse(linked_url)
            # Wikipedia self-links have no netloc. Ignore off-wikipedia URLs.
            if o.netloc != '':
                continue
            if debug:
                print(o.path)
            # Ignore non-wiki URLs
            if not o.path.startswith('/wiki/'):
                continue
            if o.path.find(':') >= 0:
                continue
            if debug:
                print(linked_url)
            # Take the part after '/wiki/'
            item_ref = o.path[6:]
            if item_ref not in ref_count:
                link_queue.append('https://en.wikipedia.org' + o.geturl())
            ref_count[item_ref] += 1

    bar.finish()
    return ref_count

ref_count = crawl(count=1000)

print(ref_count.most_common(50))
