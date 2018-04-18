package structs

import (
	"log"
	"net/http"

	"github.com/go-xorm/xorm"

	"gopkg.in/macaron.v1"
)

// Webserver represents an OpenCTF server
type Webserver struct {
	M      *macaron.Macaron
	Db     *xorm.Engine
	Config Config
}

// Start will actually launch the web server and begin listening.
func (w *Webserver) Start() {
	log.Println("starting server...")
	log.Println(http.ListenAndServe(w.Config.BindAddress, w.M))
}
