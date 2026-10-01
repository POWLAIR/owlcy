"""W5 — Secrets dans le Windows Credential Manager (le futur « coffre » d'Owlcy).

    python -m pip install keyring
    python test_keyring.py
Vérifier ensuite dans « Gestionnaire d'identification Windows » > Informations d'identification Windows
qu'une entrée « owlcy-test » apparaît, puis qu'elle disparaît à la fin.
"""
import keyring, time

print("Backend :", keyring.get_keyring())
t = time.perf_counter()
keyring.set_password("owlcy-test", "notion", "secret-de-test-123")
print("Écriture OK en", round((time.perf_counter() - t) * 1000, 1), "ms")
input("→ Vérifie l'entrée dans le Gestionnaire d'identification, puis Entrée…")
assert keyring.get_password("owlcy-test", "notion") == "secret-de-test-123"
print("Lecture OK")
keyring.delete_password("owlcy-test", "notion")
assert keyring.get_password("owlcy-test", "notion") is None
print("Suppression OK — test réussi")
