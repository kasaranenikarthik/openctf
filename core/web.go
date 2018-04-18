package core

import (
	"github.com/easyctf/openctf/api"
	"github.com/easyctf/openctf/structs"
	"github.com/go-macaron/bindata"
	"gopkg.in/macaron.v1"
)

// CreateServer generates a new gin server
func CreateServer(config structs.Config) (server structs.Webserver, err error) {
	m := macaron.Classic()
	server = structs.Webserver{M: m, Config: config}

	// for serving the actual HTML/JS site
	m.Use(macaron.Static("public",
		macaron.StaticOptions{
			FileSystem: bindata.Static(bindata.Options{
				Asset:      Asset,
				AssetDir:   AssetDir,
				AssetNames: AssetNames,
				Prefix:     "",
			}),
		},
	))

	// API routes
	m.Group("/api", api.RouteAPI(server))
	return
}
