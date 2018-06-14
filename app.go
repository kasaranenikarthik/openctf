package main

import (
	"html/template"
	"log"
	"net/http"
	"time"
)

// OpenCTF is the struct containing all of the variables used in the app.
type OpenCTF struct {
	conf      Config
	templates map[string]*template.Template
}

// Run launches the OpenCTF app.
func (app *OpenCTF) Run() {
	srv := http.Server{
		Addr:    app.conf.Bind,
		Handler: app.buildRouter(),

		// doing this cuz mux page says so, this will be a configuration option soon
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
	}
	log.Println("serving...")
	log.Fatal(srv.ListenAndServe())
}
