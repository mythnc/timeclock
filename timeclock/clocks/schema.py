import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql import GraphQLError
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

from clocks.models import Clock


class ClockType(DjangoObjectType):
    class Meta:
        model = Clock


class Query(graphene.ObjectType):
    pass


"""
type ClockIn {
  clock: ClockType
}

type ClockOut {
  clock: ClockType
}
"""
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
        except ObjectDoesNotExist as e:
            raise GraphQLError("Alreday clocked out") from e
        else:
            clock.clocked_out = now()
            clock.save()
            return ClockOut(clock=clock)


class Mutation(graphene.ObjectType):
    clock_in = ClockIn.Field()
    clock_out = ClockOut.Field()
