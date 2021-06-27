import django_filters
from django.db.models import Avg

from django_filters import rest_framework as  filters
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter


from .filters import ProductFilter
from main.models import Product, Review, Order, WishList
from .permissions import IsAuthorOrAdminPermission, DenyAll
from .serializers import ProductListSerializer, ProductDetailSerializer, ReviewSerializer, OrderSerializer

'''
1. Список товаров, доступен всем пользователем
'''
# @api_view(['GET'])
# def products_list(request):
#     queryset = Product.objects.all()
#     filtered_qs = ProductFilter(request.GET, queryset=queryset)
#     # serializer = ProductListSerializer(queryset, many=True)
#     serializer = ProductListSerializer(filtered_qs.qs, many=True)
#     serializer_queryset = serializer.data
#     return Response(data=serializer_queryset, status=status.HTTP_200_OK)

#вариант 1
# class ProductListView(APIView):
#     def get(request):
#         queryset = Product.objects.all()
#         filtered_qs = ProductFilter(request.GET, queryset=queryset)
#         # serializer = ProductListSerializer(queryset, many=True)
#         serializer = ProductListSerializer(filtered_qs.qs, many=True)
#         serializer_queryset = serializer.data
#         return Response(data=serializer_queryset, status=status.HTTP_200_OK)
#вариант 2
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_class = ProductFilter

# 2. Детали товаров, доступен всем
class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
#
#
# class CreateProductView(CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializer
#     permission_classes = [IsAdminUser]
#
# class UpdateProductView(UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializer
#     permission_classes = [IsAdminUser]
#
# # 3. Создаение товаров, редактирование, удаление, доступно только админом
# class DeleteProductView(DestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializer
#     permission_classes = [IsAdminUser]

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializer
#     filter_backends = (filter.DjangoFilterBackend, filters.OrderingFilter)
#     filter_backends = (filters.DjangoFilterBackend, )
#     filterset_class = ProductFilter
#     ordering_fields = ['title', 'price']
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    # queryset = Product.objects.annotate(rating=Avg('review__rating'))#позваляет добовлять диномические поля

    serializer_class = ProductDetailSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['title', 'price']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return super().get_serializer_class()
    #return self.serializer_class


    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        elif self.action in ['create_review', 'like']:
            return [IsAuthenticated()]
        return []

    #здесь тоже на
    #api1/v1/products/id/create_review
    @action(detail=True, methods=['POST'])
    def create_review(self, request, pk):
        data = request.data.copy()
        # product = self.get_object()
        data['product'] = pk
        serializer = ReviewSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
    #like
    #api/v1/products/id/like
    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        product = self.get_object()
        user = request.user
        like_obj, created = WishList.objects.get_or_create(product=product, user=user)

        if like_obj.is_liked:
            like_obj.is_liked = False
            like_obj.save()
            return Response('dislike')
        else:
            like_obj.is_liked = True
            like_obj.save()
            return Response('liked')



# 4. Создания отзывов, доступен только залогиненным пользователем
# class CreateReview(CreateAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_serializer_context(self):
#         return {'request':self.request}

# class ReviewViewSet(mixins.CreateModelMixin,
#                     mixins.CreateModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     viewsets.GenericViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     #сделаем чтоб мог удалить автор и админ
#     def get_permissions(self):
#         if self.action == 'create':
#             return [IsAuthenticated()]
#         return [IsAuthorOrAdminPermission()]
class RetrieveViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthorOrAdminPermission()]




class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == ['create', 'list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            return [IsAdminUser]
        else:
            return [DenyAll()]
        #пользователи могут видить тока свои продукты а админ все продукты
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset

# 5. Просмотр отзывов (внутри деталей продукта) доступен всем
# 6. Редактирование и удаление отзыва может только автор
# 7. Заказы может создать любой залогиненный пользователь
# 8. Список заказов: Пользователь видит только свои заказы, админы видят все
# 9. Редактировать заказы может только админ
# 10.
#TODO: Фильтрация по заказам
#TODO: Пагинация
#TODO: Сортировку
#TODO: Тесты
#TODO: Документация