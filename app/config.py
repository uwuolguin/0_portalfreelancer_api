from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    normal_directory: str
    picture_directory:str
    table_name_for_select_all_free_user:str
    table_name_for_select_all_no_free_user:str
    table_name_for_select_all_contacts:str
    table_name_for_select_all_issues:str
    table_name_for_select_all_categories:str
    table_name_for_select_all_skills:str
    table_name_for_select_all_talent_cache:str
    cloud_platform_user_for_email_sending:str
    cloud_platform_password_for_email_sending:str
    api_name_for_email_sending:str
    api_password_for_email_sending:str
    cloud_platform_user_for_email_password_changes:str
    cloud_platform_password_for_email_password_changes:str
    api_name_for_email_password_cahnges:str
    api_password_for_email_password_cahnges:str
    change_password_url:str
    login_url:str
    settingsuwu_url:str
    token_seconds:int
    superadmin_email:str
    superadmin_password:str
    tableau_token_name:str
    tableau_token_password:str
    tableau_token_sitename:str
    tableau_token_server:str
    class ConfigDict:
        env_file= ".env"

settings=Settings()