from emoji_progress_bar import SlackBusySpinner


def test_clock_emoji() -> None:
    expected = [
        "clock1",
        "clock130",
        "clock2",
        "clock230",
        "clock3",
        "clock330",
        "clock4",
        "clock430",
        "clock5",
        "clock530",
        "clock6",
        "clock630",
        "clock7",
        "clock730",
        "clock8",
        "clock830",
        "clock9",
        "clock930",
        "clock10",
        "clock1030",
        "clock11",
        "clock1130",
        "clock12",
        "clock1230",
    ]
    emojis = []
    slack_answer = SlackBusySpinner()
    for _ in range(48):
        emojis.append(next(slack_answer))
    assert emojis == expected * 2
