# Zadanie 1, v 1.0, zadanie obowiązkowe
1. Pobieramy ubuntu server ISO  
2. Przekazujemy maszyny :   ftp://sr2024:sr2024@192.168.17.50 lub na dyskach, przed przekazaniem wyłączamy firewalla  oraz zmieniamy nazwę interfejsu sieciowego na ens18  
Tworzymy nową maszynę na Virtualboxie : parametry: 10GB, 4GB RAM, minimum 2CPU  
Musi być wyłączona sieć w trakcie instalacji  
Nazwa maszyny: [psisk/datascience]_nrindexu  
W trakcie instalacji bardzo ważne: przy konfiguracji dysku: wyłączamy LVM, Instalujemy jedynie OpenSSH server  
Nadajemy usera: inf2ns_systemy_rozproszone_2024Z_nrindexu  
Hasło przekazujemy mailem w sposób zaszyfrowany do prowadzącego  
**Testy sieci:**  
ustawienia obecnego adresu IP jako stałego – wyłączenie dhcp,  
odłączenie od sieci,  
przywrócenie do sieci  
apt install net-tools –y , ifconfig  
Testy widoczności maszyn pomiędzy użytkownikami  
**Instalacje:**
Uncomplicated Firewall  
Midnight commander  
Stworzenie wykonywalnego pliku bash:  firewall.sh  
będzie blokował wszystko wchodzące, otworzy tylko port 80  
Sprawdzić z pozostałych/innych maszyn, czy działa ping  
Oraz czy działa ping po porcie 80  
Połączyć się ponownie za pomocą Putty  
Dokonać aktualizacji Ubuntu  
Dokonać trimowania dysku, niech będzie ustawione w cronie co 30minut  
Zainstalować qemu-guest-agent  
Zamontować gparted.iso, sprawdzić wielkość partycji, zmniejszyć tak, by zostało maksymalnie 3GB wolnego miejsca  
Usunąć zbędne oprogramowanie za pomocą deborphan  
Sprawdzić, czy poprawnie działa połączenie z serwerem ntp  
**Zainstalować :**  
Apache  
MariaDB  
PHP w wersji 8.2  
phpmyadmin w ostatniej wersji  
Dodać autoryzację htaccess/htpasswd dla phpmyadmin oraz głównego katalogu apache’a.  
Wyłączyć globalne –indexes w Apache  
Sprawdzić i naprawić ustawienia mysql za pomocą mysql_secure_installation  
