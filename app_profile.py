from dataclasses import dataclass, field
from datetime import datetime
import os

PROFILES_DIR = "profiles"


@dataclass
class Profile:
    name: str
    ml_models: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now())
    updated_at: datetime = field(default_factory=datetime.now())

    def to_dict(self):
        return {
            "profile_name": self.name,
            "ml_models": self.ml_models,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


def create_profile(profile_name: str, ml_models: list[str], meta_data: dict):
    for profile in meta_data.keys:
        if profile_name == meta_data[profile]["profile_name"]:
            print("Profile already exists!")
            return False

    os.mkdir(os.path.join(PROFILES_DIR, profile_name))
    return (Profile(profile_name, ml_models=ml_models), True)


def add_model_to_profile(profile: Profile, model: str):
    profile.ml_models.append(model)
    profile.updated_at = datetime.now()


def delete_profile(profile_name: str):
    try:
        os.rmdir(os.path.join(PROFILES_DIR, profile_name))
    except FileNotFoundError:
        print(f"Error: The directory does not exist.")
    except OSError as e:
        print(f"Error: Could not remove the directory. {e.strerror}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def save_profiles_to_json(profiles):
    ...


def load_profile_from_dict(profile_dict: dict):
    profile_name = profile_dict.get("profile_name")
    ml_models = profile_dict.get("ml_models")
    created_at = profile_dict.get("created_at")
    updated_at = profile_dict.get("updated_at")
    return Profile(name=profile_name, ml_models=ml_models, created_at=created_at, updated_at=updated_at)
