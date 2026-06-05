import os
import pathlib
import sys
# import random
# from uuid import UUID

from alembic import command
from alembic.config import Config
# from sqlalchemy import func, select
from sqlalchemy_utils import create_database, drop_database

sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))

from app.db.models.alphabet import WrittingDirection, WrittingSystem
from app.db.models.character import AlphabetUnitType
from app.factory.factories import (
    AlphabetFactory,
    BaseSQLAlchemyModelFactory,
    CharacterFactory,
    SciptFamilyFactory,
    TransliterationCharacterFactory,
    TransliterationSystemFactory,
)
from app.config import get_settings
from app.db.session import session


# Map main db session to factories
BaseSQLAlchemyModelFactory._meta.sqlalchemy_session = session
SciptFamilyFactory._meta.sqlalchemy_session = session
AlphabetFactory._meta.sqlalchemy_session = session
TransliterationSystemFactory._meta.sqlalchemy_session = session
CharacterFactory._meta.sqlalchemy_session = session
TransliterationCharacterFactory._meta.sqlalchemy_session = session


# DB setup
print("Setting up database")
if get_settings().ENVIRONMENT == "local":
    DB_URL = get_settings().POSTGRES_URL
else:
    DB_URL = os.getenv("DB_URL", "DB_URL")
drop_database(DB_URL)
create_database(DB_URL)
alembic_config_file = os.path.join(get_settings().ROOT_DIR, "..", "alembic.ini")
alembic_cfg = Config(alembic_config_file)
alembic_cfg.set_main_option("sqlalchemy.url", DB_URL)
command.upgrade(alembic_cfg, "head")


print("Creating Script Families")
aramaic_script_family = SciptFamilyFactory(name="Aramaic")

print("Creating Alphabet")
avestan_alphabet = AlphabetFactory(
    writting_system=WrittingSystem.ALPHABET,
    writting_direction=WrittingDirection.RTL,
    script_family=aramaic_script_family,
    name="Avestan"
)

print("Creating transliteration system")
hoffmann_avestan = TransliterationSystemFactory(
    name="Hoffmann", description="Hoffmann transliteration system for Avestan",
)
simplified_polish_avestan = TransliterationSystemFactory(
    name="Simplified Polish", description="Simplified polish transliteration system for Avestan",
)

