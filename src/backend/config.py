from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SUPABASE_URL: str
    # anon / publishable key ONLY. The service_role key bypasses RLS and would
    # silently disable every tenant-isolation policy in the database.
    SUPABASE_KEY: str
    # Supabase Postgres connection string (Dashboard -> Connect). Used only by the
    # LangGraph checkpointer, which keeps the agent's conversation state.
    DATABASE_URL: str
    # Optional: page the "reset password" e-mail link should open.
    PASSWORD_RESET_REDIRECT: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
