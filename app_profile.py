from dataclasses import dataclass, field
from datetime import datetime
import json
import shutil
import os

PROFILES_DIR = "data/profiles"
META_DATA_PATH = "data/profiles_metadata.json"


@dataclass
class Profile:
    name: str   # Name of the profile
    ml_models: list[str] = field(default_factory=list)  # List of ML models
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Converts Profile object to dictionary so it can be serialized into JSON
    def to_dict(self) -> dict:
        return {
            "profile_name": self.name,
            "ml_models": self.ml_models,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


def create_profile(profile_name: str, ml_models: list[str], meta_data: dict) -> (tuple[Profile, bool] | bool):
    for profile in meta_data.keys():
        if profile_name == meta_data[profile]["profile_name"]:
            print("Profile already exists!")
            return False

    os.mkdir(os.path.join(PROFILES_DIR, profile_name))
    return (Profile(name=profile_name, ml_models=ml_models), True)


def add_model_to_profile(profile: Profile, model_name: str, model_path: str) -> bool:

    if not os.path.exists(os.path.join(PROFILES_DIR, profile.name)):
        print("Profile does not exist.")
        return False
    if not os.path.exists(model_path):
        print("Model does not exist.")
        return False
    profile.ml_models.append(model_name)
    profile.updated_at = datetime.now()

    try:
        shutil.copy(model_path, os.path.join(PROFILES_DIR, profile.name))
        return True
    except:
        print("There was an error while copying the model to the profile directory.")
        return False

    



def delete_profile(profile_name: str) -> bool:
    try:
        os.rmdir(os.path.join(PROFILES_DIR, profile_name))
        return True
    except FileNotFoundError:
        print(f"Error: The directory does not exist.")
        return False
    except OSError as e:
        print(f"Error: Could not remove the directory. {e.strerror}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def save_profiles_to_json(profiles: list[Profile]):
    metadata = {
        p.name: {
            "profile_name": p.name,
            "ml_models": p.ml_models,
            "created_at": p.created_at.isoformat(),
            "updated_at": p.updated_at.isoformat(),
        } for p in profiles
    }

    with open(META_DATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)


def load_profile_from_dict(profile_dict: dict) -> Profile:
    profile_name = profile_dict.get("profile_name")
    ml_models = profile_dict.get("ml_models")
    created_at = profile_dict.get("created_at")
    updated_at = profile_dict.get("updated_at")
    return Profile(name=profile_name, ml_models=ml_models, created_at=created_at, updated_at=updated_at)


def load_dict_from_json() -> (dict | None):
    if os.path.exists(META_DATA_PATH):
        with open(META_DATA_PATH, 'r') as f:
            metadata = json.load(f)
        return metadata
    else:
        print("Metadata file doesn't exist.")
