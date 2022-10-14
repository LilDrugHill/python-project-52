from django.utils.translation import gettext


menu = [
    {"title": gettext("All users"), "url_name": "all_users"},
    {"title": gettext("Home"), "url_name": "home"},
    {"title": gettext("Statuses"), "url_name": "all_statuses"},
    {"title": gettext("Labels"), "url_name": "all_labels"},
    {"title": gettext("Tasks"), "url_name": "all_tasks"},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu = [user_menu[0], user_menu[1]]
        context["menu"] = user_menu
        return context
