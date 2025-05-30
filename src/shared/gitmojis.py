import enum


class GitmojiEnum(enum.Enum):
    """Gitmoji symbols."""

    FIX = "🐛"
    FEAT = "✨"
    DOCS = "📝"
    STYLE = "🎨"
    REFACTOR = "♻️"
    PERF = "⚡️"
    TEST = "✅"
    BUILD = "👷"
    CI = "💚"
    REVERT = "⏪️"
    DUMP = "🔥"
    HOTFIX = "🚑️"
    DEPLOY = "🚀"
    UI = "💄"
    INIT = "🎉"
    SECURITY = "🔒️"
    SECRET = "🔐"
    BUMP = "🔖"
    FIX_LINT = "🚨"
    WIP = "🚧"
    DEP_DROP = "⬇️"
    DEP_BUMP = "⬆️"
    PIN = "📌"
    ANALYTICS = "📈"
    DEP_ADD = "➕"
    DEP_RM = "➖"
    CONFIG = "🔧"
    SCRIPT = "🔨"
    LANG = "🌐"
    TYPO = "✏️"
    POOP = "💩"
    MERGE = "🔀"
    PACKAGE = "📦️"
    EXTERNAL = "👽️"
    RESOURCE = "🚚"
    LICENSE = "📄"
    BOOM = "💥"
    ASSET = "🍱"
    ACCESSIBILITY = "♿️"
    SOURCE_DOCS = "💡"
    BEER = "🍻"
    TEXT = "💬"
    DB = "🗃️"
    LOGS_ADD = "🔊"
    LOGS_RM = "🔇"
    PEOPLE = "👥"
    UX = "🚸"
    ARCH = "🏗️"
    DESIGN = "📱"
    MOCK = "🤡"
    EGG = "🥚"
    IGNORE = "🙈"
    SNAP = "📸"
    EXPERIMENT = "⚗️"
    SEO = "🔍️"
    TYPES = "🏷️"
    SEED = "🌱"
    FLAG = "🚩"
    CATCH = "🥅"
    ANIMATION = "💫"
    DEPRECATION = "🗑️"
    AUTH = "🛂"
    FIX_SIMPLE = "🩹"
    EXPLORATION = "🧐"
    DEAD = "⚰️"
    TEST_FAIL = "🧪"
    LOGIC = "👔"
    HEALTH = "🩺"
    INFRA = "🧱"
    DEVXP = "🧑‍💻"
    MONEY = "💸"
    THREADING = "🧵"
    VALIDATION = "🦺"
    CHORE = "🧹"
    SQUASH = "👇"
    FIXUP = "🫥"

    def __str__(self) -> str:
        """Return the emoji symbol."""
        return self.value