print("Creating characters")
#region Letters
a_character = CharacterFactory(
    value="𐬀",
    name="AVESTAN LETTER A",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B00",
    alphabet=avestan_alphabet,
)
aa_character = CharacterFactory(
    value="𐬁",
    name="AVESTAN LETTER AA",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B01",
    alphabet=avestan_alphabet,
)
ao_character = CharacterFactory(
    value="𐬂",
    name="AVESTAN LETTER AO",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B02",
    alphabet=avestan_alphabet,
)
aao_character = CharacterFactory(
    value="𐬃",
    name="AVESTAN LETTER AAO",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B03",
    alphabet=avestan_alphabet,
)
an_character = CharacterFactory(
    value="𐬄",
    name="AVESTAN LETTER AN",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B04",
    alphabet=avestan_alphabet,
)
aan_character = CharacterFactory(
    value="𐬅",
    name="AVESTAN LETTER AAN",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B05",
    alphabet=avestan_alphabet,
)
ae_character = CharacterFactory(
    value="𐬆",
    name="AVESTAN LETTER AE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B06",
    alphabet=avestan_alphabet,
)
aee_character = CharacterFactory(
    value="𐬇",
    name="AVESTAN LETTER AEE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B07",
    alphabet=avestan_alphabet,
)
e_character = CharacterFactory(
    value="𐬈",
    name="AVESTAN LETTER E",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B08",
    alphabet=avestan_alphabet,
)
ee_character = CharacterFactory(
    value="𐬉",
    name="AVESTAN LETTER EE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B09",
    alphabet=avestan_alphabet,
)
o_character = CharacterFactory(
    value="𐬊",
    name="AVESTAN LETTER O",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B0A",
    alphabet=avestan_alphabet,
)
oo_character = CharacterFactory(
    value="𐬋",
    name="AVESTAN LETTER OO",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B0B",
    alphabet=avestan_alphabet,
)
i_character = CharacterFactory(
    value="𐬌",
    name="AVESTAN LETTER I",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B0C",
    alphabet=avestan_alphabet,
)
ii_character = CharacterFactory(
    value="𐬍",
    name="AVESTAN LETTER II",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B0D",
    alphabet=avestan_alphabet,
)
u_character = CharacterFactory(
    value="𐬎",
    name="AVESTAN LETTER U",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B0E",
    alphabet=avestan_alphabet,
)
uu_character = CharacterFactory(
    value="𐬏",
    name="AVESTAN LETTER UU",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B0F",
    alphabet=avestan_alphabet,
)
ke_character = CharacterFactory(
    value="𐬐",
    name="AVESTAN LETTER KE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B10",
    alphabet=avestan_alphabet,
)
xe_character = CharacterFactory(
    value="𐬑",
    name="AVESTAN LETTER XE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B11",
    alphabet=avestan_alphabet,
)
xye_character = CharacterFactory(
    value="𐬒",
    name="AVESTAN LETTER XYE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B12",
    alphabet=avestan_alphabet,
)
xve_character = CharacterFactory(
    value="𐬓",
    name="AVESTAN LETTER XVE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B13",
    alphabet=avestan_alphabet,
)
ge_character = CharacterFactory(
    value="𐬔",
    name="AVESTAN LETTER GE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B14",
    alphabet=avestan_alphabet,
)
gge_character = CharacterFactory(
    value="𐬕",
    name="AVESTAN LETTER GGE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B15",
    alphabet=avestan_alphabet,
)
ghe_character = CharacterFactory(
    value="𐬖",
    name="AVESTAN LETTER GHE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B16",
    alphabet=avestan_alphabet,
)
ce_character = CharacterFactory(
    value="𐬗",
    name="AVESTAN LETTER CE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B17",
    alphabet=avestan_alphabet,
)
je_character = CharacterFactory(
    value="𐬘",
    name="AVESTAN LETTER JE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B18",
    alphabet=avestan_alphabet,
)
te_character = CharacterFactory(
    value="𐬙",
    name="AVESTAN LETTER TE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B19",
    alphabet=avestan_alphabet,
)
the_character = CharacterFactory(
    value="𐬚",
    name="AVESTAN LETTER THE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B1A",
    alphabet=avestan_alphabet,
)
de_character = CharacterFactory(
    value="𐬛",
    name="AVESTAN LETTER DE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B1B",
    alphabet=avestan_alphabet,
)
dhe_character = CharacterFactory(
    value="𐬜",
    name="AVESTAN LETTER DHE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B1C",
    alphabet=avestan_alphabet,
)
tte_character = CharacterFactory(
    value="𐬝",
    name="AVESTAN LETTER TTE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B1D",
    alphabet=avestan_alphabet,
)
pe_character = CharacterFactory(
    value="𐬞",
    name="AVESTAN LETTER PE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B1E",
    alphabet=avestan_alphabet,
)
fe_character = CharacterFactory(
    value="𐬟",
    name="AVESTAN LETTER FE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B1F",
    alphabet=avestan_alphabet,
)
be_character = CharacterFactory(
    value="𐬠",
    name="AVESTAN LETTER BE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B20",
    alphabet=avestan_alphabet,
)
bhe_character = CharacterFactory(
    value="𐬡",
    name="AVESTAN LETTER BHE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B21",
    alphabet=avestan_alphabet,
)
nge_character = CharacterFactory(
    value="𐬢",
    name="AVESTAN LETTER NGE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B22",
    alphabet=avestan_alphabet,
)
ngye_character = CharacterFactory(
    value="𐬣",
    name="AVESTAN LETTER NGYE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B23",
    alphabet=avestan_alphabet,
)
ngve_character = CharacterFactory(
    value="𐬤",
    name="AVESTAN LETTER NGVE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B24",
    alphabet=avestan_alphabet,
)
ne_character = CharacterFactory(
    value="𐬥",
    name="AVESTAN LETTER NE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B25",
    alphabet=avestan_alphabet,
)
nye_character = CharacterFactory(
    value="𐬦",
    name="AVESTAN LETTER NYE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B26",
    alphabet=avestan_alphabet,
)
nne_character = CharacterFactory(
    value="𐬧",
    name="AVESTAN LETTER NNE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B27",
    alphabet=avestan_alphabet,
)
me_character = CharacterFactory(
    value="𐬨",
    name="AVESTAN LETTER ME",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B28",
    alphabet=avestan_alphabet,
)
hme_character = CharacterFactory(
    value="𐬩",
    name="AVESTAN LETTER HME",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B29",
    alphabet=avestan_alphabet,
)
yye_character = CharacterFactory(
    value="𐬪",
    name="AVESTAN LETTER YYE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B2A",
    alphabet=avestan_alphabet,
)
ye_character = CharacterFactory(
    value="𐬫",
    name="AVESTAN LETTER YE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B2B",
    alphabet=avestan_alphabet,
)
ve_character = CharacterFactory(
    value="𐬬",
    name="AVESTAN LETTER VE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B2C",
    alphabet=avestan_alphabet,
)
re_character = CharacterFactory(
    value="𐬭",
    name="AVESTAN LETTER RE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B2D",
    alphabet=avestan_alphabet,
)
le_character = CharacterFactory(
    value="𐬮",
    name="AVESTAN LETTER LE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B2E",
    alphabet=avestan_alphabet,
)
se_character = CharacterFactory(
    value="𐬯",
    name="AVESTAN LETTER SE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B2F",
    alphabet=avestan_alphabet,
)
ze_character = CharacterFactory(
    value="𐬰",
    name="AVESTAN LETTER ZE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B30",
    alphabet=avestan_alphabet,
)
she_character = CharacterFactory(
    value="𐬱",
    name="AVESTAN LETTER SHE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B31",
    alphabet=avestan_alphabet,
)
zhe_character = CharacterFactory(
    value="𐬲",
    name="AVESTAN LETTER ZHE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B32",
    alphabet=avestan_alphabet,
)
shye_character = CharacterFactory(
    value="𐬳",
    name="AVESTAN LETTER SHYE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B33",
    alphabet=avestan_alphabet,
)
sshe_character = CharacterFactory(
    value="𐬴",
    name="AVESTAN LETTER SSHE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B34",
    alphabet=avestan_alphabet,
)
he_character = CharacterFactory(
    value="𐬵",
    name="AVESTAN LETTER HE",
    unit_type=AlphabetUnitType.LETTER,
    unicode_codepoint="U+10B35",
    alphabet=avestan_alphabet,
)
double_i_character = CharacterFactory(
    value="𐬌𐬌",
    name="AVESTAN LETTER I (doubled)",
    unit_type=AlphabetUnitType.SEQUENCE,
    unicode_codepoint="U+10B0C",
    alphabet=avestan_alphabet,
)
double_u_character = CharacterFactory(
    value="𐬎𐬎",
    name="AVESTAN LETTER U (doubled)",
    unit_type=AlphabetUnitType.SEQUENCE,
    unicode_codepoint="U+10B0E",
    alphabet=avestan_alphabet,
)
#endregion

