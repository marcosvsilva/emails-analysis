import os
from dotenv import load_dotenv


load_dotenv()

ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TAG_SUBJECT_GESTNFE = "Verifição GestNFe"
TAG_SUBJECT_STACNFE = "Verifição StacNFe"
TAG_SUBJECT_STACCTE = "Verifição StacCTe"
NAME_SYSTEM_GESTNFE = "GestNFe"
NAME_SYSTEM_STACNFE = "StacNFe"
NAME_SYSTEM_STACCTE = "StacCTe"
