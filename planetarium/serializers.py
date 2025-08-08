from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from planetarium.models import PlanetariumDome, ShowTheme, AstronomyShow, ShowSession, Ticket, Reservation


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ["id", "name", "rows", "seats_in_row", "capacity"]


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ['id', 'name']


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ['id', 'title', 'description', 'themes']


class AstronomyShowListSerializer(AstronomyShowSerializer):
    themes = SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = AstronomyShow
        fields = ['id', 'title', 'description', 'themes']


class AstronomyShowDetailSerializer(AstronomyShowSerializer):
    themes = ShowThemeSerializer(many=True, read_only=True)

    class Meta:
        model = AstronomyShow
        fields = ['id', 'title', 'description', 'themes']


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ['id', 'astronomy_show', 'planetarium_dome', 'show_time']


class ShowSessionListSerializer(ShowSessionSerializer):
    planetarium_dome_name = serializers.CharField(
        source='planetarium_dome.name', read_only=True
    )
    astronomy_show = serializers.CharField(
        source='astronomy_show.name', read_only=True
    )
    planetarium_dome_capacity = serializers.IntegerField(
        source='planetarium_dome_capacity.name', read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShowSession
        fields = [
            'id',
            'astronomy_show',
            'planetarium_dome_name',
            'planetarium_dome_capacity',
            'tickets_available'
        ]


class TicketSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["show_session"].planetarium_dome,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ['id', 'row', 'seat', 'show_session', "reservation"]


class TicketListSerializer(TicketSerializer):
    show_session = ShowSessionListSerializer(many=False, read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ['row', 'seat']


class ShowSessionDetailSerializer(serializers.ModelSerializer):
    astronomy_show = AstronomyShowListSerializer(many=False, read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(many=False, read_only=True)
    taken_seats = TicketSeatsSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = ShowSession
        fields = (
            'id',
            'show_time',
            'astronomy_show',
            'planetarium_dome',
            'taken_seats',
        )

class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True, allow_empty=True)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
