from comment.models import Comment
from rest_framework import viewsets
from comment.serializers import CommentSerializer
from comment.permissions import IsAdminUserOrReadOnly


# Create your views here.
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
