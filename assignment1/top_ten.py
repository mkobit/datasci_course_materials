from collections import Counter
from operator import itemgetter
import json
import sys

def main():
    with open(sys.argv[1]) as tweet_file:
        hashtags_counter = Counter()
        for line in tweet_file:
            message = json.loads(line)
            if 'entities' in message and message['entities']['hashtags']:
                hashtags = message['entities']['hashtags']
                hashtags_counter.update([hashtag['text'].encode('utf-8') for hashtag in hashtags])
        ordered_hashtags = sorted([(hashtag, count) for hashtag, count in hashtags_counter.items()],
            key=itemgetter(1), reverse=True)
        for hashtag, count in ordered_hashtags[:10]:
            print('{}\t{}'.format(hashtag, count))

if __name__ == '__main__':
    main()
