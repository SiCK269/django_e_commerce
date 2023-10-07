from ninja import Schema, ModelSchema, File
from ninja.files import UploadedFile
from ninja.orm import create_schema

from core.models import User, Category, Brand, Collection, Item, Comment, Review

from typing import List


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'username']


class CategorySchema(ModelSchema):
    class Config:
        model = Category
        model_fields = "__all__"


CreateCategory = create_schema(Category, fields=['name', 'banner', 'image'])


class CollectionSchema(ModelSchema):
    class Config:
        model = Collection
        model_fields = "__all__"


CreateCollection = create_schema(Collection, fields=['name', 'banner', 'image'])


class BrandSchema(ModelSchema):
    class Config:
        model = Brand
        model_fields = "__all__"


CreateBrand = create_schema(Brand, fields=['name', 'banner', 'image'])


class ItemSchema(ModelSchema):
    class Config:
        model = Item
        model_fields = "__all__"


class ItemCreate(ModelSchema):
    seller_id: int
    category_id: int
    brand_id: int
    collection_id: int

    class Config:
        model = Item
        model_fields = ['title', 'price', 'discount_price', 'quantity', 'label', 'slug', 'description',
                        'detailed_description', 'created_at', 'width', 'height', 'depth', 'weight', 'banner_image',
                        'image_main', 'image_1', 'image_2', 'image_3']


class CommentSchema(ModelSchema):
    class Config:
        model = Comment
        model_fields = ['item', 'name', 'content', 'created_at']


class ReviewSchema(ModelSchema):
    class Config:
        model = Review
        model_fields = ['item', 'rating', 'content', 'created_by', 'created_at']
