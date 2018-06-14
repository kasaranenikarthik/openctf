package templates

//go:generate go-bindata -ignore "\\.go" -pkg "templates" -o "bindata.go" ./...

import (
	"github.com/easyctf/openctf/structs"
	"github.com/go-macaron/bindata"
	macaron "gopkg.in/macaron.v1"
)

// Renderer returns a static renderer from bindata
func Renderer(conf structs.Config) macaron.Handler {
	return macaron.Renderer(macaron.RenderOptions{
		TemplateFileSystem: bindata.Templates(bindata.Options{
			Asset:      Asset,
			AssetDir:   AssetDir,
			AssetInfo:  AssetInfo,
			AssetNames: AssetNames,
			Prefix:     "",
		}),
	})
}
