from collections import Counter
import json
import re
import sys

def main():
    with open(sys.argv[1]) as tweet_file:
        terms_counter = Counter()
        for line in tweet_file:
            message = json.loads(line)
            if 'text' in message:
                text = message['text']
                split_text = re.sub('@[\w]{1,15}(\s|:)', ' ',  text.lower()) \
                    .replace('#', ' ') \
                    .replace('?', ' ') \
                    .replace('.', ' ') \
                    .replace(',', ' ') \
                    .replace('!', ' ') \
                    .encode('utf-8') \
                    .split()
                terms_counter.update(split_text)
                # The frequency of a term can be calculated as [# of occurrences of the term in all tweets]/[# of occurrences of all terms in all tweets]
        total_terms = float(sum(terms_counter.values()))
        for key, value in terms_counter.items():
            frequency = float(value) / total_terms
            print("{}\t{}".format(key, frequency))

if __name__ == '__main__':
    main()
