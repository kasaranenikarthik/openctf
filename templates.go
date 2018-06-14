package main

import (
	"html/template"
	"log"
)

var templateList = map[string][]string{
	"home": []string{"index.html", "layout.html"},
}

func (app *OpenCTF) generateTemplates() (map[string]*template.Template, error) {
	templates := make(map[string]*template.Template)

	for name, files := range templateList {
		prefixedFiles := make([]string, len(files))
		for i, file := range files {
			prefixedFiles[i] = app.conf.TemplateDir + "/" + file
		}
		log.Println("loading from", prefixedFiles)
		if t, err := template.ParseFiles(prefixedFiles...); err == nil {
			templates[name] = t
		} else {
			return nil, err
		}
	}

	return templates, nil
}
