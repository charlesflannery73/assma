from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Org, Asset
from .forms import OrgSearchForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter

def home(request):
    return render(request, 'home.html', {'title': 'Home'})


class OrgFilter(BaseFilter):
    search_fields = {
        'search_text': ['name', 'name'],
        'search_sector': ['sector', 'sector'],
        'search_level': ['level', 'level'],
        'search_tier': ['tier', 'tier'],
        'search_comment': ['comment', 'comment'],
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

class OrgUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Org
    fields = ['name', 'sector', 'level', 'tier', 'comment']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        org = self.get_object()
        if self.request.user == org.author:
            return True
        return False


class OrgDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Org
    success_url = '/'

    def test_func(self):
        org = self.get_object()
        if self.request.user == org.author:
            return True
        return False

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

class AssetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Asset
    fields = ['name', 'org', 'type', 'comment']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        asset = self.get_object()
        if self.request.user == asset.author:
            return True
        return False

class AssetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Asset
    success_url = '/'


    def test_func(self):
        org = self.get_object()
        if self.request.user == Asset.author:
            return True
        return False


def about(request):
    return render(request, 'about.html', {'title': 'About'})

