import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_project.settings')
import django 
django.setup() 
from capturer.models import Category


def populate():

    categories = ['Still life photography', 'Portrait photography', 'Recording photography',
                  'Art photography', 'Pictorial photography', 'Commercial photography', 'Ink photography',
                  'Holographic photography']

    for c in categories:
        category = Category.objects.get_or_create(name=c)[1]
        if category == True:
	        print(c)



if __name__ == '__main__':
    print('Starting Capturer population script...') 
    populate()
    
