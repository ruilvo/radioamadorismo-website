from django.views.decorators.http import require_safe
from django.http import HttpRequest, JsonResponse

from .models import (
    FactRepeater,
)

from .filters import FactRepeaterFilterView


@require_safe
def chirp_view(request: HttpRequest):
    filtered_data = FactRepeaterFilterView(
        request.GET, queryset=FactRepeater.objects.all()
    )
    # TODO: implement the serialization to csv
    return JsonResponse(list(filtered_data.qs.values()), safe=False)
