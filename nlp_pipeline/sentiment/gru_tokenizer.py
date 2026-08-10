import re
from collections import Counter

class GRUTokenizer:
    def __init__(self, min_freq=2, max_vocab=20000):
        self.min_freq = min_freq
        self.max_vocab = max_vocab

        self.word2idx = {}
        self.idx2word = {}

        # Special tokens
        self.pad_token = "<PAD>"
        self.unk_token = "<UNK>"

    def clean_text(self, text):
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text):
        text = self.clean_text(text)
        return text.split()

    def build_vocab(self, texts):
        counter = Counter()

        for t in texts:
            tokens = self.tokenize(t)
            counter.update(tokens)

        # Start vocab with special tokens
        vocab = [self.pad_token, self.unk_token]

        # Add frequent tokens
        for word, freq in counter.most_common(self.max_vocab):
            if freq >= self.min_freq:
                vocab.append(word)

        # Build mappings
        self.word2idx = {w: i for i, w in enumerate(vocab)}
        self.idx2word = {i: w for w, i in self.word2idx.items()}

        print(f"Vocab size: {len(self.word2idx)}")

    def encode(self, text, max_len=128):
        tokens = self.tokenize(text)
        ids = [self.word2idx.get(t, self.word2idx[self.unk_token]) for t in tokens]

        # Pad or truncate
        if len(ids) < max_len:
            ids += [self.word2idx[self.pad_token]] * (max_len - len(ids))
        else:
            ids = ids[:max_len]

        return ids

    def decode(self, ids):
        return " ".join(self.idx2word.get(i, self.unk_token) for i in ids)
