from typing import List
from django.utils.text import slugify
from django.shortcuts import render

from ninja.files import UploadedFile
from ninja import NinjaAPI, File, Form
from .schema import UserSchema, CategorySchema, CreateCategory, CollectionSchema, BrandSchema, ItemSchema, CommentSchema, \
    ReviewSchema, ItemCreate, \
    CreateBrand, CreateCollection
from core.models import User, Category, Collection, Brand, Item, Comment, Review

api = NinjaAPI()


@api.get("/inventory/user/all/", response=List[UserSchema])
def user_list(request):
    qs = User.objects.all()
    return qs


@api.get("/inventory/category/all/", response=List[CategorySchema])
def category_list(request):
    qs = Category.objects.all()
    return qs


@api.get("/inventory/category/{category_name}/", response=List[CategorySchema])
def category(request, category_name):
    qs = Category.objects.filter(name=category_name)
    return qs


@api.post("/inventory/category/")
def post_category(request, data: CreateCategory, banner: UploadedFile = File(...), image: UploadedFile = File(...)):
    data.banner = banner
    data.image = image

    qs = Category.objects.create(**data.dict())

    return {'name': qs.name}



@api.get("/inventory/collection/all/", response=List[CollectionSchema])
def collection_list(request):
    qs = Collection.objects.all()
    return qs


@api.get("/inventory/collection/{collection_name}/", response=List[CollectionSchema])
def collection(request, collection_name):
    qs = Collection.objects.filter(name=collection_name)
    return qs


@api.post("/inventory/collection/")
def post_collection(request, data: CreateCollection, banner: UploadedFile = File(...), image: UploadedFile = File(...)):

    data.banner = banner
    data.image = image

    qs = Collection.objects.create(**data.dict())

    return {'name': qs.name}


@api.get("/inventory/brand/all/", response=List[BrandSchema])
def brand_list(request):
    qs = Brand.objects.all()
    return qs


@api.get("/inventory/brand/{brand_name}/", response=List[BrandSchema])
def brand(request, brand_name):
    qs = Brand.objects.filter(name=brand_name)
    return qs


@api.post("/inventory/brand/")
def post_brand(request, data: CreateBrand, banner: UploadedFile = File(...), image: UploadedFile = File(...)):

    data.banner = banner
    data.image = image

    qs = Brand.objects.create(**data.dict())

    return {'name': qs.name}


@api.get("/inventory/product/all/", response=List[ItemSchema])
def product_list(request):
    qs = Item.objects.all()
    return qs


@api.get("/inventory/product/{item_name}/", response=List[ItemSchema])
def product(request, item_name):
    qs = Item.objects.filter(title=item_name)
    return qs


@api.post("/inventory/product/")
def add_product(request, data: ItemCreate, banner_image: UploadedFile = File(...), image_main: UploadedFile = File(...),
                image_1: UploadedFile = File(...),
                image_2: UploadedFile = File(...), image_3: UploadedFile = File(...)):

    data.banner_image = banner_image
    data.image_main = image_main
    data.image_1 = image_1
    data.image_2 = image_2
    data.image_3 = image_3

    qs = Item.objects.create(**data.dict())

    return {'title': qs.title}


@api.get("/inventory/review/all/", response=List[ReviewSchema])
def review_list(request):
    qs = Review.objects.all()
    return qs


@api.get("/inventory/review/{review_item}/", response=List[ReviewSchema])
def review(request, review_item):
    qs = Review.objects.filter(item__title=review_item)
    return qs


@api.get("/inventory/comment/all/", response=List[CommentSchema])
def comment_list(request):
    qs = Comment.objects.all()
    return qs


@api.get("/inventory/comment/{comment_item}/", response=List[CommentSchema])
def comment(request, comment_item):
    qs = Comment.objects.filter(item__title=comment_item)
    return qs
