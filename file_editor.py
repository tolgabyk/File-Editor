import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # İlerleme çubuğu için gerekli

# Dosya türlerine göre hedef klasörleri belirliyoruz
dosya_turleri = {
    "Resimler": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videolar": [".mp4", ".mov", ".avi", ".mkv", ".flv"],
    "Belgeler": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Müzikler": [".mp3", ".wav", ".flac", ".aac"],
    "Arşivler": [".zip", ".rar", ".tar", ".gz"],
    "Yazılımlar": [".exe", ".msi", ".bat", ".sh"],
    "Diğer": []
}

def dosya_sirala(klasor_yolu, ilerleme_cubugu):
    dosyalar = os.listdir(klasor_yolu)
    toplam_dosya = len(dosyalar)
    ilerleme_cubugu["maximum"] = toplam_dosya

    for index, dosya_adi in enumerate(dosyalar):
        dosya_yolu = os.path.join(klasor_yolu, dosya_adi)
        
        # Dosya mı yoksa klasör mü kontrol et
        if os.path.isfile(dosya_yolu):
            tasindi = False
            # Hangi tür dosya olduğunu kontrol et ve uygun klasöre taşı
            for klasor_adi, uzantilar in dosya_turleri.items():
                if any(dosya_adi.lower().endswith(uzanti) for uzanti in uzantilar):
                    hedef_klasor = os.path.join(klasor_yolu, klasor_adi)
                    if not os.path.exists(hedef_klasor):
                        os.makedirs(hedef_klasor)
                    hedef_yol = os.path.join(hedef_klasor, dosya_adi)
                    # Dosya adı zaten varsa, isim değiştir
                    if os.path.exists(hedef_yol):
                        base, extension = os.path.splitext(dosya_adi)
                        i = 1
                        yeni_ad = f"{base}_{i}{extension}"
                        hedef_yol = os.path.join(hedef_klasor, yeni_ad)
                        while os.path.exists(hedef_yol):
                            i += 1
                            yeni_ad = f"{base}_{i}{extension}"
                            hedef_yol = os.path.join(hedef_klasor, yeni_ad)
                    shutil.move(dosya_yolu, hedef_yol)
                    tasindi = True
                    break
            
            # Eğer dosya tanımlı türlerden biri değilse, "Diğer" klasörüne taşı
            if not tasindi:
                diger_klasor = os.path.join(klasor_yolu, "Diğer")
                if not os.path.exists(diger_klasor):
                    os.makedirs(diger_klasor)
                hedef_yol = os.path.join(diger_klasor, dosya_adi)
                # Dosya adı zaten varsa, isim değiştir
                if os.path.exists(hedef_yol):
                    base, extension = os.path.splitext(dosya_adi)
                    i = 1
                    yeni_ad = f"{base}_{i}{extension}"
                    hedef_yol = os.path.join(diger_klasor, yeni_ad)
                    while os.path.exists(hedef_yol):
                        i += 1
                        yeni_ad = f"{base}_{i}{extension}"
                        hedef_yol = os.path.join(diger_klasor, yeni_ad)
                shutil.move(dosya_yolu, hedef_yol)

        # İlerleme çubuğunu güncelle
        ilerleme_cubugu["value"] = index + 1
        pencere.update_idletasks()  # Arayüzü güncelle

    messagebox.showinfo("İşlem Tamamlandı", "Dosyalar başarıyla sıralandı.")

def klasor_sec():
    klasor_yolu = filedialog.askdirectory()
    if klasor_yolu:
        dosya_sirala(klasor_yolu, ilerleme_cubugu)

# Arayüz
pencere = tk.Tk()
pencere.title("Otomatik Dosya Sıralayıcı")
pencere.geometry("350x200")

etiket = tk.Label(pencere, text="Sıralamak istediğiniz klasörü seçin:")
etiket.pack(pady=10)

buton = tk.Button(pencere, text="Klasör Seç", command=klasor_sec)
buton.pack(pady=10)

# İlerleme çubuğu 
ilerleme_cubugu = ttk.Progressbar(pencere, orient="horizontal", length=300, mode="determinate")
ilerleme_cubugu.pack(pady=20)

pencere.mainloop()
