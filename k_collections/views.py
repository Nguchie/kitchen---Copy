from django.shortcuts import render, get_object_or_404, reverse
from .models import MainCategory, SubCategory, Product

def home_page(request):
    main_categories = MainCategory.objects.all()
    sub_categories = SubCategory.objects.all()

    search_query = request.GET.get('q', '').strip()
    products = Product.objects.filter(name__icontains=search_query) if search_query else []

    breadcrumbs = [{'name': 'Home', 'url': reverse('home_page')}]

    return render(request, 'home_page.html', {
        'main_categories': main_categories,
        'sub_categories': sub_categories,
        'products': products,
        'query': search_query,
        'breadcrumbs': breadcrumbs,
    })

def search(request):
    query = request.GET.get('q', '').strip()
    results = Product.objects.filter(name__icontains=query) if query else []

    product_slug = request.GET.get('product_slug')  # Assuming 'product_slug' is passed in the query string
    if product_slug:
        product = get_object_or_404(Product, slug=product_slug)
        breadcrumbs = [
            {'name': 'Home', 'url': reverse('home_page')},
            {'name': 'Search Results', 'url': f"?q={query}"},
            {'name': product.name, 'url': reverse('product_detail', kwargs={'slug': product.slug})}
        ]
    else:
        breadcrumbs = [
            {'name': 'Home', 'url': reverse('home_page')},
            {'name': 'Search Results', 'url': f"?q={query}"},
        ]

    return render(request, 'search_results.html', {
        'query': query,
        'products': results,
        'breadcrumbs': breadcrumbs,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    main_category = product.main_category

    breadcrumbs = [
        {'name': 'Home', 'url': reverse('home_page')},
        {'name': main_category.name, 'url': reverse('main_category', kwargs={'category_slug': main_category.slug})},
        {'name': product.name, 'url': reverse('product_detail', kwargs={'slug': slug})}
    ]

    return render(request, 'productdetail.html', {'product': product, 'breadcrumbs': breadcrumbs})

def main_category(request, category_slug):
    main_category = get_object_or_404(MainCategory, slug=category_slug)
    products = main_category.products.all()

    type_filter = request.GET.getlist('type')
    if type_filter:
        products = products.filter(type__in=type_filter)

    breadcrumbs = [
        {'name': 'Home', 'url': reverse('home_page')},
        {'name': main_category.name, 'url': reverse('main_category', kwargs={'category_slug': category_slug})},
    ]

    return render(request, 'maincategory.html', {
        'main_category': main_category,
        'products': products,
        'type_filter': type_filter,
        'available_types': main_category.products.values_list('type', flat=True).distinct(),
        'breadcrumbs': breadcrumbs,
    })

def subcategory(request, subcategory_slug):
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)
    products = subcategory.products.all()

    type_filter = request.GET.getlist('type')
    if type_filter:
        products = products.filter(type__in=type_filter)

    # If a specific product is requested, handle it
    product_slug = request.GET.get('product_slug')  # Assuming 'product_slug' is passed in the query string
    if product_slug:
        product = get_object_or_404(Product, slug=product_slug)
        breadcrumbs = [
            {'name': 'Home', 'url': reverse('home_page')},
            {'name': subcategory.name, 'url': reverse('subcategory', kwargs={'subcategory_slug': subcategory.slug})},
            {'name': product.name, 'url': reverse('product_detail', kwargs={'slug': product.slug})}
        ]
    else:
        breadcrumbs = [
            {'name': 'Home', 'url': reverse('home_page')},
            {'name': subcategory.name, 'url': reverse('subcategory', kwargs={'subcategory_slug': subcategory.slug})},
        ]

    return render(request, 'subcategory.html', {
        'subcategory': subcategory,
        'products': products,
        'type_filter': type_filter,
        'available_types': subcategory.products.values_list('type', flat=True).distinct(),
        'breadcrumbs': breadcrumbs,
    })

def about(request):
    return render(request, 'about.html')

