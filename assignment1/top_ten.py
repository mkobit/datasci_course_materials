from collections import Counter
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
        for hashtag, count in hashtags_counter.items():
            print('{}\t{}'.format(hashtag, count))

if __name__ == '__main__':
    main()
