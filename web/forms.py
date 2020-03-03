from django import forms


class OrgSearchForm(forms.Form):
    search_text = forms.CharField(
        required=False,
        label='Search org name',
        widget=forms.TextInput(attrs={'placeholder': 'search here'}),
    )

    search_sector = forms.IntegerField(
        required=False,
        label='Sector ( 1 - 6 )'
    )

    search_level = forms.IntegerField(
        required=False,
        label='level'
    )

    search_tier = forms.IntegerField(
        required=False,
        label='tier'
    )

    search_comment = forms.CharField(
        required=False,
        label='comment'
    )
