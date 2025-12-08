class Summa():
    def __init__(self, sovelluslogiikka, syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._syote = syote

    def __call__(self):
        self._sovelluslogiikka.plus(self._syote())

class Erotus():
    def __init__(self, sovelluslogiikka, syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._syote = syote

    def __call__(self):
        self._sovelluslogiikka.miinus(self._syote())

class Nollaus():
    def __init__(self, sovelluslogiikka):
        self._sovelluslogiikka = sovelluslogiikka

    def __call__(self):
        self._sovelluslogiikka.nollaa()

class Kumoa():
    def __init__(self, sovelluslogiikka):
        self._sovelluslogiikka = sovelluslogiikka

    def __call__(self):
        self._sovelluslogiikka.kumoa()
