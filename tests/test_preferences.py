from pathlib import Path

from app.core.preferences import PreferencesStore


def test_preferences_auto_save(tmp_path: Path) -> None:
    preferences_path = tmp_path / "preferences.json"
    store = PreferencesStore(path=preferences_path)

    assert store.auto_save is True
    store.update(theme="dark", language="fr")

    saved = preferences_path.read_text(encoding="utf-8")
    assert '"theme": "dark"' in saved
    assert '"language": "fr"' in saved

    reloaded = PreferencesStore.load(path=preferences_path)
    assert reloaded.theme == "dark"
    assert reloaded.language == "fr"
    assert reloaded.auto_save is True
