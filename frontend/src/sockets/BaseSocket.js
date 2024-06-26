class WebSocketSingleton {
    constructor() {
        if (!WebSocketSingleton.instance) {
            this.ws = null;
            WebSocketSingleton.instance = this;
        }

        return WebSocketSingleton.instance;
    }

    connect(path) {
        if (!this.ws) {
            this.ws = new WebSocket(path);
        }
    }

    getWebSocket() {
        return this.ws;
    }
}

export default WebSocketSingleton;
