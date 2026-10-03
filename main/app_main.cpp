// SPDX-FileCopyrightText: 2026 JJ Hartnett <jj.hartnett777@gmail.com>
// SPDX-License-Identifier: BSL-1.0

// Stackchan Gemini: the base tier on the shared Stack-chan core (core/,
// tier.hpp). The core is the whole robot: face, Gemini Live voice with its
// body tools, head, LED bars, inner life, senses, themes, settings and the
// remote API. Roombot and Server Bot add their own things
// on top of the same core.

#include "app_launcher.hpp"
#include "head_screen.hpp"
#include "led_screen.hpp"
#include "settings_screen.hpp"
#include "tier.hpp"

namespace {

namespace app = stackchan::app;

void init(app::SharedState& /*state*/)
{
    // Desktop icons (Aqua) and start-menu places (Luna).
    app::launcher::register_place({"settings", "Settings", "settings", [] { app::settings::open(); }});
    app::launcher::register_place({"head", "Head", "head", [] { app::head_ui::open(); }});
    app::launcher::register_place({"leds", "LEDs", "leds", [] { app::led_ui::open(); }});
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
