"""
Define the ViewSets for the associations API.
"""

from rest_framework import status, viewsets
from rest_framework.response import Response

from associations.models import Association

from associations.models import Association
from associations.api.serializers import AssociationSerializer

from associations.api.filters import AssociationFilter


class NestedWritableModelViewSet(  # pylint: disable=too-many-ancestors
    viewsets.ModelViewSet
):
    def create(self, request, *args, **kwargs):
        """
        Create a list of model instances if a list is provided or a
        single model instance otherwise.
        """
        data = request.data
        to_return = None
        headers = {}
        if isinstance(data, list):
            to_return = [self._create_one_instance(item).data for item in data]
        else:
            serializer = self._create_one_instance(data)
            to_return = serializer.data
            headers = self.get_success_headers(to_return)
        return Response(to_return, status=status.HTTP_201_CREATED, headers=headers)

    def _create_one_instance(self, item):
        """
        Helper method to create a single model instance.
        """
        serializer = self.get_serializer(data=item)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return serializer


class AssociationViewSet(  # pylint: disable=too-many-ancestors
    NestedWritableModelViewSet
):
    """
    ViewSet for Association model.
    """

    queryset = Association.objects.all()
    serializer_class = AssociationSerializer
    filterset_class = AssociationFilter