print("Creating transliteration characters for Hoffmann")
#region Transliteration Hoffmann
a_trans_h = TransliterationCharacterFactory(
    value="a",
    character=a_character,
    transliteration_system=hoffmann_avestan,
)
aa_trans_h = TransliterationCharacterFactory(
    value="ā",
    character=aa_character,
    transliteration_system=hoffmann_avestan,
)
ao_trans_h = TransliterationCharacterFactory(
    value="ȧ",
    character=ao_character,
    transliteration_system=hoffmann_avestan,
)
aao_trans_h = TransliterationCharacterFactory(
    value="ā̊",
    character=aao_character,
    transliteration_system=hoffmann_avestan,
)
an_trans_h = TransliterationCharacterFactory(
    value="ą",
    character=an_character,
    transliteration_system=hoffmann_avestan,
)
aan_trans_h = TransliterationCharacterFactory(
    value="ą̇",
    character=aan_character,
    transliteration_system=hoffmann_avestan,
)
ae_trans_h = TransliterationCharacterFactory(
    value="ə",
    character=ae_character,
    transliteration_system=hoffmann_avestan,
)
aee_trans_h = TransliterationCharacterFactory(
    value="ə̄",
    character=aee_character,
    transliteration_system=hoffmann_avestan,
)
e_trans_h = TransliterationCharacterFactory(
    value="e",
    character=e_character,
    transliteration_system=hoffmann_avestan,
)
ee_trans_h = TransliterationCharacterFactory(
    value="ē",
    character=ee_character,
    transliteration_system=hoffmann_avestan,
)
o_trans_h = TransliterationCharacterFactory(
    value="o",
    character=o_character,
    transliteration_system=hoffmann_avestan,
)
oo_trans_h = TransliterationCharacterFactory(
    value="ō",
    character=oo_character,
    transliteration_system=hoffmann_avestan,
)
i_trans_h = TransliterationCharacterFactory(
    value="i",
    character=i_character,
    transliteration_system=hoffmann_avestan,
)
ii_trans_h = TransliterationCharacterFactory(
    value="ī",
    character=ii_character,
    transliteration_system=hoffmann_avestan,
)
u_trans_h = TransliterationCharacterFactory(
    value="u",
    character=u_character,
    transliteration_system=hoffmann_avestan,
)
uu_trans_h = TransliterationCharacterFactory(
    value="ū",
    character=uu_character,
    transliteration_system=hoffmann_avestan,
)
ke_trans_h = TransliterationCharacterFactory(
    value="k",
    character=ke_character,
    transliteration_system=hoffmann_avestan,
)
xe_trans_h = TransliterationCharacterFactory(
    value="x",
    character=xe_character,
    transliteration_system=hoffmann_avestan,
)
xye_trans_h = TransliterationCharacterFactory(
    value="x́",
    character=xye_character,
    transliteration_system=hoffmann_avestan,
)
xve_trans_h = TransliterationCharacterFactory(
    value="xᵛ",
    character=xve_character,
    transliteration_system=hoffmann_avestan,
)
ge_trans_h = TransliterationCharacterFactory(
    value="g",
    character=ge_character,
    transliteration_system=hoffmann_avestan,
)
gge_trans_h = TransliterationCharacterFactory(
    value="ġ",
    character=gge_character,
    transliteration_system=hoffmann_avestan,
)
ghe_trans_h = TransliterationCharacterFactory(
    value="γ",
    character=ghe_character,
    transliteration_system=hoffmann_avestan,
)
ce_trans_h = TransliterationCharacterFactory(
    value="c",
    character=ce_character,
    transliteration_system=hoffmann_avestan,
)
je_trans_h = TransliterationCharacterFactory(
    value="j",
    character=je_character,
    transliteration_system=hoffmann_avestan,
)
te_trans_h = TransliterationCharacterFactory(
    value="t",
    character=te_character,
    transliteration_system=hoffmann_avestan,
)
the_trans_h = TransliterationCharacterFactory(
    value="θ",
    character=the_character,
    transliteration_system=hoffmann_avestan,
)
de_trans_h = TransliterationCharacterFactory(
    value="d",
    character=de_character,
    transliteration_system=hoffmann_avestan,
)
dhe_trans_h = TransliterationCharacterFactory(
    value="δ",
    character=dhe_character,
    transliteration_system=hoffmann_avestan,
)
tte_trans_h = TransliterationCharacterFactory(
    value="t̰",
    character=tte_character,
    transliteration_system=hoffmann_avestan,
)
pe_trans_h = TransliterationCharacterFactory(
    value="p",
    character=pe_character,
    transliteration_system=hoffmann_avestan,
)
fe_trans_h = TransliterationCharacterFactory(
    value="f",
    character=fe_character,
    transliteration_system=hoffmann_avestan,
)
be_trans_h = TransliterationCharacterFactory(
    value="b",
    character=be_character,
    transliteration_system=hoffmann_avestan,
)
bhe_trans_h = TransliterationCharacterFactory(
    value="β",
    character=bhe_character,
    transliteration_system=hoffmann_avestan,
)
nge_trans_h = TransliterationCharacterFactory(
    value="ŋ",
    character=nge_character,
    transliteration_system=hoffmann_avestan,
)
ngye_trans_h = TransliterationCharacterFactory(
    value="ŋ́",
    character=ngye_character,
    transliteration_system=hoffmann_avestan,
)
ngve_trans_h = TransliterationCharacterFactory(
    value="ŋᵛ",
    character=ngve_character,
    transliteration_system=hoffmann_avestan,
)
ne_trans_h = TransliterationCharacterFactory(
    value="n",
    character=ne_character,
    transliteration_system=hoffmann_avestan,
)
nye_trans_h = TransliterationCharacterFactory(
    value="ń",
    character=nye_character,
    transliteration_system=hoffmann_avestan,
)
nne_trans_h = TransliterationCharacterFactory(
    value="ṇ",
    character=nne_character,
    transliteration_system=hoffmann_avestan,
)
me_trans_h = TransliterationCharacterFactory(
    value="m",
    character=me_character,
    transliteration_system=hoffmann_avestan,
)
hme_trans_h = TransliterationCharacterFactory(
    value="m̨",
    character=hme_character,
    transliteration_system=hoffmann_avestan,
)
yye_trans_h = TransliterationCharacterFactory(
    value="ẏ",
    character=yye_character,
    transliteration_system=hoffmann_avestan,
)
ye_trans_h = TransliterationCharacterFactory(
    value="y",
    character=ye_character,
    transliteration_system=hoffmann_avestan,
)
ve_trans_h = TransliterationCharacterFactory(
    value="v",
    character=ve_character,
    transliteration_system=hoffmann_avestan,
)
re_trans_h = TransliterationCharacterFactory(
    value="r",
    character=re_character,
    transliteration_system=hoffmann_avestan,
)
se_trans_h = TransliterationCharacterFactory(
    value="s",
    character=se_character,
    transliteration_system=hoffmann_avestan,
)
ze_trans_h = TransliterationCharacterFactory(
    value="z",
    character=ze_character,
    transliteration_system=hoffmann_avestan,
)
she_trans_h = TransliterationCharacterFactory(
    value="š",
    character=she_character,
    transliteration_system=hoffmann_avestan,
)
zhe_trans_h = TransliterationCharacterFactory(
    value="ž",
    character=zhe_character,
    transliteration_system=hoffmann_avestan,
)
shye_trans_h = TransliterationCharacterFactory(
    value="š́",
    character=shye_character,
    transliteration_system=hoffmann_avestan,
)
sshe_trans_h = TransliterationCharacterFactory(
    value="ṣ̌",
    character=sshe_character,
    transliteration_system=hoffmann_avestan,
)
he_trans_h = TransliterationCharacterFactory(
    value="h",
    character=he_character,
    transliteration_system=hoffmann_avestan,
)
ii_sequence_trans_h = TransliterationCharacterFactory(
    value="ii",
    character=double_i_character,
    transliteration_system=hoffmann_avestan,
)
uu_sequence_trans_h = TransliterationCharacterFactory(
    value="uu",
    character=double_u_character,
    transliteration_system=hoffmann_avestan,
)
le_trans_h = TransliterationCharacterFactory(
    value="l",
    character=le_character,
    transliteration_system=hoffmann_avestan,
)
#endregion

