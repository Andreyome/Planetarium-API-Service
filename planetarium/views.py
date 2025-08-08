from datetime import datetime

from django.db.models import F, Count
from django.shortcuts import render
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import GenericViewSet

from planetarium.models import (
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    ShowTheme,
    Reservation
)
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
from planetarium.serializers import (
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    ShowThemeSerializer,
    AstronomyShowDetailSerializer,
    AstronomyShowListSerializer,
    ShowSessionDetailSerializer,
    ShowSessionListSerializer,
    ReservationSerializer,
    ReservationListSerializer,
)


class ShowThemeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PlanetariumDomeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AstronomyShowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = AstronomyShow.objects.prefetch_related("themes")
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @staticmethod
    def _params_to_inits(qs):
        """Converts list of string Ids to a list of integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the astronomy shows with filters"""
        show_theme = self.request.query_params.get("show_theme")
        title = self.request.query_params.get("title")

        queryset = self.queryset

        if show_theme:
            show_theme_ids = self._params_to_inits(show_theme)
            queryset = queryset.filter(show_themes__id__in=show_theme_ids)

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AstronomyShowDetailSerializer

        if self.action == 'list':
            return AstronomyShowListSerializer

        return AstronomyShowSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "show_theme",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by show_theme id (ex. ?show_theme=1,2)",
            ),
            OpenApiParameter(
                "title",
                type={"type": "string"},
                description="Filter by title (ex. ?title=title)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = (
        ShowSession.objects.all()
        .select_related("astronomy_show", "planetarium_dome")
        .annotate(
            tickets_available=(
                    F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")
                    - Count("tickets")
            )
        )
    )
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        date = self.request.query_params.get("date")
        astronomy_show_id_str = self.request.query_params.get("astronomy_show")

        queryset = self.queryset

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if astronomy_show_id_str:
            queryset = queryset.filter(astronomy_show_id=int(astronomy_show_id_str))

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ShowSessionDetailSerializer

        if self.action == 'list':
            return ShowSessionListSerializer

        return ShowSessionSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "date",
                type=OpenApiTypes.DATE,
                description="Filter by datetime of show_time (ex. ?date=2025-10-23)",
            ),
            OpenApiParameter(
                "astronomy_show",
                type=OpenApiTypes.INT,
                description="Filter by astronomy_show id (ex. ?astronomy_show=1)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Reservation.objects.prefetch_related(
        "tickets__show_session__astronomy_show", "tickets__show_session__planetarium_dome"
    )
    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
