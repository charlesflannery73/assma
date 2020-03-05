from django import forms


class OrgSearchForm(forms.Form):
    search_text = forms.CharField(
        required=False,
        label='Search org name',
        widget=forms.TextInput(attrs={'placeholder': 'search here'}),
    )

    search_sector = forms.CharField(
        required=False,
        label='Sector'
    )

    search_level = forms.CharField(
        required=False,
        label='level'
    )

    search_tier = forms.IntegerField(
        required=False,
        label='tier'
    )

    search_id = forms.IntegerField(
        required=False,
        label='coid'
    )

    search_comment = forms.CharField(
        required=False,
        label='comment'
    )


class AssetSearchForm(forms.Form):
    search_text = forms.CharField(
        required=False,
        label='Search Asset',
        widget=forms.TextInput(attrs={'placeholder': 'search here'}),
    )

    search_org = forms.CharField(
        required=False,
        label='org'
    )

    search_type = forms.CharField(
        required=False,
        label='type'
    )

    search_comment = forms.CharField(
        required=False,
        label='comment'
    )
