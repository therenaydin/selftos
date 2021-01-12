#    [PROGRAM]
#
# Selftos Installer by therenaydin.
# Windows 10 ile test edildi. Diğer windows sürümleri veya işletim sistemleri ile düzgün çalışmayabilir!
# Gerekli kütüphaneleri pip ile indirmeniz gerekmektedir. Yoksa program başlamaz.
#
#    [YAPIMCI]
#
# Eren Aydın ~ therenaydin
# E-posta: therenaydin@gmail.com
# Discord: therenaydin#0911
#
#    [LISANS]
#
# Bu program ücretsizdir.
# İnsanların üzerinde değişiklik yapması ve kendini geliştirmesi için topluluk ile paylaşılmıştır.
# Programı düzenleyip paylaşabilirsiniz.
# Ödevlerinizde kullanabilirsiniz.
#
#    [KAYNAKÇA]
#
# https://www.neuralnine.com/
# https://python-forum.io/
# https://www.youtube.com/channel/UC8wZnXYK_CGKlBcZp-GxYPA (NeuralNine)
# https://pythonprogramming.net/
# https://www.youtube.com/user/sentdex
# https://www.youtube.com/channel/UCi8b7ab1pEJ40hz4E_PDROQ (Melih Görgülü)
# https://stackoverflow.com/



from tkinter import *
from tkinter import ttk
import paramiko
import os, winshell
import time
from win32com.client import Dispatch
from kurulum import *
from colorama import Fore, Back, Style, init
import ctypes

init(autoreset=True)
appdata = os.getenv("APPDATA")
desktop = winshell.desktop()
ctypes.windll.kernel32.SetConsoleTitleW("Selftos Durum Konsolu") # Durum Konsolu

try:
    print(Fore.YELLOW + "Ana sunucu ile bağlantı kuruluyor...") # Bağlanmaya çalışıyor...
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ipofssh, username=nicknamessh, password=password)
    transport = client.get_transport()
except TimeoutError:
    print(Fore.RED + "Ana sunucuya bağlanılamadı! Sihirbaz sonlandırılıyor...") # Bağlantı başarısız olursa sihirbazı kapatıyor.
    time.sleep(3)
    exit()
else:
    print(Fore.YELLOW + "Sunucuya bağlanıldı! Kurulumu başlatmak için start butonuna basınız.") # Bağlantı başarılı olur ise tkinter komutlarını başlatıyor.

try: # Selftos için gerekli klasörleri appdata konumunda oluşturuyor. Çok önemli burayı silmeyin.
    os.mkdir (appdata+"/Selftos")
    os.mkdir (appdata+"/Selftos/data")
except OSError:
    pass

iconp = sshmainpath+"/setico.ico"
serverVer = sshmainpath+"/Server_Data/version.txt"
localVer = appdata+"/Selftos/version.txt"
imgp = sshmainpath+"/setup.png"
gop = sshmainpath+"/gobutton.png"
localgop = appdata+"/Selftos/download.png"
localiconp = appdata+"/Selftos/icon.ico"
localimgp = appdata+"/Selftos/img.png"

