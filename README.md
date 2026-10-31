# Generator projektu środowiska JSON

Minimalny moduł Pythona: wczytuje projekt JSON, sprawdza pomieszczenia, ściany, światła, dekoracje i punkty startowe, a następnie zapisuje znormalizowany JSON. Nie generuje grafiki PNG, modeli 3D ani gotowych map do silnika gry.

## Uruchomienie

```sh
python -m pip install -e ".[test]"
python -m kf2_env_generator examples/sample_project.json output.json
python -m pytest -q
```

Nazwa pakietu `kf2_env_generator` jest zachowana dla zgodności. W kontekście WorkShop3D KF2 oznacza Kroniki Fallathanu, a nie Killing Floor 2. Projekt nie zawiera integracji z grą ani SDK i nie potwierdza zgodności wygenerowanych danych z kanonem świata.

[Architektura i ograniczenia](ARCHITECTURE_KF2.md). Bieżące testy: [GitHub Actions](https://github.com/Rotherw/Gpt/actions). Brak samodzielnego instalatora.
