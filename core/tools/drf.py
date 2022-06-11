from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response

from core.helpers.asyncio import async_


async def get_serializer_data(serializer):
    def get_data(serializer):
        return serializer.data

    return await async_(get_data)(serializer)


class AsyncMixin:
    """Provides async view compatible support for DRF Views and ViewSets.

    Overrides ViewSetMixin.as_view() and APIView.dispatch()

    This must be the first inherited class.

        class MyViewSet(AsyncMixin, GenericViewSet):
            pass
    """

    @classmethod
    def as_view(cls, *args, **initkwargs):
        """Make Django process the view as an async view."""
        view = super().as_view(*args, **initkwargs)

        async def async_view(*args, **kwargs):
            # wait for `.dispatch()`
            return await view(*args, **kwargs)

        async_view.initkwargs = initkwargs  # thanks to @Mng-dev-ai
        async_view.cls = cls  # thanks to @Mng-dev-ai
        async_view.csrf_exempt = True  # thanks to @Ariki
        async_view.actions = view.actions
        return async_view

    async def dispatch(self, request, *args, **kwargs):
        """Add async support."""
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        try:
            await sync_to_async(self.initial)(request, *args, **kwargs)  # MODIFIED HERE

            if request.method.lower() in self.http_method_names:
                handler = getattr(
                    self,
                    request.method.lower(),
                    self.http_method_not_allowed,
                )
            else:
                handler = self.http_method_not_allowed

            # accept both async and sync handlers
            # built-in handlers are sync handlers
            handler = async_(handler)
            response = await handler(request, *args, **kwargs)  # MODIFIED HERE

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response


class AsyncCreateModelMixin(CreateModelMixin):
    """
    Create a model instance.
    """

    async def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        await async_(serializer.is_valid)(raise_exception=True)
        await async_(self.perform_create)(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            await get_serializer_data(serializer),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class AsyncListModelMixin(ListModelMixin):
    """
    List a queryset.
    """

    async def list(self, request, *args, **kwargs):

        base_queryset = await async_(self.get_queryset)()
        queryset = await async_(self.filter_queryset)(base_queryset)

        page = await async_(self.paginate_queryset)(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(await get_serializer_data(serializer))

        serializer = self.get_serializer(queryset, many=True)
        return Response(await async_(get_serializer_data)(serializer))


class AsyncRetrieveModelMixin(RetrieveModelMixin):
    """
    Retrieve a model instance.
    """

    async def retrieve(self, request, *args, **kwargs):

        instance = await async_(self.get_object)()
        serializer = self.get_serializer(instance)
        return Response(await get_serializer_data(serializer))


class AsyncUpdateModelMixin(UpdateModelMixin):
    """
    Update a model instance.
    """

    async def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = await async_(self.get_object)()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        await async_(serializer.is_valid)(raise_exception=True)
        await async_(self.perform_update)(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(await get_serializer_data(serializer))

    async def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return await self.update(request, *args, **kwargs)


class AsyncDestroyModelMixin(DestroyModelMixin):
    """
    Destroy a model instance.
    """

    async def destroy(self, request, *args, **kwargs):
        instance = await async_(self.get_object)()
        await async_(self.perform_destroy)(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    async def perform_destroy(self, instance):
        await async_(instance.delete)()
