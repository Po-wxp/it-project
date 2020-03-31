from haystack import indexes
from capturer.models import Photo , Tag, Category
from django.contrib.auth.models import User

class PhotoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/Photo_text.txt")
    Title = indexes.CharField(model_attr='Title')
    Category = indexes.CharField()
    Tag = indexes.CharField()
    Description = indexes.CharField(model_attr='Description')

    def get_model(self):
        return Photo
        
    def prepare_Tag(self, object):
        return [ Tag.name for a in object.Tag.all()]
    
    def prepare_Category(self, object):
        return object.Category.name

    def prepare_Author(self, object):
        return object.User.username

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
