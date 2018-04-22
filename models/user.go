package models

import "time"

// User is a user
type User struct {
	ID    int64
	Email string `xorm:"not null"`

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
