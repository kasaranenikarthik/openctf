package models

import "github.com/easyctf/openctf/structs"
import "github.com/go-xorm/xorm"

// GetEngine returns a new xorm.Engine for the given config
func GetEngine(config structs.Config) (engine *xorm.Engine, err error) {
	// engine, err = xorm.NewEngine("", "")
	return
}
