from datetime import datetime


def log_title(title, show_datetime=True, show_separator=True):
    if show_datetime is True:
        date = datetime.now().strftime("%A %B %-m, %H:%M:%S") + ": "
    else:
        date = ""

    if show_separator is True:
        print("#" * 50)
    print(date + title)
    if show_separator is True:
        print("#" * 50)


def log_end_result(title, result, show_datetime=True, show_separator=True):
    if show_datetime is True:
        date = datetime.now().strftime("%A %B %-m, %H:%M:%S") + ": "
    else:
        date = ""

    if show_separator is True:
        print("#" * 50)
    print(date + title)
    if show_separator is True:
        print("-" * 50)
    print("  ", result)
    if show_separator is True:
        print("#" * 50)
