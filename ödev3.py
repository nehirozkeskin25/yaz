import time
import functools


def sure_olc(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        baslangic = time.time()
        sonuc = func(*args, **kwargs)
        bitis = time.time()
        print(f"[sure_olc] {func.__name__} fonksiyonu {bitis - baslangic:.4f} saniye sürdü.")
        return sonuc
    return wrapper


def tekrar(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sonuc = None
            for i in range(n):
                print(f"[tekrar] {i + 1}. çalıştırma:")
                sonuc = func(*args, **kwargs)
            return sonuc  
        return wrapper
    return decorator


def hata_yakala(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[hata_yakala] {func.__name__} fonksiyonunda hata oluştu: {e}")
            return None
    return wrapper



@sure_olc
def yavas_toplama():
    time.sleep(1)  
    return sum(range(1_000_000))


@tekrar(3)
def selam_ver(isim):
    print(f"Merhaba, {isim}!")


@hata_yakala
def bolme(a, b):
    return a / b


if __name__ == "__main__":
    print("--- sure_olc testi ---")
    sonuc = yavas_toplama()
    print(f"Sonuç: {sonuc}\n")

    print("--- tekrar(3) testi ---")
    selam_ver("Ayşe")
    print()

    print("--- hata_yakala testi ---")
    print("10 / 2 =", bolme(10, 2))
    print("10 / 0 =", bolme(10, 0))  
    print("\nProgram sorunsuz bitti")