from collections import defaultdict
import json
from operator import itemgetter
import re
import sys

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

inverted_states = {v: k for k, v in states.items()}

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

def determine_user_location(tweet):
    location = None
    if 'place' in tweet:
        place = tweet['place']
        if place and place['country_code'] == 'US':
            # print(json.dumps(place))
            name = place['name'].encode('utf-8')
            full_name = place['full_name'].encode('utf-8')
            if name in states:
                location = name
            elif name in inverted_states:
                location = inverted_states[name]
            else:
                if full_name in states:
                    location = full_name
                else:
                    split_full_name = [n.strip() for n in full_name.split(',')]
                    if len(split_full_name) > 1:
                        if split_full_name[0] in states:
                            location = split_full_name[0]
                        elif split_full_name[0] in inverted_states:
                            location = inverted_states[split_full_name[0]]
                        elif split_full_name[1] in states:
                            location = split_full_name[1]
                        elif split_full_name[1] in inverted_states:
                            location = inverted_states[split_full_name[1]]
    return location

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
        happy_states = defaultdict(list)
        for line in tweet_file:
            message = json.loads(line)
            score = 0
            cleaned_text = clean_tweet(message, remove_user_mentions=True,
                remove_urls=True, remove_media=True)
            if cleaned_text:
                location = determine_user_location(message)
                if location:
                    score = compute_sentiment(cleaned_text)
                    if score:
                        happy_states[location].append(score)
        happiest = None
        happiest_avg = None
        for state, happinesses in happy_states.items():
            avg_happiness = float(sum(happinesses)) / len(happinesses)
            if avg_happiness > happiest_avg:
                happiest = state
                happiest_avg = avg_happiness
        print(happiest)

if __name__ == '__main__':
    main()
