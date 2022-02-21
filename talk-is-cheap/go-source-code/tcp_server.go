package main

import (
	"log"
	"net"
)

func main() {
	listen, err := net.Listen("tcp", ":8888")
	if err != nil {
		log.Println("listen error: ", err)
		return
	}

	for {
		conn, err := listen.Accept()
		if err != nil {
			log.Println("accept error: ", err)
			break
		}

		// start a new goroutine to handle the new connection.
		go HandleConn(conn)
	}
}

func HandleConn(conn net.Conn) {
	defer conn.Close()
	packet := make([]byte, 1024)
	for {
		// block here if socket is not available for reading data.
		n, err := conn.Read(packet)
		if err != nil {
			log.Println("read socket error: ", err)
			return
		}

		// same as above, block here if socket is not available for writing.
		_, _ = conn.Write(packet[:n])
	}
}
