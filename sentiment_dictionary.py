import csv


class DictionaryRecord:
    pos = ""
    word_id = ""
    pos_score = 0.0
    neg_score = 0.0
    term = ""
    definition = ""

    def __init__(self):
        self.pos = ""
        self.word_id = ""
        self.pos_score = 0.0
        self.neg_score = 0.0
        self.term = ""
        self.definition = ""


class DictionaryReader:
    __file_path = ""

    def __init__(self, file_path):
        self.__file_path = file_path

    def parse(self):
        sent_dict = {}
        with open(self.__file_path, 'r') as f:
            next(f)
            reader = csv.reader(filter(lambda row: row[0] != '#', f), delimiter='\t')

            for pos, word_id, pos_score, neg_score, terms, glossary in reader:
                if (pos_score != "0") or (neg_score != "0"):
                    word_list = terms.split()

                    for word in word_list:
                        clean_word = word.split("#")[0]

                        if len(clean_word) > 1:
                            print(clean_word + " " + pos_score + " " + neg_score)
                            rec = DictionaryRecord()
                            rec.pos = pos
                            rec.word_id = word_id
                            rec.pos_score = pos_score
                            rec.neg_score = neg_score
                            rec.term = clean_word
                            rec.definition = glossary

                            sent_dict[clean_word] = rec
                            break

        return sent_dict

