# Anki utils

- `apkg_to_toml`: converts an Anki deck (.apkg file) to a TOML deck.
- `toml_to_apkg`: converts a TOML deck to an .apkg file.

Onlike other similar projects, this project aims to _only_ extract from the apkg file what is strictly necessary to recreate the apkg file.

For reference:

- https://github.com/ankidroid/Anki-Android/wiki/Database-Structure
- https://github.com/Stvad/CrowdAnki


## TODO

- Hooks when exporting and importing for deck-specific logic.

### `apkg_to_toml`

- Map fields as defined in `col`
- `apkg_to_toml` only extracts `notes`, it should also extract and process `col`, so that the deck can be fully recreated
- Extract metdata: title, description (if present), modified date (of deck and cards)
- Export and import media (when necessary)

### `toml_to_apkg`

- Instead of dealing with SQL directly, it may make sense to use one of the projects below, which provide a Python API to creating apkg files.
  - https://github.com/kerrickstaley/genanki
  - https://github.com/patarapolw/ankisync2
- `col`
- Nested decks
- Metadata
- Media
