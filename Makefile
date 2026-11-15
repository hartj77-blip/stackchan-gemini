IDF_PATH    ?= $(HOME)/esp/esp-idf
IDF_EXPORTS  = $(IDF_PATH)/export.sh
TARGET      ?= esp32s3

# Board profile. Only `cores3` (M5Stack CoreS3 + Stack-chan base, 16 MB flash /
# Quad PSRAM) ships in v1; the variable stays so another board can be added
# without reworking the build-dir / sdkconfig plumbing.
BOARD       ?= cores3
BUILD_DIR    = build-$(BOARD)

# Serial port for flash / monitor / erase-flash. Leave unset to let idf.py
# auto-detect; pass on the command line (`make flash PORT=/dev/ttyACM0`) or
# pin in Makefile.local.
PORT        ?=
IDFPY_PORT   = $(if $(PORT),-p $(PORT))

# Allow developers to keep local overrides in an untracked file.
-include Makefile.local

# Build sdkconfig defaults chains.
#   - sdkconfig.defaults                  (committed, common)
#   - sdkconfig.defaults.<target>         (committed, per-chip — esp32s3 here)
#   - sdkconfig.defaults.<board>          (committed, per-board variant —
#     cores3; PSRAM mode lives here)
#   - sdkconfig.defaults.local            (gitignored, host-specific overrides;
#     the last entry wins for duplicate keys so local values trump committed
#     defaults)
SDKCONFIG_DEFAULTS_HW   = sdkconfig.defaults
ifneq (,$(wildcard sdkconfig.defaults.$(TARGET)))
SDKCONFIG_DEFAULTS_HW  := $(SDKCONFIG_DEFAULTS_HW);sdkconfig.defaults.$(TARGET)
endif
ifneq (,$(wildcard sdkconfig.defaults.$(BOARD)))
SDKCONFIG_DEFAULTS_HW  := $(SDKCONFIG_DEFAULTS_HW);sdkconfig.defaults.$(BOARD)
endif
ifneq (,$(wildcard sdkconfig.defaults.local))
SDKCONFIG_DEFAULTS_HW  := $(SDKCONFIG_DEFAULTS_HW);sdkconfig.defaults.local
endif

.PHONY: build clean set-target flash flash-monitor monitor monitor-log erase-flash sdcard update \
        build-docker docker-shell docker-clean


# Capture serial output non-interactively (for CI / agent contexts where
# idf.py monitor refuses to attach without a TTY). SECONDS defaults to 8.
MONITOR_LOG_SECONDS ?= 8

# --- Over Wi-Fi (HOST = the robot's address, or $STACKCHAN_HOST) ------------

HOST ?= $(STACKCHAN_HOST)

# The starter card (sdcard/: stickers, a song, a video) onto the robot's microSD.
sdcard:
	STACKCHAN_HOST=$(HOST) python3 core/tools/sd_push.py push sdcard

# Build and send the firmware over Wi-Fi (after the first USB flash).
update: build
	python3 script/ota_wifi.py $(HOST)

# --- Target builds ----------------------------------------------------------

set-target:
	bash -c "source $(IDF_EXPORTS) && idf.py -B $(BUILD_DIR) -DSDKCONFIG=$(BUILD_DIR)/sdkconfig -DSDKCONFIG_DEFAULTS='$(SDKCONFIG_DEFAULTS_HW)' set-target $(TARGET)"

build:
	bash -c "source $(IDF_EXPORTS) && idf.py -B $(BUILD_DIR) -DSDKCONFIG=$(BUILD_DIR)/sdkconfig -DSDKCONFIG_DEFAULTS='$(SDKCONFIG_DEFAULTS_HW)' build"

flash:
	bash -c "source $(IDF_EXPORTS) && idf.py -B $(BUILD_DIR) $(IDFPY_PORT) flash"

monitor:
	bash -c "source $(IDF_EXPORTS) && idf.py -B $(BUILD_DIR) $(IDFPY_PORT) monitor"

# Non-interactive log capture: resets the target and reads stdout for
# MONITOR_LOG_SECONDS seconds. Requires pyserial.
monitor-log:
	python3 tools/monitor_log.py --port $(if $(PORT),$(PORT),/dev/ttyACM0) --seconds $(MONITOR_LOG_SECONDS)

# Convenience: flash + monitor in a single idf.py invocation (faster than
# `make flash monitor` because the IDF env is sourced once).
flash-monitor:
	bash -c "source $(IDF_EXPORTS) && idf.py -B $(BUILD_DIR) $(IDFPY_PORT) flash monitor"

erase-flash:
	bash -c "source $(IDF_EXPORTS) && idf.py -B $(BUILD_DIR) $(IDFPY_PORT) erase-flash"

clean:
	bash -c "source $(IDF_EXPORTS) && idf.py -B $(BUILD_DIR) fullclean"

# --- Docker build (mirrors CI) ----------------------------------------------
DOCKER_IMAGE         ?= espressif/idf:v5.4.2
DOCKER_WORKDIR       ?= /work
DOCKER_BUILD_DIR     ?= build-docker
DOCKER_SDKCONFIG     ?= sdkconfig.docker
DOCKER_TARGET_CHIP   ?= esp32s3

define docker-run
	docker run --rm -t \
		-u $$(id -u):$$(id -g) \
		-v "$(CURDIR):$(DOCKER_WORKDIR)" \
		-w $(DOCKER_WORKDIR) \
		-e HOME=/tmp \
		-e CI=true \
		$(DOCKER_IMAGE) \
		bash -c '\
			git config --global --add safe.directory "$(DOCKER_WORKDIR)" && \
			. "$$IDF_PATH/export.sh" && \
			$(1)'
endef

build-docker:
	$(call docker-run, \
		idf.py -B $(DOCKER_BUILD_DIR) -DSDKCONFIG=$(DOCKER_SDKCONFIG) \
		       -DSDKCONFIG_DEFAULTS=sdkconfig.defaults \
		       set-target $(DOCKER_TARGET_CHIP) && \
		idf.py -B $(DOCKER_BUILD_DIR) -DSDKCONFIG=$(DOCKER_SDKCONFIG) \
		       -DSDKCONFIG_DEFAULTS=sdkconfig.defaults build)

docker-clean:
	$(call docker-run, \
		idf.py -B $(DOCKER_BUILD_DIR) -DSDKCONFIG=$(DOCKER_SDKCONFIG) \
		       fullclean)
	@rm -f $(DOCKER_SDKCONFIG)

docker-shell:
	docker run --rm -it \
		-u $$(id -u):$$(id -g) \
		-v "$(CURDIR):$(DOCKER_WORKDIR)" \
		-w $(DOCKER_WORKDIR) \
		-e HOME=/tmp \
		$(DOCKER_IMAGE) \
		bash -c '\
			git config --global --add safe.directory "$(DOCKER_WORKDIR)" && \
			. "$$IDF_PATH/export.sh" && \
			exec bash'
