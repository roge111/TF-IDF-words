import re
import math

class FileProcessing():
    def __init__(self):
        pass

    def _clean_text(self, text: str) -> list[str]:
        text = re.sub(r'[^a-zA-Z0-9 \u0400-\u04FF]', '', text).lower().split()
        return text
    
    def tfidf(self, upload_file):
        content = upload_file.file.read().decode('utf-8')
        #content = upload_file.read()
        document = content.split("\n")

        count_files = {}
        count_doc = 0
        tf_hash = {}
        idf_hash ={}
        for text in document:
            count_doc += 1
            words = self._clean_text(text)
            hash_count_word = {}
            
            for word in words:

                if word not in hash_count_word:
                    hash_count_word[word] = 1
                else:
                    hash_count_word[word] += 1

                if word not in count_files:
                    count_files[word] = 1
                elif hash_count_word[word] < 2:
                    count_files[word] += 1
            
            for key in hash_count_word:
                if key in tf_hash:
                    tf_hash[key] += hash_count_word[key]/len(text)
                else:
                    tf_hash[key] = hash_count_word[key]/len(text)
        
        for key in count_files:
            idf_hash[key] = math.log(count_doc/count_files[key])
        
        return tf_hash, idf_hash
        

# f = open("./files/Test.txt", encoding='utf-8')
# file = FileProcessing()
# print(file.tfidf(f))


    