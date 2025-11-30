ROS 2 DOCKER PROJECT - BYM412 ROBOTİK ÖDEV 3

PROJE HAKKINDA
================================================================================

Bu proje, Docker konteynerizasyon teknolojisi kullanılarak ROS 2 Humble 
tabanlı üç düğümlü bir robotik sistem içermektedir.

Proje, sensör verisi üretimi, veri işleme ve servis sunumu işlevlerini yerine 
getiren üç ROS 2 düğümünden oluşmaktadır:

- sensor_publisher: Sahte sensör verisi üretir
- data_processor: Sensör verisini işler
- command_server: Servis isteklerine yanıt verir

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

GÜVENLİK NOTLARI
================================================================================

- Konteynerleri --rm flag ile çalıştırarak otomatik temizlik yapın
- Üretim ortamında root kullanıcısı yerine ayrı kullanıcı oluşturun
- Docker imajlarını düzenli olarak güncelleyin
- Hassas bilgileri environment variable olarak saklayın
- Network izolasyonu için Docker network kullanın


GELİŞTİRİCİ BİLGİLERİ
================================================================================

Ad Soyad        : Fatma Cüre
Öğrenci No      : 220601023
Üniversite      : İstanbul Sağlık ve Teknoloji Üniversitesi
Ders            : BYM412 Robotik
Dönem           : 2024-2025 Güz


LİSANS
================================================================================

Bu proje eğitim amaçlı geliştirilmiştir.
İstanbul Sağlık ve Teknoloji Üniversitesi BYM412 Robotik dersi 
Ödev 3 kapsamında hazırlanmıştır.


SON GÜNCELLEME
================================================================================

Tarih: Kasım 2025
Versiyon: 1.0
