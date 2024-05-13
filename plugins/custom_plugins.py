from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        "FEATURES['ENABLE_SPECIAL_EXAMS'] = True"
    )
)

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-cms-common-settings",
        "FEATURES['ENABLE_SPECIAL_EXAMS'] = True"
    )
)
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        "SKIP_EMAIL_VALIDATION = True"
    )
)
