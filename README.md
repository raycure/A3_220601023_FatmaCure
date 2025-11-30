================================================================================
                    ROS 2 DOCKER PROJECT - BYM412 ROBOTİK ÖDEV 3
================================================================================

PROJE HAKKINDA
================================================================================

Bu proje, Docker konteynerizasyon teknolojisi kullanılarak ROS 2 Humble 
tabanlı üç düğümlü bir robotik sistem içermektedir.

Proje, sensör verisi üretimi, veri işleme ve servis sunumu işlevlerini yerine 
getiren üç ROS 2 düğümünden oluşmaktadır:

- sensor_publisher: Sahte sensör verisi üretir
- data_processor: Sensör verisini işler
- command_server: Servis isteklerine yanıt verir


SİSTEM MİMARİSİ
================================================================================

+------------------+
|sensor_publisher  |
|                  |
| 0.1s aralıklarla |
| rastgele veri    |
+--------+---------+
         |
         | /sensor_value (Float32)
         |
         v
+------------------+
| data_processor   |
|                  |
| value × 2        |
+--------+---------+
         |
         | /processed_value (Float32)
         |
         v
    [Yayınlanır]

+------------------+
| command_server   |
|                  |
| /compute_command |
| (Service)        |
+------------------+


PROJE YAPISI
================================================================================

ros2DockerProject/
├── Dockerfile
├── entrypoint.sh
├── README.md
├── SSF_HASH.txt
├── launch/
│   └── my_project.launch.py
└── src/
    ├── sensor_publisher_pkg/
    │   ├── sensor_publisher_pkg/
    │   │   ├── __init__.py
    │   │   └── sensor_publisher.py
    │   ├── package.xml
    │   ├── setup.cfg
    │   └── setup.py
    ├── data_processor_pkg/
    │   ├── data_processor_pkg/
    │   │   ├── __init__.py
    │   │   └── data_processor.py
    │   ├── package.xml
    │   ├── setup.cfg
    │   └── setup.py
    └── command_server_pkg/
        ├── command_server_pkg/
        │   ├── __init__.py
        │   └── command_server.py
        ├── srv/
        │   └── ComputeCommand.srv
        ├── package.xml
        ├── setup.cfg
        └── setup.py


KURULUM VE ÇALIŞTIRMA
================================================================================

GEREKSİNİMLER
--------------------------------------------------------------------------------
- Docker 20.10+
- Ubuntu 22.04 LTS (önerilen)
- 2 GB boş disk alanı


DOCKER İMAJINI OLUŞTURMA
--------------------------------------------------------------------------------

# Proje dizinine gidin
cd ros2DockerProject

# Docker imajını oluşturun
docker build -t myrosapp .


KONTEYNERİ BAŞLATMA
--------------------------------------------------------------------------------

# Konteyneri çalıştırın
docker run --rm myrosapp

Bu komut ile üç düğüm otomatik olarak başlatılacaktır.


DOĞRULAMA VE TEST
================================================================================

1. YENİ TERMİNAL AÇIN VE KONTEYNERE BAĞLANIN
--------------------------------------------------------------------------------

# Çalışan konteyner ID'sini alın
docker ps

# Konteynere bağlanın (CONTAINER_ID'yi kendi değerinizle değiştirin)
docker exec -it <CONTAINER_ID> bash


2. ROS 2 ORTAMINI YÜKLEYİN
--------------------------------------------------------------------------------

source /opt/ros/humble/setup.bash
source /ws/install/setup.bash


3. TOPIC'LERİ KONTROL EDİN
--------------------------------------------------------------------------------

# Topic listesini görüntüleyin
ros2 topic list

Beklenen çıktı:
/parameter_events
/processed_value
/rosout
/sensor_value


4. VERİ AKIŞINI İZLEYİN
--------------------------------------------------------------------------------

# İşlenmiş veriyi dinleyin
ros2 topic echo /processed_value

Çıktı örneği:
data: 19.64
---
data: 30.30
---
data: 11.52
---

Durdurmak için Ctrl+C tuşlayın.


5. SERVİSİ TEST EDİN
--------------------------------------------------------------------------------

# Servis çağrısı yapın (input > 10)
ros2 service call /compute_command command_server_pkg/srv/ComputeCommand "{input: 12.5}"

Beklenen yanıt:
response:
command_server_pkg.srv.ComputeCommand_Response(output='HIGH')


# Servis çağrısı yapın (input ≤ 10)
ros2 service call /compute_command command_server_pkg/srv/ComputeCommand "{input: 5.0}"

