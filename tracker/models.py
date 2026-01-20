from django.db import models

# This table stores the TV Shows you follow
class Show(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField()
    poster_path = models.URLField()
    tmdb_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.title

# This table stores every episode for those shows
class Episode(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='episodes')
    season_number = models.IntegerField()
    episode_number = models.IntegerField()
    name = models.CharField(max_length=200)
    watched = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.show.title} - S{self.season_number}E{self.episode_number}"
