package proxy

import (
	"log"
	"time"
)

type IUser interface {
	Login(username, password string) error
}

type User struct {
}

func (u *User) Login(username, password string) error {
	// 不实现细节
	return nil
}

type UserProxy struct {
	user *User
}

// 构造函数
func NewUserProxy(user *User) *UserProxy {
	return &UserProxy{
		user: user,
	}
}

func (p *UserProxy) Login(username, password string) error {
	// bbefore 这里可能会有一些统计的逻辑
	start := time.Now()

	// 这里是原有的业务逻辑
	if err := p.user.Login(username, password); err != nil {
		return err
	}

	// after 这里可能也有一些监控统计的逻辑
	log.Printf("user login cost time: %s", time.Now().Sub(start))

	return nil
}
