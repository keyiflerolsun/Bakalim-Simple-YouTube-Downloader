# from __future__ import unicode_literals

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
# from . import __version__ as VERSION
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
class MyLogger(object):
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
web_location    = "web"
web_path        = os.path.dirname(os.path.realpath(__file__)) + "/" + web_location
eel.init(web_path)

# ayar yolu kurulumu
config_location = "ayar.ini"
config_path     = os.path.dirname(os.path.realpath(__file__)) + "/" + config_location


# gerçek indirme işlevi
@eel.expose
def download(url):
    # YouTube_dl özellikleri
    ydl_opts = {
        "verbose": "true",
        "noplaylist": "true",
        "format": "best",
        "outtmpl": get_save_path() + "/%(title)s.%(ext)s",
        "progress_hooks": [hook],
        "logger": MyLogger(),
    }

    try:
        with yt.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except KeyboardInterrupt:
        print("KeyboardInterrupt. ❌")
        eel.update_status("KeyboardInterrupt. ❌")
        sys.exit(0)

    except yt.utils.DownloadError:
        print("Geçerli bir URL değil. ❌")
        eel.update_status("Geçerli bir URL değil. ❌")


# updates the progress bar as the download goes on
def hook(d):
    try:
        total_bytes         = int(d["total_bytes"])
        downloaded_bytes    = int(d["downloaded_bytes"])
        percentage          = round((downloaded_bytes / total_bytes) * 100)
        eel.update_progressbar(percentage)

        eel.update_status("")

        if d["status"] == "downloading":
            try:
                filename        = os.path.basename(d["filename"])
                speed           = round(d["speed"] / 1000000, 2)                          # mb/s cinsinden hız
                elapsed_time    = datetime.timedelta(seconds=round(d["elapsed"]))  # gecen zaman
                estimated_time  = datetime.timedelta(seconds=d["eta"])           # tahmini süre
            except TypeError:
                speed           = 0  # yedekleme değeri - çünkü yukarıdakiler bazen başarısız olur
                elapsed_time    = 0
                estimated_time  = 0

            eel.update_status("İndiriliyor ...\nHız: {:.2f} mb/s | {} / {}".format(speed, elapsed_time, estimated_time))

        if d["status"] == "finished":
            eel.update_status("İndirme başarıyla tamamlandı ✔️")

    except KeyError:
        print("Video muhtemelen zaten var. ❌")
        eel.update_status("Video muhtemelen zaten var. ❌")


# çıktı dizinini seçmek için bir gezgin penceresi açar
@eel.expose
def open_dir_browser():
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    folder = filedialog.askdirectory()      # dizin seçiciyi aç

    config = configparser.ConfigParser()    # seçilen dizini yapılandırmaya yaz
    config.read(config_path)
    config["MAIN"]["save_path"] = folder
    with open(config_path, "w") as configfile:
        config.write(configfile)
    update_status_output()


# geçerli çıktı yolunu döndür
def get_save_path():
    config = configparser.ConfigParser()
    config.read(config_path)
    return config["MAIN"]["save_path"]

# durum metin alanındaki çıktı yolunu değiştir
@eel.expose
def update_status_output():
    eel.update_status("Output: " + get_save_path())

# mevcut sürümle sürüm rozetini günceller (html body onload'da çağrılır)
@eel.expose
def update_version_badge():
    eel.update_version_badge("v" + '1.0.3')

# yapılandırma dosyasının var olup olmadığını kontrol eder. eğer yoksa yaratır
def check_config():
    if not os.path.isfile(config_path):
        print("ayar.ini eksik, yenisini oluşturuyorum")
        with open(config_path, "a") as f:
            f.write("[MAIN]\nsave_path = \n")

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

# close program when closing window
def close(path, sockets):
    print("hoşçakal...")
    sys.exit(0)


# main function
def run():
    check_config()
    # check_for_update()
    try:
        eel.start("main.html", mode="chrome", port=0, size=(600, 840), close_callback=close)
    except (SystemExit, KeyboardInterrupt):
        pass
    except OSError:
        print(
            "Bu programı çalıştırmak için Chrome gereklidir. Chrome'u burdan yükleyin:"
            "https://www.google.com/chrome/"
        )


if __name__ == "__main__":
    run()