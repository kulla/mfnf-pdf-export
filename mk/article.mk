REVISIONS = revisions

$(REVISIONS):
	$(eval ARCTICLE := $(patsubst %/,%,$(dir $(MAKECMDGOALS))))
	$(eval REVISION := $(notdir $(MAKECMDGOALS)))
	@[[ -d $(ARCTICLE) ]] || mkdir $(ARCTICLE)
	$(MAKE) -C $(ARCTICLE) -f $(MK)/revision.mk ARTICLE=$(ARCTICLE) MK=$(MK) $(REVISION)

% :: $(REVISIONS) ;

.PHONY: $(REVISIONS)