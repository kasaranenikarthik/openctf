package main

import "github.com/gorilla/mux"

func buildRouter(conf Config) *mux.Router {
	r := mux.NewRouter()
	return r
}
