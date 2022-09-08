JAZZMIN_SETTINGS = {
    "site_title": "NJohnny",
    "site_header": "NJohnny",
    "site_brand": "NJohnny",
    "login_logo": None,

    "site_logo": None,
    "site_logo_classes": None,
    "site_icon": None,

    "welcome_sign": "Добро пожаловать в административную панель NJohnny",
    "copyright": "NJohnny",
    "user_avatar": "None",

    "topmenu_links": [
        {
            "name": "Home",
            "url": "admin:index",
            "permissions": ["auth.view_user"]
        },
    ],

    "show_sidebar": True,

    # "order_with_respect_to": [
    #     # apps
    #     "banners",
    #     "news",
    #     "prices",
    #     "clinic",
    #     "auth",
    #     # models
    #     "clinic.AboutUs",
    #     "clinic.Specialization",
    #     "clinic.Doctors",
    #     "clinic.Services",
    #     "clinic.SubService",
    #     "clinic.Popular",
    #     "clinic.Review",
    #     "clinic.Statistic",
    #     "clinic.SocialMedia",
    #     "clinic.Contacts",
    #     "clinic.Vacancies",
    #     "clinic.ContactHR",
    # ],

    "navigation_expanded": False,
    "icons": {
        "users.user": "fas fa-user",
    },

    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
        "clinic.AboutUs": "single",
    },
    # "language_chooser": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": False,
    "theme": "lumen",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": True
}
