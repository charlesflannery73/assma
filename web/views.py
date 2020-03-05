from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Org, Asset
from .forms import OrgSearchForm, AssetSearchForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter

def home(request):
    return render(request, 'home.html', {'title': 'Home'})


class AssetFilter(BaseFilter):
    search_fields = {
        'search_text': ['name'],
        'search_org': ['org__name'],
        'search_type': ['type'],
        'search_comment': ['comment'],
    }


class AssetSearchList(SearchListView):
    # regular django.views.generic.list.ListView configuration
    model = Asset
    paginate_by = 5
    template_name = "web/asset_search_result.html"
    ordering = ['name']

    # additional configuration for SearchListView
    form_class = AssetSearchForm
    filter_class = AssetFilter


class OrgFilter(BaseFilter):
    search_fields = {
        'search_text': ['name'],
        'search_sector': ['sector__sector'],
        'search_level': ['level__level'],
        'search_tier': ['tier'],
        'search_id': ['id'],
        'search_comment': ['comment'],
    }


class OrgSearchList(SearchListView):
    # regular django.views.generic.list.ListView configuration
    model = Org
    paginate_by = 5
    template_name = "web/org_search_result.html"
    ordering = ['name']

    # additional configuration for SearchListView
    form_class = OrgSearchForm
    filter_class = OrgFilter


class OrgListView(ListView):       # <app>/<model>_<viewtype>.html
    model = Org
    template_name = 'org_list.html'
    context_object_name = 'orgs'
    ordering = ['-modified']
    paginate_by = 5


class OrgDetailView(DetailView):
    model = Org


class OrgCreateView(LoginRequiredMixin, CreateView):
    model = Org
    fields = ['name', 'sector', 'level', 'tier', 'comment']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class OrgUpdateView(LoginRequiredMixin, UpdateView):
    model = Org
    fields = ['name', 'sector', 'level', 'tier', 'comment']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class OrgDeleteView(LoginRequiredMixin, DeleteView):
    model = Org
    success_url = '/'


class AssetListView(ListView):       # <app>/<model>_<viewtype>.html
    model = Asset
    template_name = 'asset_list.html'
    context_object_name = 'assets'
    ordering = ['-modified']
    paginate_by = 5

class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Asset
    fields = ['name', 'org', 'type', 'comment']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AssetDetailView(DetailView):
    model = Asset

class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    fields = ['name', 'org', 'type', 'comment']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    success_url = '/'


def about(request):
    return render(request, 'about.html', {'title': 'About'})

