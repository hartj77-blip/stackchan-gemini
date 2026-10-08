// SPDX-FileCopyrightText: 2026 JJ Hartnett <jj.hartnett777@gmail.com>
// SPDX-License-Identifier: BSL-1.0

// Stackchan Gemini: the base tier on the shared Stack-chan core (core/,
// tier.hpp). The core is the whole robot: face, Gemini Live voice with its
// body tools, head, LED bars, inner life, senses, themes, settings and the
// remote API; its photo component adds the camera, the microSD card and the
// photo booth, its media component music from the card, its NFC component
// cards you tap to make it play, dance or say something. Roombot and Server
// Bot add their own things on top of the same core.

#include "app_launcher.hpp"
#include "head_screen.hpp"
#include "media_player.hpp"
#include "media_remote.hpp"
#include "nfc_cards.hpp"
#include "nfc_screen.hpp"
#include "photo.hpp"
#include "photobooth_screen.hpp"
#include "remote.hpp"
#include "player_screen.hpp"
#include "sd_music.hpp"
#include "settings_screen.hpp"
#include "tier.hpp"
#include "ui_theme/theme.hpp"

namespace {

namespace app = stackchan::app;

std::uint16_t rgb(std::uint8_t r, std::uint8_t g, std::uint8_t b)
{
    return static_cast<std::uint16_t>(((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3));
}

void init(app::SharedState& state)
{
    app::photo::init(state); // microSD, the photo booth, /api/gemini/sd
    // Music from the card. Playback borrows the conversation's speaker
    // buffers; the conversation is paused while media owns the speaker.
    app::media::init(state);
    app::sd_music::init(state); // the Music app, play_media / media_control
    // NFC cards: written cards only (no PC to link cards by UID).
    app::nfc::init(state);
    app::nfc_ui::init(state);
    app::remote::set_status_extra([](cJSON* r) {
        app::media::add_status(r);
        app::nfc::add_status(r);
    });

    // Its apps come before the core's (Head, LEDs, Settings).
    app::launcher::register_app({"Photo Booth", "say cheese", rgb(240, 90, 150), [] { app::photobooth_ui::open(); },
                                 [] { return app::photobooth_ui::status(); }, "photobooth"});
    app::launcher::register_app({"NFC cards", "tap to play", rgb(230, 140, 60), [] { app::nfc_ui::open(); }, {}, "nfc"});

    // Desktop icons (Aqua) and start-menu places (Luna).
    app::launcher::register_place({"photos", "Photos", "photobooth", [] { app::photobooth_ui::open_gallery(); }});
    app::launcher::register_place({"music", "Music", "media", [] { app::sd_music::open(); }});
    app::launcher::register_place({"settings", "Settings", "settings", [] { app::settings::open(); }});
    app::launcher::register_place({"head", "Head", "head", [] { app::head_ui::open(); }});
}

// The strip under the face: what's playing.
void hud(stackchan::ui::HudView& v)
{
    using Icon = stackchan::ui::HudView::LineIcon;
    if (!app::media::active()) return;
    const app::media::Status st = app::media::status();
    v.line = st.title.empty() ? std::string{"Playing"} : st.title;
    v.line_icon = st.state == app::media::State::Paused ? Icon::Paused : Icon::Playing;
}

} // namespace

extern "C" void app_main()
{
    app::tier::Hooks hooks;
    hooks.name = "gemini"; // remote API at /api/gemini/*
    hooks.title = "Stack-chan";
    hooks.init = init;
    hooks.tick = [](app::SharedState& state, std::uint32_t now_ms) { app::media_ui::talk_tick(state, now_ms); };
    hooks.hud = hud;
    hooks.strip_tap = [] { app::media_ui::open_player(); };
    hooks.busy = [] { return app::media::active(); };
    hooks.quiet_glow = [] { return app::media::active(); };
    // Music playing minimised holds the mic, so a pat pauses it first.
    hooks.listen_opened = [] {
        if (app::media::playing()) app::media::pause_for_talk();
    };
    app::run(hooks);
}
