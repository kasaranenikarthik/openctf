package structs

import (
	"log"
	"net/http"

	"gopkg.in/macaron.v1"
)

// Webserver represents an OpenCTF server
type Webserver struct {
	M      *macaron.Macaron
	Config Config
}

// Start will actually launch the web server and begin listening.
func (w Webserver) Start() {
	log.Println("starting server...")
	log.Println(http.ListenAndServe(w.Config.BindAddress, w.M))
}
