package core

import (
	"github.com/easyctf/openctf/api"
	"github.com/easyctf/openctf/models"
	"github.com/easyctf/openctf/structs"

	"github.com/go-macaron/bindata"
	"github.com/go-macaron/csrf"
	"github.com/go-macaron/session"

	"gopkg.in/macaron.v1"
)

// CreateServer generates a new gin server
func CreateServer(config structs.Config) (*structs.Webserver, error) {
	db, err := models.GetEngine(config)
	if err != nil {
		return nil, err
	}
	server := structs.Webserver{
		M:      macaron.Classic(),
		Db:     db,
		Config: config,
	}

	// middleware
	server.M.Use(macaron.Renderer())
	server.M.Use(session.Sessioner(session.Options{
		CookieName: "session",
	}))
	server.M.Use(csrf.Csrfer())

	// custom service to give endpoints access to the config/models
	server.M.Map(&server)

	// for serving the actual HTML/JS site
	if !server.Config.NoFrontend {
		server.M.Use(macaron.Static("generated",
			macaron.StaticOptions{
				FileSystem: bindata.Static(bindata.Options{
					Asset:      Asset,
					AssetDir:   AssetDir,
					AssetNames: AssetNames,
					Prefix:     "",
				}),
			},
		))
	} else {
		server.M.Get("/", func() string {
			return "nope"
		})
	}

	// API routes
	server.M.Group("/api", api.RouteAPI(&server))
	return &server, nil
}
