package api

import (
	"github.com/easyctf/openctf/structs"
	macaron "gopkg.in/macaron.v1"
)

// RouteAPI will set up the routes from the endpoints to their respective handler functions.
func RouteAPI(w *structs.Webserver) func() {
	wrapped := func() { w.M.Get("/", apiHome) }
	return wrapped
}

func apiHome(c *macaron.Context) {
	sanity := struct {
		Message string `json:"message"`
	}{
		Message: "hi there!",
	}
	c.JSON(200, &sanity)
}
