# Stackchan Gemini: the base tier. Everything is the shared core
# (core/components/stackchan_app); this only names the tier.
idf_component_register(
    SRCS
        "app_main.cpp"
    INCLUDE_DIRS "."
    REQUIRES
        stackchan_app
)
target_compile_features(${COMPONENT_LIB} PRIVATE cxx_std_20)
