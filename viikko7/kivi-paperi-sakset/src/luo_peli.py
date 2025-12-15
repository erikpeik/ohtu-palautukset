from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


def luo_peli(tyyppi):
    pelit = {
        "a": KPSPelaajaVsPelaaja(),
        "b": KPSTekoaly(),
        "c": KPSParempiTekoaly()
    }

    return pelit.get(tyyppi)
