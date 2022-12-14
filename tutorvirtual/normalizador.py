import unidecode
import re 
import spacy

class Normalizador:
    simbolos = ''
    
    
    def __init__(self,simbolos = None,stopwords = None ):
        self.simbolos = simbolos if simbolos else set("{}[]|/*-+.,<>?/:;\\\'\"%$#@!^&*()=`~1234567890")
        self.stopwords = stopwords if stopwords else []
        
    def normaliza_texto(self,testinput):
        nlp = spacy.load('es_core_news_sm')
        # Remover espacios extra
        testinput = re.sub('  +',' ',testinput)
        #convertir a ascii
        testinput = unidecode.unidecode(testinput)
        # convertir a minusculas
        testinput = testinput.lower()
        
        #eliminar Latex

        testinput = re.sub('\\\\begin{equation}\s*\\n\s*(.*)\s*\\n\\\\end{equation}','',testinput)
        testinput = re.sub('\\\\begin{align}\s*\\n\s*(.*)\s*\\n\\\\end{align}','',testinput)
        testinput = re.sub('\$(.*)\$','',testinput)
        # elminar simbolos
        testinput = ''.join(char for char in testinput if not char in self.simbolos)

        #Tokenizar oraciones
        doc = nlp(testinput)
        #tokenizar palabras
        tokens = [t.orth_ for t in doc]
        lexical_tokens = [t.orth_ for t in doc if not t.is_punct ]
        words = [t.lower() for t in lexical_tokens if len(t) > 3 and t.isalpha()]
        cleanwords = [word for word in words if word not in self.stopwords]
        lexical_tokens = [t.lower() for t in cleanwords if len(t) > 3 and     
    t.isalpha()]
        #lemmas = [tok.lemma_.lower() for tok in lexical_tokens]
        
        return ' '.join(lemma for lemma in lexical_tokens)