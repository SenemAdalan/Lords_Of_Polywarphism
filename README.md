# Lords of the Polywarphism

Bu proje, 2-boyutlu bir dünyada çok oyunculu bir savaş oyununu simüle eder ve Python programlama dili kullanılarak yazılmıştır.

## 📋 Proje Açıklaması
- **Yapılış Tarihi:** 18 Mart 2024 
- **Son Güncelleme:** 6 Şubat 2025
  
Proje 2-boyutlu matris formunda bir dünyada çok oyunculu bir savaş oyunu geliştirmeyi amaçlamaktadır. Oyuncular belirli kurallar çerçevesinde savaşçılar üretir ve yerleştirir. Savaşçılar belirli özelliklere ve saldırı yeteneklerine sahiptir. Oyunun amacı, dünyada en uzun süre hayatta kalmak veya dünyanın %60'ını ele geçirmektir.

## Ana Özellikler
- **Dünya Boyutları**: 16x16, 24x24, 32x32 veya kullanıcı tanımlı boyutlarda kare bir dünya.
- **Oyuncu Sayısı**: Minimum 1, maksimum 4 oyuncu.
- **Savaşçı Türleri**: Muhafız, Okçu, Topçu, Atlı, Sağlıkçı.
- **Kaynak Yönetimi**: Oyuncular, her elde kaynak kazanır ve bu kaynaklarla savaşçı üretir.
- **Savaş Mekaniği**: Savaşçılar, belirli kurallar çerçevesinde saldırı yapar ve savunma gerçekleştirir.
- **Oyun Sonu**: Oyuncuların dünyada kalma süresi veya ele geçirdikleri alan yüzdesine göre belirlenir.

## 🚀 Başlarken
Bu projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler
- Python 3.x
- ```pygame```
- ```sys```
- ```random```
- ```ABC```

### Kurulum
1. Repoyu klonlayın:
    ```bash
    git clone https://github.com/kullanici_adi/proje_adi.git
    ```
2. Proje dizinine gidin:
    ```bash
    cd proje_adi
    ```
3. Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
4. Projeyi çalıştırın:
    ```bash
    python main.py
    ```

## 🛠️ Kullanım
Proje bir komut satırı arayüzü (CLI) üzerinden çalışır. Oyuncular menü seçeneklerini kullanarak savaşçı türlerini seçer ve yerleştirir. Oyun her hamle sonunda ve tur sonunda durumu ekranda gösterir.

### Komutlar
- **Savaşçı Üret**: Savaşçı türünü seçer ve koordinatları girerek yerleştirir.
- **Pas Geç**: Hamleyi pas geçer.
- **Durum Göster**: Dünyadaki mevcut durumu gösterir.
- **Çıkış**: Oyundan çıkar.

## 🖥️ Proje Arayüzü
![Image](https://github.com/user-attachments/assets/7e4cff69-4873-4625-8491-2e7b977126e3)

![Image](https://github.com/user-attachments/assets/8f80559b-6a4a-41b6-987e-5f4b4412aac9)

![Image](https://github.com/user-attachments/assets/6a473786-98c1-4a88-9d84-35b926f9b34f)
