class Summa():
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._alkuperaiset_arvot = []

    def suorita(self):
        self._alkuperaiset_arvot.append(self._sovelluslogiikka.arvo())
        self._sovelluslogiikka.plus(self._lue_syote())

    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._alkuperaiset_arvot.pop())

class Erotus():
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._alkuperaiset_arvot = []

    def suorita(self):
        self._alkuperaiset_arvot.append(self._sovelluslogiikka.arvo())
        self._sovelluslogiikka.miinus(self._lue_syote())

    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._alkuperaiset_arvot.pop())

class Nollaus():
    def __init__(self, sovelluslogiikka):
        self._sovelluslogiikka = sovelluslogiikka
        self._alkuperaiset_arvot = []

    def suorita(self):
        self._alkuperaiset_arvot.append(self._sovelluslogiikka.arvo())
        self._sovelluslogiikka.nollaa()

    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._alkuperaiset_arvot.pop())


class Kumoa():
    def __init__(self, sovelluslogiikka, hae_suoritetut_komennot):
        self._sovelluslogiikka = sovelluslogiikka
        self._hae_suoritetut_komennot = hae_suoritetut_komennot

    def suorita(self):
        komento = self._hae_suoritetut_komennot().pop()
        komento.kumoa()
