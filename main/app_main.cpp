// SPDX-FileCopyrightText: 2026 JJ Hartnett <jj.hartnett777@gmail.com>
// SPDX-License-Identifier: BSL-1.0

// Stackchan Gemini: the base tier on the shared Stack-chan core (core/,
// tier.hpp). The core is the whole robot: face, Gemini Live voice with its
// body tools, head, LED bars, inner life, senses, themes, settings and the
// remote API; its photo component adds the camera, the microSD card and the
// photo booth. Roombot and Server Bot add their own things on top of the
// same core.

#include "app_launcher.hpp"
#include "head_screen.hpp"
#include "photo.hpp"
#include "photobooth_screen.hpp"
#include "settings_screen.hpp"
#include "tier.hpp"

namespace {

namespace app = stackchan::app;

std::uint16_t rgb(std::uint8_t r, std::uint8_t g, std::uint8_t b)
{
    return static_cast<std::uint16_t>(((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3));
}

void init(app::SharedState& state)
{
    app::photo::init(state); // microSD, the photo booth, /api/gemini/sd

    // Its apps come before the core's (Head, LEDs, Settings).
    app::launcher::register_app({"Photo Booth", "say cheese", rgb(240, 90, 150), [] { app::photobooth_ui::open(); },
                                 [] { return app::photobooth_ui::status(); }, "photobooth"});

    // Desktop icons (Aqua) and start-menu places (Luna).
    app::launcher::register_place({"photos", "Photos", "photobooth", [] { app::photobooth_ui::open_gallery(); }});
    app::launcher::register_place({"settings", "Settings", "settings", [] { app::settings::open(); }});
    app::launcher::register_place({"head", "Head", "head", [] { app::head_ui::open(); }});
}

} // namespace

extern "C" void app_main()
{
    app::tier::Hooks hooks;
    hooks.name = "gemini"; // remote API at /api/gemini/*
    hooks.title = "Stack-chan";
    hooks.init = init;
    app::run(hooks);
}
