class BaseSocket {
    constructor() {
        if (BaseSocket.instance) {
            return BaseSocket.instance;
        }

        this.socket = null;
        BaseSocket.instance = this;
    }
    
    connect() {
        try {
            this.socket = new WebSocket("ws://localhost:8009/ws/notification/");
            
            this.socket.onopen = () => {
                console.log("Connected to user socket");
            };

            this.socket.onerror = (error) => {
                console.log(`WebSocket error: ${error}`);
            };

            this.socket.onclose = (event) => {
                if (event.wasClean) {
                    console.log(`Connection closed cleanly, code=${event.code} reason=${event.reason}`);
                } else {
                    console.log('Connection died');
                }

            this.socket.onmessage = (event) => {
                console.log(`Data received from WebSocket: ${event.data}`);
            }
        };
        } catch (error) {
            console.error(`Failed to create WebSocket connection: ${error}`);
        }
    }
    
    send(data) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(data));
        } else {
            console.error('Cannot send data, WebSocket is not open');
        }
    }
    
    close() {
        if (this.socket) {
            this.socket.close();
        }
    }

    getSocket() {
        if (this.socket)
            return this.socket;
        else
            return null;
    }
}

const socketInstance = new BaseSocket();

export { socketInstance };
