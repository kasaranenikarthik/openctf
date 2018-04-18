package api

import "github.com/easyctf/openctf/structs"

// RouteAPI will set up the routes from the endpoints to their respective handler functions.
func RouteAPI(w structs.Webserver) func() {
	wrapped := func() { w.M.Get("/", func() string { return "hello" }) }
	return wrapped
}
