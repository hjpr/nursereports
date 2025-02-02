from dotenv import load_dotenv

import os

load_dotenv()
api_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("SUPABASE_ANON_KEY")
jwt_key = os.getenv("SUPABASE_JWT_KEY")
admin_key = os.getenv("SUPABASE_ADMIN_KEY")
anyscale_url = os.getenv("ANYSCALE_URL")
anyscale_api_key = os.getenv("ANYSCALE_API_KEY")
groq_key = os.getenv("GROQ_KEY")
mailgun_url = os.getenv("MAILGUN_URL")
mailgun_api_key = os.getenv("MAILGUN_API_KEY")