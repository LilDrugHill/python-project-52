from django.views.generic.base import TemplateView
from task_manager.utils import DataMixin


class HomePageView(DataMixin, TemplateView):
    template_name = "base.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Home page")
        return dict(list(context.items()) + list(c_def.items()))
