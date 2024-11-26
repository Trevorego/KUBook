# KUBook

Koç Üniversitesi Kütüphanesi Odaları için AutoBooker

---

### Kullanım Talimatları

config.json dosyasında gün (1-31), ay (1-12), yıl (son 2 hane), oda numarası ve tutmak istediğiniz saati yazın. Sonra .exe dosyasını çalıştırın. 

Çalışma prensibi şu şekilde:
1. Gece saat yaklaşık 11.58-11.59 gibi çalıştıracaksınız.
2. Tarayıcınızdan siteyi açıp otomatik olarak (en erken 2 gün sonrası açılıyor biliyorsunuz) yazdığınız tarih için oda rezervasyonu açılana kadar sayfayı yeniler.
3. Daha sonrasında açıldığı anda sizin önceden belirttiğiniz saati (mesela 11) ve sonraki saati (yani 12) 2 saat art arda olacak şekilde rezerve edip otomatik submitler.

Eğer bir sıkıntı olursa pull request atın. Ben birkaç gündür kullanıyorum, şimdilik çalışıyor gibi. :D

---

### Ek Bilgiler

Aslında direkt indirip çalıştırabileceğiniz bir .exe dosyası da var ama Windows kendisini virüs algılıyor. Bu sebeple *internal* klasörünü ayrıca yükledim. Sizin çalıştırabilmeniz için şu 3 dosyanın yüklü olması gerek:
- internal klasörü  
- KUBook.exe  
- config.json  

İsteyenler için *source* adlı klasörde Python dosyası da var. Direkt oradan da çalıştırabilirsiniz ama yine .json gerek. En kötü, onu yanına kopyalayın. Birkaç module'u da pip install ile indirmeniz gerekir.

---

**Created by Trevorego**
