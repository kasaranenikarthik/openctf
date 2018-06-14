package main

// Config describes the configuration for this run of the application.
type Config struct {
	Bind        string `description:"The address to which the application should bind."`
	TemplateDir string `description:"The directory containing templates to load."`
}

var defaultConfig = Config{
	Bind:        ":4000",
	TemplateDir: "./templates",
}
