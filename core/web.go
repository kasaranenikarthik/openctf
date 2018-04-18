package core

import (
	"log"
	"net/http"

	"gopkg.in/macaron.v1"
)

// Webserver represents an OpenCTF server
type Webserver struct {
	m      *macaron.Macaron
	config Config
}

// CreateServer generates a new gin server
func CreateServer(config Config) (server Webserver, err error) {
	m := macaron.Classic()

	server = Webserver{m, config}
	return
}

// Start will actually launch the web server and begin listening.
func (w Webserver) Start() {
	log.Println("starting server...")
	log.Println(http.ListenAndServe(w.config.BindAddress, w.m))
}
