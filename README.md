# Zadanie 1, v 1.0, zadanie obowiązkowe
1. **Pobieramy ubuntu server ISO**  
2. **Przekazujemy maszyny :**  ftp://sr2024:sr2024@192.168.17.50 lub na dyskach, przed przekazaniem wyłączamy firewalla  oraz zmieniamy nazwę interfejsu sieciowego na ens18    
3. **Tworzymy nową maszynę na Virtualboxie :**  parametry: 10GB, 4GB RAM, minimum 2CPU  
4. **Musi być wyłączona sieć w trakcie instalacji**  
5. **Nazwa maszyny:**   [psisk/datascience]_nrindexu  
6. **W trakcie instalacji bardzo ważne:**   przy konfiguracji dysku: wyłączamy LVM,   Instalujemy jedynie OpenSSH server  
7. **Nadajemy usera:**   inf2ns_systemy_rozproszone_2024Z_nrindexu  
8. **Hasło przekazujemy mailem w sposób zaszyfrowany do prowadzącego (Cleopatra/ GNUPG)** 
9. **Testy sieci:**   
- ustawienia obecnego adresu IP jako stałego – wyłączenie dhcp,    
- odłączenie od sieci,    
- przywrócenie do sieci    
10. **apt install net-tools –y , ifconfig**  
11. **Testy widoczności maszyn pomiędzy użytkownikami**  
12. **Instalacje:**
- Uncomplicated Firewall    
- Midnight commander    
13. **Stworzenie wykonywalnego pliku bash firewall.sh**    
- Będzie blokował wszystko wchodzące, otworzy tylko port 80    
- Sprawdzić z pozostałych/innych maszyn, czy działa ping    
- Czy działa ping po porcie 80    
- Połączyć się ponownie za pomocą Putty    
14. **Dokonać aktualizacji Ubuntu**  
15. **Dokonać trimowania dysku,   niech będzie ustawione w cronie co 30minut**  
16. **Zainstalować qemu-guest-agent**  
17. **Zamontować gparted.iso, sprawdzić wielkość partycji,   zmniejszyć tak, by zostało maksymalnie 3GB wolnego miejsca**  
18. **Usunąć zbędne oprogramowanie za pomocą deborphan**  
19. **Sprawdzić, czy poprawnie działa połączenie z serwerem ntp**  
20. **Zainstalować :**  
- Apache  
- MariaDB  
- PHP w wersji 8.2  
- phpmyadmin w najnowszej wersji  
21. **Dodać autoryzację htaccess/htpasswd dla   phpmyadmin oraz głównego katalogu apache’a**  
22. **Wyłączyć globalne –indexes w Apache**  
23. **Sprawdzić i naprawić ustawienia mysql za pomocą mysql_secure_installation**  
