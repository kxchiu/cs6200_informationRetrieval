import os
import re
import time
import urllib.parse
import urllib.request

SeedUrl = 'https://en.wikipedia.org/wiki/Karen_Sp%C3%A4rck_Jones'
Numpages = 1000

class Stats:
    def __init__(self):
        self.max_size = float('-inf')
        self.min_size = float('inf')
        self.max_depth = 0
        self.total_size = 0
        self.num_pages = 0

    def add_result(self, size, *, depth):
        self.max_size = max(self.max_size, size)
        self.min_size = min(self.min_size, size)
        self.max_depth = max(self.max_depth, depth)
        self.total_size += size
        self.num_pages += 1

    @property
    def average_size(self):
        return self.total_size / self.num_pages

    def save(self, filename):
        with open(filename, 'w', encoding='utf-8') as fp:
            fp.write('Maximum size: {} bytes\n'.format(self.max_size))
            fp.write('Minimum size: {} bytes\n'.format(self.min_size))
            fp.write('Average size: {:.3f} bytes\n'.format(self.average_size))
            fp.write('Maximum depth reach: {}\n'.format(self.max_depth))


def crawl(seed_url, num_pages, *, stats_file='stats.txt', visited_file='URLsCrawled.txt', outputs_dir='outputs',
          max_depth=5):
    os.makedirs(outputs_dir, exist_ok=True)

    # Truncate visited file.
    with open(visited_file, 'w', encoding='utf-8'):
        pass

    queue = [(seed_url, 1)]
    visited = set()
    stats = Stats()
    while queue:
        url, depth = queue.pop(0)
        if depth >= max_depth:
            continue

        # Stop when maximum number of pages reached.
        if len(visited) >= num_pages:
            print('Reached maximum pages {}. Aborting...'.format(num_pages))
            break

        # Continue if url is already visited.
        if url in visited:
            continue
        visited.add(url)

        print('Crawling page {} at depth {}: {}'.format(len(visited), depth, url))

        # Try reading data; continue when exception occurs
        try:
            response = urllib.request.urlopen(url)
            data = response.read()
        except:
            continue
        

        with open(os.path.join(outputs_dir, '{}.txt'.format(len(visited))), 'wb') as fp:
            fp.write(data)

        # Update the stats file.
        stats.add_result(len(data), depth=depth)
        stats.save(stats_file)
        with open(visited_file, 'a', encoding='utf-8') as fp:
            fp.write(url + '\n')

        # Find and append relative paths in parsed data to queue.
        relative_paths = re.findall(b'(?<=")/wiki/[^:"]+', data)
        for relative_path in relative_paths:
            next_url = urllib.parse.urljoin(url, str(relative_path, 'utf-8'))
            queue.append((next_url, depth + 1))

        # Politeness rule: Sleep 1 second after each crawl.
        time.sleep(1)

crawl(SeedUrl, Numpages)