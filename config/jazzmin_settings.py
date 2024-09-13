JAZZMIN_SETTINGS = {
    "site_title": "My Admin",
    "welcome_sign": "Welcome to Admin Panel",
    "login_logo": None,
    'LANGUAGE_CODE': 'en-us',
    "search_model": ["auth.User"],
    "topmenu_links": [

        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},

        {"name": "Support", "url": "https://github.com/Asror200", "new_window": True},
        {"name": "About", "url": "/about/", "new_window": True},
    ],
    "copyright": "Admin Panel",
    "language_chooser": True,

}