from django import forms


class MorseCodeForm(forms.Form):
	input = forms.CharField(
		widget=forms.Textarea(
			attrs={
				'placeholder': 'Enter Morse Code here'
			}
		)
	)
	output = forms.CharField(
		widget=forms.Textarea(
			attrs={'placeholder': 'Translated text will appear here'}
		),
		required=False
	)