print("Creating transliteration characters for Simplified Polish")
#region Transliteration Simplified Polish
a_trans_pl = TransliterationCharacterFactory(
    value="a",
    character=a_character,
    transliteration_system=simplified_polish_avestan,
)
aa_trans_pl = TransliterationCharacterFactory(
    value="a",
    character=aa_character,
    transliteration_system=simplified_polish_avestan,
)
ao_trans_pl = TransliterationCharacterFactory(
    value="o",
    character=ao_character,
    transliteration_system=simplified_polish_avestan,
)
aao_trans_pl = TransliterationCharacterFactory(
    value="o",
    character=aao_character,
    transliteration_system=simplified_polish_avestan,
)
an_trans_pl = TransliterationCharacterFactory(
    value="ą",
    character=an_character,
    transliteration_system=simplified_polish_avestan,
)
aan_trans_pl = TransliterationCharacterFactory(
    value="ą",
    character=aan_character,
    transliteration_system=simplified_polish_avestan,
)
ae_trans_pl = TransliterationCharacterFactory(
    value="e",
    character=ae_character,
    transliteration_system=simplified_polish_avestan,
)
aee_trans_pl = TransliterationCharacterFactory(
    value="e",
    character=aee_character,
    transliteration_system=simplified_polish_avestan,
)
e_trans_pl = TransliterationCharacterFactory(
    value="e",
    character=e_character,
    transliteration_system=simplified_polish_avestan,
)
ee_trans_pl = TransliterationCharacterFactory(
    value="e",
    character=ee_character,
    transliteration_system=simplified_polish_avestan,
)
o_trans_pl = TransliterationCharacterFactory(
    value="o",
    character=o_character,
    transliteration_system=simplified_polish_avestan,
)
oo_trans_pl = TransliterationCharacterFactory(
    value="o",
    character=oo_character,
    transliteration_system=simplified_polish_avestan,
)
i_trans_pl = TransliterationCharacterFactory(
    value="i",
    character=i_character,
    transliteration_system=simplified_polish_avestan,
)
ii_trans_pl = TransliterationCharacterFactory(
    value="i",
    character=ii_character,
    transliteration_system=simplified_polish_avestan,
)
u_trans_pl = TransliterationCharacterFactory(
    value="u",
    character=u_character,
    transliteration_system=simplified_polish_avestan,
)
uu_trans_pl = TransliterationCharacterFactory(
    value="u",
    character=uu_character,
    transliteration_system=simplified_polish_avestan,
)
ke_trans_pl = TransliterationCharacterFactory(
    value="k",
    character=ke_character,
    transliteration_system=simplified_polish_avestan,
)
xe_trans_pl = TransliterationCharacterFactory(
    value="ch",
    character=xe_character,
    transliteration_system=simplified_polish_avestan,
)
xye_trans_pl = TransliterationCharacterFactory(
    value="chj",
    character=xye_character,
    transliteration_system=simplified_polish_avestan,
)
xve_trans_pl = TransliterationCharacterFactory(
    value="chw",
    character=xve_character,
    transliteration_system=simplified_polish_avestan,
)
ge_trans_pl = TransliterationCharacterFactory(
    value="g",
    character=ge_character,
    transliteration_system=simplified_polish_avestan,
)
gge_trans_pl = TransliterationCharacterFactory(
    value="gj",
    character=gge_character,
    transliteration_system=simplified_polish_avestan,
)
ghe_trans_pl = TransliterationCharacterFactory(
    value="gh",
    character=ghe_character,
    transliteration_system=simplified_polish_avestan,
)
ce_trans_pl = TransliterationCharacterFactory(
    value="cz",
    character=ce_character,
    transliteration_system=simplified_polish_avestan,
)
je_trans_pl = TransliterationCharacterFactory(
    value="dż",
    character=je_character,
    transliteration_system=simplified_polish_avestan,
)
te_trans_pl = TransliterationCharacterFactory(
    value="t",
    character=te_character,
    transliteration_system=simplified_polish_avestan,
)
the_trans_pl = TransliterationCharacterFactory(
    value="th",
    character=the_character,
    transliteration_system=simplified_polish_avestan,
)
de_trans_pl = TransliterationCharacterFactory(
    value="d",
    character=de_character,
    transliteration_system=simplified_polish_avestan,
)
dhe_trans_pl = TransliterationCharacterFactory(
    value="dh",
    character=dhe_character,
    transliteration_system=simplified_polish_avestan,
)
tte_trans_pl = TransliterationCharacterFactory(
    value="t",
    character=tte_character,
    transliteration_system=simplified_polish_avestan,
)
pe_trans_pl = TransliterationCharacterFactory(
    value="p",
    character=pe_character,
    transliteration_system=simplified_polish_avestan,
)
fe_trans_pl = TransliterationCharacterFactory(
    value="f",
    character=fe_character,
    transliteration_system=simplified_polish_avestan,
)
be_trans_pl = TransliterationCharacterFactory(
    value="b",
    character=be_character,
    transliteration_system=simplified_polish_avestan,
)
bhe_trans_pl = TransliterationCharacterFactory(
    value="bh",
    character=bhe_character,
    transliteration_system=simplified_polish_avestan,
)
nge_trans_pl = TransliterationCharacterFactory(
    value="ng",
    character=nge_character,
    transliteration_system=simplified_polish_avestan,
)
ngye_trans_pl = TransliterationCharacterFactory(
    value="ngj",
    character=ngye_character,
    transliteration_system=simplified_polish_avestan,
)
ngve_trans_pl = TransliterationCharacterFactory(
    value="ngw",
    character=ngve_character,
    transliteration_system=simplified_polish_avestan,
)
ne_trans_pl = TransliterationCharacterFactory(
    value="n",
    character=ne_character,
    transliteration_system=simplified_polish_avestan,
)
nye_trans_pl = TransliterationCharacterFactory(
    value="ń",
    character=nye_character,
    transliteration_system=simplified_polish_avestan,
)
nne_trans_pl = TransliterationCharacterFactory(
    value="n",
    character=nne_character,
    transliteration_system=simplified_polish_avestan,
)
me_trans_pl = TransliterationCharacterFactory(
    value="m",
    character=me_character,
    transliteration_system=simplified_polish_avestan,
)
hme_trans_pl = TransliterationCharacterFactory(
    value="mh",
    character=hme_character,
    transliteration_system=simplified_polish_avestan,
)
yye_trans_pl = TransliterationCharacterFactory(
    value="i",
    character=yye_character,
    transliteration_system=simplified_polish_avestan,
)
ye_trans_pl = TransliterationCharacterFactory(
    value="j",
    character=ye_character,
    transliteration_system=simplified_polish_avestan,
)
ve_trans_pl = TransliterationCharacterFactory(
    value="w",
    character=ve_character,
    transliteration_system=simplified_polish_avestan,
)
re_trans_pl = TransliterationCharacterFactory(
    value="r",
    character=re_character,
    transliteration_system=simplified_polish_avestan,
)
se_trans_pl = TransliterationCharacterFactory(
    value="s",
    character=se_character,
    transliteration_system=simplified_polish_avestan,
)
ze_trans_pl = TransliterationCharacterFactory(
    value="z",
    character=ze_character,
    transliteration_system=simplified_polish_avestan,
)
she_trans_pl = TransliterationCharacterFactory(
    value="sz",
    character=she_character,
    transliteration_system=simplified_polish_avestan,
)
zhe_trans_pl = TransliterationCharacterFactory(
    value="ż",
    character=zhe_character,
    transliteration_system=simplified_polish_avestan,
)
shye_trans_pl = TransliterationCharacterFactory(
    value="szj",
    character=shye_character,
    transliteration_system=simplified_polish_avestan,
)
sshe_trans_pl = TransliterationCharacterFactory(
    value="sz",
    character=sshe_character,
    transliteration_system=simplified_polish_avestan,
)
he_trans_pl = TransliterationCharacterFactory(
    value="h",
    character=he_character,
    transliteration_system=simplified_polish_avestan,
)
ii_sequence_trans_pl = TransliterationCharacterFactory(
    value="ii",
    character=double_i_character,
    transliteration_system=simplified_polish_avestan,
)
uu_sequence_trans_pl = TransliterationCharacterFactory(
    value="ó",
    character=double_u_character,
    transliteration_system=simplified_polish_avestan,
)
le_trans_pl = TransliterationCharacterFactory(
    value="l",
    character=le_character,
    transliteration_system=simplified_polish_avestan,
)
#endregion

session.commit()
