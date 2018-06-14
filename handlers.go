package main

import (
	"gopkg.in/macaron.v1"

	"github.com/easyctf/openctf/structs"
)

func buildRoutes(app *structs.OpenCTF) {
	h := Handlers{app}

	app.Macaron.Get("/", h.homeHandler)
}

// Handlers is a struct which is associated with route handlers
type Handlers struct {
	app *structs.OpenCTF
}

func (h *Handlers) homeHandler(c *macaron.Context) {
	c.Data["Version"] = Version
	c.HTML(200, "index")
}
