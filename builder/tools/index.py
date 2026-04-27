import math

from builder.core import Entry, raw_tool
import re

@raw_tool
def keep_common_sections(entries: list[Entry], min_section_count: float|int=3):
    """keep only sections whose titles appear multiple times across entries"""
    count_section_names: dict[str,int] = dict()
    if isinstance(min_section_count, float):
        min_section_count = int(min_section_count*len(entries))
    for entry in entries:
        for section in entry.unparsed_sections:
            count_section_names[section] = count_section_names.get(section, 0) + 1
    allowed = {k for k, v in count_section_names.items() if v>=min_section_count}
    #print({k for k, v in count_section_names.items() if v<min_section_count})
    for entry in entries:
        entry.unparsed_sections = {k: v for k, v in entry.unparsed_sections.items() if k in allowed}


@raw_tool
def keywords(entries: list[Entry], cutoff=0.8):
    """identifies and tf-idf weighs keywords by considering all sections across all software"""
    import nltk
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    # add some html tags
    stop_words.add("li")
    stop_words.add("div")
    stop_words.add("ul")
    stop_words.add("lt")
    stop_words.add("gt")
    stop_words.add("le")
    stop_words.add("ge")
    stop_words.add("img")
    stop_words.add("h1")
    stop_words.add("h2")
    stop_words.add("h3")
    stop_words.add("h4")
    stop_words.add("h5")
    stop_words.add("em")
    stop_words.add("it")

    df: dict[str,int] = dict()

    def tokenize(text: str):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        return [t for t in text.split() if len(t) > 1 and not any(c in "0123456789" for c in t)]

    for entry in entries:
        for k, v in entry.unparsed_sections.items():
            for item in v:
                for token in set(tokenize(item)):
                    df[token] = df.get(token, 0) + 1

    for entry in entries:
        tf: dict[str,float] = dict()
        for k, v in entry.unparsed_sections.items():
            for item in v:
                for token in tokenize(item):
                    tf[token] = tf.get(token, 0) + 1
        for k, v in tf.items():
            tf[k] /= math.log(df[k]+1) # should always exist
        entry.keywords = {k: v for k, v in tf.items() if v>cutoff and k not in stop_words}
