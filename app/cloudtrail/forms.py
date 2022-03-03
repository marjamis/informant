from django import forms


class TimeForm(forms.Form):
    search_key = forms.CharField(
        label='Search Identifier - Used for easy reference in Informant', required=True, max_length=100)
    accountId = forms.CharField(
        label='Account ID that owns the bucket', required=True, max_length=20)
    bucket = forms.CharField(
        label='Bucket Name', required=True, max_length=255)
    bucket_region = forms.CharField(
        label='Buckets Region', required=True, max_length=20)
    prefix = forms.CharField(
        label='Prefix - This is if you have specified a location before the default path, generally this can be left blank', required=False, max_length=1000)
    date = forms.DateTimeField(
        label='Date - Format has to be in the form of YYYY/MM/DD', required=True)


class LocationForm(forms.Form):
    load = forms.CharField(
        label='Search Identifier - Used for easy reference in Informant', required=True, max_length=100)
    file = forms.FileField(
        label='NOTE: This should be a tar.gz file of all the native CloudTrail gzip files.')
