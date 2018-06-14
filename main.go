package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/thehowl/conf"
)

var VERSION = "dev"

type OpenCTF struct {
	c Config
}

func main() {
	confFile := flag.String("conf", "openctf.conf", "Location of the config file (will be created if it doesn't exist).")
	flag.Parse()

	if *confFile == "" {
		fmt.Println("Config file required. See -h for more details.")
		return
	}

	c := Config{}
	err := conf.Load(&c, *confFile)
	if err == conf.ErrNoFile {
		conf.Export(defaultConfig, *confFile)
		fmt.Printf("The default configuration has been written to '%s'. Please modify this file and rerun the application.\n", *confFile)
		return
	}
	if err != nil {
		log.Fatal(err)
	}

	app := OpenCTF{c}
	app.Run()
}

func (app *OpenCTF) Run() {
	srv := http.Server{
		Addr:    app.c.Bind,
		Handler: buildRouter(app.c),

		// doing this cuz mux page says so, this will be a configuration option soon
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
	}
	log.Fatal(srv.ListenAndServe())
}
