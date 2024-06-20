# forms.py
from django import forms
from .models import Word, WordImage

class WordImageForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=[(category, category) for category in Word.objects.values_list('category', flat=True).distinct()],
        label='Категория'
    )
    word = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите слово или выберите из списка'}), label='Слово')

    class Meta:
        model = WordImage
        fields = ['category', 'word', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['word'].widget.attrs.update({'list': 'word_list'})
        if 'category' in self.data:
            self.fields['word'].widget.attrs['data-category'] = self.data['category']
        elif self.instance.pk:
            self.fields['word'].widget.attrs['data-category'] = self.instance.category

    def get_word_choices(self):
        category = self.data.get('category') or self.initial.get('category')
        if category:
            words_without_images = Word.objects.filter(category=category).exclude(word__in=WordImage.objects.values_list('word', flat=True))
            choices = [(word.word, word.word) for word in words_without_images]
            choices.insert(0, ('', '--- Добавить новое слово ---'))
            return choices
        return []

    def clean_word(self):
        word = self.cleaned_data.get('word')
        category = self.cleaned_data.get('category')
        if word:
            existing_word = Word.objects.filter(word=word, category=category).first()
            if existing_word and WordImage.objects.filter(word=existing_word.word).exists():
                raise forms.ValidationError(f"Изображение для слова '{word}' уже существует.")
            if not existing_word:
                Word.objects.create(word=word, category=category)
        return word