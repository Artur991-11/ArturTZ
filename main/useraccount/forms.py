from django import forms
from moderation.models import TicketComment, TicketCommentMedia
from useraccount.models import Profile, ChatMessage, Chat
from django.contrib.auth import get_user_model
from useraccount.models import Profile
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] += ' form-control'

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    GENDER_CHOICES = [
        (1, 'Мужской'),
        (2, 'Женский'),
    ]
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    cover = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}))
    username = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Логин',  'name':'emailaddress', 'id': 'profile-username', 'class':'form-input'}))
    birthday = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'type': 'date', 'placeholder': '31.12.2000', 'name': 'birthday', 'id': 'profile-birthday',
                   'class': 'datepicker_input form-control'}),
    )
    phone = forms.CharField(required=False, max_length=11, widget=forms.TextInput(attrs={'placeholder': 'Телефон',  'name': 'phone', 'id': 'phone', 'class':'form-input'}))
    name = forms.CharField(required=False, max_length=11, widget=forms.TextInput(attrs={'placeholder': 'ФИО',  'name': 'name', 'id': 'name', 'class':'form-input'}))
    city = forms.CharField(required=False, max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Город',  'name':'city', 'id': 'profile-city', 'class':'form-input'}))
    email = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Email',  'name':'emailaddress', 'id': 'profile-email', 'class':'form-input'}))
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'}),
    )
    description = forms.CharField(
        max_length=5000,
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'profile-bio', 'class': 'form-control'}),
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'city', 'username', 'birthday', 'phone', 'gender', 'description', 'email']

class PasswordResetEmailForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email'}))

class SetPasswordFormCustom(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='New password confirmation', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'autocomplete': 'new-password'})
        self.fields['new_password2'].widget.attrs.update({'autocomplete': 'new-password'})





class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Написать сообщение', 'class': 'form-control'}),
        }

    files = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )


class ChatForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    administrators = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Chat
        fields = ['name', 'users', 'administrators']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название', 'class': 'form-control input-default'}),
        }

    def __init__(self, *args, **kwargs):
        users_queryset = kwargs.pop('users_queryset', None)
        super().__init__(*args, **kwargs)
        if users_queryset:
            self.fields['users'].queryset = users_queryset
            self.fields['administrators'].queryset = users_queryset

class ChatCreateForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name', 'type']

    # Поле для указания пользователя
    user_id = forms.IntegerField(widget=forms.HiddenInput())