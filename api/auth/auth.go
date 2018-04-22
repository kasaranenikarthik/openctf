package auth

import (
	"github.com/easyctf/openctf/models"
	"github.com/easyctf/openctf/structs"
	"gopkg.in/macaron.v1"
)

// RegisterForm is a registration form
type RegisterForm struct {
	Email           string `binding:"Required"`
	Password        string
	ConfirmPassword string
}

// RegisterUserEndpoint is an API handler that allows users to register
func RegisterUserEndpoint(c *macaron.Context, w *structs.Webserver, f RegisterForm) error {
	user := models.User{}

	id, err := models.CreateUser(user)
	if err != nil {
		return err
	}
	c.JSON(200, struct{ ID int64 }{
		ID: id,
	})
	return nil
}
