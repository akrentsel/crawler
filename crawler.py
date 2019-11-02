import requests
# from urlextract import URLExtract
from lxml import html
from collections import deque, Counter
from urllib.parse import urlparse

def crawl(count=10, debug=False):
    # extractor = URLExtract()
    link_queue = deque()
    link_queue.append('https://en.wikipedia.org/wiki/Main_Page')

    ref_count = Counter()

    while count > 0 and link_queue:
        print(count)
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
            # if o.path.startswith('/wiki/List_of_Wikipedias'):
                # print(url)
                # return
                # print(o)
            if debug:
                print(linked_url)
            # Take the part after '/wiki/'
            item_ref = o.path[6:]
            if item_ref not in ref_count:
                link_queue.append('https://en.wikipedia.org' + o.geturl())
            ref_count[item_ref] += 1

    return ref_count

ref_count = crawl(count=10)

print(ref_count.most_common(20))
