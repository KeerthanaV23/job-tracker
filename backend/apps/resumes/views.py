from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from . import matcher
from .models import ResumeAnalysis
from .parser import ResumeParseError, extract_text_from_pdf
from .serializers import AnalyzeRequestSerializer, ResumeAnalysisSerializer


class AnalyzeView(APIView):
    """Upload a PDF (or paste text) + job description -> match score and missing keywords."""

    parser_classes = (MultiPartParser, FormParser, JSONParser)
    throttle_scope = "analyzer"

    @extend_schema(request=AnalyzeRequestSerializer, responses=ResumeAnalysisSerializer)
    def post(self, request):
        ser = AnalyzeRequestSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        try:
            resume_text = (
                extract_text_from_pdf(data["file"]) if data.get("file") else data["resume_text"]
            )
            result = matcher.analyze(resume_text, data["job_description"])
        except (ResumeParseError, ValueError) as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        analysis = ResumeAnalysis.objects.create(
            user=request.user,
            application=data.get("application"),
            resume_text=resume_text,
            job_description=data["job_description"],
            **result,
        )
        return Response(ResumeAnalysisSerializer(analysis).data, status=status.HTTP_201_CREATED)


class AnalysisListView(generics.ListAPIView):
    serializer_class = ResumeAnalysisSerializer

    def get_queryset(self):
        return ResumeAnalysis.objects.filter(user=self.request.user)
