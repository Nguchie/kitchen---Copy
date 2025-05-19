from .models import MainCategory

def main_categories_processor(request):
    return {'main_categories': MainCategory.objects.all()}
