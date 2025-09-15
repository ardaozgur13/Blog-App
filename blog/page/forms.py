from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import UserProfile, UserPost, Tag

gender_choices = [
	(None, "Select Gender"),
    ("Female", "Female"), 
    ("Male", "Male"),
    ]

class PostAddForm(forms.ModelForm):
	post_title = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Post Title', 'name':'post_title'}), required=False)	
	post_text = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 15, 'cols': 59, 'placeholder': 'Post Text', 'name':'post_text'}), required=False)
	post_image = forms.ImageField(label='', widget=forms.FileInput(attrs={'class':'form-control', 'accept': 'image/*', 'name':'post_image'}), required=False)
	tag_category = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input', 'name':'tag_category'}), required=False)
	
	class Meta:
		model = UserPost
		fields = ('post_title', 'post_text', 'post_image', 'tag_category')

class UserInfoForm(forms.ModelForm):
	gender = forms.ChoiceField(label='', choices=gender_choices, widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Gender'}), required=False)
	phone = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), required=False)
	city = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=False)
	country = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=False)	
	continent = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Continent'}), required=False)
	profile_picture = forms.ImageField(label='', widget=forms.FileInput(attrs={'class':'form-control', 'accept': 'image/*'}), required=False)	
	about = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 4, 'cols': 50, 'placeholder': 'About'}), required=False)

	class Meta:
		model = UserProfile
		fields = ('gender', 'phone', 'city', 'country', 'continent', 'profile_picture', 'about')

class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class UpdateUserForm(UserChangeForm):
	# Hide password stuff
	password = None
	# Get user things
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
