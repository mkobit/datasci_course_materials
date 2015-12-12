import collections
import json
import re
import sys

def main():
    scores = {}
    with open(sys.argv[1]) as sentiments_file:
        for line in sentiments_file:
            term, score = line.split('\t')
            scores[term] = int(score)

    def compute_new_sentiments(text):
        score = 0
        # replace user names with space
        normalized_text = re.sub('@[\w]{1,15}(\s|:)', ' ',  text.lower()) \
            .replace('#', ' ') \
            .replace('?', ' ') \
            .replace('.', ' ') \
            .replace(',', ' ') \
            .replace('!', ' ') \
            .encode('utf-8')
        for term in scores:
            if term in normalized_text:
                score += scores[term]
        new_sentiments = {}
        if score:
            split_normalized_text = normalized_text.split()
            missing_term_counts = collections.Counter()
            missing_terms = [term for term in split_normalized_text if term not in scores]
            missing_term_counts.update(missing_terms)
            for term, count in missing_term_counts.items():
                new_sentiments[term] = float(score) * (float(count) / len(split_normalized_text))
        return new_sentiments

    with open(sys.argv[2]) as tweet_file:
        new_term_values = collections.defaultdict(list)
        for line in tweet_file:
            message = json.loads(line)
            score = 0
            if 'text' in message:
                new_sentiments = compute_new_sentiments(message['text'])
                for key, value in new_sentiments.items():
                    new_term_values[key].append(value)
        for key, value in new_term_values.items():
            average = sum(value) / len(value)
            print('{}\t{}'.format(key, average))

if __name__ == '__main__':
    main()
