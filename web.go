package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// Webserver represents an OpenCTF server
type Webserver struct {
	gin    *gin.Engine
	config Config
}

// CreateServer generates a new gin server
func CreateServer(config Config) (server Webserver, err error) {
	if config.Environment == "production" {
		gin.SetMode(gin.ReleaseMode)
	}
	r := gin.Default()
	r.GET("/", func(c *gin.Context) {
		c.String(http.StatusOK, "hey there")
	})

	server = Webserver{r, config}
	return
}

// Start will actually launch the web server and begin listening.
func (w Webserver) Start() {
	w.gin.Run(w.config.BindAddress)
}
