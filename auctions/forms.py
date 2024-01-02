from django import forms
from .models import categoryModel

class searchByCatedory(forms.Form):
    category = forms.ModelChoiceField(
        queryset=categoryModel.objects.all(),
        widget=forms.Select
    )

class createListingForm(forms.Form):
    """ 
    this form is for create new listing
    if you see some widget in the form, you can get more information about how to use it
    visit https://docs.djangoproject.com/en/4.1/ref/forms/widgets/
    """
    
    title = forms.CharField(
        max_length=50, 
        label="Title",
        widget=forms.TextInput(attrs={'placeholder': 'Enter title', 'class': 'form-control'}))
    
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={'placeholder': 'Enter Description', 'class': 'form-control'})
    )

    """ All URL must end in a image format e.g.: jpg, jpeg, png . Else it will not work """
    url = forms.URLField(
        widget=forms.URLInput(attrs={'placeholder': 'Enter URL Image', 'class': 'form-control'}), 
        label="URL Image",
    )
    
    price = forms.DecimalField(
        label="Price $", 
        max_digits = 9, 
        decimal_places = 2,
        min_value = 0,
        max_value = 1000000,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Price', 'class': 'form-control'})
    )
    
    status = forms.TypedChoiceField(
        label="Status",
        choices=((True, "Active"), (False, "Inactive")),
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect
    )
    
    category = forms.ModelChoiceField(
        label="Category", 
        queryset = categoryModel.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    

    