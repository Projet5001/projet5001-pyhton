#!make -s

all:
	@if [ ! -d assets ]; then \
		git clone git@bitbucket.org:projet5001/assets.git; \
	else \
		sh -c "cd assets/; git pull"; \
	fi
