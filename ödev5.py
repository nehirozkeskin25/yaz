import json
import os
from datetime import datetime
from functools import wraps

DOSYA = "gorevler.json"


def hata_yakala(func):
    """Hatalı girişlerde program çökmesin, mesaj bassın."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print("Geçersiz giriş! Lütfen bir sayı gir.")
        except KeyError:
            print("Bu ID'ye sahip bir görev yok.")
        except Exception as e:
            print(f"Beklenmeyen hata: {type(e).__name__} → {e}")
    return wrapper


class Gorev:
    def __init__(self, id, baslik, tamamlandi=False, tarih=None):
        self.id = id
        self.baslik = baslik
        self.tamamlandi = tamamlandi
        self.tarih = tarih or datetime.now().strftime("%d.%m.%Y %H:%M")

    def sozluge_cevir(self):
        return {
            "id": self.id,
            "baslik": self.baslik,
            "tamamlandi": self.tamamlandi,
            "tarih": self.tarih,
        }

    @classmethod
    def sozlukten_olustur(cls, d):
        return cls(d["id"], d["baslik"], d["tamamlandi"], d["tarih"])

    def __str__(self):
        durum = "✅" if self.tamamlandi else "⬜"
        return f"{durum} [{self.id}] {self.baslik}  ({self.tarih})"


class GorevYoneticisi:
    def __init__(self):
        self.gorevler = self.yukle()

    def yukle(self):
        if not os.path.exists(DOSYA):
            return []
        with open(DOSYA, "r", encoding="utf-8") as f:
            veri = json.load(f)
        return [Gorev.sozlukten_olustur(d) for d in veri]

    def kaydet(self):
        with open(DOSYA, "w", encoding="utf-8") as f:
            json.dump(
                [g.sozluge_cevir() for g in self.gorevler],
                f, ensure_ascii=False, indent=4,
            )

    def yeni_id(self):
        if not self.gorevler:
            return 1
        return max(g.id for g in self.gorevler) + 1

    def gorev_bul(self, id):
        for g in self.gorevler:
            if g.id == id:
                return g
        raise KeyError(id)  

    def ekle(self, baslik):
        gorev = Gorev(self.yeni_id(), baslik)
        self.gorevler.append(gorev)
        self.kaydet()
        print(f"Görev eklendi: {gorev}")

    def tamamla(self, id):
        gorev = self.gorev_bul(id)
        gorev.tamamlandi = True
        self.kaydet()
        print(f"Tamamlandı: {gorev}")

    def sil(self, id):
        gorev = self.gorev_bul(id)
        self.gorevler.remove(gorev)
        self.kaydet()
        print(f"Silindi: {gorev.baslik}")

    def listele(self):
        if not self.gorevler:
            print("Hiç görev yok. Yeni bir tane ekle!")
            return
        print("\n----- GÖREVLER -----")
        for g in self.gorevler:
            print(g)
        tamam = sum(1 for g in self.gorevler if g.tamamlandi)
        print(f"--------------------\n{tamam}/{len(self.gorevler)} görev tamamlandı.\n")


@hata_yakala
def gorev_ekle_menu(yonetici):
    baslik = input("Görev başlığı: ").strip()
    if not baslik:
        print("Boş başlık olmaz!")
        return
    yonetici.ekle(baslik)


@hata_yakala
def gorev_tamamla_menu(yonetici):
    id = int(input("Tamamlanan görevin ID'si: ")) 
    yonetici.tamamla(id)


@hata_yakala
def gorev_sil_menu(yonetici):
    id = int(input("Silinecek görevin ID'si: "))
    yonetici.sil(id)


def main():
    yonetici = GorevYoneticisi()
    print("CLI Görev Yöneticisi'ne hoş geldin!")

    while True:
        print(
            "\n1) Görev ekle"
            "\n2) Tamamlandı işaretle"
            "\n3) Görev sil"
            "\n4) Listele"
            "\n5) Çıkış"
        )
        secim = input("Seçimin (1-5): ").strip()

        if secim == "1":
            gorev_ekle_menu(yonetici)
        elif secim == "2":
            yonetici.listele()
            gorev_tamamla_menu(yonetici)
        elif secim == "3":
            yonetici.listele()
            gorev_sil_menu(yonetici)
        elif secim == "4":
            yonetici.listele()
        elif secim == "5":
            print("Görüşürüz! Görevlerin gorevler.json'a kaydedildi.")
            break
        else:
            print("ssss1-5 arası bir sayı gir.")


if __name__ == "__main__":
    main()