Beklenen yanıt:
response:
command_server_pkg.srv.ComputeCommand_Response(output='LOW')


DÜĞÜM DETAYLARI
================================================================================

1. SENSOR_PUBLISHER
--------------------------------------------------------------------------------
İşlev: Sahte sensör verisi üretir ve yayınlar

Yayınlanan Topic:
- /sensor_value (std_msgs/msg/Float32)

Özellikler:
- Frekans: 10 Hz (0.1 saniye)
- Veri aralığı: 0-20 arası rastgele sayı
- Fonksiyon: random.uniform(0, 20)


2. DATA_PROCESSOR
--------------------------------------------------------------------------------
İşlev: Gelen sensör verisini işler ve yeni topic'e yayınlar

Dinlediği Topic:
- /sensor_value (std_msgs/msg/Float32)

Yayınladığı Topic:
- /processed_value (std_msgs/msg/Float32)

İşleme Mantığı:
processed_value = sensor_value × 2

Örnek:
- Input: 9.82 → Output: 19.64
- Input: 15.15 → Output: 30.30


3. COMMAND_SERVER
--------------------------------------------------------------------------------
İşlev: Servis isteklerine yanıt verir

Servis Adı: /compute_command

Servis Tipi: command_server_pkg/srv/ComputeCommand

Servis Tanımı:
float64 input
---
string output

Mantık:
- input > 10 → "HIGH"
- input ≤ 10 → "LOW"


GELİŞTİRME
================================================================================

MANUEL BUILD (DOCKER OLMADAN)
--------------------------------------------------------------------------------

# ROS 2 ortamını yükleyin
source /opt/ros/humble/setup.bash

# Workspace'e gidin
cd ros2DockerProject

# Build edin
colcon build --symlink-install

# Workspace'i yükleyin
source install/setup.bash

# Launch dosyasını çalıştırın
ros2 launch launch/my_project.launch.py


YENİ DÜĞÜM EKLEME
--------------------------------------------------------------------------------

1. src/ dizininde yeni paket oluşturun
2. launch/my_project.launch.py dosyasına düğümü ekleyin
3. Docker imajını yeniden build edin


TEKNİK ÖZELLİKLER
================================================================================

Özellik                 | Değer
------------------------|------------------------
ROS Dağıtımı           | Humble Hawksbill
Python Versiyonu       | 3.10+
Docker Base Image      | ros:humble-ros-base
Build Sistemi          | colcon
Topic Frekansı         | 10 Hz
Servis Yanıt Süresi    | < 100ms


BİLİNEN SORUNLAR VE ÇÖZÜMLER
================================================================================

SORUN 1: "No such container" hatası
--------------------------------------------------------------------------------
Çözüm: Konteyner ID'sini doğru aldığınızdan emin olun

docker ps


SORUN 2: "The passed service type is invalid"
--------------------------------------------------------------------------------
Çözüm: Tam servis yolunu kullanın

ros2 service call /compute_command command_server_pkg/srv/ComputeCommand "{input: 12.5}"


SORUN 3: Topic'ler görünmüyor
--------------------------------------------------------------------------------
Çözüm: ROS 2 ortamını yüklediğinizden emin olun

source /opt/ros/humble/setup.bash
source /ws/install/setup.bash


KOMUT REFERANSI
================================================================================

DOCKER KOMUTLARI
--------------------------------------------------------------------------------

# İmaj oluşturma
docker build -t myrosapp .

# İmajları listeleme
docker images

# Konteyner başlatma
docker run --rm myrosapp

# Çalışan konteynerleri listeleme
docker ps

# Konteynere bağlanma
docker exec -it <CONTAINER_ID> bash

# Konteyneri durdurma
docker stop <CONTAINER_ID>

# Tüm konteynerleri durdurma
docker stop $(docker ps -q)


ROS 2 KOMUTLARI
--------------------------------------------------------------------------------

# Topic listesi
ros2 topic list

# Topic bilgisi
ros2 topic info /sensor_value

# Topic dinleme
ros2 topic echo /processed_value

# Servis listesi
ros2 service list

# Servis tipi
ros2 service type /compute_command

# Servis çağrısı
ros2 service call /compute_command command_server_pkg/srv/ComputeCommand "{input: 12.5}"

# Node listesi
ros2 node list

# Node bilgisi
ros2 node info /sensor_publisher


HIZLI BAŞLANGIÇ REHBERİ
================================================================================

ADIM 1: Docker İmajını Oluşturun
--------------------------------------------------------------------------------
cd ros2DockerProject
docker build -t myrosapp .


