package main

import (
	"net/http"

	"github.com/easyctf/openctf/models"
)

type Context struct {
	user *models.User
}

func (app *OpenCTF) homeHandler(w http.ResponseWriter, r *http.Request) {
	app.templates["home"].ExecuteTemplate(w, "layout", struct{}{})
}
