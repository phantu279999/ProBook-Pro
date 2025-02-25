from django import forms


class MorseCodeForm(forms.Form):
	morse_code = forms.CharField(
		widget=forms.Textarea(
			attrs={
				'placeholder': 'Enter Morse Code here'
			}
		)
	)
	text = forms.CharField(
		widget=forms.Textarea(
			attrs={'placeholder': 'Translated text will appear here'}
		),
		required=False
	)
