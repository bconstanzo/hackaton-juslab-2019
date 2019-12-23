import colorama
import glob
import re
import spacy


from docx import Document


nlp = spacy.load("es_core_news_md")


C_RE_DNI          = re.compile(r"(DNI|D\.N\.I\.) ((N\°|nro\.)( )*)*(\d{1,3}\.*){1,3}") 
C_RE_TEL          = re.compile(r"tel(\.){0,1}(:|\.)( |\+)*?((\d{1,11})(\-| )*)+", flags=re.IGNORECASE)
C_RE_PATENTE      = re.compile(r"([a-z]{3}(\-){0,1}\d{3})|([a-z]{2}\d{3}[a-z]{2})", flags=re.IGNORECASE)
C_RE_URL          = re.compile(r"", flags=re.IGNORECASE)
C_RE_EMAIL        = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", flags=re.IGNORECASE)
C_RE_IP           = re.compile(r"(\d{1,3}\.){3}(\d{1,3})", flags=re.IGNORECASE)
C_RE_CARATULA     = re.compile(r'(\"|\“).*(s\.|s\/|sobre|contra).*(\"|\”)', flags=re.IGNORECASE)
C_RE_CAUSA        = re.compile(r"(causa (N\°|nro\.?)|expte\.) \d*?\/\d*?(\D)", flags=re.IGNORECASE)
C_RE_DOMICILIO    = re.compile(r"(en la(s)? intersecci(ón|ones) de |ubicad(a|o) en |sit(a|o) en |residencia en |se domicilia en |calle |calle  |domicilio real en |domicilio constituido en )([A-Za-z0-9'\.\-\s\,|[\w \d\.\d\º \“\d\”|\w \d\,\.\d \“\d\”]*?)(de (esta|la) )", flags=re.IGNORECASE)
# trabajar aparte
C_RE_FUNCIONARIOS = re.compile(r"(juez(a)?|magistrad(a|o)|(pro)?secretari(a|o)( coadyuvante)?|defensor(a)?|fiscal|titular del juzgado|representante del (ministerio publico fiscal|mpf))\:(.*?)(\,\s|\.\s)", flags=re.IGNORECASE)
C_RE_IMP_VICT     = re.compile(r"(imputad(a|o)|v(í|i)ctima|denunciante)\:(.*?)(\,|\.\s)", flags=re.IGNORECASE)

C_L_RRSS        = ["Google Drive", "Facebook", "Twitter", "Instagram", "WhatsApp",
                   "fb", "ig", "wa", "wsp", "wapp",
                  ]

PATH = "pancho/1992 SILVA 114 tener por cumplidas reglas de conducta pena en suspenso - control de ejecución - hace lugar TESTADO.docx"
PATH = "pancho/CONTRAVENCIONAL AUDIENCIA CONDENA 114 PENA EN SUSPENSO Proyecto.docx"
#PATH = "pancho/VISU CONTRAVENCIONAL TESTADO.docx"

paths = glob.glob("pancho/*.docx")[2:]

####
class Domicilio:
    def __init__(self, pattern):
        self.pattern = pattern
    
    def sub(self, repl, string):
        ret = []
        pos = 0
        for match in self.pattern.finditer(string):
            grupos = match.groups()
            substr = string[match.start():match.end()]
            substr = substr.replace(grupos[-3], repl)
            ret.append(string[pos:match.start()])
            ret.append(substr)
            pos = match.end()
        ret.append(string[pos:])
        return "".join(ret)

C_RE_DOMICILIO = Domicilio(C_RE_DOMICILIO)

reemplazos = [
    (C_RE_DNI, f"{colorama.Fore.RED}~DNI~{colorama.Fore.RESET}"),
    (C_RE_TEL, f"{colorama.Fore.RED}~TEL~{colorama.Fore.RESET}"),
    (C_RE_EMAIL, f"{colorama.Fore.RED}~EMAIL~{colorama.Fore.RESET}"),
    (C_RE_DOMICILIO, f"{colorama.Fore.RED}~DOMICILIO~{colorama.Fore.RESET}"),
    (C_RE_PATENTE, f"{colorama.Fore.RED}~PATENTE~{colorama.Fore.RESET}"),
    # (C_RE_CARATULA, f"{colorama.Fore.RED}~CARATULA~{colorama.Fore.RESET}"),
    (C_RE_IP, f"{colorama.Fore.RED}~IP~{colorama.Fore.RESET}"),
    (C_RE_CAUSA, f"{colorama.Fore.RED}~CAUSA~{colorama.Fore.RESET}"),
]

def anonimizar(path):
    documento = Document(path)
    texto = "\n".join([p.text for p in documento.paragraphs])

    parrafos = texto.split("\n", 20)
    n_parrafos = []
    for p in parrafos[:-1]:
        p = C_RE_CARATULA.sub(f"{colorama.Fore.RED}~CARATULA~{colorama.Fore.RESET}", p)
        n_parrafos.append(p)

    n_parrafos.append(parrafos[-1])

    texto = "\n".join(n_parrafos)

    for regex, simbolo in reemplazos:
        texto = regex.sub(simbolo, texto)

    def clean_per(ent, prohibidas):
        if any([p in str(ent) for p in prohibidas]):
            return False
        return any(["PROPN" in [t.pos_ for t in ent.as_doc()]])


    doc = nlp(texto)
    partes = []
    funcionarios = [t[-2].strip() for t in C_RE_FUNCIONARIOS.findall("".join(parrafos[:10]))]
    anonimos = [t[-2].strip() for t in C_RE_FUNCIONARIOS.findall("".join(parrafos[:10]))]
    prohibidas = ["DOMICILIO~", "DNI~", "TEL~", "NOMBRE~", "PATENTE~", "IP~",
                "CAUSA~", "CARATULA~"]
    prohibidas.extend(funcionarios)
    pos = 0
    personas = [e for e in doc.ents if e.label_ == "PER"]
    personas = [p for p in personas if clean_per(p, prohibidas)]
    for e in personas:
        partes.append(texto[pos: e.start_char])
        partes.append(f"{colorama.Fore.RED}~NOMBRE~{colorama.Fore.RESET}")
        pos = e.end_char
    partes.append(texto[pos:])

    texto_final = "".join(partes)
    colorama.init()
    print(texto_final)

def main():
    for path in paths:
        print(f"Anonimizando {path}...")
        anonimizar(path)

if __name__ == "__main__":
    main()