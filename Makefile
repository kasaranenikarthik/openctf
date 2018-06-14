# Largely based on https://github.com/go-gitea/gitea/blob/master/Makefile

GO ?= go
GOFMT ?= gofmt -s

GOFLAGS := -i -v
EXTRA_GOFLAGS ?=

SOURCES ?= $(shell find . -name "*.go" -type f)
TAGS ?=
LDFLAGS := -X "main.Version=$(shell git describe --tags --always | sed 's/-/+/' | sed 's/^v//')" -X "main.Tags=$(TAGS)"

ifeq ($(OS), Windows_NT)
	EXECUTABLE := openctf.exe
else
	EXECUTABLE := openctf
endif

.PHONY: all
all: build

.PHONY: build
build: $(EXECUTABLE)

.PHONY: clean
clean:
	$(GO) clean -i ./...
	rm -rf $(EXECUTABLE)

.PHONY: generate
generate:
	@hash go-bindata > /dev/null 2>&1; if [ $$? -ne 0 ]; then \
		$(GO) get -u github.com/jteeuwen/go-bindata/...; \
	fi
	$(GO) generate $(PACKAGES)

$(EXECUTABLE): $(SOURCES)
	$(GO) build $(GOFLAGS) $(EXTRA_GOFLAGS) -tags '$(TAGS)' -ldflags '-s -w $(LDFLAGS)' -o $@