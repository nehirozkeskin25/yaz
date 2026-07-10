import json
import os

DOSYA = "notlar.json"

def dosyayi_yukle():
    if not os.path.exists(DOSYA):
        with open(DOSYA, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    with open(DOSYA, "r", encoding="utf-8") as f:
        return json.load(f)


def dosyaya_kaydet(veri):
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)


def not_ekle(isim, not_degeri):
    veri = dosyayi_yukle()
    if isim in veri:
        veri[isim].append(not_degeri)
    else:
        veri[isim] = [not_degeri]
    dosyaya_kaydet(veri)
    print(f"{isim} için {not_degeri} notu eklendi.")


def not_goster(isim):
    veri = dosyayi_yukle()
    if isim not in veri:
        print(f"'{isim}' adında kayıtlı öğrenci bulunamadı.")
        return
    notlar = veri[isim]
    print(f"📋 {isim} → notlar: {notlar} | kişisel ortalama: {sum(notlar) / len(notlar):.2f}")


def ortalama():
    veri = dosyayi_yukle()
    tum_notlar = [n for notlar in veri.values() for n in notlar]
    if not tum_notlar:
        print("Henüz hiç not girilmemiş.")
        return None
    ort = sum(tum_notlar) / len(tum_notlar)
    print(f"Genel ortalama ({len(tum_notlar)} not): {ort:.2f}")
    return ort


if __name__ == "__main__":
    not_ekle("Ayşe", 85)
    not_ekle("Ayşe", 90)
    not_ekle("Mehmet", 70)
    not_ekle("Zeynep", 95)

    print()
    not_goster("Ayşe")
    not_goster("Mehmet")
    not_goster("Ali")  

    print()
    ortalama()