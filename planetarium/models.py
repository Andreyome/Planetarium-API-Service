from django.contrib.auth import get_user_model
from django.db import models



class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    themes = models.ManyToManyField(ShowTheme, blank=True)

    def __str__(self):
        return self.title


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE, related_name='sessions')
    planetarium_dome = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE, related_name='sessions')
    show_time = models.DateTimeField()

    class Meta:
        ordering = ["-show_time"]

    def __str__(self):
        return f"{self.astronomy_show.title} {self.show_time}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation by {self.user.username} at {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE, related_name='tickets')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='tickets')

    class Meta:
        unique_together = ('row', 'seat', 'show_session')

    def __str__(self):
        return f"Row: {self.row}, Seat: {self.seat} for {self.show_session}"
