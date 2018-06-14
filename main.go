package main

import (
	"flag"
	"fmt"
	"log"

	"github.com/easyctf/openctf/structs"
	"github.com/easyctf/openctf/templates"
	"github.com/go-macaron/csrf"
	"github.com/go-macaron/session"
	"github.com/thehowl/conf"
	macaron "gopkg.in/macaron.v1"
)

// Version is the current version of OpenCTF, will be injected by the build script on release builds.
var Version = "dev"

// Tags
var Tags = ""

func main() {
	confFile := flag.String("conf", "openctf.conf", "Location of the config file (will be created if it doesn't exist).")
	flag.Parse()

	if *confFile == "" {
		fmt.Println("Config file required. See -h for more details.")
		return
	}

	c := structs.Config{}
	err := conf.Load(&c, *confFile)
	if err == conf.ErrNoFile {
		conf.Export(structs.DefaultConfig, *confFile)
		fmt.Printf("The default configuration has been written to '%s'. Please modify this file and rerun the application.\n", *confFile)
		return
	}
	if err != nil {
		log.Fatal(err)
	}

	// initialize app
	app := structs.OpenCTF{
		Conf: c,
	}
	app.Macaron = newServer(&app)

	// build routes
	buildRoutes(&app)

	log.Println("Starting Openctf build", Version)
	app.Run()
}

// newServer initializes the app.
func newServer(app *structs.OpenCTF) *macaron.Macaron {
	srv := macaron.Classic()

	// middleware
	srv.Use(macaron.Renderer())
	srv.Use(session.Sessioner(session.Options{CookieName: "session"}))
	srv.Use(csrf.Csrfer())

	// custom service to give endpoints access to the config/models
	srv.Map(app)

	// templates
	srv.Use(templates.Renderer(app.Conf))

	return srv
}
