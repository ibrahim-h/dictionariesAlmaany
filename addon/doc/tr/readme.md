# Almaany Sözlükleri #

*	Yazarı: İbrahim Hamadeh
*	Katkıda Bulunanlar: Abdel
*	NVDA uyumluluğu: 2019.3 ve sonrası
*	[Sürüm 2.6.3'ü indirin][1]  

Bu eklenti, almaany.com web sitesi aracılığıyla kelimelerin anlamlarını anlamanıza yardımcı olur.  
[almaany.com](https://www.almaany.com/en/dict/ar-en/).

dikkat: Kullanılan tüm sözlükler iki dillidir; bu, örneğin arapça ingilizce sözlüğün arapçadan ingilizceye ve ingilizceden arapçaya çevrildiği anlamına gelir. 

***

## Kullanım

*	Nvda+windows+d tuşlarına basın, seçim yapılmazsa Almaany Sözlükleri iletişim kutusu görüntülenecektir  
Bu komuta bastığınızda seçili bir kelimenin üzerinde duruyorsanız, kelimenin varsayılan sözlükteki anlamına doğrudan erişeceksiniz.  
*	aksi halde seçim yapılmadığında bir diyalog açılır, düzenleme alanına istediğiniz kelimeyi girin, sekmeye tıklayın ve istediğiniz sözlüğü seçin ve enter tuşuna basın.  
Varsayılan Arapçadan İngilizceye, İngilizceden Arapçaya sözlükteki anlamı almak istiyorsanız, düzenleme alanında her zaman enter tuşuna basabilirsiniz; bundan sonra kelimenin anlamı ayrı bir göz atılabilir pencerede görüntülenecektir.  
*	Elbette eklentinin varsayılan sözlüğünü, tercihler menüsündeki eklentinin ayar panelinden değiştirebilirsiniz.  

## Ayar panelindeki seçenekler ##

*	Bu seçenekleri istediğiniz zaman eklentinin ayar paneline giderek aşağıdakileri kullanarak ayarlayabilirsiniz:
NVDA menüsü/tercihler/Ayarlar/Almaany sözlükleri  
*	Öncelikle bir açılan kutunuz var ve buradan eklentinin varsayılan sözlüğünü seçebilirsiniz.
Bu, bir kelimeyi seçip eklentinin hareketine bastığınızda, bu sözlükteki anlamına doğrudan erişmenize olanak tanıyacağı anlamına gelir.
Bundan sonra anlamı görüntülemek için kullanılan pencere türünü seçebilirsiniz.  
	1.	varsayılan ve ilk tercih, sıradan varsayılan tarayıcınızdır
bunu seçtiğinizde sonuç, varsayılan normal tam tarayıcınızda görüntülenecektir.  
	2.	ikinci seçenek, firefox veya google chrome'daki gibi bir tarayıcı penceresidir, dosya menüleri veya adres brar'ı olmayan bir tarayıcı penceresidir.
lütfen bu pencereyi yalnızca control+w veya alt+f4 tuşlarıyla kapatabileceğinizi unutmayın.  
	3.	üçüncüsü, yerel NVDA mesaj kutusudur, onu yalnızca test ettikten sonra kullanın ve eğer size uygunsa, deneyimlerimize göre bazen NVDA'nın donmasına neden olabilir.  
*	Bundan sonra, kelimenin anlamını talep ettikten sonra Sözlükler Almaany iletişim kutusunun kapatılıp kapatılmayacağını seçmek için bir onay kutunuz olur.  
*	Son olarak, NVDA'nın başlangıcında eklentinin otomatik güncellemesini etkinleştirmek veya devre dışı bırakmak için bir onay kutunuz var.

## 2.6.3'teki değişiklikler.

*	son test edilen sürüm güncellendi; böylece eklenti artık NVDA 2024.1 ile uyumludur.

## 2.6.2'deki değişiklikler.

*	Başlangıçta yeni sürümleri denetleyen otomatik güncelleme özelliği eklendi.
*	Ayar panelinde otomatik güncelleme için onay kutusu eklendi, varsayılan olarak etkindir. Dilerseniz devre dışı bırakılabilir.

## 2.6.1'deki değişiklikler.

*	İstenen sayfanın kodlamasının bazen Yok olması nedeniyle bir hata düzeltildi.
dolayısıyla bu durumda kodlamanın 'utf-8' olduğunu düşünüyoruz.

## 2.6 için değişiklikler.

*	Eklentiyi NVDA 2023.1 ile uyumlu hale getirmek için en son test edilen sürüm güncellendi.
 
## 2.5 için değişiklikler.

*	Eklenti NVDA 2022.1 ile uyumlu hale getirildi.
*	Sayfadan yeni eklenen İstenmeyen metin parçalarının normal ifade kullanılarak kaldırılması ve yerine boş bir dize konulması.

## 2.4 için değişiklikler.

*	Eklentinin ayar paneli aracılığıyla varsayılan sözlüğü değiştirme mümkün kılındı.
*	Python2 desteği bırakıldı ve urllib2 paketi eklentiden kaldırıldı.
Bu, test edilen minimum sürümün 2019.3 olarak değiştirildiği anlamına gelir.  
*	Eklenti doğru anlam veya sonuç alamadığında yakın zamanda ortaya çıkan bir sorun çözüldı.
Sorun, eski kullanıcı aracısını kaldırarak ve bunun yerine user_agent modülünü kullanarak çözüldü.

## 2.3 için değişiklikler.

*	Ayarlar iletişim kutusunda sonucu görüntülemek için varsayılan tam tarayıcıyı seçme seçeneği eklendi.
*	Başta Arapça Almanca ve Arapça Rusça sözlükler olmak üzere mevcut sözlüklerin listesine beş yeni sözlük eklendi.

## 2.1 için değişiklikler.

*	Eklenti için ayarlar iletişim kutusu oluşturuldu
*	Kullanıcıya, chrome veya firefox gibi kiosk modundaki tarayıcı penceresinde, menüler veya adres çubuğu olmadan tam ekranda sonuç alma seçeneği sunuldu.
*	Kullanıcıya çeviri talebinde bulunduktan sonra Almaany Sözlükleri iletişim kutusunu kapatma seçeneği sunuldu.

## 2.0 için değişiklikler.

*	Python 3 kullanılarak NVDA sürümleriyle uyumluluk eklendi.

## 1.1 için değişiklikler ##

bazı hatalar düzeltildi, eklentinin sunucuda çalışmayı bıraktıktan sonra çalışmaya geri dönmesi sağlandı
*	bir istek nesnesi oluşturmak için urllib2'yi kullanma
*	istek başlıklarına kullanıcı aracısı eklendi.

## 1.0 için değişiklikler ##

*	İlk sürüm.

### Katkılar ###

*	Eklentiyi python3'e taşıdığı ve son nvda eklenti şablonunu kullandığı için Abdel'in katkısına teşekkür ederiz.

[1]: https://github.com/ibrahim-h/dictionariesAlmaany/releases/download/2.6.3/DictionariesAlmaany-2.6.3.nvda-addon
