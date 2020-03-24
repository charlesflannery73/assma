from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Org, Asset
from .forms import OrgSearchForm, AssetSearchForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter
from django.db.models import Q
from django.urls import reverse


class HomeView(View):
    def get(self, request, *args, **kwargs):
        orgs = Org.objects.filter().order_by('-modified')[:5]
        assets = Asset.objects.filter().order_by('-modified')[:5]
        return render(request, 'home.html', {'orgs': orgs, 'assets': assets})


def about(request):
    return render(request, 'about.html', {'title': 'About'})


class AssetFilter(BaseFilter):
    search_fields = {
        'search_text': ['name'],
        'search_org': ['org__name'],
        'search_type': ['type'],
        'search_comment': ['comment'],
    }


class OrgFilter(BaseFilter):
    search_fields = {
        'search_text': ['name'],
        'search_sector': ['sector'],
        'search_level': ['level'],
        'search_tier': ['tier'],
        'search_id': ['id'],
        'search_comment': ['comment'],
    }

class AssetSearch(SearchListView):
    model = Asset
    template_name = "web/search.html"
    form_class = AssetSearchForm
    filter_class = AssetFilter
    ordering = ['name']

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['search_text']
            org = form.cleaned_data['search_org']
            type = form.cleaned_data['search_type']
            comment = form.cleaned_data['search_comment']
            params = "name=" + name + "&org=" + org + "&type=" + type + "&comment=" + comment
            return HttpResponseRedirect(reverse('asset-list') +'?%s' % params)

        return render(request, self.template_name, {'form': form})


class OrgSearch(SearchListView):
    model = Org
    template_name = "web/search.html"
    form_class = OrgSearchForm
    filter_class = OrgFilter
    ordering = ['name']

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['search_text']
            sector = form.cleaned_data['search_sector']
            level = form.cleaned_data['search_level']
            tier = form.cleaned_data['search_tier']
            if tier == None:
                tier = ""
            coid = form.cleaned_data['search_id']
            if coid == None:
                coid = ""
            comment = form.cleaned_data['search_comment']
            params = "name=" + name + "&sector=" + sector + "&level=" + level + "&comment=" + comment + "&tier=" + str(tier) + "&coid=" + str(coid)
            return HttpResponseRedirect(reverse('org-list') +'?%s' % params)

        return render(request, self.template_name, {'form': form})


class OrgListView(ListView):
    model = Org
    template_name = 'web/org_list.html'
    context_object_name = 'orgs'
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get('name') == None:
            return Org.objects.filter().order_by('name')
        name_val = self.request.GET.get('name')
        sector_val = self.request.GET.get('sector')
        level_val = self.request.GET.get('level')
        tier_val = self.request.GET.get('tier')
        id_val = self.request.GET.get('coid')
        comment_val = self.request.GET.get('comment')
        new_context = Org.objects.filter(
            Q(name__icontains=name_val) &
            Q(sector__icontains=sector_val) &
            Q(level__icontains=level_val) &
            Q(tier__icontains=tier_val) &
            Q(id__icontains=id_val) &
            Q(comment__icontains=comment_val)
        ).order_by('name')
        return new_context


class OrgDetailView(DetailView):
    model = Org


class OrgCreateView(LoginRequiredMixin, CreateView):
    model = Org
    fields = ['name', 'sector', 'level', 'tier', 'comment']
    success_url = '/'


class OrgUpdateView(LoginRequiredMixin, UpdateView):
    model = Org
    fields = ['name', 'sector', 'level', 'tier', 'comment']
    success_url = '/'


class OrgDeleteView(LoginRequiredMixin, DeleteView, View):
    model = Org
    success_url = '/'


class AssetListView(ListView):
    model = Asset
    template_name = 'web/asset_list.html'
    context_object_name = 'assets'
    ordering = ['-modified']
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get('name') == None:
            return Asset.objects.filter().order_by('name')
        name_val = self.request.GET.get('name')
        org_val = self.request.GET.get('org')
        type_val = self.request.GET.get('type')
        comment_val = self.request.GET.get('comment')
        new_context = Asset.objects.filter(
            ((Q(end_ip__gte=name_val) & Q(start_ip__lte=name_val)) | Q(name__icontains=name_val)) &
            Q(org__name__icontains=org_val) &
            Q(type__icontains=type_val) &
            Q(comment__icontains=comment_val)
        ).order_by('name')
        return new_context

class AssetCreateView(LoginRequiredMixin, CreateView):
    model = Asset
    fields = ['name', 'org', 'type', 'comment']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AssetDetailView(DetailView):
    model = Asset


class AssetUpdateView(LoginRequiredMixin, UpdateView):
    model = Asset
    fields = ['name', 'org', 'type', 'comment']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AssetDeleteView(LoginRequiredMixin, DeleteView):
    model = Asset
    success_url = '/'

