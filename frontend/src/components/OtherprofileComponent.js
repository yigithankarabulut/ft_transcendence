class  OtherprofileComponent {
    constructor(path) {
        this.path = path;
    }

    async render() {
        return fetch(this.path)
            .then(res => {
                if (!res.ok)
                    throw new Error("couldn't fetch route");
                return res.text();
            });
    }
}

export default OtherprofileComponent;
