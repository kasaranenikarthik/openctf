// +build !bindata

package templates

import (
	"github.com/easyctf/openctf/structs"
	macaron "gopkg.in/macaron.v1"
)

// Renderer returns a static renderer from bindata
func Renderer(conf structs.Config) macaron.Handler {
	return macaron.Renderer(macaron.RenderOptions{
		Directory: conf.TemplateDir,
	})
}
