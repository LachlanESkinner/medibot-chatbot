from pickle import dump, load
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.tokenize import _treebank_word_tokenizer
# from chatterbot.corpus import load_corpus, list_corpus_files
from chatterbot import languages


def get_sentence_tokenizer(language):
    """
    Return the sentence tokenizer callable.
    """

    pickle_path = 'sentence_tokenizer.pickle'

    try:
        input_file = open(pickle_path, 'rb')
        sentence_tokenizer = load(input_file)
        input_file.close()
    except FileNotFoundError:

        sentences = []

        # Fallback: minimal sentence set to train tokenizer
        fallback_sentences = [
            "Hello, how can I help you?",
            "What product are you looking for?",
            "This item is available under NDIS funding.",
            "Would you like a free sample?"
        ]

        for text in fallback_sentences:
            sentences.append(text.upper())
            sentences.append(text.lower())

        trainer = PunktTrainer()
        trainer.INCLUDE_ALL_COLLOCS = True
        trainer.train('\n'.join(sentences))

        sentence_tokenizer = PunktSentenceTokenizer(trainer.get_params())

        # Pickle the sentence tokenizer for future use
        output_file = open(pickle_path, 'wb')
        dump(sentence_tokenizer, output_file, -1)
        output_file.close()

    return sentence_tokenizer


def get_word_tokenizer(language):
    """
    Return the word tokenizer callable.
    """
    return _treebank_word_tokenizer
