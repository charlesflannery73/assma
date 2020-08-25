from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from .models import Org, Asset
from .forms import OrgSearchForm, AssetSearchForm
from search_views.search import SearchListView
from search_views.filters import BaseFilter
from django.db.models import Q
from django.urls import reverse
import ipaddress
import logging
from django.contrib import messages


logger = logging.getLogger(__name__)


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logger.info("user=" + str(self.request.user) + ", action=view, data=[home_page]")
        orgs = Org.objects.filter().order_by('-modified')[:5]
        assets = Asset.objects.filter().order_by('-modified')[:5]
        return render(request, 'home.html', {'orgs': orgs, 'assets': assets})


class AboutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logger.info("user=" + str(self.request.user) + ", action=view, data=[about_page]")
        return render(request, 'about.html')


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

class AssetSearch(LoginRequiredMixin, SearchListView):
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
            logger.info("user=" + str(self.request.user) + ", action=search_assets, data=[" + params + "]")
            return HttpResponseRedirect(reverse('asset-list') +'?%s' % params)

        return render(request, self.template_name, {'form': form})


class OrgSearch(LoginRequiredMixin, SearchListView):
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
            logger.info("user=" + str(self.request.user) + ", action=search_orgs, data=[" + params + "]")
            return HttpResponseRedirect(reverse('org-list') +'?%s' % params)

        return render(request, self.template_name, {'form': form})


class OrgListView(LoginRequiredMixin, ListView):
    model = Org
    template_name = 'web/org_list.html'
    context_object_name = 'orgs'
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get('name') == None:
            logger.info("user=" + str(self.request.user) + ", action=list, data=[orgs]")
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


class OrgCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Org
    fields = ['name', 'sector', 'level', 'tier', 'comment']
    success_url = '/'
    permission_required = ('web.add_org')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        sector = form.cleaned_data['sector']
        level = form.cleaned_data['level']
        tier = form.cleaned_data['tier']
        comment = form.cleaned_data['comment']
        data = "name=" + name + ", sector=" + sector + ", level=" + level + ", tier=" + str(tier) + ", comment=" + comment
        logger.info("user=" + str(self.request.user) + ", action=create_org, data=[" + data + "]")
        return super().form_valid(form)


class OrgUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Org
    fields = ['name', 'sector', 'level', 'tier', 'comment']
    success_url = '/'
    permission_required = ('web.change_org')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        sector = form.cleaned_data['sector']
        level = form.cleaned_data['level']
        tier = form.cleaned_data['tier']
        comment = form.cleaned_data['comment']
        data = "name=" + name + ", sector=" + sector + ", level=" + level + ", tier=" + str(tier) + ", comment=" + comment
        logger.info("user=" + str(self.request.user) + ", action=update_org, data=[" + data + "]")
        return super().form_valid(form)


class OrgDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView, View):
    model = Org
    success_url = '/'
    permission_required = ('web.delete_org')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        pk = self.object.id
        assets = Asset.objects.filter(org=pk)
        if assets:
            messages.warning(request, 'Cannot delete the org "' + name + '" while it has assets.')
            return HttpResponseRedirect(reverse('asset-list') +'?org=%s' % name)
        sector = self.object.sector
        level = self.object.level
        tier = self.object.tier
        comment = self.object.comment
        data = "name=" + name + ", sector=" + sector + ", level=" + level + ", tier=" + str(tier) + ", comment=" + comment
        logger.info("user=" + str(self.request.user) + ", action=delete_org, data=[" + data + "]")
        return super(OrgDeleteView, self).delete(request, *args, **kwargs)


class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = 'web/asset_list.html'
    context_object_name = 'assets'
    ordering = ['-modified']
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get('name') == None:
            logger.info("user=" + str(self.request.user) + ", action=list, data=[assets]")
            return Asset.objects.filter().order_by('name')
        name_val = self.request.GET.get('name')
        org_val = self.request.GET.get('org')
        type_val = self.request.GET.get('type')
        comment_val = self.request.GET.get('comment')

        try:
            ip = int(ipaddress.ip_address(name_val))
            new_context = Asset.objects.filter(
                (
                    Q(start_ip__lte=ip) &
                    Q(end_ip__gte=ip) &
                    Q(org__name__icontains=org_val) &
                    Q(type__icontains=type_val) &
                    Q(comment__icontains=comment_val)) |
                Q(comment__icontains=name_val)
            ).order_by('name')
            return new_context
        except:
            new_context = Asset.objects.filter(
                (
                    Q(name__icontains=name_val) &
                    Q(org__name__icontains=org_val) &
                    Q(type__icontains=type_val) &
                    Q(comment__icontains=comment_val)) |
                Q(comment__icontains=name_val)

            ).order_by('name')
            return new_context

class AssetCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Asset
    fields = ['name', 'org', 'type', 'comment']
    success_url = '/'
    permission_required = ('web.add_asset')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        org = form.cleaned_data['org']
        type = form.cleaned_data['type']
        comment = form.cleaned_data['comment']
        data = "name=" + name + ", org=" + str(org) + ", type=" + type + ", comment=" + comment
        logger.info("user=" + str(self.request.user) + ", action=create_asset, data=[" + data + "]")
        return super().form_valid(form)


class AssetUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Asset
    fields = ['name', 'org', 'type', 'comment']
    success_url = '/'
    permission_required = ('web.change_asset')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        org = form.cleaned_data['org']
        type = form.cleaned_data['type']
        comment = form.cleaned_data['comment']
        data = "name=" + name + ", org=" + str(org) + ", type=" + type + ", comment=" + comment
        logger.info("user=" + str(self.request.user) + ", action=update_asset, data=[" + data + "]")
        return super().form_valid(form)


class AssetDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Asset
    success_url = '/'
    permission_required = ('web.delete_asset')

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        org = self.object.org
        type = self.object.type
        comment = self.object.comment
        data = "name=" + name + ", org=" + str(org) + ", type=" + type + ", comment=" + comment
        logger.info("user=" + str(self.request.user) + ", action=delete_asset, data=[" + data + "]")
        return super(AssetDeleteView, self).delete(*args, **kwargs)
