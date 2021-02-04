
install-parent:
	@cd .. && make install >/dev/null


print: install-parent
ifeq ($(stage), )
	@poetry run python bin/generate.py
else
	@poetry run python bin/generate.py --stage $(stage)
endif


assert-path:
ifeq ($(path), )
	$(error 'make apply' must be given a 'path=...' argument to apply _to_)
endif


apply: assert-path install-parent
ifeq ($(stage), )
	@poetry run python bin/apply.py -i $(path) --pretty
else
	@poetry run python bin/apply.py -i $(path) --pretty --stage $(stage)
endif
