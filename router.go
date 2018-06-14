package main

import "github.com/gorilla/mux"

func (app *OpenCTF) buildRouter() *mux.Router {
	r := mux.NewRouter()

	r.HandleFunc("/", app.homeHandler)

	return r
}
