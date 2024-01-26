from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# I got this from dj4e tutorial.
class OwnerDeleteView(LoginRequiredMixin, DeleteView):

    def get_queryset(self):
        qs = super(OwnerDeleteView, self).get_queryset()
        if self.request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=self.request.user)