ADIM 2: Konteyneri Başlatın
--------------------------------------------------------------------------------
docker run --rm myrosapp


ADIM 3: Yeni Terminal Açın ve Test Edin
--------------------------------------------------------------------------------
# Konteyner ID'sini alın
docker ps

# Konteynere girin
docker exec -it <CONTAINER_ID> bash

# Ortamı yükleyin
source /opt/ros/humble/setup.bash
source /ws/install/setup.bash

# Topic'leri kontrol edin
ros2 topic list

# Veriyi izleyin
ros2 topic echo /processed_value

# Servisi test edin
ros2 service call /compute_command command_server_pkg/srv/ComputeCommand "{input: 12.5}"


PROJE ÖZETİ
================================================================================

Bu projede, Docker konteynerizasyon teknolojisi kullanılarak ROS 2 Humble 
tabanlı üç düğümlü bir robotik sistem geliştirilmiştir. 

Geliştirilen sistem:
✓ sensor_publisher düğümü ile 0.1 saniye aralıklarla sensör verisi üretiyor
✓ data_processor düğümü ile veriyi işleyip yayınlıyor
✓ command_server düğümü ile servis sunuyor
✓ Launch dosyası ile tüm düğümleri birlikte başlatıyor
✓ Docker konteyneri içinde sorunsuz çalışıyor

Sistem, taşınabilir, ölçeklenebilir ve yeniden kullanılabilir bir yapıya 
sahiptir.


SORU-CEVAP
================================================================================

S: Docker olmadan çalıştırabilir miyim?
C: Evet, manuel build bölümündeki adımları takip edin.

S: Yeni düğüm nasıl eklerim?
C: src/ dizininde yeni paket oluşturun ve launch dosyasına ekleyin.

S: Servis yanıt vermiyor?
C: Tam servis yolunu kullandığınızdan emin olun.

S: Topic'ler görünmüyor?
C: ROS 2 ortamını source ile yüklediğinizden emin olun.

S: Konteyner durmuyor?
C: docker stop <CONTAINER_ID> komutunu kullanın.


PERFORMANS İPUÇLARI
================================================================================

1. Docker imaj boyutunu azaltmak için multi-stage build kullanın
2. --symlink-install ile hızlı geliştirme yapın
3. QoS ayarlarını optimize edin
4. Log seviyesini ihtiyaca göre ayarlayın
5. Gereksiz paketleri Docker imajından çıkarın


GÜVENLİK NOTLARI
================================================================================

- Konteynerleri --rm flag ile çalıştırarak otomatik temizlik yapın
- Üretim ortamında root kullanıcısı yerine ayrı kullanıcı oluşturun
- Docker imajlarını düzenli olarak güncelleyin
- Hassas bilgileri environment variable olarak saklayın
- Network izolasyonu için Docker network kullanın


GELİŞTİRİCİ BİLGİLERİ
================================================================================

Ad Soyad        : [Adınız Soyadınız]
Öğrenci No      : 220601023
Üniversite      : İstanbul Sağlık ve Teknoloji Üniversitesi
Ders            : BYM412 Robotik
Dönem           : 2024-2025 Güz
İletişim        : [email@example.com]


FAYDALI BAĞLANTILAR
================================================================================

ROS 2 Humble Dokumentasyonu:
https://docs.ros.org/en/humble/

Docker Dokumentasyonu:
https://docs.docker.com/

ROS 2 Launch Dosyaları:
https://docs.ros.org/en/humble/Tutorials/Intermediate/Launch/Launch-Main.html

colcon Build Sistemi:
https://colcon.readthedocs.io/


LİSANS
================================================================================

Bu proje eğitim amaçlı geliştirilmiştir.
İstanbul Sağlık ve Teknoloji Üniversitesi BYM412 Robotik dersi 
Ödev 3 kapsamında hazırlanmıştır.


TEŞEKKÜRLER
================================================================================

- ROS 2 Documentation Team
- Docker Community
- İSTE BYM412 Dersi Öğretim Üyeleri
- Açık Kaynak Topluluğu


SON GÜNCELLEME
================================================================================

Tarih: Kasım 2025
Versiyon: 1.0


================================================================================
                              PROJE TAMAMLANDI
================================================================================

Bu README dosyası, projenin kurulumu, kullanımı ve testi hakkında tüm 
gerekli bilgileri içermektedir. Herhangi bir sorunla karşılaşırsanız, 
"Bilinen Sorunlar ve Çözümler" bölümüne bakın veya iletişim bilgilerini 
kullanarak ulaşın.

Başarılar dileriz!

================================================================================
