package api

import (
	"github.com/easyctf/openctf/api/auth"
	"github.com/easyctf/openctf/structs"
	"github.com/go-macaron/binding"
	"gopkg.in/macaron.v1"
)

// RouteAPI will set up the routes from the endpoints to their respective handler functions.
func RouteAPI(w *structs.Webserver) func() {
	wrapped := func() {
		w.M.Get("/", apiHome)
		w.M.Post("/auth/register", binding.Bind(auth.RegisterForm{}), auth.RegisterUserEndpoint)
	}
	return wrapped
}

func apiHome(c *macaron.Context) {
	sanity := struct{ Message string }{
		Message: "hi there!",
	}
	c.JSON(200, &sanity)
}
