package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"github.com/thehowl/conf"
)

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

	r := mux.NewRouter()
	r.HandleFunc("/", homeHandler)

	srv := http.Server{
		Addr:    c.Bind,
		Handler: r,

		// doing this cuz mux page says so, this will be a configuration option soon
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
	}
	log.Fatal(srv.ListenAndServe())
}
