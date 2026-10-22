import os
from supabase import create_client
from dotenv import load_dotenv

from src.backend.auth.models import Company

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

email: str ="iliasbessiness123456@gmail.com"
password: str = "lostady455"

#create_user
#user = supabase.auth.sign_up({"email": email, "password": password})

# login_user
session = supabase.auth.sign_in_with_password({"email": email, "password": password})

# authorisation after login and setup rls policys on supabase database
supabase.postgrest.auth(session.access_token)

print(session.session.access_token)


#_________________________________________________

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)


#insert_1 = supabase.table("User").insert({'email': 'markterstegebn@gmail.com', 'password': 'hcbudhcidjdsuh'}).execute()
#update_1 = supabase.table("User").update({"password": "updated pass"}).eq("uuid", 2).execute()
delete_1 = supabase.table("User").delete().eq("uuid",3).execute()
data = supabase.table("User").select("*").execute()