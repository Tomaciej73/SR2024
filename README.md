# Zadanie nr 5, v 1.0, grupa zadań: 3
Zadaniem jest przygotowanie systemu prezentującego sposoby uwierzytelniania i dostępu do zasobów w środowisku rozproszonym.
Zabezpieczenie powinno zostać wykonane przy pomocy tokenów JWT. Żądania mają być wykonywane za pomocą CURL.
Przygotowany projekt powinien wypełniać następujące założenia i scenariusze:

**Projekt wypełniać następujące założenia:**
1. Przygotować system uwierzytelniający
2. Przygotować system dziedzinowy
3. System uwierzytelniający posiada możliwość logowania, tworzenia tokenów JWT i posiada API, które można wykorzystać do uzyskiwania uprawnień do zasobów
4. Uwierzytelnienie powinno być wykonane przy zachowaniu zasad bezpieczeństwa
5. System dziedzinowy powinien posiadać routing, na którym będzie można podejżeć zawartość tokenu po autoryzacji

**API powinno wypełniać następujące scenariusze:**
*Jako użytkownik*
- Powinienem móc zalogować się poprzez system uwierzytelniający i uzyskać token JWT
- Powinienem móc sprawdzić czy token jest poprawny
- Powinienem móc przy pomocy uzyskanego tokenu JWT uzyskać dostęp do “zasobu”

**Dodatkowo**
- Powinien móc podejrzeć zawartość tokenu JWT

**Projekt zaliczeniowy ma być napisany w frameworku Symfony 6.4.x**

**Sprawozdanie powinno zawierać:**
1. Prezentację struktury tokenu JWT
2. Schemat struktury komunikacji systemów
3. Przepływ uwierzytelniania
4. Udokumentowane wszystkie scenariusze z żądaniami i odpowiedziami serwera
5. Udokumentowane zastosowane środki zabezpieczania samego tokenu i jego bezpiecznej obsługi
