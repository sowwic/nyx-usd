# Common targets come from sowwic/makefiles, fetched into .make/ (commit it). `make update-make` fetches them again.
APP_NAME = nyx-usd
PACKAGE_NAME = nyx_usd
RELEASE_BRANCH ?= main
DEVELOP_BRANCH ?= develop

MAKEFILES_REF ?= v1
MAKEFILES_URL ?= https://raw.githubusercontent.com/sowwic/makefiles/$(MAKEFILES_REF)
MAKEFILES_MODULES = general/python general/repo general/pypi

.make/%.mk:
	@mkdir -p $(dir $@)
	@curl -fsSL $(MAKEFILES_URL)/$*.mk -o $@
include $(MAKEFILES_MODULES:%=.make/%.mk)

# The Qt resources of the Nyx plugin, compiled next to their .qrc file.
PLUGIN_QRC_FILES = $(shell find plugins -name resources.qrc)

.PHONY: qrc
qrc: ## Generate Python resources from the Qt .qrc files under plugins
	$(call banner, Generating QRC resources...)
	@for qrc in $(PLUGIN_QRC_FILES); do \
		uv run pyside6-rcc $$qrc -o $$(dirname $$qrc)/resources_rc.py || exit 1; \
	done
	@printf "$(GREEN)QRC generation complete.$(RESET)\n"
