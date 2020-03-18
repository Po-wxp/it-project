from haystack import indexes
from capturer.models import Photo , UserProfile , Tag, Category

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

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


# class TagIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True, template_name="search/Tag_text.txt")
#     name = indexes.CharField(model_attr='name')

#     def get_model(self):
#         return Tag
    
#     #  def prepare_Tag(self, obj):
#     #     return [ Photo.Tag for a in obj.Tag.all()]

#     def index_queryset(self, using=None):
        
#         return self.get_model().objects.all()

class UserProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/UserProfile_text.txt")
    # nickname = indexes.CharField(model_attr='nickname')

    def get_model(self):
        return UserProfile

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
    
    # def photo(self):
    #     photos = set()
    #     for a in self.get_model().objects.all():
    #         photos.add(Photo.objects.filter(author = a.user))
    #     print("sda")
    #     return photos

# class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True, template_name="search/Category_text.txt")
#     name = indexes.CharField(model_attr='name')

#     def get_model(self):
#         return Category

#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()
