from datetime import timedelta

import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql import GraphQLError
from django.utils.timezone import now

from clocks.models import Clock


class ClockType(DjangoObjectType):
    class Meta:
        model = Clock


class CurrentClockType(graphene.ObjectType):
    clock = graphene.Field(ClockType)


class ClockedHoursType(graphene.ObjectType):
    today = graphene.Int()
    current_week = graphene.Int()
    current_month = graphene.Int()


class Query(graphene.ObjectType):
    current_clock = graphene.Field(CurrentClockType)
    clocked_hours = graphene.Field(ClockedHoursType)

    @login_required
    def resolve_current_clock(self, info):
        user = info.context.user
        try:
            clock = Clock.objects.filter(user=user, clocked_in__isnull=False, clocked_out__isnull=True).get()
        except Clock.DoesNotExist as e:
            return None
        else:
            return CurrentClockType(clock=clock)

    @login_required
    def resolve_clocked_hours(self, info):
        user = info.context.user
        today = now().replace(hour=0, minute=0, second=0, microsecond=0)
        return ClockedHoursType(
            today = Query.get_clocked_hours_today(today, user),
            current_week = Query.get_clocked_hours_week(today, user),
            current_month = Query.get_clocked_hours_month(today, user)
        )
    
    @staticmethod
    def get_clocked_hours_today(today, user):
        return Query.get_working_hours(today, today + timedelta(days=1), user)

    @staticmethod
    def get_working_hours(gte_datetime, lt_datetime, user):
        working_seconds = 0
        for clock in Clock.objects.filter(
            user=user,
            clocked_in__gte=gte_datetime,
            clocked_in__lt=lt_datetime,
            clocked_out__isnull=False
        ):
            end_datetime = clock.clocked_out
            if end_datetime > lt_datetime:
                end_datetime = lt_datetime
            working_seconds += (end_datetime.timestamp() - clock.clocked_in.timestamp())

        print(working_seconds)
        return round(int(working_seconds) / 3600)

    @staticmethod
    def get_clocked_hours_week(today, user):
        week_start = today - timedelta(days=today.weekday())
        return Query.get_working_hours(week_start, week_start + timedelta(days=7), user)

    @staticmethod
    def get_clocked_hours_month(today, user):
        month_start = today - timedelta(days=today.day-1)
        month_end = month_start.replace(month=month_start.month+1)
        return Query.get_working_hours(month_start, month_end, user)


class ClockIn(graphene.Mutation):
    clock = graphene.Field(ClockType)

    @login_required
    def mutate(self, info):
        user = info.context.user
        # Check existed clockin before doing anything
        if Clock.objects.filter(user=user, clocked_in__isnull=False, clocked_out__isnull=True).exists():
            raise GraphQLError("Alreday clocked in")

        clock = Clock(user=user)
        clock.save()
        return ClockIn(clock=clock)


class ClockOut(graphene.Mutation):
    clock = graphene.Field(ClockType)

    @login_required
    def mutate(self, info):
        user = info.context.user
        # Check existed clockin before doing anything
        try:
            clock = Clock.objects.filter(user=user, clocked_in__isnull=False, clocked_out__isnull=True).get()
        except Clock.DoesNotExist as e:
            raise GraphQLError("Alreday clocked out") from e
        else:
            clock.clocked_out = now()
            clock.save()
            return ClockOut(clock=clock)


class Mutation(graphene.ObjectType):
    clock_in = ClockIn.Field()
    clock_out = ClockOut.Field()
