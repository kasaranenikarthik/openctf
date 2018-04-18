package models

import "github.com/easyctf/openctf/core"
import "github.com/go-xorm/xorm"

// GetEngine returns a new xorm.Engine for the given config
func GetEngine(config core.Config) (engine *xorm.Engine, err error) {
	engine, err = xorm.NewEngine("", "")
	return
}
