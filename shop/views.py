from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category, Product, Comment
from .forms import CommentForm



class Index(View):
    def get(self, request):
        return render(request, 'index.html')





def product_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    elif query:
        products = Product.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(category__name__icontains=query)
        )
    else:
        products = Product.objects.all()

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = product.comments.all()
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            messages.success(request, "Izoh qo'shildi!")
            return redirect('product_detail', product_id=product.id)

    return render(request, 'products/product_detail.html', {
        'product': product,
        'comments': comments,
        'form': form
    })
