package static

import (
	"github.com/go-macaron/bindata"
	macaron "gopkg.in/macaron.v1"
)

//go:generate go-bindata -ignore "\\.go" -pkg "static" -o "bindata.go" ./...

// Static returns a static renderer from bindata
func Static() macaron.Handler {
	return macaron.Static("static", macaron.StaticOptions{
		Prefix:      "/static",
		SkipLogging: true,
		FileSystem: bindata.Static(bindata.Options{
			Asset:      Asset,
			AssetDir:   AssetDir,
			AssetInfo:  AssetInfo,
			AssetNames: AssetNames,
			Prefix:     "",
		}),
	})
}
