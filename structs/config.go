package structs

// Config describes the configuration for this run of the application.
type Config struct {
	Bind        string `description:"The address to which the application should bind."`
	TemplateDir string `description:"The directory containing templates to load. (only applicable for non-bindata builds)"`
}

var DefaultConfig = Config{
	Bind:        ":4000",
	TemplateDir: "./templates",
}
