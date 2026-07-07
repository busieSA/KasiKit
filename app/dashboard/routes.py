from flask import Blueprint, render_template

dashboard_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates"
)


@dashboard_bp.get('/')
def admin():

    return render_template(
        "dashboard/index.html"
    )


