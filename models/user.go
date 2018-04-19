package models

// User is a user
type User struct {
	ID    int64
	Email string `xorm:"not null"`
}