def download():
    print(Fore.GREEN + "Kurulum başlatıldı! Bu biraz zaman alabilir, program yanıt vermezse endişelenmeyin.") # Start butonuna basınca çıkacak mesaj.
    def close():
        try:
            top1.destroy()
        except:
            pass
        try:
            top2.destroy()
            setup.destroy()
            os.remove(appdata+"/Selftos/icon.ico")
            os.remove(appdata+"/Selftos/download.png")
            os.remove(appdata+"/Selftos/img.png")
        except:
            pass
        try:
            setup.destroy()
            os.remove(appdata+"/Selftos/icon.ico")
            os.remove(appdata+"/Selftos/download.png")
            os.remove(appdata+"/Selftos/img.png")
        except:
            pass
    try:
        os.mkdir(appdata+"/Selftos/Sources/")
    except OSError:
        pass
    try:
        localaiconp = appdata+"/Selftos/Sources/icon.ico"
        localfile1 = appdata+"/Selftos/Sources/settings.png"
        localfile2 = appdata+"/Selftos/Sources/download.png"
        localfile3 = appdata+"/Selftos/Sources/upload.png"
        localimgp = appdata+"/Selftos/Sources/img.png"
        locallinkp = appdata+"/Selftos/Sources/linkbutton.png"
        localexep = appdata+"/Selftos/Selftos.exe"
        servericonp = sshmainpath+"/downloadtr/Sources/icon.ico"
        settingspath = sshmainpath+"/downloadtr/Sources/settings.png"
        downloadpath1 = sshmainpath+"/downloadtr/Sources/download.png"
        serverlinkp = sshmainpath+"/downloadtr/Sources/linkbutton.png"
        serverlupload = sshmainpath+"/downloadtr/Sources/upload.png"
        serverimgp = sshmainpath+"/downloadtr/Sources/img.png"
        mainexe = sshmainpath+"/downloadtr/Selftos.exe"
        # Bütün dosyaları appdata konumuna getiriyor.
        sftp = client.open_sftp()
        sftp.get(servericonp, localaiconp)
        download_progress['value'] = 10
        sftp.get(downloadpath1, localfile2)
        sftp.get(settingspath, localfile1)
        download_progress['value'] = 30
        sftp.get(serverlupload, localfile3)
        sftp.get(serverimgp, localimgp)
        download_progress['value'] = 40
        sftp.get(mainexe, localexep)
        sftp.get(serverlinkp, locallinkp)
        download_progress['value'] = 10
        sftp.close()
        path = os.path.join(desktop, "Selftos.lnk")
        target = appdata+"/Selftos/Selftos.exe"
        wDir = appdata+"/Selftos/"
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        shortcut.save()
        download_progress['value'] = 10
    except: # indirme başarısız olursa konsola yazı yazıyor.
        print(Fore.RED + "Bir şeyler ters gitti. Daha sonra tekrar deneyin.")
        top1 = Toplevel(setup, bg = "#C3FFF2")
        top1.iconbitmap(localiconp)
        top1.geometry("550x60")
        top1.resizable(False, False)
        top1.wm_attributes("-topmost" , -1)
        top1.title("Selftos Kurulum Başarsız")
        top1.configure(background = "#C3FFF2")
        error = Label(top1, text = "Bir şeyler ters gitti. Sonra tekrar deneyin.",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
        error.pack()
        exit_button = Button(top1, text="Çık",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = close)
        exit_button.pack()
        top1.protocol("WM_DELETE_WINDOW", close)
    else: # Kurulum tamamlandığı zaman çıkacak mesaj.
        print(Fore.GREEN + "Kurulum tamamlandı!")
        top2 = Toplevel(setup, bg = "#C3FFF2")
        top2.iconbitmap(localiconp)
        top2.geometry("550x60")
        top2.resizable(False, False)
        top2.wm_attributes("-topmost" , -1)
        top2.title("Selftos Kurulum Tamamlandı!")
        top2.configure(background = "#C3FFF2")
        done = Label(top2, text = "Bitti! Masaüstünde kısayol oluşturuldu.",font = "Consolas 15", bg = "#C3FFF2", fg = "#FF0000", anchor = "n")
        done.pack()
        exit_button = Button(top2, text="Çık",font = "Consolas 10 bold", bg = "#007CFF", activebackground = "light blue", fg = "white", command = close)
        exit_button.pack()
        top2.protocol("WM_DELETE_WINDOW", close)

def closing():
    try:
        os.remove(appdata+"/Selftos/icon.ico")
        os.remove(appdata+"/Selftos/download.png")
        os.remove(appdata+"/Selftos/img.png")
        setup.destroy()
    except:
        pass

# Ana menü

setup = Tk()
sftp = client.open_sftp()
sftp.get(iconp, localiconp)
sftp.get(imgp, localimgp)
sftp.get(gop, localgop)
sftp.get(serverVer, localVer)
sftp.close()
with open(localVer, 'r') as f:
    ver = f.readline().strip()
f.close()
os.remove(localVer)
setup.configure(background = "#C3FFF2")
setup.iconbitmap(localiconp)
setupimage = PhotoImage(file=localimgp)
downloadimage = PhotoImage(file=localgop)
downloadimage.image = downloadimage
img_label = Label(image = setupimage, borderwidth=0, highlightthickness=0)
img_label.image = setupimage
img_label.pack()
L1 = Label(setup, text="Selftos Kurulum Sihirbazı\nVersiyon: "+ver,font = "Consolas 14 bold", height = 3, bg = "#C3FFF2", fg = "#C100D8")
L1.pack()
L2 = Label(setup, text="Bu sihirbaz bilgisayarınıza Selftos yazılımını kuracaktır.\nİndirme Konumu: C:/Users/%username%/AppData/Roaming/Selftos",font = "Consolas 14", height = 2, bg = "#C3FFF2", fg = "black")
L2.pack()
download_progress = ttk.Progressbar(setup, orient=HORIZONTAL,length=700, mode="determinate")
download_progress.pack(pady=20)
setup.title("Selftos Kurulum Sihirbazı")
setup.geometry("800x400")
setup.resizable(False, False)
setup.protocol("WM_DELETE_WINDOW", closing)
download = Button(setup, image = downloadimage, highlightthickness=0, borderwidth = 0, command=download)
download.place(x = 352, y = 283, height = 100, width = 100)
mainloop()
