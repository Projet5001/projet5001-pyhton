#!make -s

all:
	@if [ ! -d assets ]; then \
		git clone git@bitbucket.org:projet5001/assets.git; \
	else \
		echo "Les assets sont déjà disponibles."; \
	fi
