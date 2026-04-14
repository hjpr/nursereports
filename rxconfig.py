
import os
import reflex as rx

from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
    app_name="nursereports",
    plugins=[
        rx.plugins.TailwindV4Plugin(
            config={
                "darkMode": "class",
                "plugins": ["@tailwindcss/typography@0.5.19"],
                "theme": {
                    "extend": {
                        "fontFamily": {
                            "sans": ["Inter Variable", "system-ui", "sans-serif"],
                            "mono": ["Geist Mono", "monospace"],
                        }
                    }
                },
            }
        ),
        rx.plugins.SitemapPlugin(),
    ],
    state_auto_setters=True,
    api_url='http://localhost:8000',
    show_built_with_reflex=False,
    suplex={
        "api_url": os.getenv("api_url"),
        "api_key": os.getenv("api_key"),
        "jwt_secret": os.getenv("jwt_secret"),
        "service_role": os.getenv("service_role"),
        "let_jwt_expire": False,
    },
    openrouter_api_url=os.getenv("OPENROUTER_API_URL"),
    openrouter_key=os.getenv("OPENROUTER_KEY"),
    openrouter_moderator_model="google/gemma-4-31b-it"
    mailgun_url=os.getenv("MAILGUN_URL"),
    mailgun_api_key=os.getenv("MAILGUN_API_KEY"),
)