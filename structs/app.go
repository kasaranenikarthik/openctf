package structs

import (
	"log"
	"net/http"

	"gopkg.in/macaron.v1"
)

// OpenCTF is the struct containing all of the variables used in the app.
type OpenCTF struct {
	Conf    Config
	Macaron *macaron.Macaron
}

// Run launches the OpenCTF app.
func (app *OpenCTF) Run() {
	log.Printf("Serving on '%s'...\n", app.Conf.Bind)
	log.Fatal(http.ListenAndServe(app.Conf.Bind, app.Macaron))
}
