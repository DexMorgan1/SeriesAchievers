import requests
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Show, Episode

def index(request):
    shows = Show.objects.all()
    return render(request, 'tracker/index.html', {'shows': shows})

def show_detail(request, pk):
    show = get_object_or_404(Show, pk=pk)
    episodes = show.episodes.all().order_by('season_number', 'episode_number')
    return render(request, 'tracker/show_detail.html', {'show': show, 'episodes': episodes})

def add_show(request):
    results = []
    if request.method == 'POST':
        if 'query' in request.POST:
            query = request.POST.get('query')
            url = f"https://api.tvmaze.com/search/shows?q={query}"
            response = requests.get(url)
            if response.status_code == 200:
                results = response.json()
        
        elif 'tmdb_id' in request.POST:
            show_id = request.POST.get('tmdb_id')
            if not Show.objects.filter(tmdb_id=show_id).exists():
                url = f"https://api.tvmaze.com/shows/{show_id}?embed=episodes"
                resp = requests.get(url).json()
                
                new_show = Show.objects.create(
                    title=resp['name'],
                    overview=resp.get('summary', ''),
                    poster_path=resp['image']['medium'] if resp.get('image') else '',
                    tmdb_id=show_id
                )
                
                episodes_data = resp.get('_embedded', {}).get('episodes', [])
                for ep in episodes_data:
                    Episode.objects.create(
                        show=new_show,
                        season_number=ep['season'],
                        episode_number=ep['number'],
                        name=ep['name']
                    )
            return redirect('index')

    return render(request, 'tracker/add_show.html', {'results': results})

@api_view(['POST'])
def mark_watched(request):
    episode_id = request.data.get('episode_id')
    episode = get_object_or_404(Episode, id=episode_id)
    episode.watched = not episode.watched
    episode.save()
    return Response({'status': 'ok', 'watched': episode.watched})
              
