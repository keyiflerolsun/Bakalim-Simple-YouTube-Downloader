from __future__ import unicode_literals

"""
Main function of this project.
Code Style: Black (Please continue with Black if contributing)
(c) Tom Gaimann, 2020
"""
import os
import eel
import sys
import datetime
import configparser
import youtube_dl as yt
# import json
# import urllib.request
# from pathlib import Path
# from threading import Thread
# from distutils.version import LooseVersion

try:  # tkinter olup olmadığını kontrol edin...
    from tkinter import Tk, filedialog
except ImportError:
    print("Hata: tkinter bulunamadı")
    print("Linux'ta tkinter'ı şu kodu çalıştırarak kurabilirsiniz:")
    print("sudo apt-get install python3-tk")
    print("veya")
    print("sudo pacman -S tk")

# temel logger
class LogYok(object):
    def __init__(self):
        pass

    def debug(self, msg):
        # print(msg)
        pass

    def warning(self, msg):
        # print(msg)
        pass

    def error(self, msg):
        print(msg)


# eels kök klasörü ve yapılandırma konumu kurulumu
web_konumu = "web"
web_yolu   = os.path.dirname(os.path.realpath(__file__)) + "/" + web_konumu
eel.init(web_yolu)

# ayar yolu kurulumu
ayar_konumu = "ayar.ini"
ayar_yolu   = os.path.dirname(os.path.realpath(__file__)) + "/" + ayar_konumu


# gerçek indirme işlevi
@eel.expose
def indir(url):
    # YouTube_dl özellikleri
    ydl_opts = {
        "verbose": "true",
        "noplaylist": "true",
        "format": "best",
        "outtmpl": ver_kayit_yolu() + "/%(title)s.%(ext)s",
        "progress_hooks": [progress],
        "logger": LogYok(),
    }

    try:
        with yt.YoutubeDL(ydl_opts) as ydl:
            ydl.indir([url])

    except KeyboardInterrupt:
        print("KeyboardInterrupt. ❌")
        eel.update_status("KeyboardInterrupt. ❌")
        sys.exit(0)

    except yt.utils.DownloadError:
        print("Geçerli bir URL değil. ❌")
        eel.update_status("Geçerli bir URL değil. ❌")


# indirme devam ederken ilerleme çubuğunu günceller
def progress(d):
    try:
        toplam_byte     = int(d["total_bytes"])
        indirilen_byte  = int(d["downloaded_bytes"])
        yuzde           = round((indirilen_byte / toplam_byte) * 100)
        eel.update_progressbar(yuzde)

        eel.update_status("")

        if d["status"] == "downloading":
            try:
                dosya_adi   = os.path.basename(d["filename"])
                hiz         = round(d["speed"] / 1000000, 2)        # mb/s cinsinden hız
                gecen_zaman = datetime.timedelta(
                    seconds=round(d["elapsed"])
                )  # elapsed time
                tahmini_sure = datetime.timedelta(seconds=d["eta"]) # tahmini süre
            except TypeError:
                hiz = 0  # yedekleme değeri - çünkü yukarıdakiler bazen başarısız olur
                gecen_zaman = 0
                tahmini_sure = 0

            eel.update_status("Downloading ...\nSpeed: {:.2f} mb/s | {} / {}".format(hiz, gecen_zaman, tahmini_sure))

        if d["status"] == "finished":
            eel.update_status("İndirme başarıyla tamamlandı ✔️")

    except KeyError:
        print("Video muhtemelen zaten var. ❌")
        eel.update_status("Video muhtemelen zaten var. ❌")


# çıktı dizinini seçmek için bir gezgin penceresi açar
@eel.expose
def dizin_tarayicisi_ac():
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    dizin = filedialog.askdirectory()   # dizin seçiciyi aç

    ayar = configparser.ConfigParser()  # seçilen dizini yapılandırmaya yaz
    ayar.read(ayar_yolu)
    ayar["MAIN"]["save_path"] = dizin
    with open(ayar_yolu, "w") as ayar_dosyasi:
        ayar.write(ayar_dosyasi)
    durum_cikti_guncelle()


# geçerli çıktı yolunu döndür
def ver_kayit_yolu():
    ayar = configparser.ConfigParser()
    ayar.read(ayar_yolu)
    return ayar["MAIN"]["save_path"]


# durum metin alanındaki çıktı yolunu değiştir
@eel.expose
def durum_cikti_guncelle():
    eel.update_status("Çıktı: " + ver_kayit_yolu())


# mevcut sürümle sürüm rozetini günceller (html body onload'da çağrılır)
@eel.expose
def surum_rozeti_guncelle():
    eel.surum_rozeti_guncelle("v" + '1.0.1')


# yapılandırma dosyasının var olup olmadığını kontrol eder. eğer yoksa yaratır
def ayar_kontrol():
    if not os.path.isfile(ayar_yolu):
        print("ayar.ini eksik, yenisini oluşturuyorum")
        with open(ayar_yolu, "a") as ayar:
            ayar.write("[MAIN]\nsave_path = \n")


# # check if a new version of sytd is available on pypi
# def check_for_update():
#     current_version = VERSION
#     latest_version = ""
#     url = "https://pypi.org/pypi/sytd/json"  # pypi json url
#     try:
#         with urllib.request.urlopen(url) as request:
#             latest_version = json.loads(request.read().decode())["info"]["version"]
#     except:
#         pass

#     if LooseVersion(current_version) < LooseVersion(latest_version):
#         print("Version {} of sytd is available!".format(latest_version))
#         eel.show_update_available()


# pencereyi kapatırken programı kapat
def kapat(path, sockets):
    print("Hoşçakal...")
    sys.exit(0)


# main function
def run():
    ayar_kontrol()
    # check_for_update()
    try:
        eel.start("main.html", mode="chrome", port=0, size=(600, 840), close_callback=kapat)
    except (SystemExit, KeyboardInterrupt):
        pass
    except OSError:
        print(
            "Bu programı çalıştırmak için Chrome gereklidir. Chrome'u burdan yükleyin:"
            "https://www.google.com/chrome/"
        )


if __name__ == "__main__":
    run()
