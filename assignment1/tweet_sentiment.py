import json
import re
import sys

def main():
    scores = {}
    with open(sys.argv[1]) as sentiments_file:
        for line in sentiments_file:
            term, score = line.split('\t')
            scores[term] = int(score)

    def compute_sentiment(text):
        score = 0
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
        return score

    with open(sys.argv[2]) as tweet_file:
        for line in tweet_file:
            message = json.loads(line)
            score = 0
            if 'text' in message:
                score = compute_sentiment(message['text'])
            print(score)

if __name__ == '__main__':
    main()
