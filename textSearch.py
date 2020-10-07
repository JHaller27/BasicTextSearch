import re


BAD_CHARS_REGEX = re.compile(r"[^\w\s]")

def sanitize_text(text: str) -> str:
    clean_text = text

    clean_text = clean_text.lower()
    clean_text = BAD_CHARS_REGEX.sub('', clean_text)

    return clean_text


class SearchMethod:
    def search(self, word_map, terms):
        raise NotImplementedError


class StrictSearch(SearchMethod):
    """
    Find only ids that have ALL search terms
    """
    def __repr__(self) -> str:
        return "<StrictSearch>"

    def search(self, word_map, terms):
        terms = map(sanitize_text, terms)

        ids = None
        for term in terms:
            if term in word_map:
                found_ids = set(word_map[term])
                if ids is None:
                    ids = found_ids
                else:
                    ids.intersection_update(found_ids)

            if len(ids) == 0:
                return None

        return ids


class LooseSearch(SearchMethod):
    """
    Find ids that have ANY of the search terms
    """
    def __repr__(self) -> str:
        return "<LooseSearch>"

    def search(self, word_map, terms):
        terms = map(sanitize_text, terms)

        ids = set()
        for term in terms:
            if term in word_map:
                found_ids = set(word_map[term])
                ids.update(found_ids)

        if len(ids) == 0:
            return None

        return ids


class PrioritySearch(SearchMethod):
    """
    Return ids in priority order by count of search terms present
    Do not return any ids that have none of the search terms
    """
    def __repr__(self) -> str:
        return "<PrioritySearch>"

    def search(self, word_map, terms):
        terms = map(sanitize_text, terms)

        # Dict of [id] => # of times seen, ie count of terms
        ids = {}
        for term in terms:
            if term in word_map:
                found_ids = word_map[term]
                for i in found_ids:
                    if i not in ids:
                        ids[i] = 1
                    else:
                        ids[i] += 1

        if len(ids) == 0:
            return None

        # Invert id dict to dict of [count of terms] => ids
        count_dict = {}
        for i in ids:
            count = ids[i]
            if count not in count_dict:
                count_dict[count] = set()
            count_dict[count].add(i)

        counts = sorted(list(count_dict.keys()))
        for c in reversed(counts):
            for i in count_dict[c]:
                yield i


class TextSearcher:
    def __init__(self, default_method: SearchMethod = None):
        self._next_id = 0
        self._word_map = {}
        self._text_map = {}

        self._default_method = default_method


    def __len__(self) -> int:
        return len(self._text_map)


    def __repr__(self) -> str:
        return f"<TextSearcher len={len(self)} search_methd={repr(self._default_method)}>"


    def __str__(self) -> str:
        lines = []

        for i in self._text_map:
            text = self._text_map[i]
            lines.append(f'[{i}] => "{text}"')

        return "\n".join(lines)

    def add(self, text):
        clean_text = sanitize_text(text)

        self._next_id += 1
        self._text_map[self._next_id] = text

        for word in clean_text.split():
            word = word.lower()
            self._link_word_to_text(word, self._next_id)

    def search(self, terms, method: SearchMethod = None):
        method = self._get_method(method)

        text_ids = method.search(self._word_map, terms)

        return map(lambda tid: self._text_map[tid], text_ids)

    def _link_word_to_text(self, word, text_id):
        if word not in self._word_map:
            self._word_map[word] = set()
        self._word_map[word].add(text_id)

    def _get_method(self, method_override: SearchMethod):
        if method_override is None:
            if self._default_method is None:
                raise ValueError("Must either define a default SearchMethod in the constructor, or pass as a parameter for one-time use")

            return self._default_method

        return method_override
