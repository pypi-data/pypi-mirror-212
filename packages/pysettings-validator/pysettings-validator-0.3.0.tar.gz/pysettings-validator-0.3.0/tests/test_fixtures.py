def test_settings_changes_1(settings):
    assert settings.description == "A shiny Website!"
    settings.description = "Test 1"
    assert settings.description == "Test 1"


def test_settings_changes_2(settings):
    assert settings.description == "A shiny Website!"
    settings.description = "Test 2"
    assert settings.description == "Test 2"
