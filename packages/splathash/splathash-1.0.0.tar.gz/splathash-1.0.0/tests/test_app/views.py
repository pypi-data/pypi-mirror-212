from rest_framework.response import Response
from rest_framework.views import APIView

from splathash.engine.application.application import NALOApplication
from splathash.engine.router.router import BaseLookupTableRouter

from .routes import USSDRoutes


class USSDView(APIView, BaseLookupTableRouter):
    """USSD Application view"""

    table = {
        **USSDRoutes.baseTable,
    }

    def post(self, request):
        """start application with appropriate data"""
        app = NALOApplication()
        response = app.run_with_pagination(request=request, router=self)

        return Response(response)
