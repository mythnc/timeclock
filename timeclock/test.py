from datetime import datetime, timedelta, timezone

from django.contrib.auth import get_user_model

from clocks.models import Clock


def create_user():
    user = get_user_model()(
        username = "test",
        email = "kk@aa.com",
    )
    user.set_password("pp")
    user.save()
    return user


def add_clock_data(user):
    date_start = datetime(2022, 5, 1, tzinfo=timezone.utc)
    date_end = datetime(2022, 5 , 31, tzinfo=timezone.utc)
    dt = date_start
    while dt <= date_end:
        clock = Clock(user=user, clocked_in=dt.replace(hour=8), clocked_out=dt.replace(hour=18))
        clock.save()
        print(clock)
        dt = dt + timedelta(days=1)


def main():
    user = create_user()
    print(user)
    add_clock_data(user)


main()