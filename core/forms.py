from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Nombre:", widget= forms.TextInput(attrs={"class": "bg-gray-200 mb-2 shadow-none dark:bg-gray-800", 'placeholder': 'Nombre'}) ,required=True)
    surname = forms.CharField(label="Apellido:", widget= forms.TextInput(attrs={"class": "bg-gray-200 mb-2 shadow-none dark:bg-gray-800", 'placeholder': 'Apellido'}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "bg-gray-200 mb-2 shadow-none dark:bg-gray-800", 'placeholder': 'Escribi tu mensaje', "rows":"5"}))
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={"class": "bg-gray-200 mb-2 shadow-none dark:bg-gray-800", 'placeholder': 'Correo electrónico'}), required=True)