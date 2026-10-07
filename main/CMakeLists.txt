# Stackchan Gemini: the base tier. Everything is the shared core
# (core/components/stackchan_app, stackchan_photo, stackchan_media,
# stackchan_nfc); this names the tier and adds the photo booth, SD music and
# NFC cards to the launcher.
idf_component_register(
    SRCS
        "app_main.cpp"
    INCLUDE_DIRS "."
    REQUIRES
        stackchan_app
        stackchan_photo
        stackchan_media
        stackchan_nfc
)
target_compile_features(${COMPONENT_LIB} PRIVATE cxx_std_20)
