class SSEClient {
    private eventSource: EventSource | null = null;
    private messageCallback: ((data: any) => void) | null = null;
    private errorCallback: ((error: Event) => void) | null = null;

    constructor(url: string) {
        this.eventSource = new EventSource(url);

        this.eventSource.onmessage = (event) => {
            if (this.messageCallback) {
                this.messageCallback(JSON.parse(event.data));
            }
        };

        this.eventSource.onerror = (error) => {
            console.error("SSE error:", error);
            if (this.errorCallback) {
                this.errorCallback(error);
            }
        };
    }

    public onMessage(callback: (data: any) => void) {
        this.messageCallback = callback;
    }

    public onError(callback: (error: Event) => void) {
        this.errorCallback = callback;
    }

    public close() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    }
}

export { SSEClient };
