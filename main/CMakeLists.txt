# Stackchan Gemini: the base tier. Everything is the shared core
# (core/components/stackchan_app, stackchan_photo); this names the tier
# and adds the photo booth to the launcher.
idf_component_register(
    SRCS
        "app_main.cpp"
    INCLUDE_DIRS "."
    REQUIRES
        stackchan_app
        stackchan_photo
)
target_compile_features(${COMPONENT_LIB} PRIVATE cxx_std_20)
