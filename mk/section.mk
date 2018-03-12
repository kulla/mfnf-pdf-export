THE_SECTIONS = the_sections
BUILD_YML = build_yml
REVID := $(shell $(MK)/resolve_revid.sh $(ARTICLE) $(MAKECMDGOALS))

$(THE_SECTIONS): $(BASE)/articles/$(ARTICLE)/$(REVID).yml
	$(MK)/article_sections.sh $(ARTICLE) < $<

$(BASE)/articles/%.yml :: $(BUILD_YML) ;

% :: $(THE_SECTIONS) ;

$(BUILD_YML):
	$(MAKE) -C $(BASE) articles/$(ARTICLE)/$(REVID:%=%.yml)

.PHONY: $(THE_SECTIONS) $(BUILD_YML)