from borgmatic.commands import completion as module


def test_bash_completion_does_not_raise():
    assert module.bash_completion()


def test_fish_completion_does_not_raise():
    assert module.fish_completion()
