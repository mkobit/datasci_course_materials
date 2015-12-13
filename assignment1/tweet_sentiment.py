import json
from operator import itemgetter
import re
import sys

def clean_tweet(tweet, substitute=' ', remove_hashtags=False,
        remove_user_mentions=False, remove_urls=False, remove_media=False):
    """Removes user mentions, hash tags, and other media
    from the tweet. If the tweet does not have text then nothing is done.
    """
    if 'text' in tweet:
        text = tweet['text'].encode('utf-8')
        hashtags = tweet['entities']['hashtags']
        user_mentions = tweet['entities']['user_mentions']
        urls = tweet['entities']['urls']
        medias = tweet['entities'].get('media')
        # process hashtags
        removal_intervals = []
        extract_indices = lambda ents: [(left, right) for left, right in [ent['indices'] for ent in ents]]
        if hashtags and remove_hashtags:
            removal_intervals.extend(extract_indices(hashtags))
        if user_mentions and remove_user_mentions:
            removal_intervals.extend(extract_indices(user_mentions))
        if urls and remove_urls:
            removal_intervals.extend(extract_indices(urls))
        if medias and remove_media:
            removal_intervals.extend(extract_indices(medias))
        sorted(removal_intervals, key=itemgetter(0))

        if removal_intervals:
            shifted_index = 0
            for left, right in removal_intervals:
                adjusted_left = left - shifted_index
                adjusted_right = right - shifted_index
                text = text[0:adjusted_left] + text[adjusted_right::]
                shifted_index += right - left
        return text.replace('#', ' ') \
            .replace('?', ' ') \
            .replace(':', ' ') \
            .replace('.', ' ') \
            .replace(',', ' ') \
            .replace('!', ' ')

def main():
    scores = {}
    with open(sys.argv[1]) as sentiments_file:
        for line in sentiments_file:
            term, score = line.split('\t')
            scores[term] = int(score)

    def compute_sentiment(text):
        score = 0
        for term in scores:
            if term in text:
                score += scores[term]
        return score

    with open(sys.argv[2]) as tweet_file:
        for line in tweet_file:
            message = json.loads(line)
            score = 0
            cleaned_text = clean_tweet(message, remove_user_mentions=True,
                remove_urls=True, remove_media=True)
            if cleaned_text:
                score = compute_sentiment(cleaned_text)
            print(score)

if __name__ == '__main__':
    main()
