package main

import (
	"net/http"
)

func (app *OpenCTF) homeHandler(w http.ResponseWriter, r *http.Request) {
	app.templates["home"].ExecuteTemplate(w, "layout", struct{}{})
}
