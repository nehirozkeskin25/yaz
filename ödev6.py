class Hayvan:
    def __init__(self, isim, yas):
        self.isim = isim
        self.yas = yas

    def ses_cikar(self):
        # Alt sınıflar bu metodu override edecek
        raise NotImplementedError("Bu metot alt sınıfta override edilmeli!")


class Kedi(Hayvan):
    def ses_cikar(self):
        return "Miyav"

    def tirmala(self):
        return f"{self.isim} koltuğu tırmalıyor!"


class Kopek(Hayvan):
    def ses_cikar(self):
        return "Hav"

    def getir(self):
        return f"{self.isim} topu getirdi!"


if __name__ == "__main__":
    kedi = Kedi("Pamuk", 3)
    kopek = Kopek("Karabas", 5)

    for hayvan in (kedi, kopek):
        print(f"{hayvan.isim} ({hayvan.yas} yaşında): {hayvan.ses_cikar()}")

    print(kedi.tirmala())
    print(kopek.getir())