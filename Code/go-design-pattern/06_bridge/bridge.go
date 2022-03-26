package bridge

type IMsgSender interface {
	Send(msg string) error
}

type EmailMsgSender struct {
	emails []string
}

func NewEmailMsgSender(emails []string) *EmailMsgSender {
	return &EmailMsgSender{emails: emails}
}

func (s *EmailMsgSender) Send(msg string) error {
	// 这里去发送消息
	return nil
}

// INotification 通知接口
type INotification interface {
	Notiry(msg string) error
}

type ErrorNotification struct {
	sender IMsgSender
}

func NewErrorNotification(sender IMsgSender) *ErrorNotification {
	return &ErrorNotification{sender: sender}
}

func (n *ErrorNotification) Notify(msg string) error {
	return n.sender.Send(msg)
}
