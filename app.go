package main

import (
	"log"
	"net/http"
	"time"
)

// OpenCTF is the struct containing all of the variables used in the app.
type OpenCTF struct {
	c Config
}

// Run launches the OpenCTF app.
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
