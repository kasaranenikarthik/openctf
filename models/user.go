package models

import (
	"strings"
	"time"
)

// User is a user
type User struct {
	ID            int64
	Username      string `xorm:"UNIQUE NOT NULL"`
	LowerUsername string `xorm:"UNIQUE NOT NULL"`

	Email    string `xorm:"not null"`
	Password string

	Created time.Time `xorm:"created"`
	Updated time.Time `xorm:"updated"`
}

// CreateUser inserts a user into the database and retrieves its new ID
func CreateUser(user User) (int64, error) {
	sess := globEngine.NewSession()
	defer sess.Close()

	_, err := sess.Insert(&user)
	if err != nil {
		return -1, err
	}

	return user.ID, nil
}

func isValidUsername(name string) bool {

}

func isAvailableUsername(name string) (bool, error) {
	if !isValidUsername(s) {
		return false, nil
	}

	return globEngine.
		Where("id!=?", uid).
		Get(&User{LowerName: strings.ToLower(name)})
}
